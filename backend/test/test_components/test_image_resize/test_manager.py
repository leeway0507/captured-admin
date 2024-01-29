import pytest
from components.image_resize import ImageResizeManager


current_path = __file__.rsplit("/", 1)[0]
sku = "test_pant"


@pytest.fixture(scope="module")
def manager():
    yield ImageResizeManager(current_path)


# def test_upload_and_delete(S3: S3ImgUploader):
#     S3.upload_image("thumbnail.webp")

#     assert S3.get_image_files() == ["cdn-images/product/test/thumbnail.webp"]

#     S3.delete_image("thumbnail.webp")
#     assert S3.get_image_files() == []


def test_upload_all_and_delete_all(manager: ImageResizeManager):
    manager.execute("test")
    print(manager.s3.get_image_files())

    manager.s3.delete_all()
    print(manager.s3.get_image_files())
