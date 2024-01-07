import os
import pytest
import json

from components.file_manager import ScrapTempFile


test_json_text = """{"a": null, "b": true, "c": false}"""
test_json_file = {"a": None, "b": True, "c": False}

test_current_path = __file__.rsplit("/", 1)[0]
test_folder_path = os.path.join(test_current_path, "_temp")
test_file_name = "test"
test_file_path = os.path.join(test_folder_path, test_file_name + ".json")


### Test Functions ###
@pytest.fixture
def scrap_temp_file():
    create_test_folder()
    yield ScrapTempFile(test_folder_path)


def create_test_folder():
    os.makedirs(test_folder_path, exist_ok=True)

    with open(test_file_path, "w") as f:
        f.write("")


def load_test_json_text():
    with open(test_file_path, "r") as f:
        return f.read()


def reset_test_json_text():
    with open(test_file_path, "w") as f:
        f.write(json.dumps(test_json_file))


### start Test ###


def test_ScrapTempFile_is_singleton(scrap_temp_file: ScrapTempFile):
    # Given
    changed_temp_path = test_folder_path.split("/", 1)[0]

    # When
    scrap_temp_file_other = ScrapTempFile(changed_temp_path)

    # Then
    assert scrap_temp_file is scrap_temp_file_other


def test_convert_to_json(scrap_temp_file: ScrapTempFile):
    # When
    json_file = scrap_temp_file._convert_to_json(test_json_text)
    assert json_file == test_json_file


def test_get_file_path(scrap_temp_file: ScrapTempFile):
    # Given
    file_name = "test"

    # When
    file_path = scrap_temp_file._get_file_path(file_name)
    test_file_path = os.path.join(test_folder_path, file_name + ".json")

    # Then
    assert file_path == test_file_path


def test_init_file(scrap_temp_file: ScrapTempFile):
    # When
    scrap_temp_file.init()

    # Then
    json_text = load_test_json_text()
    assert json_text == ""

    reset_test_json_text()


@pytest.mark.asyncio
async def test_append_text_to_file(scrap_temp_file: ScrapTempFile):
    # Given
    scrap_temp_file.init()
    data = {"a": None, "b": True, "c": False}

    # When
    await scrap_temp_file.append_temp_file(test_file_name, data)

    # Then
    json_text = load_test_json_text()

    # append 방식이므로 마지막에 ,가 붙는 특징이 있음
    test_json_text_with_comma = test_json_text + ","

    assert json_text == test_json_text_with_comma


@pytest.mark.asyncio
async def test_load_file(scrap_temp_file: ScrapTempFile):
    # Given
    reset_test_json_text()

    # When
    json_file = await scrap_temp_file.load_temp_file(test_file_name)

    # Then
    assert json_file == test_json_file
