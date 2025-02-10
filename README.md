# CellAlgoritm
# Cell Structure Generator

This project is a Python-based simulation for generating cell-like structures using a custom vector emission algorithm within a chunked environment. The system creates an initial point in a central chunk that emits rays, and each new point can, in turn, emit additional rays. Rays are truncated at intersections with existing rays, and new points are only added if they remain inside loaded chunks. A separate ChunkManager automatically creates unloaded neighbor chunks around each loaded chunk, and new points from adjacent chunks can be merged when a chunk is loaded via mouse click.

## Features

- **Modular Design:**  
  Separate classes for basic entities:
  - **CellPoint:** Represents a point in the structure, with a position (x, y, z), a flag indicating if it has emitted rays, and a list of emitted vectors.
  - **CellLine:** Represents a line (edge) between two points, along with a counter for polygon membership.
  - **CellPolygon:** (Placeholder) Represents a polygonal cell constructed from an ordered list of points.
  - **Chunk:** Represents a rectangular region of the simulation space, holding points, lines, and (optionally) polygons.
  - **ChunkManager:** Manages a grid of chunks, automatically creating unloaded neighbors around each loaded chunk and handling chunk loading on mouse click.
  
- **Vector Emission and Ray Intersection:**  
  - The initial point emits multiple rays whose vector sum is zero.
  - Each new point (created at the end of a ray) emits child rays based on its parent’s direction with a limited deviation (up to 80°).
  - Before adding a new ray, the system checks for intersections with existing lines; if an intersection is found, the ray is truncated at the intersection point.

- **Chunked Environment:**  
  - The simulation space is divided into chunks.  
  - Only loaded chunks are actively used for further emission; neighbor chunks are created unloaded and can be loaded on user interaction.
  - New points are added to a chunk based on their position, ensuring proper merging of structure between adjacent chunks.

- **Visualization:**  
  - Uses Pygame for real-time visualization.
  - Displays chunk boundaries (loaded chunks in green, unloaded in red), points (yellow if inside, red if outside), and lines (cyan).
  - Mouse click on an unloaded chunk loads that chunk.

## File Structure
    project
    ├── cell_point.py # Defines the CellPoint class. 
    ├── cell_line.py # Defines the CellLine class. 
    ├── cell_polygon.py # Defines the CellPolygon class (for future expansion). 
    ├── chunk.py # Defines the Chunk class. 
    ├── chunk_manager.py # Implements the ChunkManager class. 
    ├── cell_structure_demo.py # Main demo script; contains the algorithm and Pygame visualization. 
    └── README.md # This file.

## Requirements

- Python 3.x
- Pygame
- NumPy (for math utilities; optional if using math and random modules)

To install Pygame, you can run:
```bash
pip install pygame