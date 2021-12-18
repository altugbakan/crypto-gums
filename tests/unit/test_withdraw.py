from brownie import network, config, accounts, exceptions
import random
import pytest

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
    fund_with_link,
)
from scripts.deploy import deploy, mint


def test_can_withdraw():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    initial_balance = account.balance()
    gum = deploy(account)
    tx = fund_with_link(
        gum.address, account, config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)
    tx = mint(gum, 1, account)
    tx.wait(1)
    requestID = tx.events["requestedCollectible"]["requestID"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestID, random.randrange(0, 2 ** 24), gum.address, {"from": account}
    )

    # Act
    tx = gum.withdraw({"from": account})
    tx.wait(1)

    # Assert
    assert initial_balance == account.balance()


def test_only_owner_can_withdraw():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    gum = deploy(account)
    tx = fund_with_link(
        gum.address, account, config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)
    tx = mint(gum, 1, account)
    tx.wait(1)
    requestID = tx.events["requestedCollectible"]["requestID"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestID, random.randrange(0, 2 ** 24), gum.address, {"from": account}
    )

    # Act / Assert
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        gum.withdraw({"from": bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        gum.withdrawLink({"from": bad_actor})


def test_can_withdraw_link():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    gum = deploy(account)
    link_token = get_contract("link_token")
    initial_balance = link_token.balanceOf(account)
    tx = fund_with_link(
        gum.address, account, config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)

    # Act
    tx = gum.withdrawLink({"from": account})
    tx.wait(1)

    # Assert
    assert link_token.balanceOf(account) == initial_balance
