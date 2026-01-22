import re

import lxml
import requests
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

    def get_product(self, url: str) -> Product:
        response = requests.get(url, headers=self.headers)
        if response.status_code == 410:
            print(f"Ошибка 410: Ссылка {url} больше не активна.")
            return Product("Удалено", 0.0)
        if response.status_code != 200:
            raise requests.HTTPError(
                f"Запрос отклонен со статусом {response.status_code}"
            )

        soup = BeautifulSoup(response.text, "lxml")
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


headres = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}
parser = OZBY(headres)
product = parser.get_product("https://oz.by/books/more101453162.html")
print(product)
