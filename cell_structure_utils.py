import math
import random
from cell_point import CellPoint


def line_intersection(p1: CellPoint, p2: CellPoint, p3: CellPoint, p4: CellPoint, tol=1e-6):
    """
    Вычисляет точку пересечения двух отрезков (p1, p2) и (p3, p4) с учетом допуска tol.
    p1, p2, p3, p4 – кортежи (x, y).
    Возвращает (x, y), если отрезки пересекаются, иначе None.
    """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y

    if abs(x1 - x4) < 1e-6 and abs(y1 - y4) < 1e-6:
        return None  # Новый отрезок исходит из этой прямой
    if abs(x1 - x3) < 1e-6 and abs(y1 - y3) < 1e-6:
        return None  # Новый отрезок исходит из этой прямой

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < tol:
        return None  # Отрезки параллельны или коллинеарны

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

    if -tol <= t <= 1 + tol and -tol <= u <= 1 + tol:
        inter_x = x1 + t * (x2 - x1)
        inter_y = y1 + t * (y2 - y1)
        return CellPoint(inter_x, inter_y)
    return None


def generate_initial_rays(parent_point: CellPoint, ray_count=2, min_length=30, max_length=50):
    """
    Генерирует ray_count лучей из parent_point, равномерно распределенных по окружности.
    Чтобы сумма лучей была 0, для каждой пары (напр., при четном ray_count) применяем компенсирующее смещение.
    Здесь мы будем генерировать лучи как пары: для каждого луча вычисляем случайное смещение, и противоположный луч
    получает отрицательное смещение.
    Возвращает список лучей: каждый луч – кортеж (dx, dy) и также возвращается базовый угол (в радианах).
    """
    rays = []
    # ray_count должно быть четным
    if ray_count % 2 != 0:
        ray_count += 1
    base_angle_step = (2 * math.pi) / ray_count
    for i in range(ray_count // 2):
        base_angle = i * base_angle_step
        offset = random.uniform(-0.1, 0.1)  # маленькое смещение в радианах (примерно ±6°)
        angle1 = base_angle + offset
        angle2 = base_angle + math.pi - offset  # противоположное направление
        length1 = random.uniform(min_length, max_length)
        length2 = random.uniform(min_length, max_length)
        rays.append(((math.cos(angle1) * length1, math.sin(angle1) * length1), angle1))
        rays.append(((math.cos(angle2) * length2, math.sin(angle2) * length2), angle2))
    return rays


def generate_child_rays(start_point: CellPoint, base_direction: float, child_count: int = 2,
                        min_length: float = 30, max_length: float = 50,
                        max_deviation: float = math.radians(80)) -> list:
    """
    Генерирует child_count лучей из start_point.
    Направление каждого луча основывается на base_direction (в радианах) с отклонением не более max_deviation.

    Возвращает список лучей, где каждый луч представлен как список [start_point, end_point],
    а end_point – объект CellPoint с целочисленными координатами.
    """
    rays = []
    for _ in range(child_count):
        # Вычисляем случайное отклонение
        deviation = random.uniform(-max_deviation, max_deviation)
        new_angle = base_direction + deviation
        # Выбираем случайную длину луча
        length = random.uniform(min_length, max_length)
        dx = math.cos(new_angle) * length
        dy = math.sin(new_angle) * length
        # Вычисляем координаты конечной точки и округляем до целых чисел
        new_x = int(round(start_point.x + dx))
        new_y = int(round(start_point.y + dy))
        end_point = CellPoint(new_x, new_y)
        rays.append(end_point)
    return rays


def calculate_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.atan2(dy, dx)

def distance(p1: CellPoint, p2: CellPoint) -> float:
        """
        Вычисляет евклидово расстояние до другой точки.
        """
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        return (dx * dx + dy * dy) ** 0.5