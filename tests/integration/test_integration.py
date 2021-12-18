from brownie import network, config
import pytest

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)
from scripts.deploy import deploy, mint


def test_can_create_and_withdraw():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    account = get_account()
    link_token = get_contract("link_token")
    fee = config["networks"][network.show_active()]["fee"]
    initial_balance = account.balance()
    initial_link_balance = link_token.balanceOf(account)
    gum = deploy(account)
    tx = fund_with_link(gum.address, account, fee * 5)
    tx.wait(1)

    # Act
    tx = mint(gum, 1, account)
    tx.wait(1)
    tx = gum.withdraw({"from": account})
    tx.wait(1)
    tx = gum.withdrawLink({"from": account})

    # Assert
    assert gum.requestCounter() == 1
    assert initial_balance - account.balance() < 2 * 10 ** 18
    assert initial_link_balance - link_token.balanceOf(account) == fee
