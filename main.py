import asyncio

import aiohttp
from tqdm import tqdm

from dataDB import Database
from logger_config import logger
from model import Product
from parsers import OZBY, FetchUrl


async def main(parser):

    count_currents_id = 0
    negative_cache = set(db.get_bad_id())
    current_id = db.get_last_id()
    butch_size = 10
    total_to_parse = 10
    progress_bar = tqdm(total=total_to_parse, desc="Parsing", unit=" items ")

    connector = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        sem = asyncio.Semaphore(50)
        ft = FetchUrl(session, sem)

        for _ in range(0, total_to_parse, butch_size):
            url_list = [
                (f"https://oz.by/books/more{x}.html")
                for x in range(current_id, current_id + butch_size)
                if x not in negative_cache
            ]

            skipped = butch_size - len(url_list)
            if skipped > 0:
                progress_bar.update(skipped)

            if not url_list:
                current_id += butch_size
                db.update_last_id(current_id)

                continue

            task_list = [parser.get_product(url, ft) for url in url_list]

            results = []

            for task in asyncio.as_completed(task_list):
                product = await task
                results.append(product)

                progress_bar.update(1)

                if isinstance(product, Product):
                    progress_bar.set_postfix(last_found=product.name[:15])

            for product in results:
                if isinstance(product, Product):
                    db.add_data(product)
                elif isinstance(product, int) and product != 0:
                    count_currents_id += 1
                    db.add_bad_id(product)

            current_id += butch_size
            db.update_last_id(current_id)

            await asyncio.sleep(1)

    progress_bar.close()
    logger.info(f"Finished. Added bad ID's during this session: {count_currents_id}.")


if __name__ == "__main__":
    headres = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }

    db = Database("ozby.db")
    db.create_table()
    parser = OZBY(headres)

    try:
        logger.info("Programm is running")
        asyncio.run(main(parser))
        logger.info("Programm is finished")
    except KeyboardInterrupt:
        raise
