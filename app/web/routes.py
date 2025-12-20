"""Web routes for HTML pages"""
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from . import web_bp
from ..database.db_manager import DatabaseManager
from ..agent.rule_agent import RuleAgent
from ..agent.notification_agent import NotificationAgent
from ..auth.auth_service import AuthService
from ..auth.session_manager import login_required, get_current_user
from ..models import LostItem, FoundItem

# 初始化服务
db_manager = DatabaseManager()
agent = RuleAgent()
notification_agent = NotificationAgent(db_manager)
auth_service = AuthService(db_manager)


@web_bp.context_processor
def inject_unread_count():
    """在所有模板中注入未读通知数量"""
    current_user = get_current_user(db_manager)
    unread_count = 0
    if current_user:
        db_session = db_manager.get_session()
        try:
            unread_count = db_manager.get_unread_notification_count(db_session, current_user.id)
        finally:
            db_session.close()
    return dict(unread_count=unread_count)


@web_bp.route('/')
def index():
    """首页 - 显示失物和招领列表（支持搜索和筛选）"""
    db_session = db_manager.get_session()
    try:
        from ..database import models_db
        from sqlalchemy import or_
        
        # 获取查询参数
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        item_type = request.args.get('type', '').strip()  # lost 或 found
        sort = request.args.get('sort', 'time_desc').strip()
        
        # 构建查询
        lost_query = db_session.query(models_db.LostItemDB).filter(
            models_db.LostItemDB.is_resolved == False
        )
        found_query = db_session.query(models_db.FoundItemDB).filter(
            models_db.FoundItemDB.is_resolved == False
        )
        
        # 搜索条件
        if search:
            search_filter = or_(
                models_db.LostItemDB.item_name.like(f'%{search}%'),
                models_db.LostItemDB.category.like(f'%{search}%'),
                models_db.LostItemDB.lost_location.like(f'%{search}%'),
                models_db.LostItemDB.description.like(f'%{search}%')
            )
            lost_query = lost_query.filter(search_filter)
            
            search_filter = or_(
                models_db.FoundItemDB.item_name.like(f'%{search}%'),
                models_db.FoundItemDB.category.like(f'%{search}%'),
                models_db.FoundItemDB.found_location.like(f'%{search}%'),
                models_db.FoundItemDB.description.like(f'%{search}%')
            )
            found_query = found_query.filter(search_filter)
        
        # 类别筛选
        if category:
            lost_query = lost_query.filter(models_db.LostItemDB.category == category)
            found_query = found_query.filter(models_db.FoundItemDB.category == category)
        
        # 排序
        if sort == 'time_asc':
            lost_query = lost_query.order_by(models_db.LostItemDB.lost_time.asc())
            found_query = found_query.order_by(models_db.FoundItemDB.found_time.asc())
        elif sort == 'name':
            lost_query = lost_query.order_by(models_db.LostItemDB.item_name.asc())
            found_query = found_query.order_by(models_db.FoundItemDB.item_name.asc())
        else:  # time_desc (默认)
            lost_query = lost_query.order_by(models_db.LostItemDB.lost_time.desc())
            found_query = found_query.order_by(models_db.FoundItemDB.found_time.desc())
        
        # 根据类型筛选
        if item_type == 'lost':
            lost_items = lost_query.limit(50).all()
            found_items = []
        elif item_type == 'found':
            lost_items = []
            found_items = found_query.limit(50).all()
        else:
            # 显示两种类型，各限制数量
            lost_items = lost_query.limit(25).all()
            found_items = found_query.limit(25).all()
        
        current_user = get_current_user(db_manager)
        
        return render_template('index.html', 
                             lost_items=lost_items,
                             found_items=found_items,
                             current_user=current_user,
                             search=search,
                             category=category,
                             item_type=item_type,
                             sort=sort)
    finally:
        db_session.close()


@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        password = request.form.get('password', '')
        
        if not student_id or not password:
            flash('请输入学号和密码', 'error')
            return render_template('login.html')
        
        db_session = db_manager.get_session()
        try:
            success, error_msg, user = auth_service.login_user(db_session, student_id, password)
            if success:
                session['user_id'] = user.id
                session['student_id'] = user.student_id
                session['name'] = user.name
                flash('登录成功！', 'success')
                return redirect(url_for('web.index'))
            else:
                flash(error_msg or '登录失败', 'error')
        finally:
            db_session.close()
    
    return render_template('login.html')


