# cell_point.py
class CellPoint:
    """
    Класс, представляющий точку в чанке.
    Атрибуты:
        position (tuple): координаты точки кортеж (x, y)
        has_emitted (bool): флаг, испустила ли точка лучи
        parent_direction (list): направление (в радианах) от родительской точки, может быть None для стартовой точки
    """
    def __init__(self, position, parent_direction=None):
        self.position = position
        self.parent_direction = parent_direction
        self.has_emitted = False

    def __repr__(self):
        return f"CellPoint({self.position})"
