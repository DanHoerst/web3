from brownie import accounts, network

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account(index=0):
    # account = accounts.load("metamask-rinkeby")
    # account = accounts.add(config["wallets"]["from_key"])
    # account = accounts[0]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[index]
    else:
        return accounts.load("metamask-rinkeby")
