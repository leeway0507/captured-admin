import os


class FileManager:
    def __init__(self, path: str):
        self.path = path

    def set_default_path(self, path: str):
        self.path = path
        return path

    def init(self):
        """임시 파일 초기화"""
        file_list = os.listdir(self.path)
        for file in file_list:
            file_path = os.path.join(self.path, file)
            with open(file_path, "w") as f:
                f.write("")

    def _get_file_path(self, file_name: str):
        """파일 경로 생성"""
        return os.path.join(self.path, file_name + ".json")

    @classmethod
    def create_folder(cls, path: str):
        """폴더 존재 X인 경우 폴더 생성"""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
