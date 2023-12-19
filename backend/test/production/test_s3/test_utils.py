from components.production.s3.utils import optimize_image
import os


def test_optimize_image():
    """
    GIVEN : 해당 경로에 파일 존재
    WHEN : 파일 경로와 이름을 변수로 입력
    THEN : resize 폴더 생성 및 webp 파일 생성
    """

    # GIVEN
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(curr_dir, "image")
    file_name = "test.webp"

    # WHEN
    resize_folder, file_name = optimize_image(test_dir, file_name)

    # THEN
    file_path = os.path.join(resize_folder, file_name)
    assert os.path.isfile(file_path)
    os.remove(file_path)
    os.rmdir(resize_folder)
