# Crypto Gums

<div align="center">
    <a href=https://cryptogum.shop>
        <img src=https://user-images.githubusercontent.com/43248015/146649062-4479da2a-f528-4593-8330-5ede0a0dffeb.gif>
    </a>
    <h3>Contract for the <a href=https://cryptogum.shop>Crypto Gums</a> NFT.<h3>
    <h3> <a href=https://polygonscan.com/address/0xe7d8Db9d11D56dB3cf11de9bA624f3891318483F>0xe7d8Db9d11D56dB3cf11de9bA624f3891318483F</a> on Polygon Chain</h3>
</div>
<br />

## Features
- Gums are generated using the results from [Chainlink VRF](https://docs.chain.link/docs/chainlink-vrf/).

- The metadata is saved on [NFT.Storage](https://nft.storage), which uses [IPFS](https://ipfs.io/) for decentralized storage.

## Usage

You need [eth-brownie](https://eth-brownie.readthedocs.io/en/stable/) to deploy the contract and run scripts.

You can deploy a version of the contract using
```shell
$ brownie run scripts/deploy.py
```
You will need testnet ETH and LINK for testing on Rinkeby. You can get some from the [Chainlink Faucet](https://faucets.chain.link/rinkeby).

The script for building the Gum image can be found in [create_gum_image.py](./scripts/create_gum_image.py). You can use [set_token_uri.py](./scripts/set_token_uri.py) to build and set the image metadata.

## Thanks
Thanks to [freeCodeCamp](https://www.freecodecamp.org/), [Patrick Collins](https://twitter.com/PatrickAlphaC) and [buildspace](https://buildspace.so/) for their content.

Special thanks to [Begüm Bakan](https://github.com/begumbakan) for providing the assets.

## License
The contract and code are MIT licensed.
