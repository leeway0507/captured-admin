import argparse
import os
from PIL import Image
import numpy as np


def crop_image(prod_img: Image.Image, size: int = 900):
    if prod_img.mode == "RGBA":
        cropped_image = crop_transparent_background(prod_img)
    else:
        cropped_image = prod_img

    if cropped_image.width >= cropped_image.height:
        aspect_ratio = cropped_image.width / cropped_image.height
        target_height = round(size / aspect_ratio)
        return cropped_image.resize((size, target_height))
    else:
        aspect_ratio = cropped_image.height / cropped_image.width
        target_width = round(size / aspect_ratio)
        return cropped_image.resize((target_width, size))


def crop_transparent_background(image):
    # Find indices of non-transparent pixels (indices where alpha channel value is above zero).
    image = np.array(image)
    idx = np.where(image[:, :, 3] > 100)

    # Get minimum and maximum index in both axes (top left corner and bottom right corner)
    x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()

    # Crop rectangle and convert to Image
    cropped_image = Image.fromarray(image[y0 : y1 + 1, x0 : x1 + 1, :])

    return cropped_image


def set_template(image, size=900):
    image = crop_image(image, size=size)
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


def save_resize_image(template_img: Image.Image, file_path: str):
    resize_file_path = os.path.join(file_path.split(".")[0] + ".webp")

    return template_img.save(
        resize_file_path, quality=100, optimize=True, format="WEBP"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="image template")
    parser.add_argument("--file_path", default=None, help="file_path")

    args = parser.parse_args()

    file_path: str = args.file_path
    if not file_path:
        raise ValueError("file_path not exist", file_path)

    prod_img = Image.open(file_path)

    if file_path.rsplit("/", 1)[-1].split(".")[0] == "main":
        prod_img = set_template(prod_img, size=700)
    else:
        prod_img = set_template(prod_img, size=900)

    save_resize_image(prod_img, file_path)
    print("complete convert!")
