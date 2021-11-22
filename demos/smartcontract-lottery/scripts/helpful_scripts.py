from brownie import accounts, config, Contract, LinkToken, MockV3Aggregator, network, VRFCoordinator

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 18
STARTING_PRICE = 200000000000
CONTRACT_TO_MOCK = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinator,
    "link_token": LinkToken
}

def get_account():
    # account = accounts.load("metamask-rinkeby")
    # account = accounts.add(config["wallets"]["from_key"])
    # account = accounts[0]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.load("metamask-kovan")

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {
            "from": get_account()
        })
    link_token = LinkToken.deploy({"from": get_account()})
    VRFCoordinator.deploy(link_token, {
        "from": get_account()
    })
    print("Mocks deployed!")

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config if defined,
    otherwise, it will deploy a mock version of that contract, and return that mock contract.

    :args:
        contract_name (string)

    :return:
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract
    """
    contract_type = CONTRACT_TO_MOCK[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    #link_token_contra = interface.LinkTokenInterface(link_token.address, )
    tx.wait(1)
    print("Fund contract!")
    return tx
