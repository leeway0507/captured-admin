import pytest
from components.image_resizer import ImageResizer
import os
from os.path import join
from tqdm import tqdm

current_path = __file__.rsplit("/", 1)[0]
sku = "test"


@pytest.fixture(scope="module")
def Resizer():
    path = join(current_path, "product")
    # path = current_path
    image = ImageResizer(path)
    image.sku = sku
    yield image


def test_exctract_product(Resizer: ImageResizer):
    for sku in tqdm(os.listdir(join(current_path, "product"))):
        if sku == ".DS_Store":
            continue
        resize_path = join(current_path, "product", sku)
        if os.path.exists(resize_path):
            Resizer.sku = str(sku)
            Resizer.resize_v2()


# def test_resize_v2(Resizer: ImageResizer):
#     Resizer.resize_v2()
#     resize_path = os.path.join(current_path, sku, "resize")
#     assert os.path.exists(os.path.join(resize_path, "main.webp"))
#     # shutil.rmtree(resize_path)


# def test_preprocess_resize_image(Resizer: ImageResizer):
#     file_name = "main.jpg"
#     img = Resizer.preprocess_resize_image(file_name)
#     file_path = os.path.join(
#         current_path, sku, "test_preprocess_resize_image", "test.webp"
#     )
#     img.save(file_path, quality=100, optimize=True, format="webp")

#     assert os.path.exists(file_path)
#     # shutil.rmtree(file_path)


# def test_preprocess_bg_remove_image(Resizer: ImageResizer):
#     # file_name = "main.jpg"
#     file_name = "sub-3.webp"
#     img = Resizer.preprocess_bg_remove_image(file_name)
#     file_path = os.path.join(
#         current_path, sku, "test_preprocess_resize_image", "test.webp"
#     )
#     img.save(file_path, quality=100, optimize=True, format="webp")

#     assert os.path.exists(file_path)
#     # shutil.rmtree(resize_path)


# def test_create_logo_thumbnail():
#     files = os.listdir(
#         "/Users/yangwoolee/repo/captured/main/frontend/public/brands/white"
#     )
#     current_path = "/Users/yangwoolee/repo/captured/main/frontend/public/brands/"
#     sku = "white"
#     Resizer = ImageResizer(current_path)
#     Resizer.sku = sku

#     for f in files:
#         if f.split(".")[-1] == "png":
#             Resizer.create_logo_thumbnail(f)


# def test_thumbnail(Resizer: ImageResizer):
#     Resizer.create_thumbnail()
#     resize_path = os.path.join(current_path, sku, "resize")
#     assert os.path.exists(os.path.join(resize_path, "thumbnail.webp"))


# def test_resize_images(Resizer: ImageResizer):
#     Resizer.resize()
#     resize_path = os.path.join(current_path, sku, "resize")
#     # shutil.rmtree(resize_path)
