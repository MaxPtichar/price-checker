import asyncio
import json
import os
import time
from collections import defaultdict
from sqlite3 import connect

import aiohttp
from requests import session

from model import Product
from parsers import OZBY
from system import SaveLoad


async def main(parser, load, url_list):
    await load.load_db()
    await load.load_negative_cash()
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:

        sem = asyncio.Semaphore(5)
        task_list = [parser.get_product(url, session, sem) for url in url_list]
        results = await asyncio.gather(*task_list)
        print(results)
        for product in results:
            if isinstance(product, Product):
                load.add_to_db(product)
            elif isinstance(product, int) and product != 0:
                load.id_add_to_set(product)

    await load.save_negative_cash()
    await load.save_db()


if __name__ == "__main__":
    headres = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    parser = OZBY(headres)
    load = SaveLoad()
    a = 60  # 101436802
    b = a + 5
    url_list = [f"https://oz.by/books/more{x}.html" for x in range(a, b)]

    try:
        asyncio.run(main(parser, load, url_list))
    except KeyboardInterrupt:
        raise
