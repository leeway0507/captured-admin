import sys

path = "/Users/yangwoolee/.pyenv/versions/3.10.9/lib/python3.10/site-packages/"
sys.path.append(path)
import os
from PIL import Image
import pillow_avif  # don't delete this line
import numpy as np

from components.file_manager import FileManager
from components.bg_remover import BgRemovalModel


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
        self._sku = None
        self.work_dir = ""
        self.model = BgRemovalModel()

    @property
    def sku(self):
        if not self._sku:
            raise (ValueError("sku is None"))
        return self._sku

    @sku.setter
    def sku(self, sku: str):
        self._sku = sku
        self.work_dir = os.path.join(self.path, sku)
        # self._create_resize_folder()
        self._create_upload_folder()

    def resize_v2(self):
        for file_raw in os.listdir(self.work_dir):
            file_name = file_raw.split(".")[0]
            if file_name in ["main"]:
                # if file_name in ["main", "sub-1", "sub-2", "sub-3", "sub-4"]:
                prod_img = self.preprocess_bg_remove_image(file_raw)
                # upload folder
                if file_name == "main":
                    template_img = self.set_template(prod_img, size=700)
                else:
                    template_img = self.set_template(prod_img, size=900)
                self.save_bg_remove_image(template_img, file_name)

    def preprocess_bg_remove_image(self, file_raw: str):
        origin_file_path = os.path.join(self.work_dir, file_raw)
        return self.remove_bg(origin_file_path)

    def remove_bg(self, file_path: str):
        self.model.file_path = file_path
        image = self.model.load_image()
        return self.model.remove_bg(image)

    def set_template(self, image: Image.Image, size=900):
        image = self.crop_image(image, size=size)
        image = image.convert("RGBA")

        # Create a new image with a transparent square of size 1000x1000
        new_size = (1000, 1000)
        paste_position = (
            (new_size[0] - image.width) // 2,
            (new_size[1] - image.height) // 2,
        )

        transparent_bg = Image.new("RGBA", new_size)
        transparent_bg.paste(image, paste_position, image)
        return transparent_bg

    def crop_image(self, prod_img: Image.Image, size: int = 900):
        cropped_image = self.crop_transparent_background(prod_img)

        if cropped_image.width >= cropped_image.height:
            aspect_ratio = cropped_image.width / cropped_image.height
            target_height = round(size / aspect_ratio)
            return cropped_image.resize((size, target_height))
        else:
            aspect_ratio = cropped_image.height / cropped_image.width
            target_width = round(size / aspect_ratio)
            return cropped_image.resize((target_width, size))

    def crop_transparent_background(self, image):
        # Find indices of non-transparent pixels (indices where alpha channel value is above zero).
        image = np.array(image)
        idx = np.where(image[:, :, 3] > 100)

        # Get minimum and maximum index in both axes (top left corner and bottom right corner)
        x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()

        # Crop rectangle and convert to Image
        cropped_image = Image.fromarray(image[y0 : y1 + 1, x0 : x1 + 1, :])

        return cropped_image

    def save_bg_remove_image(self, template_img: Image.Image, file_name: str):
        resize_file_path = os.path.join(self.work_dir, "upload", file_name + ".webp")

        return template_img.save(
            resize_file_path, quality=100, optimize=True, format="WEBP"
        )

    def preprocess_resize_image(self, file_raw: str):
        origin_file_path = os.path.join(self.work_dir, file_raw)
        prod_img = Image.open(origin_file_path)
        return self.set_template(prod_img, size=1000)

    def save_resize_image(self, template_img: Image.Image, file_name: str):
        resize_file_path = os.path.join(self.work_dir, "resize", file_name + ".webp")

        return template_img.save(
            resize_file_path, quality=100, optimize=True, format="WEBP"
        )

    def create_logo_thumbnail(self, name: str):
        file_path = os.path.join(self.work_dir, name)
        image = Image.open(file_path)
        prod_img = self.crop_image(image, size=700)
        prod_img = prod_img.convert("RGBA")

        # prod_wtih_gray_bg = Image.open(os.path.join(self.path, "gray_bg.png"))
        # prod_wtih_gray_bg = prod_wtih_gray_bg.resize(prod_img.size)
        # prod_wtih_gray_bg.paste(prod_img, (0, 0), prod_img)

        # Create a new image with a transparent square of size 1000x1000
        transparent_bg = Image.new("RGBA", prod_img.size)
        transparent_bg.paste(prod_img, (0, 0), prod_img)

        resize_file_path = self.resize_file_path(name)
        return transparent_bg.save(
            resize_file_path, quality=100, optimize=False, format="png"
        )

    ## depreciated

    def resize(self):
        for file_name in os.listdir(self.work_dir):
            if file_name.split(".")[0] in ["main", "sub-1", "sub-2", "sub-3", "sub-4"]:
                self.optimize_image(file_name)
        self.create_thumbnail()

    def _create_resize_folder(self):
        return FileManager.create_folder(os.path.join(self.work_dir, "resize"))

    def _create_upload_folder(self):
        return FileManager.create_folder(os.path.join(self.work_dir, "upload"))

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
        image = Image.open(file_path)
        prod_img = self.crop_image(image, size=700)
        prod_img = prod_img.convert("RGBA")

        # prod_wtih_gray_bg = Image.open(os.path.join(self.path, "gray_bg.png"))
        # prod_wtih_gray_bg = prod_wtih_gray_bg.resize(prod_img.size)
        # prod_wtih_gray_bg.paste(prod_img, (0, 0), prod_img)

        # Create a new image with a transparent square of size 1000x1000
        new_size = (1000, 1000)
        transparent_bg = Image.new("RGBA", new_size)

        paste_position = (
            (new_size[0] - prod_img.width) // 2,
            (new_size[1] - prod_img.height) // 2,
        )

        transparent_bg.paste(prod_img, paste_position, prod_img)

        resize_file_path = self.resize_file_path("thumbnail.webp")
        return transparent_bg.save(
            resize_file_path, quality=100, optimize=False, format="WEBP"
        )
