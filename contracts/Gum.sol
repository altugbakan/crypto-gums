// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Gum is ERC721URIStorage, VRFConsumerBase {
    uint256 public constant MAX_MINT = 20000;
    uint256 public constant PRICE = 2000000000000000000; // 2 MATIC

    event requestedCollectible(
        bytes32 indexed requestID,
        uint256 tokenID,
        Flavor flavor
    );
    event gumAssigned(uint256 indexed tokenID, Properties properties);

    struct Properties {
        Flavor flavor;
        Wrapper wrapper;
        uint256 color;
    }

    enum Flavor {
        MINT,
        STRAWBERRY,
        BUBBLEGUM,
        BANANA
    }

    enum Wrapper {
        NONE,
        CHECKERS,
        DOTS,
        HEARTS,
        STRIPES
    }

    mapping(uint256 => Properties) public tokenIDToProperties;
    mapping(bytes32 => address) internal requestIDToSender;
    mapping(bytes32 => Flavor) internal requestIDToFlavor;

    uint256 public requestCounter;
    uint256 public tokenCounter;
    address public owner;
    uint256 internal fee;
    address internal linkToken;
    bytes32 internal keyHash;

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Crypto Gums", "GUM")
    {
        keyHash = _keyHash;
        fee = _fee;
        owner = msg.sender;
        linkToken = _linkToken;
    }

    function createCollectible(Flavor flavor) public payable {
        require(msg.value >= PRICE, "You need to send 2 MATIC.");
        require(requestCounter < MAX_MINT, "Cannot mint more gums.");
        requestCounter++;
        bytes32 requestID = requestRandomness(keyHash, fee);
        requestIDToSender[requestID] = msg.sender;
        requestIDToFlavor[requestID] = flavor;
        emit requestedCollectible(requestID, requestCounter, flavor);
    }

    function setTokenURI(uint256 _tokenID, string memory _tokenURI) public {
        require(msg.sender == owner, "Only admin can set URI");
        _setTokenURI(_tokenID, _tokenURI);
    }

    function withdraw() public {
        require(msg.sender == owner, "Only admin can withdraw");
        payable(msg.sender).transfer(address(this).balance);
    }

    function withdrawLink() public {
        require(msg.sender == owner, "Only admin can withdraw");
        IERC20 _linkToken = IERC20(linkToken);
        _linkToken.transfer(msg.sender, _linkToken.balanceOf(address(this)));
    }

    function fulfillRandomness(bytes32 _requestID, uint256 _randomNumber)
        internal
        override
    {
        uint256[] memory randomValues = _expand(_randomNumber, 3);
        Properties storage properties = tokenIDToProperties[tokenCounter];
        properties.flavor = requestIDToFlavor[_requestID];
        properties.wrapper = Wrapper(
            randomValues[0] % 2 == 0 ? 0 : (randomValues[1] % 4) + 1
        );
        properties.color = randomValues[2] % 2**24;
        emit gumAssigned(tokenCounter, properties);
        _safeMint(requestIDToSender[_requestID], tokenCounter);
        tokenCounter++;
    }

    function _expand(uint256 _randomValue, uint256 _n)
        internal
        pure
        returns (uint256[] memory expandedValues)
    {
        expandedValues = new uint256[](_n);
        for (uint256 i = 0; i < _n; i++) {
            expandedValues[i] = uint256(keccak256(abi.encode(_randomValue, i)));
        }
        return expandedValues;
    }
}
