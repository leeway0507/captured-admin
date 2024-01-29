import pytest
from components.image_resize.image_resizer import ImageResizer
import os

current_path = __file__.rsplit("/", 1)[0]
sku = "test_pant"


@pytest.fixture(scope="module")
def Resizer():
    image = ImageResizer(current_path)
    image.sku = sku
    yield image


# def test_optimize_image(Resizer: ImageResizer):
#     file_name = "main.avif"
#     Resizer.optimize_image(file_name)
#     resize_path = os.path.join(current_path, sku, "resize")

#     assert os.path.exists(os.path.join(resize_path, "main.webp"))
#     # shutil.rmtree(resize_path)


def test_thumbnail(Resizer: ImageResizer):
    Resizer.create_thumbnail()
    resize_path = os.path.join(current_path, sku, "resize")
    assert os.path.exists(os.path.join(resize_path, "thumbnail.webp"))


# def test_resize_images(Resizer: ImageResizer):
#     Resizer.resize()
#     resize_path = os.path.join(current_path, sku, "resize")
#     # shutil.rmtree(resize_path)