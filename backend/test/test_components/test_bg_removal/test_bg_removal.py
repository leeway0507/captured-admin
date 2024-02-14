import pytest
import os
from components.bg_removal import BgRemovalModel

current_path = __file__.rsplit("/", 1)[0]
sku = "test_grey_bg"


@pytest.fixture(scope="module")
def Model():
    model = BgRemovalModel()
    yield model


def test_bg_removal(Model: BgRemovalModel):
    path = os.path.join(current_path, "test2.avif")
    Model.execute(path)

    assert os.path.exists(os.path.join(current_path, "removal", "tes2.avif"))
