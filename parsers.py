import asyncio
import re
from typing import Union
from unittest import result

import aiohttp
from bs4 import BeautifulSoup

from logger_config import logger
from model import Product


class BaseParser:
    def __init__(self, headers) -> None:
        self.headers = headers

    def get_product(self, url: str) -> None:

        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")


class FetchUrl:
    def __init__(self, session: aiohttp.ClientSession, sem: asyncio.Semaphore) -> None:
        self.session = session
        self.sem = sem

    async def fetch_html(self, url: str, retries: int = 3) -> str:
        for attempt in range(retries):
            try:
                async with self.sem:
                    async with self.session.get(url) as response:
                        # await asyncio.sleep(2)
                        if response.status == 410:
                            logger.error(f"Error 410: link {url} is inactive")
                            nums = re.findall(r"\d+", url)
                            return int(nums[0]) if nums else 0

                        elif response.status == 200:
                            return await response.text()

                        elif response.status == 503:
                            wait_time = (attempt + 1) * 2
                            logger.warning(
                                f"503 Error. Retrying in {wait_time}s... {url}"
                            )
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            logger.info(f"Status: {response.status} for link {url}")
                            return 0

            except Exception as e:
                logger.error(f"Network error: {e}. {url}")
                return 0
        return 0


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

    def _extract_id(self, url: str) -> int:

        find_id = re.findall(r"\d+", url)
        # added find ID

        return int(find_id[0]) if find_id else 0

    async def get_product(
        self, url: str, fetcher: FetchUrl
    ) -> Union[Product, float, int]:
        result = await fetcher.fetch_html(url, 3)

        if isinstance(result, int):
            return result

        return self.parse(url, result)

    def parse(self, url: str, html_text: str) -> Union[Product, float, int]:

        soup = BeautifulSoup(html_text, "lxml")

        title_tag = soup.select_one("h1")

        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "Title not found"
            logger.warning(f"Unable to find the title at {url}.")

        final_id = self._extract_id(url)
        final_price = self._parse_price(soup)

        product = Product(name=title, price=final_price, id_on_site=final_id)
        logger.debug(f"Successfully parsed: {product.id_on_site}")

        return product
