# grid_gen.py

import random
import config as cfg


# -----------------------------
# VALID NEIGHBORS (ORTHOGONAL)
# -----------------------------
def neighbors(r, c):

    moves = [(1,0),(-1,0),(0,1),(0,-1)]

    result = []

    for dr, dc in moves:
        nr, nc = r + dr, c + dc

        if 0 <= nr < cfg.GRID_ROWS and 0 <= nc < cfg.GRID_COLS:
            result.append((nr, nc))

    return result


# -----------------------------
# RANDOM PATH BETWEEN 2 CELLS
# -----------------------------
def random_path(start, goal):

    r, c = start
    path = [(r, c)]
    visited = set(path)

    while (r, c) != goal:

        neighbors = []

        moves = [(1,0),(-1,0),(0,1),(0,-1)]

        for dr, dc in moves:

            nr = r + dr
            nc = c + dc

            if 0 <= nr < cfg.GRID_ROWS and 0 <= nc < cfg.GRID_COLS:

                if (nr, nc) not in visited:

                    neighbors.append((nr, nc))

        if not neighbors:
            break

        # sort by Manhattan distance to goal
        neighbors.sort(
            key=lambda cell:
            abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])
        )

        # choose mostly good move but keep randomness
        if random.random() < 0.7:
            next_cell = neighbors[0]
        else:
            next_cell = random.choice(neighbors)

        r, c = next_cell
        path.append((r, c))
        visited.add((r, c))

    return path
# -----------------------------
# ANCHOR SELECTION
# -----------------------------
def select_anchors():

    while True:

        r1 = random.randint(1, cfg.GRID_ROWS-2)
        c1 = random.randint(1, cfg.GRID_COLS-2)

        r2 = random.randint(1, cfg.GRID_ROWS-2)
        c2 = random.randint(1, cfg.GRID_COLS-2)

        a1 = (r1, c1)
        a2 = (r2, c2)

        if a1 == a2:
            continue

        if r1 == r2:
            continue

        if c1 == c2:
            continue

        if abs(r1-r2) + abs(c1-c2) <= 1:
            continue

        return a1, a2


# -----------------------------
# HAZARD ADJACENCY CHECK
# -----------------------------
def not_adjacent(a, b):

    return abs(a[0]-b[0]) + abs(a[1]-b[1]) > 1


# -----------------------------
# BUILD GRID
# -----------------------------
def build_grid():

    grid = [[None for _ in range(cfg.GRID_COLS)]
            for _ in range(cfg.GRID_ROWS)]

    start = cfg.START
    goal = cfg.GOAL

    # -------- Select anchors --------
    anchor1, anchor2 = select_anchors()

    # -------- Build path segments --------
    path1 = random_path(start, anchor1)
    path2 = random_path(anchor1, anchor2)[1:]
    path3 = random_path(anchor2, goal)[1:]

    path = path1 + path2 + path3

    # remove duplicates while preserving order
    seen = set()
    unique_path = []

    for cell in path:
        if cell not in seen:
            unique_path.append(cell)
            seen.add(cell)

    path = unique_path

    # -------- Initialize path cells as LAND --------
    for r, c in path:
        grid[r][c] = cfg.LAND

    # -------- Place hazards on path --------
    while True:

        volcano = random.sample(path[1:-1], 2)

        if not not_adjacent(volcano[0], volcano[1]):
            continue

        remaining = [p for p in path[1:-1] if p not in volcano]

        water = random.sample(remaining, 2)

        if not not_adjacent(water[0], water[1]):
            continue

        break

    for r, c in volcano:
        grid[r][c] = cfg.VOLCANO

    for r, c in water:
        grid[r][c] = cfg.WATER

    # -------- Fill remaining cells --------
    # -------- Fill remaining cells with exact distribution --------

    remaining_cells = []

    for r in range(cfg.GRID_ROWS):
        for c in range(cfg.GRID_COLS):

            if grid[r][c] is None:
                remaining_cells.append((r, c))

    total = len(remaining_cells)

    hazard_count = round(0.5 * total)
    land_count = round(0.4 * total)
    brick_count = total - hazard_count - land_count


    terrain_list = []

    # hazards (W or V)
    for _ in range(hazard_count):
        terrain_list.append(random.choice(cfg.HAZARDS))

    # land
    for _ in range(land_count):
        terrain_list.append(cfg.LAND)

    # bricks
    for _ in range(brick_count):
        terrain_list.append(cfg.BRICK)


    random.shuffle(terrain_list)

    for (r, c), terrain in zip(remaining_cells, terrain_list):
        grid[r][c] = terrain

    return grid, path, anchor1, anchor2