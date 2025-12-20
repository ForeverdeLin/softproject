"""测试匹配引擎"""
import unittest
from datetime import datetime, timedelta
from app.models import LostItem, FoundItem
from app.agent.matcher import Matcher


class TestMatcher(unittest.TestCase):
    """匹配引擎测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.matcher = Matcher()
    
    def test_match_by_category_same(self):
        """测试类别匹配 - 相同类别"""
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=datetime.now(), description="黑色钱包"
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="钱包",
            category="钱包", found_location="图书馆",
            found_time=datetime.now(), description="黑色钱包"
        )
        score = self.matcher.match_by_category(lost, found)
        self.assertEqual(score, 40.0)
    
    def test_match_by_category_different(self):
        """测试类别匹配 - 不同类别"""
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=datetime.now(), description="黑色钱包"
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="手机",
            category="手机", found_location="图书馆",
            found_time=datetime.now(), description="黑色手机"
        )
        score = self.matcher.match_by_category(lost, found)
        self.assertEqual(score, 0.0)
    
    def test_match_by_location_exact(self):
        """测试地点匹配 - 完全相同"""
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆一楼",
            lost_time=datetime.now(), description=""
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="钱包",
            category="钱包", found_location="图书馆一楼",
            found_time=datetime.now(), description=""
        )
        score = self.matcher.match_by_location(lost, found)
        self.assertEqual(score, 25.0)
    
    def test_match_by_location_contained(self):
        """测试地点匹配 - 包含关系"""
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=datetime.now(), description=""
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="钱包",
            category="钱包", found_location="图书馆一楼",
            found_time=datetime.now(), description=""
        )
        score = self.matcher.match_by_location(lost, found)
        self.assertEqual(score, 20.0)
    
    def test_match_by_time_24h(self):
        """测试时间匹配 - 24小时内"""
        now = datetime.now()
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=now - timedelta(hours=12),
            description=""
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="钱包",
            category="钱包", found_location="图书馆",
            found_time=now,
            description=""
        )
        score = self.matcher.match_by_time(lost, found)
        self.assertEqual(score, 20.0)
    
    def test_match_by_time_72h(self):
        """测试时间匹配 - 72小时内"""
        now = datetime.now()
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=now - timedelta(hours=48),
            description=""
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="钱包",
            category="钱包", found_location="图书馆",
            found_time=now,
            description=""
        )
        score = self.matcher.match_by_time(lost, found)
        self.assertEqual(score, 15.0)
    
    def test_match_by_features_color(self):
        """测试特征匹配 - 颜色匹配"""
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=datetime.now(), description="",
            color="黑色"
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="钱包",
            category="钱包", found_location="图书馆",
            found_time=datetime.now(), description="",
            color="黑色"
        )
        score = self.matcher.match_by_features(lost, found)
        self.assertGreaterEqual(score, 5.0)
    
    def test_match_by_features_brand(self):
        """测试特征匹配 - 品牌匹配"""
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=datetime.now(), description="",
            brand="LV"
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="钱包",
            category="钱包", found_location="图书馆",
            found_time=datetime.now(), description="",
            brand="LV"
        )
        score = self.matcher.match_by_features(lost, found)
        self.assertGreaterEqual(score, 5.0)
    
    def test_calculate_total_score_high(self):
        """测试综合评分 - 高匹配度"""
        now = datetime.now()
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆一楼",
            lost_time=now - timedelta(hours=12),
            description="黑色钱包", color="黑色", brand="LV"
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="钱包",
            category="钱包", found_location="图书馆一楼",
            found_time=now,
            description="黑色钱包", color="黑色", brand="LV"
        )
        score = self.matcher.calculate_total_score(lost, found)
        self.assertGreaterEqual(score, 60.0)
    
    def test_calculate_total_score_category_mismatch(self):
        """测试综合评分 - 类别不匹配应返回0"""
        lost = LostItem(
            item_id=1, user_id=1, item_name="钱包",
            category="钱包", lost_location="图书馆",
            lost_time=datetime.now(), description=""
        )
        found = FoundItem(
            item_id=1, user_id=2, item_name="手机",
            category="手机", found_location="图书馆",
            found_time=datetime.now(), description=""
        )
        score = self.matcher.calculate_total_score(lost, found)
        self.assertEqual(score, 0.0)


if __name__ == '__main__':
    unittest.main()

