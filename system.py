import asyncio
import json
import os

import aiofiles


class SaveLoad:
    def __init__(self) -> None:
        self.file_path = "data.json"
        self.file_path_id_errors = "id_not_exist.json"
        self.db_data = {}
        self.negative_id = set()

    def add_to_db(self, product):
        """Принимает объект Product и сохраняет его данные в словарь"""
        if product:
            # Мы используем имя товара как ключ в словаре
            # И вызываем твой метод to_dict() для получения данных
            self.db_data[product.name] = product.to_dict()

    def id_add_to_set(self, id: int):
        self.negative_id.add(id)

    async def load_negative_cash(self):
        if os.path.exists(self.file_path_id_errors):
            async with aiofiles.open(
                self.file_path_id_errors, "r", encoding="utf-8"
            ) as f:
                content = await f.read()
                self.negative_id = set(json.loads(content))
        return self.negative_id

    async def load_db(self):
        if os.path.exists(self.file_path):
            async with aiofiles.open(self.file_path, "r", encoding="utf-8") as f:
                data = await f.read()
                self.db_data = json.loads(data)
            print(f"Загружено из кэша: {len(self.db_data)} товаров")
        return self.db_data

    async def save_negative_cash(self):
        async with aiofiles.open(self.file_path_id_errors, "w", encoding="utf-8") as f:
            id_to_save = list(self.negative_id)
            await f.write(json.dumps(id_to_save, ensure_ascii=False, indent=4))

    async def save_db(self, product_dict=None):
        if product_dict:
            self.db_data.update(product_dict)
        async with aiofiles.open(self.file_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self.db_data, ensure_ascii=False, indent=4))
