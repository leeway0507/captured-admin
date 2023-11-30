from fastapi import APIRouter, Depends, HTTPException, status
from .utils import *

s3_router = APIRouter()


@s3_router.get("/s3_list")
def s3_list(folder_name: str = ""):
    return load_s3_file_list(folder_name)


@s3_router.get("/s3_rename")
def s3_rename(old_folder_dir: str, new_folder_dir: str):
    return rename_s3_folder(old_folder_dir, new_folder_dir)


@s3_router.get("/s3_check")
def s3_check():
    return check_s3_access()


@s3_router.get("/upload-product-image-to-s3")
def upload_product_image(sku: int):
    req = upload_product_image_to_s3(sku)
    if req["status"] == "success":
        return req
    if req["status"] == "file_not_found":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=req)
    if req["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=req
        )


@s3_router.get("/load-objects-from-s3")
def load_objects_from_s3(folder_name: str):
    return load_s3_object(folder_name)


@s3_router.get("/create-thumbnail")
def crop_white_bg(root_dir: str, file_name: str):
    return create_thumbnail(root_dir, file_name)
