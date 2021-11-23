from brownie import config, HoerstToken, network
from scripts.helpful_scripts import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")

def deploy_erc20():
    account = get_account()

    token = HoerstToken.deploy(
        initial_supply,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    account_balance = token.balanceOf(account)
    print(f"{account} balance is {account_balance}")

def main():
    deploy_erc20()
