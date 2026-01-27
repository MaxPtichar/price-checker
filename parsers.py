import asyncio
import re
from gettext import find
from typing import Union

import aiohttp
from bs4 import BeautifulSoup

from model import Product


class BaseParser:
    def __init__(self, headers) -> None:
        self.headers = headers

    def get_product(self, url: str) -> None:

        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")


class OZBY(BaseParser):
    def __init__(self, headers) -> None:

        super().__init__(headers)

    def __str__(self) -> str:
        return super().__str__()

    async def get_product(
        self, url: str, session: aiohttp.ClientSession, sem: asyncio.Semaphore
    ) -> Union[Product, int]:
        async with sem:
            async with session.get(url) as response:
                await asyncio.sleep(2)
                if response.status == 410:
                    print(f"Ошибка 410: Ссылка {url} больше не активна.")
                    nums = re.findall(r"\d+", url)

                    return int(nums[0]) if nums else 0
                if response.status != 200:
                    print(f"{response.status} ")
                    return 0

                html_text = await response.text()

            soup = BeautifulSoup(html_text, "lxml")
            price_pattern = re.compile(r"(\d+[,.]\d+)\s*р\.?")

            title_tag = soup.select_one("h1")
            title = title_tag.text.strip() if title_tag else "Текст не найден"

            final_price = 0.0
            price_text = soup.find(text=price_pattern)

            final_id = 0
            find_id = re.findall(r"\d+", url)
            # added find ID

            final_id = int(find_id[0]) if find_id else 0

            if price_text:
                match = price_pattern.search(price_text)
                if match:

                    clean_price = match.group(1).replace(",", ".")
                    final_price = float(clean_price)

        return Product(name=title, price=final_price, id_on_site=final_id)
