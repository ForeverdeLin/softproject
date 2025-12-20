from typing import List, Optional
from sqlalchemy.orm import Session
from .db import SessionLocal, init_db
from . import models_db
from ..models import LostItem, FoundItem, MatchRecord, User


class DatabaseManager:
    def __init__(self):
        init_db()

    def get_session(self) -> Session:
        return SessionLocal()

    def create_lost_item(self, session: Session, lost: LostItem) -> models_db.LostItemDB:
        dbitem = models_db.LostItemDB(
            user_id=lost.user_id,
            item_name=lost.item_name,
            category=lost.category,
            lost_location=lost.lost_location,
            lost_time=lost.lost_time,
            description=lost.description,
            color=lost.color,
            brand=lost.brand,
        )
        session.add(dbitem)
        session.commit()
        session.refresh(dbitem)
        return dbitem

    def create_found_item(self, session: Session, found: FoundItem) -> models_db.FoundItemDB:
        dbitem = models_db.FoundItemDB(
            user_id=found.user_id,
            item_name=found.item_name,
            category=found.category,
            found_location=found.found_location,
            found_time=found.found_time,
            description=found.description,
            color=found.color,
            brand=found.brand,
        )
        session.add(dbitem)
        session.commit()
        session.refresh(dbitem)
        return dbitem

    def get_all_found_items(self, session: Session) -> List[FoundItem]:
        rows = session.query(models_db.FoundItemDB).all()
        return [FoundItem(
            item_id=r.id,
            user_id=r.user_id,
            item_name=r.item_name,
            category=r.category,
            found_location=r.found_location,
            found_time=r.found_time,
            description=r.description or "",
            color=r.color,
            brand=r.brand,
        ) for r in rows]

    def get_all_lost_items(self, session: Session) -> List[LostItem]:
        """获取所有失物信息"""
        rows = session.query(models_db.LostItemDB).order_by(models_db.LostItemDB.lost_time.desc()).all()
        return [LostItem(
            item_id=r.id,
            user_id=r.user_id,
            item_name=r.item_name,
            category=r.category,
            lost_location=r.lost_location,
            lost_time=r.lost_time,
            description=r.description or "",
            color=r.color,
            brand=r.brand,
        ) for r in rows]

    def get_all_found_items_dict(self, session: Session, include_resolved: bool = False):
        """获取所有招领信息（返回字典格式，用于API）"""
        query = session.query(models_db.FoundItemDB)
        if not include_resolved:
            query = query.filter_by(is_resolved=False)
        rows = query.order_by(models_db.FoundItemDB.found_time.desc()).all()
        return [
            {
                "id": r.id,
                "user_id": r.user_id,
                "item_name": r.item_name,
                "category": r.category,
                "found_location": r.found_location,
                "found_time": r.found_time.isoformat(),
                "description": r.description or "",
                "color": r.color,
                "brand": r.brand,
                "is_resolved": r.is_resolved,
            }
            for r in rows
        ]

    def get_all_lost_items_dict(self, session: Session, include_resolved: bool = False):
        """获取所有失物信息（返回字典格式，用于API）"""
        query = session.query(models_db.LostItemDB)
        if not include_resolved:
            query = query.filter_by(is_resolved=False)
        rows = query.order_by(models_db.LostItemDB.lost_time.desc()).all()
        return [
            {
                "id": r.id,
                "user_id": r.user_id,
                "item_name": r.item_name,
                "category": r.category,
                "lost_location": r.lost_location,
                "lost_time": r.lost_time.isoformat(),
                "description": r.description or "",
                "color": r.color,
                "brand": r.brand,
                "is_resolved": r.is_resolved,
            }
            for r in rows
        ]

    def create_match_record(self, session: Session, record: MatchRecord) -> models_db.MatchRecordDB:
        dbrec = models_db.MatchRecordDB(
            lost_item_id=record.lost_item_id,
            found_item_id=record.found_item_id,
            match_score=record.match_score,
            match_reason=record.match_reason,
        )
        session.add(dbrec)
        session.commit()
        session.refresh(dbrec)
        return dbrec

    def get_match_records_by_lost_item(self, session: Session, lost_item_id: int):
        rows = session.query(models_db.MatchRecordDB).filter_by(lost_item_id=lost_item_id).order_by(models_db.MatchRecordDB.match_score.desc()).all()
        return [
            {
                "lost_item_id": r.lost_item_id,
                "found_item_id": r.found_item_id,
                "match_score": r.match_score,
                "match_reason": r.match_reason,
                "created_at": r.created_at.isoformat()
            }
            for r in rows
        ]

    # 用户相关操作方法
    def create_user(self, session: Session, user: User, password_hash: str) -> models_db.UserDB:
        """创建新用户"""
        db_user = models_db.UserDB(
            student_id=user.student_id,
            name=user.name,
            email=user.email,
            password_hash=password_hash,
            phone=getattr(user, 'phone', None)
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def get_user_by_student_id(self, session: Session, student_id: str) -> Optional[models_db.UserDB]:
        """根据学号查询用户"""
        return session.query(models_db.UserDB).filter_by(student_id=student_id).first()

    def get_user_by_id(self, session: Session, user_id: int) -> Optional[models_db.UserDB]:
        """根据ID查询用户"""
        return session.query(models_db.UserDB).filter_by(id=user_id).first()

    # 通知相关操作方法
    def get_user_notifications(self, session: Session, user_id: int, 
                              unread_only: bool = False, limit: int = 20):
        """获取用户的通知列表"""
        query = session.query(models_db.NotificationDB).filter(
            models_db.NotificationDB.user_id == user_id
        )
        if unread_only:
            query = query.filter(models_db.NotificationDB.is_read == False)
        return query.order_by(models_db.NotificationDB.created_at.desc()).limit(limit).all()

    def mark_notification_as_read(self, session: Session, notification_id: int, user_id: int) -> bool:
        """标记通知为已读"""
        notification = session.query(models_db.NotificationDB).filter(
            models_db.NotificationDB.id == notification_id,
            models_db.NotificationDB.user_id == user_id
        ).first()
        if notification:
            notification.is_read = True
            session.commit()
            return True
        return False

    def get_unread_notification_count(self, session: Session, user_id: int) -> int:
        """获取用户未读通知数量"""
        return session.query(models_db.NotificationDB).filter(
            models_db.NotificationDB.user_id == user_id,
            models_db.NotificationDB.is_read == False
        ).count()

    def mark_lost_item_resolved(self, session: Session, lost_id: int, user_id: int, resolved: bool = True) -> bool:
        """标记失物为已解决/未解决"""
        lost_item = session.query(models_db.LostItemDB).filter(
            models_db.LostItemDB.id == lost_id,
            models_db.LostItemDB.user_id == user_id
        ).first()
        if lost_item:
            lost_item.is_resolved = resolved
            session.commit()
            return True
        return False

    def mark_found_item_resolved(self, session: Session, found_id: int, user_id: int, resolved: bool = True) -> bool:
        """标记招领为已解决/未解决"""
        found_item = session.query(models_db.FoundItemDB).filter(
            models_db.FoundItemDB.id == found_id,
            models_db.FoundItemDB.user_id == user_id
        ).first()
        if found_item:
            found_item.is_resolved = resolved
            session.commit()
            return True
        return False

