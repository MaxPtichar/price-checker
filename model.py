from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    id_on_site: int
