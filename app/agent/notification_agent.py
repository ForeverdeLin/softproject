"""
通知型智能体 - 基于规则的实现
职责：发送匹配通知、提醒、系统消息
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..database import models_db
from ..database.db_manager import DatabaseManager


class NotificationAgent:
    """通知型智能体 - 基于规则的简单实现"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        初始化通知智能体
        
        Args:
            db_manager: 数据库管理器实例
        """
        self.db_manager = db_manager
        # 通知规则配置
        self.rules = {
            'high_match_threshold': 80.0,  # 高匹配度阈值
            'reminder_days': 7,  # 提醒天数（超过7天未解决）
            'urgent_reminder_days': 14,  # 紧急提醒天数
        }
    
    def notify_on_match(self, session: Session, match_record: models_db.MatchRecordDB,
                       lost_item: models_db.LostItemDB, found_item: models_db.FoundItemDB):
        """
        规则：匹配成功时通知失主和拾主
        
        Args:
            session: 数据库会话
            match_record: 匹配记录
            lost_item: 失物信息
            found_item: 招领信息
        """
        # 规则1：如果匹配度 >= 高阈值，发送紧急通知
        if match_record.match_score >= self.rules['high_match_threshold']:
            # 通知失主
            self._create_notification(
                session=session,
                user_id=lost_item.user_id,
                notification_type='match',
                title='🎉 高匹配度！发现可能的失物',
                content=f'您的失物"{lost_item.item_name}"找到了高匹配度的招领信息（匹配度：{match_record.match_score:.1f}分），请尽快查看！',
                related_item_id=lost_item.id,
                related_match_id=match_record.id
            )
            
            # 通知拾主
            if found_item.user_id:
                self._create_notification(
                    session=session,
                    user_id=found_item.user_id,
                    notification_type='match',
                    title='🎯 发现匹配的失物信息',
                    content=f'您拾获的"{found_item.item_name}"可能与失物信息匹配（匹配度：{match_record.match_score:.1f}分），请查看详情。',
                    related_item_id=found_item.id,
                    related_match_id=match_record.id
                )
        else:
            # 规则2：普通匹配度，发送常规通知
            # 通知失主
            self._create_notification(
                session=session,
                user_id=lost_item.user_id,
                notification_type='match',
                title='📋 发现可能的匹配',
                content=f'您的失物"{lost_item.item_name}"找到了可能的招领信息（匹配度：{match_record.match_score:.1f}分），请查看详情。',
                related_item_id=lost_item.id,
                related_match_id=match_record.id
            )
        
        # 标记匹配记录为已通知
        match_record.is_notified = True
        session.commit()
    
    def check_and_remind_unresolved(self, session: Session):
        """
        规则：检查并提醒未解决的失物/招领
        
        Args:
            session: 数据库会话
        """
        now = datetime.utcnow()
        reminder_threshold = now - timedelta(days=self.rules['reminder_days'])
        urgent_threshold = now - timedelta(days=self.rules['urgent_reminder_days'])
        
        # 检查未解决的失物
        unresolved_lost = session.query(models_db.LostItemDB).filter(
            models_db.LostItemDB.is_resolved == False
        ).all()
        
        for lost_item in unresolved_lost:
            days_passed = (now - lost_item.lost_time).days
            
            # 规则3：超过紧急提醒天数，发送紧急提醒
            if lost_item.lost_time < urgent_threshold:
                self._create_notification(
                    session=session,
                    user_id=lost_item.user_id,
                    notification_type='reminder',
                    title='⚠️ 紧急提醒：失物信息已超过14天',
                    content=f'您的失物"{lost_item.item_name}"已发布{days_passed}天，仍未解决。建议更新信息或重新发布。',
                    related_item_id=lost_item.id
                )
            # 规则4：超过提醒天数，发送常规提醒
            elif lost_item.lost_time < reminder_threshold:
                self._create_notification(
                    session=session,
                    user_id=lost_item.user_id,
                    notification_type='reminder',
                    title='📅 提醒：失物信息已超过7天',
                    content=f'您的失物"{lost_item.item_name}"已发布{days_passed}天，请及时关注匹配结果。',
                    related_item_id=lost_item.id
                )
        
        # 检查未解决的招领
        unresolved_found = session.query(models_db.FoundItemDB).filter(
            models_db.FoundItemDB.is_resolved == False
        ).all()
        
        for found_item in unresolved_found:
            days_passed = (now - found_item.found_time).days
            
            # 规则5：超过紧急提醒天数，发送紧急提醒
            if found_item.found_time < urgent_threshold:
                self._create_notification(
                    session=session,
                    user_id=found_item.user_id,
                    notification_type='reminder',
                    title='⚠️ 紧急提醒：招领信息已超过14天',
                    content=f'您发布的招领信息"{found_item.item_name}"已发布{days_passed}天，建议更新信息或重新发布。',
                    related_item_id=found_item.id
                )
            # 规则6：超过提醒天数，发送常规提醒
            elif found_item.found_time < reminder_threshold:
                self._create_notification(
                    session=session,
                    user_id=found_item.user_id,
                    notification_type='reminder',
                    title='📅 提醒：招领信息已超过7天',
                    content=f'您发布的招领信息"{found_item.item_name}"已发布{days_passed}天，请及时关注。',
                    related_item_id=found_item.id
                )
    
    def send_announcement(self, session: Session, user_ids: List[int], title: str, content: str):
        """
        规则：发送系统公告
        
        Args:
            session: 数据库会话
            user_ids: 接收公告的用户ID列表（空列表表示所有用户）
            title: 公告标题
            content: 公告内容
        """
        if not user_ids:
            # 如果用户列表为空，发送给所有用户
            users = session.query(models_db.UserDB).all()
            user_ids = [user.id for user in users]
        
        for user_id in user_ids:
            self._create_notification(
                session=session,
                user_id=user_id,
                notification_type='announcement',
                title=title,
                content=content
            )
    
    def _create_notification(self, session: Session, user_id: int, notification_type: str,
                            title: str, content: str, related_item_id: Optional[int] = None,
                            related_match_id: Optional[int] = None):
        """
        创建通知记录（内部方法）
        
        Args:
            session: 数据库会话
            user_id: 用户ID
            notification_type: 通知类型
            title: 通知标题
            content: 通知内容
            related_item_id: 相关物品ID
            related_match_id: 相关匹配记录ID
        """
        notification = models_db.NotificationDB(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            content=content,
            related_item_id=related_item_id,
            related_match_id=related_match_id,
            is_read=False
        )
        session.add(notification)
        session.commit()
    
    def get_user_notifications(self, session: Session, user_id: int, 
                              unread_only: bool = False, limit: int = 20) -> List[models_db.NotificationDB]:
        """
        获取用户的通知列表
        
        Args:
            session: 数据库会话
            user_id: 用户ID
            unread_only: 是否只获取未读通知
            limit: 返回数量限制
        
        Returns:
            通知列表
        """
        query = session.query(models_db.NotificationDB).filter(
            models_db.NotificationDB.user_id == user_id
        )
        
        if unread_only:
            query = query.filter(models_db.NotificationDB.is_read == False)
        
        return query.order_by(models_db.NotificationDB.created_at.desc()).limit(limit).all()
    
    def mark_as_read(self, session: Session, notification_id: int, user_id: int) -> bool:
        """
        标记通知为已读
        
        Args:
            session: 数据库会话
            notification_id: 通知ID
            user_id: 用户ID（验证权限）
        
        Returns:
            是否成功
        """
        notification = session.query(models_db.NotificationDB).filter(
            models_db.NotificationDB.id == notification_id,
            models_db.NotificationDB.user_id == user_id
        ).first()
        
        if notification:
            notification.is_read = True
            session.commit()
            return True
        return False

