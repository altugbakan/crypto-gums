from brownie import Gum, network, config, Contract
from brownie.network.account import Account
import random

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_contract,
    get_opensea_uri,
)


def deploy(account: Account = get_account()):
    return Gum.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def mint(
    gum: Contract,
    flavor: int = random.randrange(0, 4),
    account: Account = get_account(),
):
    return gum.createCollectible(flavor, {"from": account, "value": gum.PRICE()})


def withdraw(gum: Contract, account: Account = get_account()):
    return gum.withdraw({"from": account})


def withdraw_link(gum: Contract, account: Account = get_account()):
    return gum.withdrawLink({"from": account})


def main():
    account = get_account()

    # Deploy the NFT contract
    print("Deploying NFT contract...")
    gum = deploy(account)
    print("Deployed.")

    # Fund the NFT contract with LINK
    print("Funding contract with LINK...")
    tx = fund_with_link(
        gum.address, account, config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)
    print("Funded.")

    # Mint an NFT
    print("Minting an NFT...")
    tx = mint(gum, 3, account=account)
    tx.wait(1)
    print("Minted.")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(
            f"You can view your NFT at {get_opensea_uri(gum.address, gum.tokenCounter())}"
        )

    # Withdraw tokens
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("Withdrawing tokens...")
        tx = withdraw(gum, account)
        tx.wait(1)
        tx = withdraw_link(gum, account)
        tx.wait(1)
        print("Withdrawn.")
