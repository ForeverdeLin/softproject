"""测试规则型智能体"""
import unittest
from datetime import datetime, timedelta
from app.models import LostItem, FoundItem
from app.agent.rule_agent import RuleAgent


class TestRuleAgent(unittest.TestCase):
    """规则型智能体测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.agent = RuleAgent()
    
    def test_match_cycle_no_matches(self):
        """测试匹配循环 - 无匹配"""
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=datetime.now(), description=""
        )
        found_items = [
            FoundItem(
                item_id=1, user_id=2, item_name="手机",
                category="手机", found_location="图书馆",
                found_time=datetime.now(), description=""
            )
        ]
        matches = self.agent.match_cycle(lost, found_items)
        self.assertEqual(len(matches), 0)
    
    def test_match_cycle_has_matches(self):
        """测试匹配循环 - 有匹配"""
        now = datetime.now()
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆一楼",
            lost_time=now - timedelta(hours=12),
            description="黑色钱包", color="黑色"
        )
        found_items = [
            FoundItem(
                item_id=1, user_id=2, item_name="钱包",
                category="钱包", found_location="图书馆一楼",
                found_time=now,
                description="黑色钱包", color="黑色"
            )
        ]
        matches = self.agent.match_cycle(lost, found_items)
        self.assertGreater(len(matches), 0)
        self.assertGreaterEqual(matches[0].match_score, 40.0)
    
    def test_match_cycle_sorted(self):
        """测试匹配循环 - 结果按分数排序"""
        now = datetime.now()
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=now, description=""
        )
        found_items = [
            FoundItem(
                item_id=1, user_id=2, item_name="钱包",
                category="钱包", found_location="图书馆",
                found_time=now, description=""
            ),
            FoundItem(
                item_id=2, user_id=3, item_name="钱包",
                category="钱包", found_location="教学楼",
                found_time=now, description=""
            )
        ]
        matches = self.agent.match_cycle(lost, found_items)
        if len(matches) >= 2:
            self.assertGreaterEqual(matches[0].match_score, matches[1].match_score)


if __name__ == '__main__':
    unittest.main()

