import math
import random
from cell_point import CellPoint


# def line_intersection(p1, p2, p3, p4):
#     """
#     Вычисляет точку пересечения двух отрезков (p1,p2) и (p3,p4), если оно существует.
#     p1, p2, p3, p4 – кортежи (x, y)
#     Возвращает (x, y) или None.
#     """
#     x1, y1 = p1
#     x2, y2 = p2
#     x3, y3 = p3
#     x4, y4 = p4
#
#     if abs(x1-x4) < 1e-6 and abs(y1-y4) < 1e-6:
#         return None  # Новый отрезок исходит из этой прямой
#     if abs(x1-x3) < 1e-6 and abs(y1-y3) < 1e-6:
#         return None  # Новый отрезок исходит из этой прямой
#
#     denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
#     if abs(denom) < 1e-6:
#         return None  # Отрезки параллельны
#     t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
#     u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
#     if 0 <= t <= 1 and 0 <= u <= 1:
#         inter_x = x1 + t * (x2 - x1)
#         inter_y = y1 + t * (y2 - y1)
#         return (inter_x, inter_y)
#     return None

def line_intersection(p1, p2, p3, p4, tol=1e-6):
    """
    Вычисляет точку пересечения двух отрезков (p1, p2) и (p3, p4) с учетом допуска tol.
    p1, p2, p3, p4 – кортежи (x, y).
    Возвращает (x, y), если отрезки пересекаются, иначе None.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    if abs(x1-x4) < 1e-6 and abs(y1-y4) < 1e-6:
        return None  # Новый отрезок исходит из этой прямой
    if abs(x1-x3) < 1e-6 and abs(y1-y3) < 1e-6:
        return None  # Новый отрезок исходит из этой прямой

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < tol:
        return None  # Отрезки параллельны или коллинеарны

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

    if -tol <= t <= 1 + tol and -tol <= u <= 1 + tol:
        inter_x = x1 + t * (x2 - x1)
        inter_y = y1 + t * (y2 - y1)
        return (inter_x, inter_y)
    return None

def generate_initial_rays(parent_point: CellPoint, ray_count=8, min_length=30, max_length=50):
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


def generate_child_rays(parent_point: CellPoint, base_direction: float, child_count=2, min_length=30, max_length=50,
                        max_deviation=math.radians(80)):
    """
    Генерирует child_count лучей из parent_point.
    Направление каждого луча основывается на base_direction (в радианах) с отклонением не более max_deviation.
    Возвращает список лучей: каждый луч – кортеж ((dx, dy), new_direction)
    """
    rays = []
    base_angle_step = math.pi / child_count
    for i in range(child_count):
        base_angle = i * base_angle_step - max_deviation
        offset = base_angle + random.uniform(-0.1, 0.1)
        new_angle = base_direction + offset
        length = random.uniform(min_length, max_length)
        dx = math.cos(new_angle) * length
        dy = math.sin(new_angle) * length
        rays.append(((dx, dy), new_angle))
    return rays