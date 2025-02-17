# demo_visualization.py
import pygame
import sys
import math
import random

from cell_point import CellPoint
from cell_line import CellLine
from cell_structure_utils import line_intersection, generate_initial_rays, generate_child_rays, calculate_angle
from chunk import Chunk
from chunk_manager import ChunkManager


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
                target = chunk_manager.get_chunk_for_point(CellPoint(mouse_pos[0], mouse_pos[1]))
                if target and not target.need_expand:
                    chunk_manager.load_chunk(chunk_manager.get_chunk_key_for_point(CellPoint(mouse_pos[0], mouse_pos[1])))
                    print("Loaded chunk at", target.grid_pos)
                # Выполняем несколько итераций расширения
                for _ in range(20):
                    chunk_manager.expand_structure(connection_threshold=300)

        screen.fill((30, 30, 30))
        # Рисуем границы всех чанков
        for chunk in chunk_manager.chunks.values():
            color = (0, 255, 0) if chunk.need_expand else (255, 0, 0)
            rect = pygame.Rect(chunk.x, chunk.y, chunk.width, chunk.height)
            pygame.draw.rect(screen, color, rect, 3)
            if chunk.need_expand:
                for line in chunk.lines:
                    start = (int(line.start.position[0]), int(line.start.position[1]))
                    end = (int(line.end.position[0]), int(line.end.position[1]))
                    pygame.draw.line(screen, (0, 255, 255), start, end, 2)
                for line in chunk.lines:
                    pt = line.start
                    pt2 = line.end
                    col = (255, 255, 0) if chunk.contains(pt) else (255, 0, 0)
                    pygame.draw.circle(screen, col, (int(pt.position[0]), int(pt.position[1])), 5)
                    pygame.draw.circle(screen, col, (int(pt2.position[0]), int(pt2.position[1])), 5)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# --- Основная функция демонстрации ---
def main():
    # Создаем менеджер чанков. Пусть origin = (250, 150) для всей сетки, размер чанка 300x300, сетка 3x3
    grid_cols = 3
    grid_rows = 3
    chunk_width = 250
    chunk_height = 250
    origin = (250, 150)
    from chunk_manager import ChunkManager
    chunk_manager = ChunkManager(origin, chunk_width, chunk_height)

    # Загружаем центральный чанк
    central_key = (grid_cols // 2, grid_rows // 2)
    chunk_manager.load_chunk(central_key)

    # В центральном чанке размещаем стартовую точку в центре
    central_chunk = chunk_manager.chunks[central_key]
    start_point = CellPoint(int(central_chunk.x + central_chunk.width / 2), int(central_chunk.y + central_chunk.height / 2))

    # Генерируем начальные лучи из стартовой точки
    initial_rays = generate_initial_rays(start_point, ray_count=3, min_length=50, max_length=80)
    start_point.has_emitted = True
    for (vec, angle) in initial_rays:
        new_x = start_point.position[0] + vec[0]
        new_y = start_point.position[1] + vec[1]
        new_point = CellPoint(new_x, new_y)
        line = CellLine(start_point, new_point)
        central_chunk.add_line(line)

    # Выполняем несколько итераций расширения
    for _ in range(20):
        chunk_manager.expand_structure(connection_threshold=300)

    visualize_chunks(chunk_manager)


if __name__ == "__main__":
    main()
