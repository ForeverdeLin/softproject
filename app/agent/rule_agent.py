from typing import List
from ..models import LostItem, FoundItem, MatchRecord
from .matcher import Matcher


class RuleAgent:
    def __init__(self):
        self.matcher = Matcher()

    def match_cycle(self, lost_item: LostItem, found_items: List[FoundItem]) -> List[MatchRecord]:
        matches: List[MatchRecord] = []
        for f in found_items:
            score = self.matcher.calculate_total_score(lost_item, f)
            if score >= 40.0:
                reason = f"score={score:.1f}"
                matches.append(MatchRecord(lost_item_id=lost_item.item_id or -1,
                                           found_item_id=f.item_id or -1,
                                           match_score=score,
                                           match_reason=reason))
        matches.sort(key=lambda m: m.match_score, reverse=True)
        return matches
