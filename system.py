import json
import os

import aiofiles


class SaveLoad:
    def __init__(self) -> None:
        self.file_path_id_errors = "id_not_exist.json"
        self.negative_id = set()

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

    async def save_negative_cash(self):
        async with aiofiles.open(self.file_path_id_errors, "w", encoding="utf-8") as f:
            id_to_save = list(self.negative_id)
            await f.write(json.dumps(id_to_save, ensure_ascii=False, indent=4))
            print(f"Добавлено {len(id_to_save)} id.")
