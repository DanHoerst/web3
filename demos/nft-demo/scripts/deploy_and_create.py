from brownie import SimpleCollectible
from scripts.helpful_scripts import get_account

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def deploy_nft():
    account = get_account()
    collectible = SimpleCollectible.deploy({"from": account})
    tx = collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(f"Awesome, you can view your NFT at {OPENSEA_URL.format(collectible.address, collectible.tokenCounter() - 1)}")
    return collectible

def main():
    deploy_nft()
