import boto3
import os
from pathlib import Path
from PIL import Image
import pillow_avif  # don't delete this line
from dotenv import dotenv_values
import shutil
import time
from components.file_manager import FileManager


config = dotenv_values(".env.production")
img_type = (
    ".jpg",
    ".jpeg",
    ".png",
    ".avif",
    ".webp",
    ".JPG",
    ".JPEG",
    ".PNG",
    ".AVIF",
)


class ImageResizer:
    def __init__(self, path: str) -> None:
        self.path = path
        self.File = FileManager(path)
        self._sku = None
        self.work_dir = ""

    @property
    def sku(self):
        if not self._sku:
            raise (ValueError("sku is None"))
        return self._sku

    @sku.setter
    def sku(self, sku: str):
        self._sku = sku
        self.work_dir = os.path.join(self.path, sku)
        self._create_resize_folder()

    def resize(self):
        for file_name in os.listdir(self.work_dir):
            if file_name.split(".")[0] in ["main", "sub-1", "sub-2", "sub-3", "sub-4"]:
                self.optimize_image(file_name)
        self.create_thumbnail()

    def _create_resize_folder(self):
        return self.File.create_folder(os.path.join(self.work_dir, "resize"))

    def optimize_image(self, file_name: str):
        img = Image.open(os.path.join(self.work_dir, file_name))
        aspect_ratio = img.width / img.height

        resize_file_name = file_name.split(".")[0] + ".webp"
        resize_file_path = self.resize_file_path(resize_file_name)

        if img.width > 1000:
            target_width = 1000
            target_height = round(target_width / aspect_ratio)
            img = img.resize((target_width, target_height))

        return img.save(resize_file_path, quality=100, optimize=True, format="WEBP")

    def resize_file_path(self, resize_file_name: str):
        return os.path.join(self.work_dir, "resize", resize_file_name)

    def create_thumbnail(self):
        file_path = os.path.join(self.work_dir, "thumbnail.png")
        img = self.crop_image(file_path, size=700)
        img_with_white_bg = Image.new("RGBA", img.size, "WHITE")
        img_with_white_bg.paste(img, (0, 0), img)

        # Create a new image with a transparent square of size 1000x1000
        new_size = (1000, 1000)
        centered_image = Image.new("RGB", new_size, "white")

        paste_position = (
            (new_size[0] - img.width) // 2,
            (new_size[1] - img.height) // 2,
        )

        centered_image.paste(img_with_white_bg, paste_position)

        resize_file_path = self.resize_file_path("thumbnail.webp")
        return centered_image.save(
            resize_file_path, quality=100, optimize=False, format="WEBP"
        )

    def crop_image(self, file_path: str, size: int = 700):
        image = Image.open(file_path)
        bbox = image.getbbox()
        cropped_image = image.crop(bbox)

        if cropped_image.width >= cropped_image.height:
            aspect_ratio = cropped_image.width / cropped_image.height
            target_height = round(size / aspect_ratio)
            return cropped_image.resize((size, target_height))
        else:
            aspect_ratio = cropped_image.height / cropped_image.width
            target_width = round(size / aspect_ratio)
            return cropped_image.resize((target_width, size))
