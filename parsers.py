import asyncio
import re
from typing import Union

import aiohttp
import lxml
from bs4 import BeautifulSoup

from model import Product
from system import SaveLoad


class BaseParser:
    def __init__(self, headers) -> None:
        self.headers = headers

    def get_product(self, url: str) -> None:

        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")


class OZBY(BaseParser):
    def __init__(self, headers) -> None:
        self.id_add = SaveLoad()
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

                soup = BeautifulSoup(await response.text(), "lxml")
                price_pattern = re.compile(r"(\d+[,.]\d+)\s*р\.?")

                title_tag = soup.select_one("h1")
                title = title_tag.text.strip() if title_tag else "Текст не найден"

                final_price = 0.0
                price_text = soup.find(text=price_pattern)

                if price_text:
                    match = price_pattern.search(price_text)
                    if match:

                        clean_price = match.group(1).replace(",", ".")
                        final_price = float(clean_price)

        return Product(name=title, price=final_price)
