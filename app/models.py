from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    user_id: Optional[int]
    student_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class LostItem:
    item_id: Optional[int]
    user_id: Optional[int]
    item_name: str
    category: str
    lost_location: str
    lost_time: datetime
    description: str
    color: Optional[str] = None
    brand: Optional[str] = None


@dataclass
class FoundItem:
    item_id: Optional[int]
    user_id: Optional[int]
    item_name: str
    category: str
    found_location: str
    found_time: datetime
    description: str
    color: Optional[str] = None
    brand: Optional[str] = None


@dataclass
class MatchRecord:
    lost_item_id: int
    found_item_id: int
    match_score: float
    match_reason: str
