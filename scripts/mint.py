from brownie import Gum, config, network

from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_opensea_uri,
)
from scripts.deploy import deploy, mint, withdraw


def main():
    account = get_account()
    gum = (
        Gum[-1]
        if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        else deploy(account)
    )

    # Fund the NFT contract with LINK
    print("Funding contract with LINK...")
    tx = fund_with_link(
        gum.address, account, config["networks"][network.show_active()]["fee"]
    )
    tx.wait(1)
    print("Funded.")

    # Mint an NFT
    print("Minting an NFT...")
    tx = mint(gum, account=account)
    tx.wait(1)
    print("Minted.")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(
            f"You can view your NFT at {get_opensea_uri(gum.address, gum.requestCounter())}"
        )

    # Withdraw tokens
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("Withdrawing tokens...")
        tx = withdraw(gum, account)
        tx.wait(1)
        print("Withdrawn.")
