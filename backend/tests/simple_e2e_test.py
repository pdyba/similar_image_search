import os
from glob import glob

import requests
from requests import Response
from tqdm import tqdm

BASE_URL = "http://localhost/v1"
HEALTH_URL = f"{BASE_URL}/health"
UPLOAD_URL = f"{BASE_URL}/upload"
DOWNLOAD_URL = f"{BASE_URL}/download/{{img_id}}"
SIMILAR_URL = f"{BASE_URL}/similar/{{img_id}}"


def get_health() -> dict:
    return requests.get(HEALTH_URL).json()


def upload_file(file_path) -> str:
    with open(file_path, "rb") as file:
        resp = requests.post(UPLOAD_URL, files={"file": file})
        return resp.json()["id"]


def get_img(img_id) -> Response:
    resp = requests.get(DOWNLOAD_URL.format(img_id=img_id))
    return resp


def get_similar_imgs(img_id) -> Response:
    resp = requests.get(SIMILAR_URL.format(img_id=img_id))
    return resp


def upload_data_set() -> None:
    data_dir = "../test_images_set/"
    image_paths = glob(os.path.join(data_dir, "**/*.JPEG"))
    image_paths += glob(os.path.join(data_dir, "**/*.jpeg"))
    image_paths += glob(os.path.join(data_dir, "**/*.png"))
    image_paths += glob(os.path.join(data_dir, "**/*.jpg"))

    for file_path in tqdm(image_paths, desc="Uploading"):
        upload_file(file_path)


def test_all() -> None:
    print(get_health())
    # upload_data_set()
    data_dir = "../test_images/*"
    image_paths = glob(os.path.join(data_dir))
    for file in image_paths:
        print(f"uploadig: {file}")
        img_id = upload_file(file)
        print("file details")
        print(get_img(img_id).json())
        print("similar images")
        print(get_similar_imgs(img_id).json())
