import os
import json

import pytest

from components.file_manager import FileManager


test_json_text = """{"a": null, "b": true, "c": false}"""
test_json_file = {"a": None, "b": True, "c": False}

test_current_path = __file__.rsplit("/", 1)[0]
test_folder_path = os.path.join(test_current_path, "test_folder")
test_file_name = "test"
test_file_path = os.path.join(test_folder_path, test_file_name + ".json")


### Test Functions ###
@pytest.fixture
def file_manager():
    yield FileManager(test_folder_path)


def load_test_json_text():
    with open(test_file_path, "r") as f:
        return f.read()


def create_test_json_text():
    with open(test_file_path, "w") as f:
        f.write(json.dumps(test_json_file))


### start Test ###


def test_create_folder(file_manager: FileManager):
    # When
    file_manager.create_folder(test_folder_path)

    # Then
    assert os.path.exists(test_folder_path)


def test_change_path(file_manager: FileManager):
    # Given

    changed_temp_path = test_folder_path.split("/", 1)[0]

    # When
    file_manager.path = changed_temp_path

    # Then
    assert file_manager.path == changed_temp_path


def test_get_file_path(file_manager: FileManager):
    # Given
    file_name = "test"

    # When
    file_path = file_manager._get_file_path(file_name)

    # Then
    test_file_path = os.path.join(test_folder_path, file_name + ".json")
    assert file_path == test_file_path


def test_init_file(file_manager: FileManager):
    # Given
    create_test_json_text()

    # When
    file_manager.init()

    # Then
    json_text = load_test_json_text()
    assert json_text == ""
