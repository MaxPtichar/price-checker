import asyncio
import re
from itertools import product
from typing import Union

import aiohttp
from bs4 import BeautifulSoup

from logger_config import logger
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

    def _parse_price(self, soup: BeautifulSoup) -> float:
        price_pattern = re.compile(r"(\d+[,.]\d+)\s*р\.?")
        price_text = soup.find(text=price_pattern)

        if price_text:
            match = price_pattern.search(price_text)
            if match:

                clean_price = match.group(1).replace(",", ".")
                return float(clean_price)
        else:
            return 0.0

    def _url_id_reg(self, url: str) -> int:
        final_id = 0
        find_id = re.findall(r"\d+", url)
        # added find ID

        return int(find_id[0]) if find_id else 0

    async def get_product(
        self, url: str, session: aiohttp.ClientSession, sem: asyncio.Semaphore
    ) -> Union[Product, float, int]:
        try:
            async with sem:
                async with session.get(url) as response:
                    # await asyncio.sleep(2)
                    if response.status == 410:
                        logger.error(f"Error 410: link {url} is not active.")
                        nums = re.findall(r"\d+", url)

                        return int(nums[0]) if nums else 0
                    if response.status != 200:
                        logger.info(f"Status: {response.status} for linr {url}")
                        return 0

                    html_text = await response.text()

                soup = BeautifulSoup(html_text, "lxml")

                title_tag = soup.select_one("h1")

                if title_tag:
                    title = title_tag.text.strip()
                else:
                    title = "Text not found"
                    logger.warning(f"Unable to find the title at {url}.")

                final_id = self._url_id_reg(url)
                final_price = self._parse_price(soup)

            product = Product(name=title, price=final_price, id_on_site=final_id)
            logger.debug(f"Successfully parsed: {product.id_on_site}")

            return product

        except Exception as e:
            logger.error(f"Network error: {e}. {url}")
            return 0
