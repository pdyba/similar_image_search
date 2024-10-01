from db import MilvusConnector


if __name__ == "__main__":
    milvus_client = MilvusConnector()
    if resp := milvus_client.create_collection():
        print("Collection Created")
        print(resp)
    else:
        print("Collection already exists")
