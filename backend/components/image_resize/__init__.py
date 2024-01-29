from .image_resizer import ImageResizer
from .uploader import S3ImgUploader
from .thumbnail_uploader import S3ThumbnailUploader


class ImageResizeManager:
    def __init__(self, local_path: str) -> None:
        self.resizer = ImageResizer(local_path)
        self.s3 = S3ImgUploader(local_path)

    def execute(self, sku: str):
        self.resizer.sku = sku
        self.s3.sku = sku

        self.resizer.resize()
        self.s3.upload_all()
        return sku

    def update_image(self, sku: str, file_name: str):
        self.s3.sku = sku
        self.resizer.sku = sku

        # if file_name == "thumbnail":
        #     self.resizer.create_thumbnail()
        # else:
        #     self.resizer.optimize_image(file_name)

        self.s3.update_image(file_name + ".webp")

    def update_thumbnail_image(self):
        self.resizer.create_thumbnail()

    def update_product_images(self, file_name: str):
        self.resizer.optimize_image(file_name)
