import boto3
import os
from pathlib import Path
from PIL import Image


bucket_name = "captured-leeway"
s3 = boto3.client("s3")


def check_s3_access():
    return s3.list_buckets()


def folder_is_exist(folder_name: str = ""):
    file_list = load_s3_file_list(folder_name)

    return len(file_list) > 0


def load_s3_object(folder_name: str):
    return s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)


def load_s3_file_list(folder_name: str = ""):
    # Initialize S3 client

    # List objects in the folder
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

    # Extract the file names
    file_names = [obj["Key"] for obj in objects.get("Contents", [])]

    return file_names


def rename_s3_folder(old_folder_name: str, new_folder_name: str):
    if not old_folder_name.endswith("/"):
        old_folder_name += "/"

    if not new_folder_name.endswith("/"):
        new_folder_name += "/"

    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=old_folder_name)

    # Rename each object by copying to the new folder
    for obj in objects.get("Contents", []):
        old_key = obj["Key"]
        new_key = new_folder_name + old_key[len(old_folder_name) :]

        # Copy object to new location
        s3.copy_object(
            Bucket=bucket_name,
            CopySource={"Bucket": bucket_name, "Key": old_key},
            Key=new_key,
        )

        # Delete old object
        s3.delete_object(Bucket=bucket_name, Key=old_key)
    return {"s3_folder_list": load_s3_file_list(new_folder_name)}


def upload_product_image_to_s3(sku: int):
    local_folder = f"/Users/yangwoolee/repo/captured/keynote/image/product/{sku}"
    s3_folder = f"product/{sku}"
    return upload_folder_to_s3(local_folder, s3_folder)


def upload_folder_to_s3(
    local_folder: str,
    s3_folder: str,
    image_opt: bool = True,
    thumbnail_opt: bool = True,
):
    if not image_opt and thumbnail_opt:
        Warning("create_thumbnail은 image_opt가 True일 때만 작동합니다.")

    if os.path.exists(local_folder) == False:
        return {"status": "file_not_found", "error": "local folder not found"}

    try:
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)
                s3_path = os.path.join(s3_folder, file)

                if file == ".DS_Store":
                    continue

                if image_opt and file.endswith(
                    (".jpg", ".jpeg", ".png", ".avif", ".webp")
                ):
                    if thumbnail_opt and file == "thumbnail.png":
                        create_thumbnail(root, file)
                    else:
                        optimize_image(root, file)
                        local_path = os.path.join(root, "resize", file)

                s3.upload_file(local_path, bucket_name, s3_path)
        return {"status": "success", "upload_result": load_s3_file_list(s3_folder)}

    except Exception as e:
        return {"status": "error", "error": e}


def optimize_image(root_dir: str, file_name: str):
    img = Image.open(root_dir + "/" + file_name)
    aspect_ratio = img.width / img.height

    resize_folder = os.path.join(root_dir, "resize")
    Path(resize_folder).mkdir(parents=True, exist_ok=True)

    resize_path = os.path.join(resize_folder, file_name)

    if img.width < 1000:
        img.save(resize_path, quality=80, optimize=True)

    target_width = 1000
    target_height = round(target_width / aspect_ratio)
    resized_img = img.resize((target_width, target_height))
    resized_img.save(resize_path, quality=80, optimize=True)

    return True


def remove_white_background(input_path: str):
    # Open the image
    image = Image.open(input_path)

    # Convert the image to RGBA if it's not already
    image = image.convert("RGBA")

    # Get the image data as a list of tuples
    data = list(image.getdata())

    # Create a new list to store the updated image data
    new_data = []

    # Define the white color
    white = (255, 255, 255, 0)  # RGBA format, with 0 alpha (fully transparent)

    # Loop through the original data and replace white pixels with transparent ones
    for item in data:
        if item[:3] == (255, 255, 255):
            new_data.append(white)
        else:
            new_data.append(item)

    # Update the image data
    image.putdata(new_data)

    # Save the new image with a transparent background
    dirname = os.path.dirname(input_path)
    output_path = os.path.join(dirname, "thumbnail.png")
    image.save(output_path, format="PNG")


def create_thumbnail(root_dir: str, file_name: str):
    resize_folder = os.path.join(root_dir, "resize")
    Path(resize_folder).mkdir(parents=True, exist_ok=True)

    file_dir = os.path.join(root_dir, file_name)
    cropped_img = crop_image(file_dir)

    # Create a new image with a transparent square of size 1000x1000
    new_size = (1000, 1000)
    centered_image = Image.new("RGBA", new_size, (0, 0, 0, 0))

    # Calculate the position to paste the cropped image in the center
    paste_position = (
        (new_size[0] - cropped_img.width) // 2,
        (new_size[1] - cropped_img.height) // 2,
    )

    # Paste the cropped image onto the new image
    centered_image.paste(cropped_img, paste_position)

    output_path = os.path.join(resize_folder, "thumbnail.png")
    return centered_image.save(output_path, quality=80, optimize=True)


def crop_image(input_path: str, target_width: int = 700):
    image = Image.open(input_path)
    bbox = image.getbbox()
    cropped_image = image.crop(bbox)

    aspect_ratio = cropped_image.width / cropped_image.height
    target_height = round(target_width / aspect_ratio)

    return cropped_image.resize((target_width, target_height))
