from datetime import timedelta
from typing import List
from ..models import LostItem, FoundItem


class Matcher:
    """Simple implementation of matching rules described in the UML/docs."""

    def match_by_category(self, lost: LostItem, found: FoundItem) -> float:
        # 如果类别是"其他"，不加分
        if lost.category == "其他" or found.category == "其他":
            return 0.0
        # 类别相同才给分
        return 40.0 if lost.category == found.category else 0.0

    def match_by_location(self, lost: LostItem, found: FoundItem) -> float:
        # Very simple heuristic based on string equality / containment
        if lost.lost_location == found.found_location:
            return 25.0
        if lost.lost_location in found.found_location or found.found_location in lost.lost_location:
            return 20.0
        if lost.lost_location.split()[0] == found.found_location.split()[0]:
            return 15.0
        return 5.0

    def match_by_time(self, lost: LostItem, found: FoundItem) -> float:
        diff = abs(found.found_time - lost.lost_time)
        hours = diff.total_seconds() / 3600
        if hours <= 24:
            return 20.0
        if hours <= 72:
            return 15.0
        if hours <= 168:
            return 10.0
        return 5.0

    def match_by_features(self, lost: LostItem, found: FoundItem) -> float:
        score = 0.0
        if lost.color and found.color and lost.color.lower() == found.color.lower():
            score += 5.0
        if lost.brand and found.brand and lost.brand.lower() == found.brand.lower():
            score += 5.0
        # keyword overlap in description (very small heuristic)
        lost_words = set(lost.description.lower().split())
        found_words = set(found.description.lower().split())
        common = lost_words & found_words
        score += min(5.0, len(common))
        return min(score, 15.0)

    def calculate_total_score(self, lost: LostItem, found: FoundItem) -> float:
        cat = self.match_by_category(lost, found)
        if cat == 0.0:
            return 0.0
        loc = self.match_by_location(lost, found)
        time = self.match_by_time(lost, found)
        feat = self.match_by_features(lost, found)
        return cat + loc + time + feat
