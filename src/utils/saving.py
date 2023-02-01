import os
import json


def goto_data_dir():
    current_path = os.getcwd()
    if current_path.endswith("src"):
        parent_folder = os.path.abspath(os.path.join(current_path, os.pardir))
        os.chdir(parent_folder)
    if not os.path.exists('data'):
        os.mkdir('data')


def save_json(obj: list[dict]):
    goto_data_dir()
    json_data = json.dumps({'ads': obj}, ensure_ascii=False).encode("utf-8")
    with open("data/data.json", "wb") as file:
        file.write(json_data)


async def save_image(url: str, item_id: int, index: int, session):
    goto_data_dir()
    async with session.get(url) as response:
        image = await response.read()
        folder = f'data/{item_id}'
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(os.path.join(folder, f'{index}.jpg'), 'wb') as f:
            f.write(image)
