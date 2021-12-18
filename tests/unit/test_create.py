from brownie import network, config
import random
import pytest

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
    fund_with_link,
)
from scripts.deploy import deploy, mint


def test_can_create():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    gum = deploy(account)
    tx = fund_with_link(
        gum.address, account, config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)

    # Act / Assert
    tx = mint(gum, account=account)
    tx.wait(1)
    assert gum.requestCounter() == 1
    assert gum.tokenCounter() == 0
    requestID = tx.events["requestedCollectible"]["requestID"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestID, random.randrange(0, 2 ** 24), gum.address, {"from": account}
    )
    assert gum.tokenCounter() == 1


def test_can_set_flavor():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    gum = deploy(account)
    tx = fund_with_link(
        gum.address, account, config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)

    # Act
    tx = mint(gum, 1, account)
    tx.wait(1)
    requestID = tx.events["requestedCollectible"]["requestID"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestID, random.randrange(0, 2 ** 24), gum.address, {"from": account}
    )

    # Assert
    assert gum.tokenIDToProperties(0)[0] == 1
