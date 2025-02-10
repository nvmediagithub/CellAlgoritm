# cell_structure_demo.py
import pygame
import sys
import math
import random

from cell_point import CellPoint
from cell_line import CellLine
from chunk import Chunk
from chunk_manager import ChunkManager


def line_intersection(p1, p2, p3, p4):
    """
    Вычисляет точку пересечения двух отрезков (p1,p2) и (p3,p4), если оно существует.
    p1, p2, p3, p4 – кортежи (x, y)
    Возвращает (x, y) или None.
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
    if abs(denom) < 1e-6:
        return None  # Отрезки параллельны
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    if 0 <= t <= 1 and 0 <= u <= 1:
        inter_x = x1 + t * (x2 - x1)
        inter_y = y1 + t * (y2 - y1)
        return (inter_x, inter_y)
    return None


# Менеджер чанков: создаем сетку чанков
def create_chunk_grid(x0, y0, chunk_width, chunk_height, grid_cols, grid_rows):
    chunks = {}
    for i in range(grid_cols):
        for j in range(grid_rows):
            # Определяем координаты каждого чанка
            x = x0 + i * chunk_width
            y = y0 + j * chunk_height
            # Загружаем центральный чанк, остальные не загружаем
            loaded = (i == grid_cols // 2 and j == grid_rows // 2)
            chunks[(i, j)] = Chunk(x, y, chunk_width, chunk_height, loaded=loaded, grid_pos=(i, j))
    return chunks


# Поиск чанка по координате точки
def get_chunk_for_point(point, chunks):
    for chunk in chunks.values():
        if chunk.contains(point):
            return chunk
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


# --- Основной алгоритм расширения структуры ---

def expand_structure(chunk_manager: ChunkManager, connection_threshold=300):
    """
    Обрабатываем все загруженные чанки. Для каждой точки, которая еще не испустила лучи, генерируем child-лучи.
    Если новая точка выходит за границы текущего чанка, пытаемся добавить её в соответствующий соседний чанк,
    если тот загружен.
    """
    for chunk in chunk_manager.get_loaded_chunks():
        if not chunk.loaded:
            continue
        new_points = []
        for pt in chunk.points:
            if pt.has_emitted:
                continue
            # Если точка вне чанка, пропускаем
            if not chunk.contains(pt):
                continue
            # Если родительская точка имеет определенное направление, используем его, иначе используем случайное направление
            base_direction = pt.parent_direction if pt.parent_direction is not None else random.uniform(0, 2 * math.pi)
            rays = generate_child_rays(pt, base_direction, child_count=2, min_length=20, max_length=30,
                                       max_deviation=math.radians(30))
            pt.has_emitted = True
            for (vec, new_angle) in rays:
                has_emitted = False
                candidate = (pt.position[0] + vec[0], pt.position[1] + vec[1], 0)
                candidate_2d = (candidate[0], candidate[1])
                origin_2d = (pt.position[0], pt.position[1])
                # Проверяем пересечение с каждой уже существующей линией
                for line in chunk.lines:
                    # Берем координаты существующей линии
                    p1 = (line.start.position[0], line.start.position[1])
                    p2 = (line.end.position[0], line.end.position[1])
                    inter = line_intersection(origin_2d, candidate_2d, p1, p2)
                    if inter is not None:
                        candidate = (inter[0], inter[1], 0)
                        has_emitted = True

                new_point = CellPoint(candidate, parent_direction=new_angle)
                new_point.has_emitted = has_emitted
                new_points.append(new_point)
                new_line = CellLine(pt, new_point)
                chunk.add_line(new_line)

        # Добавляем новые точки, но только те, которые внутри текущего чанка
        for np in new_points:
            # Попытка добавить точку в соответствующий чанк
            target_chunk = chunk_manager.get_chunk_for_point(np.position)
            if target_chunk is not None:
                target_chunk.add_point(np)


# --- Визуализация через Pygame ---

def visualize_chunks(chunk_manager: ChunkManager):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Cell Structure Demo (Chunk Manager)")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # По клику мышью загружаем чанк, в который попадает точка
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                target = chunk_manager.get_chunk_for_point((mouse_pos[0], mouse_pos[1], 0))
                if target and not target.loaded:
                    chunk_manager.load_chunk(chunk_manager.get_chunk_key_for_point((mouse_pos[0], mouse_pos[1], 0)))
                    print("Loaded chunk at", target.grid_pos)
                # Выполняем несколько итераций расширения
                for _ in range(20):
                    expand_structure(chunk_manager, connection_threshold=300)

        screen.fill((30, 30, 30))
        # Рисуем границы всех чанков
        for chunk in chunk_manager.chunks.values():
            color = (0, 255, 0) if chunk.loaded else (255, 0, 0)
            rect = pygame.Rect(chunk.x, chunk.y, chunk.width, chunk.height)
            pygame.draw.rect(screen, color, rect, 3)
            if chunk.loaded:
                for line in chunk.lines:
                    start = (int(line.start.position[0]), int(line.start.position[1]))
                    end = (int(line.end.position[0]), int(line.end.position[1]))
                    pygame.draw.line(screen, (0, 255, 255), start, end, 2)
                for pt in chunk.points:
                    col = (255, 255, 0) if chunk.contains(pt) else (255, 0, 0)
                    pygame.draw.circle(screen, col, (int(pt.position[0]), int(pt.position[1])), 5)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# --- Основная функция демонстрации ---
def main() -> object:
    # Создаем менеджер чанков. Пусть origin = (250, 150) для всей сетки, размер чанка 300x300, сетка 3x3
    grid_cols = 3
    grid_rows = 3
    chunk_width = 150
    chunk_height = 150
    origin = (250, 150)
    from chunk_manager import ChunkManager
    chunk_manager = ChunkManager(origin, chunk_width, chunk_height)

    # Загружаем центральный чанк
    central_key = (grid_cols // 2, grid_rows // 2)
    chunk_manager.load_chunk(central_key)

    # В центральном чанке размещаем стартовую точку в центре
    central_chunk = chunk_manager.chunks[central_key]
    start_point = CellPoint((central_chunk.x + central_chunk.width / 2, central_chunk.y + central_chunk.height / 2, 0))
    central_chunk.add_point(start_point)

    # Генерируем начальные лучи из стартовой точки
    initial_rays = generate_initial_rays(start_point, ray_count=8, min_length=20, max_length=30)
    start_point.has_emitted = True
    for (vec, angle) in initial_rays:
        new_x = start_point.position[0] + vec[0]
        new_y = start_point.position[1] + vec[1]
        new_point = CellPoint((new_x, new_y, 0), parent_direction=angle)
        central_chunk.add_point(new_point)
        line = CellLine(start_point, new_point)
        central_chunk.add_line(line)

    # Выполняем несколько итераций расширения
    for _ in range(20):
        expand_structure(chunk_manager, connection_threshold=300)

    visualize_chunks(chunk_manager)


if __name__ == "__main__":
    main()