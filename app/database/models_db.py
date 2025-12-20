from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime


class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(64), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    email = Column(String(256), nullable=True)
    password_hash = Column(String(256), nullable=False)  # 密码哈希
    phone = Column(String(64), nullable=True)  # 联系方式
    created_at = Column(DateTime, default=datetime.utcnow)  # 创建时间


class LostItemDB(Base):
    __tablename__ = 'lost_items'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    item_name = Column(String(256), nullable=False)
    category = Column(String(64), nullable=False)
    lost_location = Column(String(256), nullable=False)
    lost_time = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
    color = Column(String(64), nullable=True)
    brand = Column(String(128), nullable=True)
    is_resolved = Column(Boolean, default=False)


class FoundItemDB(Base):
    __tablename__ = 'found_items'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    item_name = Column(String(256), nullable=False)
    category = Column(String(64), nullable=False)
    found_location = Column(String(256), nullable=False)
    found_time = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
    color = Column(String(64), nullable=True)
    brand = Column(String(128), nullable=True)
    is_resolved = Column(Boolean, default=False)


class MatchRecordDB(Base):
    __tablename__ = 'match_records'
    id = Column(Integer, primary_key=True, index=True)
    lost_item_id = Column(Integer, nullable=False)
    found_item_id = Column(Integer, nullable=False)
    match_score = Column(Float, nullable=False)
    match_reason = Column(Text, nullable=True)
    is_notified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class NotificationDB(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # 接收通知的用户ID
    notification_type = Column(String(64), nullable=False)  # 通知类型：match, reminder, announcement
    title = Column(String(256), nullable=False)  # 通知标题
    content = Column(Text, nullable=False)  # 通知内容
    related_item_id = Column(Integer, nullable=True)  # 相关物品ID（失物或招领）
    related_match_id = Column(Integer, nullable=True)  # 相关匹配记录ID
    is_read = Column(Boolean, default=False)  # 是否已读
    created_at = Column(DateTime, default=datetime.utcnow)  # 创建时间
