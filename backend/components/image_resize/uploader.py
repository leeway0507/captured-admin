import boto3
import os
from typing import List
import time
from components.file_manager import FileManager
from components.env import prod_env


class S3Uploader:
    def __init__(self, bucket_name) -> None:
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")

    def health(self):
        if self.s3.list_buckets():
            return 200
        return 400

    def get_files(self, s3_folder_path: str):
        objects = self.s3.list_objects_v2(
            Bucket=self.bucket_name, Prefix=s3_folder_path
        )
        return [obj["Key"] for obj in objects.get("Contents", [])]

    def rename_folder(self, old_s3_folder_path: str, new_s3_folder_path: str):
        # Rename each object by copying to the new folder
        for old_key in self.get_files(old_s3_folder_path):
            new_key = new_s3_folder_path + old_key[len(old_s3_folder_path) :]

            self.s3.copy_object(
                Bucket=self.bucket_name,
                CopySource={"Bucket": self.bucket_name, "Key": old_key},
                Key=new_key,
            )

            self.s3.delete_object(Bucket=self.bucket_name, Key=old_key)
        return self.get_files(new_s3_folder_path)

    def upload(self, local_file_path: str, s3_file_path: str):
        self.s3.upload_file(local_file_path, self.bucket_name, s3_file_path)

    def delete(self, s3_file_path: str):
        return self.s3.delete_object(Bucket=self.bucket_name, Key=s3_file_path)

    def update(self, local_file_path: str, s3_file_path: str):
        self.delete(s3_file_path)
        self.upload(local_file_path, s3_file_path)
        return {"status": "success"}

    def invalidate_cloudfront_distribution(self, path: List):
        cloudfront_client = boto3.client("cloudfront")
        invalidation_response = cloudfront_client.create_invalidation(
            DistributionId=prod_env.CLOUDFRONT_DISTRIBUTION_ID,
            InvalidationBatch={
                "Paths": {"Quantity": len(path), "Items": path},
                "CallerReference": f"my-invalidation-{int(time.time())}",
            },
        )

        # Print the invalidation response
        print("Invalidation request Success! ")


class S3ImgUploader(S3Uploader):
    def __init__(self, local_path: str) -> None:
        super().__init__(bucket_name="captured-prod")
        self.s3_path = "cdn-images/product"
        self._sku = ""
        self.local_path = local_path

    @property
    def sku(self):
        if not self._sku:
            raise (ValueError("sku is None"))
        return self._sku

    @sku.setter
    def sku(self, sku: str):
        self._sku = sku
        self.local_resize_dir = os.path.join(self.local_path, sku, "upload")
        self.s3_dir = os.path.join(self.s3_path, sku)

    def upload_all(self):
        if not os.path.exists(self.local_resize_dir):
            raise (FileNotFoundError(f"{self.local_resize_dir} doesn't exist"))

        for file_name in os.listdir(self.local_resize_dir):
            img_type = ["thumbnail", "main", "sub-1", "sub-2", "sub-3", "sub-4"]
            if file_name.split(".")[0] in img_type:
                self.upload_image(file_name)

        return super().get_files(self.s3_dir)

    def delete_all(self):
        for s3_file_path in self.get_image_files():
            super().delete(s3_file_path)

    def upload_image(self, file_name: str):
        local_file_path = os.path.join(self.local_resize_dir, file_name)
        s3_file_path = os.path.join(self.s3_dir, file_name)
        return super().upload(local_file_path, s3_file_path)

    def delete_image(self, file_name: str):
        s3_file_path = os.path.join(self.s3_dir, file_name)
        return super().delete(s3_file_path)

    def update_image(self, file_name: str):
        self.delete_image(file_name)
        self.upload_image(file_name)
        super().invalidate_cloudfront_distribution([f"/{self.s3_dir}/{file_name}"])

        return {"status": "success"}

    def get_image_files(self):
        return super().get_files(self.s3_dir)
