import pytest
from components.image_resize import S3ImgUploader


current_path = __file__.rsplit("/", 1)[0]
sku = "test"


@pytest.fixture(scope="module")
def S3():
    s3_uploader = S3ImgUploader(current_path)
    s3_uploader.sku = sku
    yield s3_uploader


# def test_upload_and_delete(S3: S3ImgUploader):
#     S3.upload_image("thumbnail.webp")

#     assert S3.get_image_files() == ["cdn-images/product/test/thumbnail.webp"]

#     S3.delete_image("thumbnail.webp")
#     assert S3.get_image_files() == []


def test_upload_all_and_delete_all(S3: S3ImgUploader):
    S3.upload_all()
    print(S3.get_image_files())

    S3.delete_all()
    print(S3.get_image_files())