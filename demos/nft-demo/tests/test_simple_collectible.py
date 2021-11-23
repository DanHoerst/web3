from scripts.deploy_and_create import deploy_nft
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network
import pytest

def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    collectible = deploy_nft()
    assert collectible.ownerOf(0) == get_account()