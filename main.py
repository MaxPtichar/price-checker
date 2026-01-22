import json
import os
import time
from collections import defaultdict

from model import Product
from parsers import OZBY

if __name__ == "__main__":
    file_path = "data.json"
    file_path_id_errors = "id_not_exist.json"
    if os.path.exists(file_path_id_errors):
        with open(file_path_id_errors, "r", encoding="utf-8") as f_id:
            id_not_exist = set(json.load(f_id))
    else:
        id_not_exist = set()

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Загружено из кэша: {len(data)} товаров")
    else:
        data = {}
    headres = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    parser = OZBY(headres)
    a = 101436805
    b = a + 10
    for i in range(a, b):
        if str(i) in data or i in id_not_exist:
            continue
        time.sleep(1.5)
        get_book = parser.get_product(f"https://oz.by/books/more{i}.html")
        if get_book and get_book.price > 0:

            product_dict = get_book.to_dict()
            data[i] = product_dict
            print(f"{data[i]} загружен")
        else:
            id_not_exist.add(i)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Готово! Теперь в базе {len(data)} товаров.")

    with open(file_path_id_errors, "w", encoding="utf-8") as f_id:
        json.dump(list(id_not_exist), f_id, ensure_ascii=False, indent=4)
    print(data)