@web_bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册页面"""
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # 验证
        if not student_id or not name or not password:
            flash('学号、姓名和密码不能为空', 'error')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('两次输入的密码不一致', 'error')
            return render_template('register.html')
        
        db_session = db_manager.get_session()
        try:
            success, error_msg, user = auth_service.register_user(
                db_session, student_id, name, password, email, phone
            )
            if success:
                flash('注册成功！请登录', 'success')
                return redirect(url_for('web.login'))
            else:
                flash(error_msg or '注册失败', 'error')
        finally:
            db_session.close()
    
    return render_template('register.html')


@web_bp.route('/logout')
def logout():
    """登出"""
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('web.index'))


@web_bp.route('/post_lost', methods=['GET', 'POST'])
@login_required
def post_lost():
    """发布失物页面"""
    if request.method == 'POST':
        current_user = get_current_user(db_manager)
        if not current_user:
            flash('请先登录', 'error')
            return redirect(url_for('web.login'))
        
        item_name = request.form.get('item_name', '').strip()
        category = request.form.get('category', '').strip()
        lost_location = request.form.get('lost_location', '').strip()
        lost_time_str = request.form.get('lost_time', '')
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '').strip()
        brand = request.form.get('brand', '').strip()
        
        if not item_name or not category or not lost_location:
            flash('物品名称、类别和丢失地点不能为空', 'error')
            return render_template('post_lost.html')
        
        # 解析时间
        try:
            if lost_time_str:
                lost_time = datetime.fromisoformat(lost_time_str.replace('T', ' '))
            else:
                lost_time = datetime.now()
        except:
            lost_time = datetime.now()
        
        lost = LostItem(
            item_id=None,
            user_id=current_user.id,
            item_name=item_name,
            category=category,
            lost_location=lost_location,
            lost_time=lost_time,
            description=description,
            color=color if color else None,
            brand=brand if brand else None
        )
        
        db_session = db_manager.get_session()
        try:
            from ..database import models_db
            
            db_lost = db_manager.create_lost_item(db_session, lost)
            # 触发智能体匹配
            found_items = db_manager.get_all_found_items(db_session)
            matches = agent.match_cycle(
                LostItem(
                    item_id=db_lost.id,
                    user_id=db_lost.user_id,
                    item_name=db_lost.item_name,
                    category=db_lost.category,
                    lost_location=db_lost.lost_location,
                    lost_time=db_lost.lost_time,
                    description=db_lost.description or '',
                    color=db_lost.color,
                    brand=db_lost.brand
                ),
                found_items
            )
            # 保存匹配结果并发送通知
            for m in matches:
                db_match = db_manager.create_match_record(db_session, m)
                # 通知智能体：匹配成功时通知
                db_found = db_session.query(models_db.FoundItemDB).filter_by(id=m.found_item_id).first()
                if db_found:
                    notification_agent.notify_on_match(db_session, db_match, db_lost, db_found)
            
            flash(f'发布成功！找到 {len(matches)} 个可能的匹配', 'success')
            return redirect(url_for('web.matches', lost_id=db_lost.id))
        finally:
            db_session.close()
    
    return render_template('post_lost.html')


@web_bp.route('/post_found', methods=['GET', 'POST'])
@login_required
def post_found():
    """发布招领页面"""
    if request.method == 'POST':
        current_user = get_current_user(db_manager)
        if not current_user:
            flash('请先登录', 'error')
            return redirect(url_for('web.login'))
        
        item_name = request.form.get('item_name', '').strip()
        category = request.form.get('category', '').strip()
        found_location = request.form.get('found_location', '').strip()
        found_time_str = request.form.get('found_time', '')
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '').strip()
        brand = request.form.get('brand', '').strip()
        
        if not item_name or not category or not found_location:
            flash('物品名称、类别和拾获地点不能为空', 'error')
            return render_template('post_found.html')
        
        # 解析时间
        try:
            if found_time_str:
                found_time = datetime.fromisoformat(found_time_str.replace('T', ' '))
            else:
                found_time = datetime.now()
        except:
            found_time = datetime.now()
        
        found = FoundItem(
            item_id=None,
            user_id=current_user.id,
            item_name=item_name,
            category=category,
            found_location=found_location,
            found_time=found_time,
            description=description,
            color=color if color else None,
            brand=brand if brand else None
        )
        
        db_session = db_manager.get_session()
        try:
            db_found = db_manager.create_found_item(db_session, found)
            flash('发布成功！', 'success')
            return redirect(url_for('web.index'))
        finally:
            db_session.close()
    
    return render_template('post_found.html')


@web_bp.route('/matches/<int:lost_id>')
@login_required
def matches(lost_id):
    """查看匹配结果页面"""
    db_session = db_manager.get_session()
    try:
        from ..database import models_db
        
        # 获取失物信息
        lost_item = db_session.query(models_db.LostItemDB).filter_by(id=lost_id).first()
        if not lost_item:
            flash('失物信息不存在', 'error')
            return redirect(url_for('web.index'))
        
        # 获取匹配记录
        match_records = db_manager.get_match_records_by_lost_item(db_session, lost_id)
        
        # 获取匹配的招领信息
        found_items = []
        for match in match_records:
            found_item = db_session.query(models_db.FoundItemDB).filter_by(
                id=match['found_item_id']
            ).first()
            if found_item:
                found_items.append({
                    'item': found_item,
                    'match_score': match['match_score'],
                    'match_reason': match['match_reason']
                })
        
        return render_template('matches.html',
                             lost_item=lost_item,
                             found_items=found_items)
    finally:
        db_session.close()


@web_bp.route('/notifications')
@login_required
def notifications():
    """通知中心页面"""
    current_user = get_current_user(db_manager)
    if not current_user:
        flash('请先登录', 'error')
        return redirect(url_for('web.login'))
    
    db_session = db_manager.get_session()
    try:
        # 获取所有通知
        all_notifications = notification_agent.get_user_notifications(
            db_session, current_user.id, unread_only=False, limit=50
        )
        
        # 获取未读数量
        unread_count = db_manager.get_unread_notification_count(db_session, current_user.id)
        
        # 按类型分组
        match_notifications = [n for n in all_notifications if n.notification_type == 'match']
        reminder_notifications = [n for n in all_notifications if n.notification_type == 'reminder']
        announcement_notifications = [n for n in all_notifications if n.notification_type == 'announcement']
        
        return render_template('notifications.html',
                             notifications=all_notifications,
                             match_notifications=match_notifications,
                             reminder_notifications=reminder_notifications,
                             announcement_notifications=announcement_notifications,
                             unread_count=unread_count,
                             current_user=current_user)
    finally:
        db_session.close()


@web_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """标记通知为已读"""
    current_user = get_current_user(db_manager)
    if not current_user:
        return jsonify({'success': False, 'error': '请先登录'}), 401
    
    db_session = db_manager.get_session()
    try:
        success = notification_agent.mark_as_read(db_session, notification_id, current_user.id)
        if success:
            return jsonify({'success': True, 'message': '已标记为已读'}), 200
        else:
            return jsonify({'success': False, 'error': '通知不存在或无权限'}), 404
    finally:
        db_session.close()


@web_bp.route('/notifications/unread-count', methods=['GET'])
@login_required
def get_unread_count():
    """获取未读通知数量（AJAX）"""
    current_user = get_current_user(db_manager)
    if not current_user:
        return jsonify({'success': False, 'error': '请先登录'}), 401
    
    db_session = db_manager.get_session()
    try:
        count = db_manager.get_unread_notification_count(db_session, current_user.id)
        return jsonify({'success': True, 'unread_count': count}), 200
    finally:
        db_session.close()


@web_bp.route('/lost/<int:lost_id>')
def lost_detail(lost_id):
    """失物详情页"""
    db_session = db_manager.get_session()
    try:
        from ..database import models_db
        
        # 获取失物信息
        lost_item = db_session.query(models_db.LostItemDB).filter_by(id=lost_id).first()
        if not lost_item:
            flash('失物信息不存在', 'error')
            return redirect(url_for('web.index'))
        
        # 获取匹配记录
        match_records = db_manager.get_match_records_by_lost_item(db_session, lost_id)
        
        # 获取匹配的招领信息
        match_list = []
        for match in match_records:
            found_item = db_session.query(models_db.FoundItemDB).filter_by(
                id=match['found_item_id']
            ).first()
            if found_item:
                match_list.append({
                    'found_item': found_item,
                    'match_score': match['match_score'],
                    'match_reason': match['match_reason']
                })
        
        # 按匹配度排序
        match_list.sort(key=lambda x: x['match_score'], reverse=True)
        
        current_user = get_current_user(db_manager)
        
        return render_template('lost_detail.html',
                             lost_item=lost_item,
                             match_records=match_list,
                             current_user=current_user)
    finally:
        db_session.close()


@web_bp.route('/found/<int:found_id>')
def found_detail(found_id):
    """招领详情页"""
    db_session = db_manager.get_session()
    try:
        from ..database import models_db
        
        # 获取招领信息
        found_item = db_session.query(models_db.FoundItemDB).filter_by(id=found_id).first()
        if not found_item:
            flash('招领信息不存在', 'error')
            return redirect(url_for('web.index'))
        
        # 获取相关失物（相同类别且未解决的）
        related_lost_items = db_session.query(models_db.LostItemDB).filter(
            models_db.LostItemDB.category == found_item.category,
            models_db.LostItemDB.is_resolved == False,
            models_db.LostItemDB.id != found_id  # 排除自己
        ).order_by(models_db.LostItemDB.lost_time.desc()).limit(10).all()
        
        current_user = get_current_user(db_manager)
        
        return render_template('found_detail.html',
                             found_item=found_item,
                             related_lost_items=related_lost_items,
                             current_user=current_user)
    finally:
        db_session.close()


@web_bp.route('/lost/<int:lost_id>/resolve', methods=['POST'])
@login_required
def mark_lost_resolved(lost_id):
    """标记失物为已解决/未解决"""
    current_user = get_current_user(db_manager)
    if not current_user:
        return jsonify({'success': False, 'error': '请先登录'}), 401
    
    data = request.json or {}
    resolved = data.get('resolved', True)
    
    db_session = db_manager.get_session()
    try:
        success = db_manager.mark_lost_item_resolved(db_session, lost_id, current_user.id, resolved)
        if success:
            status = '已解决' if resolved else '未解决'
            return jsonify({'success': True, 'message': f'已标记为{status}'}), 200
        else:
            return jsonify({'success': False, 'error': '失物不存在或无权限'}), 404
    finally:
        db_session.close()


@web_bp.route('/found/<int:found_id>/resolve', methods=['POST'])
@login_required
def mark_found_resolved(found_id):
    """标记招领为已解决/未解决"""
    current_user = get_current_user(db_manager)
    if not current_user:
        return jsonify({'success': False, 'error': '请先登录'}), 401
    
    data = request.json or {}
    resolved = data.get('resolved', True)
    
    db_session = db_manager.get_session()
    try:
        success = db_manager.mark_found_item_resolved(db_session, found_id, current_user.id, resolved)
        if success:
            status = '已解决' if resolved else '未解决'
            return jsonify({'success': True, 'message': f'已标记为{status}'}), 200
        else:
            return jsonify({'success': False, 'error': '招领不存在或无权限'}), 404
    finally:
        db_session.close()


@web_bp.route('/profile')
@login_required
def profile():
    """用户主页 - 查看自己发布的所有失物/招领"""
    current_user = get_current_user(db_manager)
    if not current_user:
        flash('请先登录', 'error')
        return redirect(url_for('web.login'))
    
    db_session = db_manager.get_session()
    try:
        from ..database import models_db
        
        # 获取用户发布的所有失物
        lost_items = db_session.query(models_db.LostItemDB).filter(
            models_db.LostItemDB.user_id == current_user.id
        ).order_by(models_db.LostItemDB.lost_time.desc()).all()
        
        # 获取用户发布的所有招领
        found_items = db_session.query(models_db.FoundItemDB).filter(
            models_db.FoundItemDB.user_id == current_user.id
        ).order_by(models_db.FoundItemDB.found_time.desc()).all()
        
        # 统计信息
        total_lost = len(lost_items)
        resolved_lost = len([item for item in lost_items if item.is_resolved])
        total_found = len(found_items)
        resolved_found = len([item for item in found_items if item.is_resolved])
        
        return render_template('profile.html',
                             current_user=current_user,
                             lost_items=lost_items,
                             found_items=found_items,
                             total_lost=total_lost,
                             resolved_lost=resolved_lost,
                             total_found=total_found,
                             resolved_found=resolved_found)
    finally:
        db_session.close()


@web_bp.route('/about')
def about():
    """关于我们页面 - 显示开发维护团队信息"""
    return render_template('about.html')

