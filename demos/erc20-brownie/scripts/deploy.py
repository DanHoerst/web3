from brownie import config, HoerstToken, network
from scripts.helpful_scripts import get_account

def deploy_erc20():
    account = get_account()
    initial_supply = 10000
    lottery = HoerstToken.deploy(
        initial_supply,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    account_balance = lottery.balanceOf(account)
    print(f"{account} balance is {account_balance}")

def main():
    deploy_erc20()
