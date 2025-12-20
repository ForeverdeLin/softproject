"""Initialize DB, add sample found item, then create a lost via Flask test client to show matching."""
from app.main import create_app
from app.database.db import init_db
from app.database.db_manager import DatabaseManager
from datetime import datetime, timedelta


def run_demo():
    init_db()
    dbm = DatabaseManager()
    session = dbm.get_session()
    try:
        # add a sample found item
        from app.models import FoundItem
        f = FoundItem(item_id=None, user_id=2, item_name='Black Wallet', category='钱包', found_location='教学楼A-二楼走廊', found_time=datetime.now()-timedelta(hours=10), description='黑色皮质钱包', color='黑色', brand='无名')
        dbm.create_found_item(session, f)
    finally:
        session.close()

    app = create_app()
    client = app.test_client()

    lost_payload = {
        'user_id': 1,
        'item_name': 'Black Wallet',
        'category': '钱包',
        'lost_location': '教学楼A-二楼走廊',
        'lost_time': (datetime.now()-timedelta(hours=20)).isoformat(),
        'description': '黑色，皮质，有两张身份证',
        'color': '黑色',
        'brand': '无名'
    }

    resp = client.post('/lost', json=lost_payload)
    print('POST /lost ->', resp.status_code, resp.get_json())

    lost_id = resp.get_json().get('lost_id')
    resp2 = client.get(f'/matches/{lost_id}')
    print('GET /matches ->', resp2.status_code, resp2.get_json())


if __name__ == '__main__':
    run_demo()
