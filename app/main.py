"""Flask application main entry point"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from app.database.db_manager import DatabaseManager
from app.agent.rule_agent import RuleAgent
from app.agent.notification_agent import NotificationAgent
from app.models import LostItem, FoundItem
from app.web import web_bp

# 初始化服务
dbm = DatabaseManager()
agent = RuleAgent()
notification_agent = NotificationAgent(dbm)


def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # 生产环境需要更改
    app.config['SESSION_COOKIE_SECURE'] = False  # 开发环境设为False，生产环境设为True
    
    # 启用CORS，允许跨域访问（供客户端共享数据）
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 注册Web蓝图（Blueprint已配置static_url_path='/static'，会自动处理静态资源）
    app.register_blueprint(web_bp)
    
    # API路由（保留原有API功能）
    @app.route('/api/lost', methods=['POST'])
    def api_post_lost():
        """API: 发布失物"""
        payload = request.json or {}
        lost = LostItem(
            item_id=None,
            user_id=payload.get('user_id'),
            item_name=payload['item_name'],
            category=payload['category'],
            lost_location=payload['lost_location'],
            lost_time=datetime.fromisoformat(payload['lost_time']) if payload.get('lost_time') else datetime.utcnow(),
            description=payload.get('description',''),
            color=payload.get('color'),
            brand=payload.get('brand')
        )
        session = dbm.get_session()
        try:
            from .database import models_db
            
            db_lost = dbm.create_lost_item(session, lost)
            # get found items as dataclasses
            found_items = dbm.get_all_found_items(session)
            matches = agent.match_cycle(LostItem(item_id=db_lost.id, user_id=db_lost.user_id, item_name=db_lost.item_name, category=db_lost.category, lost_location=db_lost.lost_location, lost_time=db_lost.lost_time, description=db_lost.description or '', color=db_lost.color, brand=db_lost.brand), found_items)
            # persist matches
            for m in matches:
                db_match = dbm.create_match_record(session, m)
                # 通知智能体：匹配成功时通知
                # 获取匹配的招领信息
                db_found = session.query(models_db.FoundItemDB).filter_by(id=m.found_item_id).first()
                if db_found:
                    notification_agent.notify_on_match(session, db_match, db_lost, db_found)
            
            return jsonify({'lost_id': db_lost.id, 'matches': [{ 'found_item_id': m.found_item_id, 'score': m.match_score } for m in matches]}), 201
        finally:
            session.close()

    @app.route('/api/found', methods=['POST'])
    def api_post_found():
        """API: 发布招领"""
        payload = request.json or {}
        found = FoundItem(
            item_id=None,
            user_id=payload.get('user_id'),
            item_name=payload['item_name'],
            category=payload['category'],
            found_location=payload['found_location'],
            found_time=datetime.fromisoformat(payload['found_time']) if payload.get('found_time') else datetime.utcnow(),
            description=payload.get('description',''),
            color=payload.get('color'),
            brand=payload.get('brand')
        )
        session = dbm.get_session()
        try:
            db_found = dbm.create_found_item(session, found)
            return jsonify({'found_id': db_found.id}), 201
        finally:
            session.close()

    @app.route('/api/matches/<int:lost_id>', methods=['GET'])
    def api_get_matches(lost_id: int):
        """API: 查看匹配结果"""
        session = dbm.get_session()
        try:
            recs = dbm.get_match_records_by_lost_item(session, lost_id)
            return jsonify({'matches': recs})
        finally:
            session.close()

    @app.route('/api/lost', methods=['GET'])
    def api_get_all_lost():
        """API: 获取所有失物列表（供客户端共享数据）"""
        session = dbm.get_session()
        try:
            # 支持查询参数：include_resolved（是否包含已解决的）
            include_resolved = request.args.get('include_resolved', 'false').lower() == 'true'
            lost_items = dbm.get_all_lost_items_dict(session, include_resolved=include_resolved)
            return jsonify({
                'success': True,
                'count': len(lost_items),
                'data': lost_items
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            session.close()

    @app.route('/api/found', methods=['GET'])
    def api_get_all_found():
        """API: 获取所有招领列表（供客户端共享数据）"""
        session = dbm.get_session()
        try:
            # 支持查询参数：include_resolved（是否包含已解决的）
            include_resolved = request.args.get('include_resolved', 'false').lower() == 'true'
            found_items = dbm.get_all_found_items_dict(session, include_resolved=include_resolved)
            return jsonify({
                'success': True,
                'count': len(found_items),
                'data': found_items
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            session.close()

    @app.route('/api/lost/<int:lost_id>', methods=['GET'])
    def api_get_lost_by_id(lost_id: int):
        """API: 根据ID获取单个失物信息"""
        session = dbm.get_session()
        try:
            from .database import models_db
            lost_item = session.query(models_db.LostItemDB).filter_by(id=lost_id).first()
            if not lost_item:
                return jsonify({'success': False, 'error': '失物信息不存在'}), 404
            return jsonify({
                'success': True,
                'data': {
                    "id": lost_item.id,
                    "user_id": lost_item.user_id,
                    "item_name": lost_item.item_name,
                    "category": lost_item.category,
                    "lost_location": lost_item.lost_location,
                    "lost_time": lost_item.lost_time.isoformat(),
                    "description": lost_item.description or "",
                    "color": lost_item.color,
                    "brand": lost_item.brand,
                    "is_resolved": lost_item.is_resolved,
                }
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            session.close()

    @app.route('/api/found/<int:found_id>', methods=['GET'])
    def api_get_found_by_id(found_id: int):
        """API: 根据ID获取单个招领信息"""
        session = dbm.get_session()
        try:
            from .database import models_db
            found_item = session.query(models_db.FoundItemDB).filter_by(id=found_id).first()
            if not found_item:
                return jsonify({'success': False, 'error': '招领信息不存在'}), 404
            return jsonify({
                'success': True,
                'data': {
                    "id": found_item.id,
                    "user_id": found_item.user_id,
                    "item_name": found_item.item_name,
                    "category": found_item.category,
                    "found_location": found_item.found_location,
                    "found_time": found_item.found_time.isoformat(),
                    "description": found_item.description or "",
                    "color": found_item.color,
                    "brand": found_item.brand,
                    "is_resolved": found_item.is_resolved,
                }
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            session.close()

    # 通知相关API
    @app.route('/api/notifications', methods=['GET'])
    def api_get_notifications():
        """API: 获取用户通知列表"""
        user_id = request.args.get('user_id', type=int)
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = request.args.get('limit', 20, type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': '缺少user_id参数'}), 400
        
        session = dbm.get_session()
        try:
            notifications = notification_agent.get_user_notifications(session, user_id, unread_only, limit)
            return jsonify({
                'success': True,
                'count': len(notifications),
                'data': [{
                    'id': n.id,
                    'type': n.notification_type,
                    'title': n.title,
                    'content': n.content,
                    'is_read': n.is_read,
                    'created_at': n.created_at.isoformat(),
                    'related_item_id': n.related_item_id,
                    'related_match_id': n.related_match_id,
                } for n in notifications]
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            session.close()

    @app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
    def api_mark_notification_read(notification_id: int):
        """API: 标记通知为已读"""
        user_id = request.json.get('user_id') if request.json else request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': '缺少user_id参数'}), 400
        
        session = dbm.get_session()
        try:
            success = notification_agent.mark_as_read(session, notification_id, user_id)
            if success:
                return jsonify({'success': True, 'message': '已标记为已读'}), 200
            else:
                return jsonify({'success': False, 'error': '通知不存在或无权限'}), 404
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            session.close()

    @app.route('/api/notifications/unread-count', methods=['GET'])
    def api_get_unread_count():
        """API: 获取用户未读通知数量"""
        user_id = request.args.get('user_id', type=int)
        
        if not user_id:
            return jsonify({'success': False, 'error': '缺少user_id参数'}), 400
        
        session = dbm.get_session()
        try:
            count = dbm.get_unread_notification_count(session, user_id)
            return jsonify({
                'success': True,
                'unread_count': count
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            session.close()

    @app.route('/api/notifications/check-reminders', methods=['POST'])
    def api_check_reminders():
        """API: 检查并发送提醒（定期任务）"""
        session = dbm.get_session()
        try:
            notification_agent.check_and_remind_unresolved(session)
            return jsonify({'success': True, 'message': '提醒检查完成'}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            session.close()

    return app


if __name__ == '__main__':
    app = create_app()
    # host='0.0.0.0' 表示监听所有网络接口，允许其他设备访问
    app.run(host='0.0.0.0', debug=True, port=5000)
