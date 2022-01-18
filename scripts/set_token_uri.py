from brownie import Gum, interface, network, config, Contract
from brownie.network.account import Account

from scripts.create_metadata import get_uri, parse_properties
from scripts.helpful_scripts import get_account, get_opensea_uri


def set_token_uri(
    gum: Contract, token_id: int, uri: str, account: Account = get_account()
):
    tx = gum.setTokenURI(token_id, uri, {"from": account})
    tx.wait(1)


def main():
    account = get_account()
    gum = interface.IGum(
        config["networks"][network.show_active()].get("gum_address", Gum[-1])
    )
    for token_id in range(gum.tokenCounter()):
        flavor, wrapper, color = parse_properties(*gum.tokenIDToProperties(token_id))
        if not gum.tokenURI(token_id).startswith("ipfs://"):
            print("Setting token URI...")
            set_token_uri(
                gum, token_id, get_uri(token_id, flavor, wrapper, color), account
            )
            print("Set.")
            print(f"You can view your NFT at {get_opensea_uri(gum.address, token_id)}")
