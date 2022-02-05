// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IGum {
    event RequestedCollectible(
        bytes32 indexed requestID,
        uint256 tokenID,
        uint256 flavor
    );
    event GumAssigned(
        uint256 indexed tokenID,
        uint256 flavor,
        uint256 wrapper,
        uint256 color
    );

    function tokenCounter() external view returns (uint256);

    function tokenID() external view returns (uint256);

    function tokenURI(uint256 tokenID)
        external
        view
        returns (string memory tokenURI);

    function tokenIDToProperties(uint256)
        external
        view
        returns (
            uint256,
            uint256,
            uint256
        );

    function createCollectible(uint256 flavor) external payable;

    function setTokenURI(uint256 tokenID, string memory tokenURI) external;

    function withdraw() external;

    function withdrawLink() external;
}
