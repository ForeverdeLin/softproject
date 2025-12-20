"""Run a small demo of the RuleAgent + Matcher without external dependencies."""
from datetime import datetime, timedelta

from app.models import LostItem, FoundItem
from app.agent.rule_agent import RuleAgent


def main():
    # build one lost item and a few found items
    lost = LostItem(item_id=1,
                    user_id=10,
                    item_name="Black Wallet",
                    category="钱包",
                    lost_location="教学楼A-二楼走廊",
                    lost_time=datetime.now() - timedelta(hours=20),
                    description="黑色，皮质，有两张身份证",
                    color="黑色",
                    brand="无名")

    found_list = [
        FoundItem(item_id=101,
                  user_id=20,
                  item_name="Wallet",
                  category="钱包",
                  found_location="教学楼A-二楼走廊",
                  found_time=datetime.now() - timedelta(hours=10),
                  description="黑色皮质钱包，内有证件",
                  color="黑色",
                  brand="无名"),
        FoundItem(item_id=102,
                  user_id=21,
                  item_name="Phone",
                  category="手机",
                  found_location="教学楼B-一楼",
                  found_time=datetime.now() - timedelta(hours=5),
                  description="一部手机，黑色壳",
                  color="黑色",
                  brand="XBrand"),
    ]

    agent = RuleAgent()
    matches = agent.match_cycle(lost, found_list)

    print("Matches found:")
    for m in matches:
        print(f"lost:{m.lost_item_id} found:{m.found_item_id} score:{m.match_score} reason:{m.match_reason}")


if __name__ == "__main__":
    main()
