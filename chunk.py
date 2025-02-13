# chunk.py
from typing import Optional, List, Tuple, Set
from cell_point import CellPoint
from cell_line import CellLine


class Chunk:
    """
    Класс, представляющий прямоугольный чанк (область) в 2D пространстве.

    Атрибуты:
        x (int): X-координата верхнего левого угла.
        y (int): Y-координата верхнего левого угла.
        width (int): Ширина чанка.
        height (int): Высота чанка.
        loaded (bool): Флаг, указывающий, загружен ли чанк.
        lines (List[CellLine]): Список линий, находящихся в чанке.
        grid_pos (Optional[Tuple[int, int]]): Позиция чанка в сетке (например, (i, j)).
    """
    def __init__(self, x: int, y: int, width: int, height: int,
                 loaded: bool = True, grid_pos: Optional[Tuple[int, int]] = None) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.loaded: bool = loaded
        self.grid_pos: Optional[Tuple[int, int]] = grid_pos
        self.lines: Set[CellLine] = []

    def contains(self, point: CellPoint) -> bool:
        """
        Проверяет, принадлежит ли заданная точка чанку (используются только координаты x и y).

        Returns:
            bool: True, если точка находится внутри чанка, иначе False.
        """
        x, y = point.position[:2]
        # Здесь включаем левую и верхнюю границы, а правую и нижнюю – исключаем (типичный подход)
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height

    def add_line(self, line: CellLine) -> None:
        """
        Добавляет линию в чанк.
        """
        self.lines.append(line)


    def __repr__(self) -> str:
        return (f"Chunk(x={self.x}, "
                f"y={self.y}, "
                f"width={self.width}, "
                f"height={self.height}, "
                f"loaded={self.loaded}, "
                )
