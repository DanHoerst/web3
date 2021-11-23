from brownie import network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import fund_with_link, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest
import time

def test_int_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    print("Lottery started!")
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10000})
    print("Lottery entrant added!")
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10000})
    print("Lottery entrant added!")
    fund_with_link(lottery)
    print("Lottery funded!")
    lottery.endLottery({"from": account})
    print("Lottery ended, sleeping...")
    print("Lottery over!")
    time_ct = 0
    while time_ct < 500:
        time.sleep(60)
        time_ct += 60
        if lottery.recentWinner() != "0x0000000000000000000000000000000000000000":
            break
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
