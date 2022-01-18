from brownie import network
import pytest

from scripts.create_gum_image import create_image
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_assemble():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    with open("tests/unit/gum.svg", "r") as f:
        gum_image = f.readlines()
    flavor = "Banana"
    wrapper = "Hearts"
    color = "2BF09F"

    # Act
    assembled_image = create_image(flavor, wrapper, color)

    # Assert
    assert gum_image == assembled_image
