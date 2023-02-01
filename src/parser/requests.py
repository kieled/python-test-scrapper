import asyncio
import math
from consts import base
import parser
from utils import save_image


async def get_addition_data(session, item_id: str):
    async with session.post(f'{base.product_detail_url}/{item_id}/0') as result:
        html_tree = parser.get_tree(await result.text())

    description_title = parser.get_description_title(html_tree)
    description = parser.get_description(html_tree)

    return {
        "params": parser.get_params(html_tree),
        "description": f'{description_title}\n{description}'
    }


async def main_request_data(
        session,
        url: str | None = None,
        page: str | None = None
):
    if url:
        async with session.get(url) as result:
            html_tree = parser.get_tree(await result.text())
    else:
        html_tree = parser.get_tree(page)

    href = parser.get_href(html_tree)

    item_id = href.split('/')[-2]

    addition_data = await get_addition_data(session, item_id)

    dict_columns = addition_data['params']

    images = parser.get_images(html_tree)
    tasks = [save_image(url, item_id, i + 1, session) for i, url in enumerate(images)]
    await asyncio.gather(*tasks)

    return {
        "id": int(item_id),
        "title": parser.get_title(html_tree),
        "price": parser.get_price(html_tree),
        "mileage": parser.get_mileage(html_tree),
        "href": href,
        "power": parser.get_power(dict_columns),
        "color": parser.get_color(dict_columns),
        "description": addition_data['description']
    }


async def get_pages(session, tree):
    params = parser.get_count_vehicles_params(tree)

    async with session.get(base.counter_url, params=params) as result:
        result = (await result.json())['results']
    result = int(result)
    count_pages = math.ceil(int(result) / 20) + 1

    pages = [i for i in range(2, count_pages)]
    # Дробим список страниц на кусочки, чтобы запускать только ограниченное кол-во параллельных запросов
    return [pages[x:x + base.concurrency_count] for x in range(0, len(pages), base.concurrency_count)]
