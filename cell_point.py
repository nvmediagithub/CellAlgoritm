# cell_point.py
from typing import Tuple


class CellPoint:
    """
    Класс, представляющий точку в чанке с целочисленными координатами.

    Атрибуты:
        x (int): x-координата.
        y (int): y-координата.
        has_emitted (bool): флаг, показывающий, испустила ли точка лучи.
    """

    def __init__(self, x: int, y: int) -> None:
        self.x: int = int(x)
        self.y: int = int(y)
        self.has_emitted: bool = False

    @property
    def position(self) -> Tuple[int, int]:
        """
        Возвращает координаты точки в виде кортежа (x, y).
        """
        return self.x, self.y

    def distance_to(self, other: "CellPoint") -> float:
        """
        Вычисляет евклидово расстояние до другой точки.
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5

    def __repr__(self) -> str:
        return f"CellPoint({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CellPoint):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))
