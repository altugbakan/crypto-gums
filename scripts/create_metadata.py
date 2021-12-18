from brownie import Gum
import os, requests, json

from scripts.create_gum_image import create_image

METADATA_TEMPLATE = {
    "name": "",
    "description": "",
    "image": "",
    "attributes": [],
}

FLAVORS = [
    "Mint",
    "Strawberry",
    "Bubble Gum",
    "Banana",
]
WRAPPERS = [
    "None",
    "Checkers",
    "Dots",
    "Hearts",
    "Stripes",
]

NFT_STORAGE_URL = "https://api.nft.storage/upload"


def parse_properties(flavor, wrapper, color):
    return FLAVORS[flavor], WRAPPERS[wrapper], f"{color:06X}"


def upload_to_nft_storage(file_path):
    file_name = file_path.split("/")[-1]
    headers = {
        "Authorization": f"Bearer {os.getenv('NFT_STORAGE_API_KEY')}",
    }
    with open(file_path, "rb") as f:
        response = requests.post(
            NFT_STORAGE_URL, files={"file": (file_name, f.read())}, headers=headers
        )
        return f"ipfs://{response.json()['value']['cid']}/{file_name}"


def save_index(token_id, json_uri):
    uri_list_file_name = "./metadata/uri_list.json"
    if os.path.exists(uri_list_file_name):
        with open(uri_list_file_name, "r") as f:
            uri_list = json.load(f)
        uri_list[token_id] = json_uri
    else:
        uri_list = {token_id: json_uri}
    with open(uri_list_file_name, "w") as f:
        json.dump(uri_list, f)


def create_metadata(token_id, flavor, wrapper, color):
    metadata_file_name = f"./metadata/{token_id}.json"
    image_file_name = f"./metadata/{token_id}.svg"
    token_metadata = METADATA_TEMPLATE
    token_metadata["name"] = f"Crypto Gum #{token_id}"
    token_metadata["description"] = f"A {flavor} flavored gum."
    create_image(image_file_name, flavor, wrapper, color)
    image_uri = upload_to_nft_storage(image_file_name)
    token_metadata["image"] = image_uri
    token_metadata["attributes"] = [
        {"trait_type": "Flavor", "value": flavor},
        {"trait_type": "Wrapper", "value": wrapper},
        {"trait_type": "Color", "value": f"#{color}"},
    ]
    with open(metadata_file_name, "w") as f:
        json.dump(token_metadata, f)
    json_uri = upload_to_nft_storage(metadata_file_name)
    save_index(token_id, json_uri)
    return json_uri


def get_uri(token_id, flavor, wrapper, color):
    uri_list_file_name = "./metadata/uri_list.json"
    if not os.path.exists(uri_list_file_name):
        return create_metadata(token_id, flavor, wrapper, color)
    with open(uri_list_file_name, "r") as f:
        uri_list = json.load(f)
    if str(token_id) in uri_list.keys():
        return uri_list[str(token_id)]
    else:
        return create_metadata(token_id, flavor, wrapper, color)


def main():
    gum = Gum[-1]
    for token_id in range(gum.tokenCounter()):
        flavor, wrapper, color = parse_properties(gum.tokenIDToProperties(token_id))
        json_uri = get_uri(token_id, flavor, wrapper, color)
        print(f"Metadata URI: {json_uri}")
