# chunk_manager.py
from chunk import Chunk

class ChunkManager:
    def __init__(self, origin, chunk_width, chunk_height):
        """
        origin: (x, y) координаты верхнего левого угла всей сетки чанков
        """
        self.origin = origin
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.chunks = {}  # ключ: (i, j), значение: объект Chunk

    def get_chunk_key_for_point(self, point):
        # point: (x, y, z) или (x, y); используем только x и y
        x = point[0]
        y = point[1]
        i = int((x - self.origin[0]) // self.chunk_width)
        j = int((y - self.origin[1]) // self.chunk_height)
        return (i, j)

    def get_neighbor_keys(self, key):
        i, j = key
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                neighbors.append((i + di, j + dj))
        return neighbors

    def load_chunk(self, key):
        # Если чанк не существует, создаем его как загруженный
        if key not in self.chunks:
            x = self.origin[0] + key[0] * self.chunk_width
            y = self.origin[1] + key[1] * self.chunk_height
            self.chunks[key] = Chunk(x, y, self.chunk_width, self.chunk_height, loaded=True, grid_pos=key)
        else:
            self.chunks[key].loaded = True

        # Создаем соседние чанки, если их нет, как незагруженные
        for nkey in self.get_neighbor_keys(key):
            if nkey not in self.chunks:
                x = self.origin[0] + nkey[0] * self.chunk_width
                y = self.origin[1] + nkey[1] * self.chunk_height
                self.chunks[nkey] = Chunk(x, y, self.chunk_width, self.chunk_height, loaded=False, grid_pos=nkey)

    def get_chunk_for_point(self, point):
        key = self.get_chunk_key_for_point(point)
        return self.chunks.get(key, None)

    def update_loaded_chunks(self):
        # Для каждого загруженного чанка загружаем его соседей
        loaded_keys = [key for key, c in self.chunks.items() if c.loaded]
        for key in loaded_keys:
            self.load_chunk(key)

    def get_loaded_chunks(self):
        return [c for c in self.chunks.values() if c.loaded]
