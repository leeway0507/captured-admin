from components.image_resizer import ImageResizer
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="bg-remove")
    parser.add_argument("--file_path", default=None, help="file_path")

    args = parser.parse_args()

    file_path: str = args.file_path
    if not file_path:
        raise ValueError("file_path not exist")

    file_dir, file_name = file_path.rsplit("/", 1)

    resizer = ImageResizer(file_dir)

    img = resizer.preprocess_bg_remove_image(file_path)

    if file_name.split(".")[0] == "main":
        img = resizer.set_template(img, size=700)
    else:
        img = resizer.set_template(img, size=900)

    resizer.work_dir = file_dir
    resizer.save_bg_remove_image(img, file_name.split(".")[0])
    print("complete convert", file_name)
