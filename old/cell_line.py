# cell_line.py
class CellLine:
    """
    Класс, представляющий линию (ребро) между двумя точками.
    Атрибуты:
        start (CellPoint): начальная точка линии
        end (CellPoint): конечная точка линии
        polygon_membership (int): количество полигонов, к которым принадлежит эта линия
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.polygon_membership = 0

    def add_polygon_membership(self):
        self.polygon_membership += 1

    def __repr__(self):
        return f"CellLine({self.start} -> {self.end})"
