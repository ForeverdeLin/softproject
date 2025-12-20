"""
测试通知智能体功能
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(project_root))

from app.database.db_manager import DatabaseManager
from app.agent.rule_agent import RuleAgent
from app.agent.notification_agent import NotificationAgent
from app.auth.auth_service import AuthService
from app.models import LostItem, FoundItem
from datetime import datetime, timedelta

def test_notification():
    """测试通知功能"""
    print("=" * 60)
    print("通知智能体功能测试")
    print("=" * 60)
    
    db_manager = DatabaseManager()
    rule_agent = RuleAgent()
    notification_agent = NotificationAgent(db_manager)
    auth_service = AuthService(db_manager)
    
    session = db_manager.get_session()
    
    try:
        # 1. 创建测试用户
        print("\n[1] 创建测试用户...")
        success, error_msg, user1 = auth_service.register_user(
            session, "2024001", "张三", "123456", "zhangsan@test.com", "13800000001"
        )
        if not success:
            # 如果用户已存在，尝试获取
            user1 = db_manager.get_user_by_student_id(session, "2024001")
            print(f"   用户已存在: {user1.name} (ID: {user1.id})")
        else:
            print(f"   ✅ 创建用户成功: {user1.name} (ID: {user1.id})")
        
        success, error_msg, user2 = auth_service.register_user(
            session, "2024002", "李四", "123456", "lisi@test.com", "13800000002"
        )
        if not success:
            user2 = db_manager.get_user_by_student_id(session, "2024002")
            print(f"   用户已存在: {user2.name} (ID: {user2.id})")
        else:
            print(f"   ✅ 创建用户成功: {user2.name} (ID: {user2.id})")
        
        # 2. 发布招领信息（先发布招领，这样后面发布失物时才能匹配）
        print("\n[2] 发布招领信息...")
        found = FoundItem(
            item_id=None,
            user_id=user2.id,
            item_name="黑色iPhone 15",
            category="手机",
            found_location="图书馆三楼",
            found_time=datetime.now() - timedelta(hours=2),
            description="黑色iPhone，有保护壳",
            color="黑色",
            brand="Apple"
        )
        db_found = db_manager.create_found_item(session, found)
        print(f"   ✅ 招领信息发布成功: {db_found.item_name} (ID: {db_found.id})")
        
        # 3. 发布失物信息（会触发匹配和通知）
        print("\n[3] 发布失物信息（触发匹配）...")
        lost = LostItem(
            item_id=None,
            user_id=user1.id,
            item_name="黑色iPhone 15",
            category="手机",
            lost_location="图书馆",
            lost_time=datetime.now() - timedelta(hours=3),
            description="黑色iPhone，有保护壳",
            color="黑色",
            brand="Apple"
        )
        db_lost = db_manager.create_lost_item(session, lost)
        print(f"   ✅ 失物信息发布成功: {db_lost.item_name} (ID: {db_lost.id})")
        
        # 4. 触发匹配
        print("\n[4] 触发智能匹配...")
        found_items = db_manager.get_all_found_items(session)
        matches = rule_agent.match_cycle(
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
        print(f"   ✅ 找到 {len(matches)} 个匹配")
        
        # 5. 保存匹配记录并发送通知
        print("\n[5] 保存匹配记录并发送通知...")
        from app.database import models_db
        
        for m in matches:
            db_match = db_manager.create_match_record(session, m)
            print(f"   匹配记录: 失物ID={m.lost_item_id}, 招领ID={m.found_item_id}, 匹配度={m.match_score:.1f}")
            
            # 获取招领信息
            db_found = session.query(models_db.FoundItemDB).filter_by(id=m.found_item_id).first()
            if db_found:
                notification_agent.notify_on_match(session, db_match, db_lost, db_found)
                print(f"   ✅ 已发送匹配通知")
        
        # 6. 检查通知记录
        print("\n[6] 检查通知记录...")
        notifications_user1 = notification_agent.get_user_notifications(session, user1.id, unread_only=False)
        notifications_user2 = notification_agent.get_user_notifications(session, user2.id, unread_only=False)
        
        print(f"\n   用户 {user1.name} 的通知 ({len(notifications_user1)} 条):")
        for n in notifications_user1:
            print(f"   - [{n.notification_type}] {n.title}")
            print(f"     内容: {n.content[:50]}...")
            print(f"     时间: {n.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"     已读: {'是' if n.is_read else '否'}")
        
        print(f"\n   用户 {user2.name} 的通知 ({len(notifications_user2)} 条):")
        for n in notifications_user2:
            print(f"   - [{n.notification_type}] {n.title}")
            print(f"     内容: {n.content[:50]}...")
            print(f"     时间: {n.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"     已读: {'是' if n.is_read else '否'}")
        
        # 7. 测试未读通知数量
        print("\n[7] 检查未读通知数量...")
        unread_count1 = db_manager.get_unread_notification_count(session, user1.id)
        unread_count2 = db_manager.get_unread_notification_count(session, user2.id)
        print(f"   用户 {user1.name} 未读通知: {unread_count1} 条")
        print(f"   用户 {user2.name} 未读通知: {unread_count2} 条")
        
        # 8. 测试提醒功能（创建一些旧的未解决项目）
        print("\n[8] 测试提醒功能...")
        old_lost = LostItem(
            item_id=None,
            user_id=user1.id,
            item_name="测试物品-8天前",
            category="其他",
            lost_location="测试地点",
            lost_time=datetime.now() - timedelta(days=8),
            description="测试提醒功能",
        )
        db_old_lost = db_manager.create_lost_item(session, old_lost)
        print(f"   ✅ 创建了8天前的失物记录 (ID: {db_old_lost.id})")
        
        # 触发提醒检查
        notification_agent.check_and_remind_unresolved(session)
        print(f"   ✅ 已执行提醒检查")
        
        # 再次检查通知
        notifications_user1_after = notification_agent.get_user_notifications(session, user1.id, unread_only=False)
        print(f"   用户 {user1.name} 现在有 {len(notifications_user1_after)} 条通知（应该包含提醒）")
        
        print("\n" + "=" * 60)
        print("✅ 测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == '__main__':
    test_notification()

