from brownie import accounts, config, MockV3Aggregator, network

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 18
STARTING_PRICE = 200000000000

def get_account():
    # account = accounts.load("metamask-rinkeby")
    # account = accounts.add(config["wallets"]["from_key"])
    # account = accounts[0]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.load("metamask-rinkeby")

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {
            "from": get_account()
        })
    print("Mocks deployed!")
