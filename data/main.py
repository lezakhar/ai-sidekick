import configs

from utils import add_points, get_points


if __name__ == "__main__":
    add_points(
        collection_name=configs.QDRANT_COLLECTION_NAME,
        points=get_points(
            path_to_json="data/payloads.json",
        ),
    )
