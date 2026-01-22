class Product:
    def __init__(self, name: str, price: float, discount: int = 0) -> None:
        self.name = name
        self.__price = price
        self.__discount = discount

    @property
    def price(self) -> float:
        return self.__price - (self.__price * (self.__discount / 100))

    @property
    def base_price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price > 0:
            self.__price = new_price
            print(f"Новая цена {self.name} - {self.__price}")
        else:
            raise ValueError(
                f"Некорректная цена: {new_price}.Цена должна быть больше нуля"
            )

    @property
    def discount(self) -> int:
        return self.__discount

    @discount.setter
    def discount(self, new_discount: int) -> float:
        if 0 <= new_discount < 100:
            self.__discount = new_discount

        else:
            raise ValueError(
                "Скидка не может быть меньше или равна нуля, так же быть больше либо равна стам"
            )

    def __str__(self) -> str:
        return f"Товар: {self.name}, Цена: {self.price} BYN"

    def to_dict(self):
        return {"name": self.name, "price": self.price, "discount": self.discount}
