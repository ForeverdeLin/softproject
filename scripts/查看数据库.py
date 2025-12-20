"""查看数据库内容的工具脚本"""
from app.database.db_manager import DatabaseManager
from app.database.db import init_db
from sqlalchemy import text

def view_database():
    """查看数据库所有表的内容"""
    db_manager = DatabaseManager()
    session = db_manager.get_session()
    
    try:
        print("=" * 60)
        print("数据库内容查看")
        print("=" * 60)
        
        # 查看用户表
        print("\n【用户表 (users)】")
        print("-" * 60)
        users = session.execute(text("SELECT id, student_id, name, email, phone, created_at FROM users")).fetchall()
        if users:
            print(f"{'ID':<5} {'学号':<15} {'姓名':<10} {'邮箱':<20} {'电话':<15} {'创建时间'}")
            print("-" * 60)
            for user in users:
                print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10} {user[3] or '':<20} {user[4] or '':<15} {user[5]}")
        else:
            print("暂无用户数据")
        
        # 查看失物表
        print("\n【失物表 (lost_items)】")
        print("-" * 60)
        lost_items = session.execute(text("""
            SELECT id, user_id, item_name, category, lost_location, 
                   lost_time, description, color, brand, is_resolved 
            FROM lost_items
        """)).fetchall()
        if lost_items:
            print(f"{'ID':<5} {'用户ID':<8} {'物品名称':<15} {'类别':<8} {'丢失地点':<20} {'丢失时间':<20} {'已解决'}")
            print("-" * 60)
            for item in lost_items:
                print(f"{item[0]:<5} {item[1] or '':<8} {item[2]:<15} {item[3]:<8} {item[4]:<20} {str(item[5])[:19]:<20} {'是' if item[9] else '否'}")
        else:
            print("暂无失物数据")
        
        # 查看招领表
        print("\n【招领表 (found_items)】")
        print("-" * 60)
        found_items = session.execute(text("""
            SELECT id, user_id, item_name, category, found_location, 
                   found_time, description, color, brand, is_resolved 
            FROM found_items
        """)).fetchall()
        if found_items:
            print(f"{'ID':<5} {'用户ID':<8} {'物品名称':<15} {'类别':<8} {'拾获地点':<20} {'拾获时间':<20} {'已解决'}")
            print("-" * 60)
            for item in found_items:
                print(f"{item[0]:<5} {item[1] or '':<8} {item[2]:<15} {item[3]:<8} {item[4]:<20} {str(item[5])[:19]:<20} {'是' if item[9] else '否'}")
        else:
            print("暂无招领数据")
        
        # 查看匹配记录表
        print("\n【匹配记录表 (match_records)】")
        print("-" * 60)
        matches = session.execute(text("""
            SELECT id, lost_item_id, found_item_id, match_score, 
                   match_reason, is_notified, created_at 
            FROM match_records
            ORDER BY match_score DESC
        """)).fetchall()
        if matches:
            print(f"{'ID':<5} {'失物ID':<8} {'招领ID':<8} {'匹配分数':<10} {'已通知':<8} {'创建时间'}")
            print("-" * 60)
            for match in matches:
                print(f"{match[0]:<5} {match[1]:<8} {match[2]:<8} {match[3]:<10.1f} {'是' if match[5] else '否':<8} {str(match[6])[:19]}")
        else:
            print("暂无匹配记录")
        
        # 统计信息
        print("\n【统计信息】")
        print("-" * 60)
        user_count = session.execute(text("SELECT COUNT(*) FROM users")).scalar()
        lost_count = session.execute(text("SELECT COUNT(*) FROM lost_items")).scalar()
        found_count = session.execute(text("SELECT COUNT(*) FROM found_items")).scalar()
        match_count = session.execute(text("SELECT COUNT(*) FROM match_records")).scalar()
        
        print(f"用户总数: {user_count}")
        print(f"失物总数: {lost_count}")
        print(f"招领总数: {found_count}")
        print(f"匹配记录总数: {match_count}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == '__main__':
    view_database()

