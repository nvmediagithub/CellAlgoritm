# chunk.py
from cell_point import CellPoint
from cell_line import CellLine
from cell_polygon import CellPolygon


class Chunk:
    def __init__(self, x, y, width, height, loaded=True, grid_pos=None):
        # Определяем прямоугольную область чанка (x, y) – верхний левый угол
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.loaded = loaded  # Если True – чанк загружен, иначе нет
        self.grid_pos = grid_pos
        self.points = []  # список CellPoint
        self.lines = []   # список CellLine
        self.polygons = []  # список CellPolygon (если потребуется)

    def contains(self, point: CellPoint) -> bool:
        # Проверяем, принадлежит ли точка этому чанку (по 2D)
        x, y = point.position[:2]
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)

    def add_point(self, point: CellPoint):
        self.points.append(point)

    def add_line(self, line: CellLine):
        self.lines.append(line)
