# BFS maze solver. White pixels are treated as paths, dark pixels as walls. Group 7!
from PIL import Image, ImageDraw
from collections import deque
import numpy as np


def load_maze(image_file, cutoff=150):
    img = Image.open(image_file).convert("L")
    data = np.array(img)
    walkable = data > cutoff
    return walkable, img.size


def locate_openings(walkable):
    h, w = walkable.shape
    candidates = []

    for x in range(w):
        if walkable[0, x]:
            candidates.append((0, x))
        if walkable[h - 1, x]:
            candidates.append((h - 1, x))

    for y in range(h):
        if walkable[y, 0]:
            candidates.append((y, 0))
        if walkable[y, w - 1]:
            candidates.append((y, w - 1))

    if len(candidates) < 2:
        raise RuntimeError("Could not detect start/end openings")

    return candidates[0], candidates[-1]


def bfs_grid(grid, source, target):
    rows, cols = grid.shape
    frontier = deque([source])
    came_from = {source: None}

    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while frontier:
        r, c = frontier.popleft()

        if (r, c) == target:
            break

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr, nc] and nxt not in came_from:
                    came_from[nxt] = (r, c)
                    frontier.append(nxt)

    if target not in came_from:
        return None

    path = []
    cur = target
    while cur:
        path.append(cur)
        cur = came_from[cur]

    return path[::-1]


def draw_solution(image_path, solution, output_file):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    for i in range(len(solution) - 1):
        x1, y1 = solution[i][1], solution[i][0]
        x2, y2 = solution[i + 1][1], solution[i + 1][0]
        draw.line((x1, y1, x2, y2), fill=(0, 255, 0), width=15)

    img.save(output_file)


def main():
    maze_file = "maze.png"
    output_file = "maze_solution.png"

    grid, _ = load_maze(maze_file)
    start, end = locate_openings(grid)
    path = bfs_grid(grid, start, end)

    draw_solution(maze_file, path, output_file)
    print("steps:", len(path))
    print("Saved to:", output_file)


if __name__ == "__main__":
    main()