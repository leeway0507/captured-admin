import pytest
import os
from components.bg_remover import BgRemovalModel

current_path = __file__.rsplit("/", 1)[0]
sku = "test_grey_bg"


@pytest.fixture(scope="module")
def Model():
    model = BgRemovalModel()
    yield model


def test_bg_removal(Model: BgRemovalModel):
    target = "main.jpg"
    path = os.path.join(current_path, target)
    Model.execute(path)

    assert os.path.exists(os.path.join(current_path, "removal", target))
