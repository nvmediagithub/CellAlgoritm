# chunk_manager.py
import math
from typing import Tuple, Dict, Any, List

from CellAlgoritm.cell_line import CellLine
from CellAlgoritm.cell_point import CellPoint
from CellAlgoritm.cell_structure_utils import line_intersection, calculate_angle, generate_child_rays, distance
from chunk import Chunk


class ChunkManager:
    """
    Класс для управления сеткой чанков.

    Атрибуты:
        origin (Tuple[int, int]): координаты верхнего левого угла всей сетки чанков.
        chunk_width (int): ширина каждого чанка.
        chunk_height (int): высота каждого чанка.
        chunks (Dict[Tuple[int, int], Chunk]): словарь, где ключ – пара (i, j), а значение – объект Chunk.
    """

    def __init__(self, origin: Tuple[int, int], chunk_width: int, chunk_height: int) -> None:
        self.origin: Tuple[int, int] = origin
        self.chunk_width: int = chunk_width
        self.chunk_height: int = chunk_height
        self.chunks: Dict[Tuple[int, int], Chunk] = {}  # ключ: (i, j), значение: объект Chunk

    def get_chunk_key_for_point(self, point: CellPoint) -> Tuple[int, int]:
        """
        Определяет ключ чанка по координате точки.

        Аргументы:
            point: кортеж (x, y) или (x, y, z); используются только x и y.

        Returns:
            Tuple[int, int]: ключ, определяющий положение чанка в сетке.
        """
        x = point.x
        y = point.y
        i = int((x - self.origin[0]) // self.chunk_width)
        j = int((y - self.origin[1]) // self.chunk_height)
        return i, j

    def get_neighbor_keys(self, key: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Возвращает список ключей для 8-соседей данного чанка.

        Аргументы:
            key: ключ чанка (i, j).

        Returns:
            List[Tuple[int, int]]: список соседних ключей.
        """
        i, j = key
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                neighbors.append((i + di, j + dj))
        return neighbors

    def load_chunk(self, key: Tuple[int, int]) -> None:
        """
        Загружает чанк по заданному ключу. Если чанк не существует, создает его и помечает как загруженный.
        Также создает соседние чанки (как незагруженные), если они отсутствуют.

        Аргументы:
            key: ключ чанка (i, j).
        """
        if key not in self.chunks:
            x = self.origin[0] + key[0] * self.chunk_width
            y = self.origin[1] + key[1] * self.chunk_height
            self.chunks[key] = Chunk(x, y, self.chunk_width, self.chunk_height, loaded=True, grid_pos=key)
        else:
            self.chunks[key].loaded = True

        # Создаем соседние чанки как незагруженные, если их еще нет
        for nkey in self.get_neighbor_keys(key):
            if nkey not in self.chunks:
                x = self.origin[0] + nkey[0] * self.chunk_width
                y = self.origin[1] + nkey[1] * self.chunk_height
                self.chunks[nkey] = Chunk(x, y, self.chunk_width, self.chunk_height, loaded=False, grid_pos=nkey)

    def get_chunk_for_point(self, point: CellPoint) -> Any:
        """
        Возвращает чанк, в который попадает данная точка.

        Аргументы:
            point: кортеж (x, y, ...) – используется только x и y.

        Returns:
            Chunk или None: чанк, если найден, иначе None.
        """
        key = self.get_chunk_key_for_point(point)
        return self.chunks.get(key, None)

    def update_loaded_chunks(self) -> None:
        """
        Для каждого загруженного чанка загружает соседние чанки.
        """
        loaded_keys = [key for key, c in self.chunks.items() if c.loaded]
        for key in loaded_keys:
            self.load_chunk(key)

    def get_loaded_chunks(self) -> List[Chunk]:
        """
        Возвращает список всех загруженных чанков.

        Returns:
            List[Chunk]: список загруженных чанков.
        """
        return [c for c in self.chunks.values() if c.loaded]

    def expand_structure(self, connection_threshold=300):
        for chunk in self.chunks.values():
            if not chunk.loaded:
                continue
            new_lines = []
            for chunk_line in chunk.lines:
                p_start = chunk_line.start
                p_end = chunk_line.end
                if p_end.has_emitted:
                    continue
                p_end.has_emitted = True
                base_direction = calculate_angle(p_start.x, p_start.y, p_end.x, p_end.y)
                target_points = generate_child_rays(p_end, base_direction, child_count=3, min_length=40, max_length=60,
                                           max_deviation=math.radians(90))
                for i in range(len(target_points)):
                    for line in chunk.lines:
                        inter = line_intersection(p_end, target_points[i], line.start, line.end)
                        if inter is not None:
                            target_points[i] = line.start if distance(inter, line.start) < \
                                                  distance(inter, line.end) else line.end
                            # target_points[i].has_emitted = True

                    neighbor_keys = self.get_neighbor_keys(chunk.grid_pos)
                    for neighbor_key in neighbor_keys:
                        if neighbor_key in self.chunks:
                            neighbor_chunk = self.chunks[neighbor_key]
                            for line in neighbor_chunk.lines:
                                inter = line_intersection(p_end, target_points[i], line.start, line.end)
                                if inter is not None:
                                    target_points[i] = line.start if distance(inter, line.start) < \
                                                          distance(inter, line.end) else line.end
                                    # target_points[i].has_emitted = True

                    for line in new_lines:
                        inter = line_intersection(p_end, target_points[i], line.start, line.end)
                        if inter is not None:
                            target_points[i] = line.start if distance(inter, line.start) < \
                                                  distance(inter, line.end) else line.end
                            # target_points[i].has_emitted = True

                    new_line = CellLine(p_end, target_points[i])
                    new_lines.append(new_line)

            for line in new_lines:
                target_chunk = self.get_chunk_for_point(line.start)
                if target_chunk is not None:
                    target_chunk.add_line(line)


    def __repr__(self) -> str:
        return f"ChunkManager(origin={self.origin}, chunk_size=({self.chunk_width}x{self.chunk_height}), total_chunks={len(self.chunks)})"