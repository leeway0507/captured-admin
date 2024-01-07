import boto3
import os
from pathlib import Path
from PIL import Image
import pillow_avif  # don't delete this line
from dotenv import dotenv_values
import shutil
import time


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

bucket_name = "captured-prod"
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
    s3_folder = f"cdn-images/product/{sku}"
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

    if os.path.exists(os.path.join(local_folder, "resize")):
        shutil.rmtree(os.path.join(local_folder, "resize"))

    try:
        for root, dirs, files in os.walk(local_folder):
            print(f"{root} 폴더에 {len(dirs)}개 폴더, {len(files)}개 파일이 있습니다.")
            print(f"총 {len(files)}건 업로드 예정")
            for file in files:
                local_path = os.path.join(root, file)
                s3_path = os.path.join(s3_folder, file)

                if file == ".DS_Store":
                    continue

                if image_opt and file.endswith(img_type):
                    if thumbnail_opt and file.find("thumbnail") > -1:
                        resize_folder, file_name = create_thumbnail(root, file)
                    else:
                        resize_folder, file_name = optimize_image(root, file)

                    local_path = os.path.join(resize_folder, file_name)
                    s3_path = os.path.join(s3_folder, file_name)

                s3.upload_file(local_path, bucket_name, s3_path)
        return {"status": "success", "upload_result": load_s3_file_list(s3_folder)}

    except Exception as e:
        print(e)
        return {"status": "error"}


def optimize_image(root_dir: str, file_name: str):
    img = Image.open(root_dir + "/" + file_name)
    aspect_ratio = img.width / img.height

    resize_folder = create_folder(root_dir, "resize")

    file_name = file_name.split(".")[0] + ".webp"
    resize_path = os.path.join(resize_folder, file_name)

    img_white_bg = Image.new(
        "RGBA", img.size, "WHITE"
    )  # Create a white rgba background
    img_white_bg.paste(img, (0, 0), img)

    if img.width < 1000:
        img_white_bg.save(resize_path, quality=80, optimize=True, format="WEBP")

    target_width = 1000
    target_height = round(target_width / aspect_ratio)
    img_white_bg = img_white_bg.resize((target_width, target_height))
    img_white_bg.save(resize_path, quality=80, optimize=True, format="WEBP")

    return resize_folder, file_name


def create_thumbnail(root_dir: str, file_name: str):
    resize_folder = create_folder(root_dir, "resize")

    crop_size = 700
    if file_name.find("_") > -1:
        crop_size = file_name.split("_")[-1]
        crop_size = int(crop_size.removesuffix(".png"))

    file_dir = os.path.join(root_dir, file_name)
    cropped_img = crop_image(file_dir, crop_size)
    cropped_img_white_bg = Image.new(
        "RGBA", cropped_img.size, "WHITE"
    )  # Create a white rgba background
    cropped_img_white_bg.paste(cropped_img, (0, 0), cropped_img)

    # Create a new image with a transparent square of size 1000x1000
    new_size = (1000, 1000)
    centered_image = Image.new("RGB", new_size, "white")

    # Calculate the position to paste the cropped image in the center
    paste_position = (
        (new_size[0] - cropped_img.width) // 2,
        (new_size[1] - cropped_img.height) // 2,
    )

    # Paste the cropped image onto the new image
    centered_image.paste(cropped_img_white_bg, paste_position)

    output_path = os.path.join(resize_folder, "thumbnail.webp")
    centered_image.save(output_path, quality=80, optimize=True, format="WEBP")
    return resize_folder, "thumbnail.webp"


def crop_image(input_path: str, target_width: int = 700):
    image = Image.open(input_path)
    bbox = image.getbbox()
    cropped_image = image.crop(bbox)

    aspect_ratio = cropped_image.width / cropped_image.height
    target_height = round(target_width / aspect_ratio)

    return cropped_image.resize((target_width, target_height))


def create_folder(root_dir: str, name: str):
    resize_folder = os.path.join(root_dir, name)
    Path(resize_folder).mkdir(parents=True, exist_ok=True)
    return resize_folder


def update_file(s3_folder_path: str, local_folder_path: str, file_name: str):
    print(f"update {file_name} \nfrom : {local_folder_path} \nto : {s3_folder_path}")

    if not file_name.endswith(img_type):
        raise ValueError("file_name should include extension")

    s3_path = os.path.join(s3_folder_path, file_name)
    local_path = os.path.join(local_folder_path, file_name)

    s3.delete_object(Bucket=bucket_name, Key=s3_path)
    s3.upload_file(local_path, bucket_name, s3_path)
    return {"status": "success"}


def change_image_file(sku: int, img_name: str):
    if not img_name.endswith(img_type):
        raise ValueError("img_name should include extension")

    img_dir = config.get("PRODUCT_IMAGE_DIR")
    assert isinstance(img_dir, str), "img_dir is not string"

    resize_folder, file_name = optimize_image(os.path.join(img_dir, str(sku)), img_name)
    update_file(f"cdn-images/product/{sku}", resize_folder, file_name)
    invalidate_cloudfront_distribution(f"/cdn-images/product/{sku}/{file_name}")

    return {"status": "success"}


def invalidate_cloudfront_distribution(path: str):
    paths = [path]

    cloudfront_client = boto3.client("cloudfront")

    distribution_id = config.get("CLOUDFRONT_DISTRIBUTION_ID")

    # Create an invalidation request
    invalidation_response = cloudfront_client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            "Paths": {"Quantity": len(paths), "Items": paths},
            "CallerReference": f"my-invalidation-{int(time.time())}",
        },
    )

    # Print the invalidation response
    print("Invalidation request Success! ")
