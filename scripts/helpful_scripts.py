from brownie import (
    MockVRFCoordinator,
    LinkToken,
    network,
    accounts,
    config,
    Contract,
)
from brownie.network.account import Account

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache"]
MAINNET_OPENSEA_URL = "https://opensea.io/assets/matic"
TESTNET_OPENSEA_URL = "https://testnets.opensea.io/assets"
CONTRACT_TO_MOCK = {
    "vrf_coordinator": MockVRFCoordinator,
    "link_token": LinkToken,
}


def get_account(index: int = None, id=None) -> Account:
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name: str) -> Contract:
    contract_type = CONTRACT_TO_MOCK[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    MockVRFCoordinator.deploy(link_token.address, {"from": account})


def fund_with_link(
    contract_address: str,
    account: Account = get_account(),
    amount: int = 2 * 10 ** 18,
):
    link_token = get_contract("link_token")
    return link_token.transfer(contract_address, amount, {"from": account})


def get_opensea_uri(address: str, token_id: int):
    if network.show_active() == "polygon-main":
        return f"{MAINNET_OPENSEA_URL}/{address}/{token_id}"
    else:
        return f"{TESTNET_OPENSEA_URL}/{address}/{token_id}"
