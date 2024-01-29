from .uploader import S3Uploader
import os


class S3ThumbnailUploader(S3Uploader):
    def __init__(self, local_path: str) -> None:
        super().__init__(bucket_name="captured-prod")
        self.s3_path = "cdn-images/thumbnail"
        self.local_path = local_path

    def upload_thumbnail(self, device: str, file_name: str):
        local_file_path = os.path.join(self.local_path, device, file_name)
        s3_file_path = os.path.join(self.s3_path, device, file_name)
        return super().upload(local_file_path, s3_file_path)

    def delete_thumbnail(self, device: str, file_name: str):
        s3_file_path = os.path.join(self.s3_path, device, file_name)
        return super().delete(s3_file_path)

    def update_thumbnail(self, device: str, file_name: str):
        self.delete_thumbnail(device, file_name)
        self.upload_thumbnail(device, file_name)
        super().invalidate_cloudfront_distribution([f"{self.s3_path}"])

    def upload_meta(self):
        local_file_path = os.path.join(self.local_path, "thumbnail.json")
        s3_file_path = os.path.join(self.s3_path, "thumbnail.json")
        return super().upload(local_file_path, s3_file_path)

    def delete_meta(self):
        s3_file_path = os.path.join(self.s3_path, "thumbnail.json")
        return super().delete(s3_file_path)

    def update_meta(self):
        self.delete_meta()
        self.upload_meta()
        super().invalidate_cloudfront_distribution([f"/{self.s3_path}/thumbnail.json"])

    def upload_all(self):
        for file_name in os.listdir(os.path.join(self.local_path, "pc")):
            self.upload_thumbnail("pc", file_name)

        for file_name in os.listdir(os.path.join(self.local_path, "mobile")):
            self.upload_thumbnail("mobile", file_name)

        self.upload_meta()

        super().invalidate_cloudfront_distribution([f"/{self.s3_path}/*"])

    def delete_all(self):
        for s3_file_path in self.get_thumbnail_files():
            super().delete(s3_file_path)

    def get_thumbnail_files(self):
        return super().get_files(self.s3_path)
