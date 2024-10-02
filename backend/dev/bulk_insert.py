import os
import sys
from glob import glob

from db import MilvusConnector
from tqdm import tqdm
from use_cases import prepare_image


def insert_image_set(data_dir: str) -> None:
    milvus_client = MilvusConnector()
    milvus_client.create_collection()

    # Load images from directory and generate embeddings
    image_paths = glob(os.path.join(data_dir, "**/*.JPEG"))
    image_paths += glob(os.path.join(data_dir, "**/*.jpeg"))
    image_paths += glob(os.path.join(data_dir, "**/*.png"))
    image_paths += glob(os.path.join(data_dir, "**/*.jpg"))
    data = []
    for i, filepath in enumerate(tqdm(image_paths, desc="Generating embeddings ...")):
        try:
            with open(filepath, "rb") as file:
                data.append(prepare_image(file, filepath.rsplit(".", maxsplit=1)[-1]))
        except Exception as e:
            print(
                f"Skipping file: {filepath} due to an error occurs "
                f"during the embedding process:\n{e}"
            )
            continue

    # Insert data into Milvus
    mr = milvus_client.insert(
        data=data,
    )
    print("Total number of inserted entities/images:", mr["insert_count"])


insert_image_set(sys.argv[-1])
