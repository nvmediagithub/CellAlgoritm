# cell_polygon.py
class CellPolygon:
    """
    Класс для представления полигона (ячейки).
    Атрибуты:
        points (list): список точек (CellPoint или их координат) в упорядоченном обходе, задающих контур полигона.
    """
    def __init__(self, points):
        self.points = points.copy()

    def __repr__(self):
        return f"CellPolygon({self.points})"
