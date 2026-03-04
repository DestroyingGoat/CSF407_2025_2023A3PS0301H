# agent.py

import heapq
import config as cfg


# Possible movements
MOVES = [
    (1, 0, "walk"),
    (-1, 0, "walk"),
    (0, 1, "walk"),
    (0, -1, "walk"),
    (2, 0, "jump"),
    (-2, 0, "jump"),
    (0, 2, "jump"),
    (0, -2, "jump")
]


def valid(r, c):
    return 0 <= r < cfg.GRID_ROWS and 0 <= c < cfg.GRID_COLS


def oracle_search(grid):

    start = cfg.START
    goal = cfg.GOAL

    # priority queue
    pq = []
    heapq.heappush(pq, (0, start, cfg.MAX_LIVES, 0, 0, []))

    visited = set()

    while pq:

        score, pos, lives, turns, time, path = heapq.heappop(pq)

        if lives <= 0:
            continue

        if pos == goal:
            return path

        state = (pos, lives)

        if state in visited:
            continue

        visited.add(state)

        r, c = pos

        # agent.py - Updated Move Logic
        for dr, dc, mode in MOVES:
            nr = r + dr
            nc = c + dc

            # Rule 4.3: Check if jump skips over a Brick Wall (B)
            if mode == "jump":
                mr = r + dr // 2
                mc = c + dc // 2
                if valid(mr, mc) and grid[mr][mc] == cfg.BRICK:
                    continue # Jumps cannot cross bricks

            # Initialize move costs
            new_time = time
            new_turns = turns + 1 # Every action costs +1 Turn
            
            # Rule 4.3: Brick Wall "Bounce" Logic
            if not valid(nr, nc) or grid[nr][nc] == cfg.BRICK:
                # Cost 1 Turn and return to previous position
                target_r, target_c = r, c 
                new_lives = lives
            else:
                # Valid move to a new cell
                target_r, target_c = nr, nc
                new_lives = lives
                if grid[nr][nc] in cfg.HAZARDS:
                    new_lives -= 1 # Hazards cost 1 life
                
                # Add Time Units based on move type
                new_time += cfg.WALK_TIME if mode == "walk" else cfg.JUMP_TIME

            if new_lives <= 0:
                continue

            # Teacher's Update: Optimize/Minimize this score
            new_score = (new_time + new_turns) / max(1, new_lives)

            heapq.heappush(
                pq,
                (
                    new_score,
                    (target_r, target_c),
                    new_lives,
                    new_turns,
                    new_time,
                    path + [(target_r, target_c, mode, new_lives)]
                )
            )

    return None