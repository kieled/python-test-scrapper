import aiohttp
import asyncio
from consts import base
from parser.requests import get_pages, main_request_data
from parser import get_tree
from utils import get_url_with_page, save_json


async def main():
    results = []
    async with aiohttp.ClientSession(headers=base.headers) as session:
        async with session.get(base.url) as result_page:
            page_text = await result_page.text()
            html_tree = get_tree(page_text)
        results.append(await main_request_data(session, page=page_text))

        pages = await get_pages(session, html_tree)

        for page_split in pages:
            tasks = [main_request_data(
                session,
                get_url_with_page(page, base.url)
            ) for page in page_split]

            result = await asyncio.gather(*tasks)

            for r in result:
                results.append(r)

        return save_json(results)


asyncio.run(main())
