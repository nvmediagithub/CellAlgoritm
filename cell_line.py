# cell_line.py

from typing import Any
from cell_point import CellPoint


class CellLine:
    """
    Класс, представляющий линию (ребро) между двумя точками.

    Атрибуты:
        start (CellPoint): начальная точка линии.
        end (CellPoint): конечная точка линии.
        polygon_membership (int): количество полигонов, к которым принадлежит эта линия.
    """
    def __init__(self, start: CellPoint, end: CellPoint) -> None:
        self.start: CellPoint = start
        self.end: CellPoint = end
        self.polygon_membership: int = 0

    def add_polygon_membership(self) -> None:
        """
        Увеличивает счётчик принадлежности линии к полигонам на единицу.
        """
        self.polygon_membership += 1

    def __repr__(self) -> str:
        return f"CellLine({self.start} -> {self.end}, membership={self.polygon_membership})"

    def __eq__(self, other: Any) -> bool:
        """
        Две линии считаются равными, если они соединяют одни и те же точки (независимо от порядка).
        """
        if not isinstance(other, CellLine):
            return NotImplemented
        return ((self.start == other.start and self.end == other.end) or
                (self.start == other.end and self.end == other.start))

    def __hash__(self) -> int:
        """
        Хэш-функция учитывает, что порядок точек не важен.
        """
        return hash(frozenset((self.start, self.end)))