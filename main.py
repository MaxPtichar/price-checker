import asyncio

import aiohttp
from tqdm import tqdm

from dataDB import Database
from model import Product
from parsers import OZBY


async def main(parser):

    count_currents_id = 0
    negative_cache = set(db.get_bad_id())
    print(negative_cache)
    current_id = db.get_last_id()
    butch_size = 10
    total_to_parse = 1000

    for _ in range(0, total_to_parse, butch_size):
        url_list = [
            (f"https://oz.by/books/more{x}.html")
            for x in range(current_id, current_id + butch_size)
            if x not in negative_cache
        ]

    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:

        sem = asyncio.Semaphore(5)
        task_list = [parser.get_product(url, session, sem) for url in url_list]

        progress_bar = tqdm(total=len(task_list), desc="Парсинг товаров", unit="стр")
        results = []

        for task in asyncio.as_completed(task_list):
            product = await task
            results.append(product)

            progress_bar.update(1)

            if isinstance(product, Product):
                progress_bar.set_postfix(last_found=product.name[:15])

        progress_bar.close()

        for product in results:
            if isinstance(product, Product):
                db.add_data(product)
            elif isinstance(product, int) and product != 0:
                count_currents_id += 1
                db.add_bad_id(product)

    current_id += butch_size
    db.update_last_id(current_id)
    print(f"Добавлено битых ссылок {count_currents_id}.")
    await asyncio.sleep(1)


if __name__ == "__main__":
    headres = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }

    db = Database("ozby.db")
    db.create_table()
    parser = OZBY(headres)

    try:
        asyncio.run(main(parser))
    except KeyboardInterrupt:
        raise
