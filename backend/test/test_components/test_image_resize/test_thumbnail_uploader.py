import pytest
from components.image_resize.thumbnail_uploader import S3ThumbnailUploader
import os

current_path = __file__.rsplit("/", 1)[0]
sku = "test"


@pytest.fixture(scope="module")
def Thumbnail():
    image = S3ThumbnailUploader(os.path.join(current_path, "thumbnail"))
    yield image


# def test_upload_and_delete(Thumbnail: S3ThumbnailUploader):
#     Thumbnail.upload_thumbnail("pc", "1.jpg")

#     print(Thumbnail.get_thumbnail_files())

#     Thumbnail.delete_thumbnail("pc", "1.jpg")

#     print(Thumbnail.get_thumbnail_files())

#     # assert Thumbnail.get_image_files() == []


def test_upload_meta(Thumbnail: S3ThumbnailUploader):
    Thumbnail.update_meta()


# def test_upload_meta(Thumbnail: S3ThumbnailUploader):
#     Thumbnail.delete_meta()
#     Thumbnail.upload_meta()


# def test_upload_all(Thumbnail: S3ThumbnailUploader):
#     Thumbnail.upload_all()
