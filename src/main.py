# main.py

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import config as cfg
from grid_gen import build_grid
from agent import oracle_search
from visualizer import animate


CELL_COLORS = {
    "L": "green",
    "V": "red",
    "W": "blue",
    "B": "gray"
}


# -----------------------------
# SAVE GRID IMAGE
# -----------------------------
def save_grid_png(grid, filename):

    fig, ax = plt.subplots(figsize=(6, 6))

    for r in range(cfg.GRID_ROWS):
        for c in range(cfg.GRID_COLS):

            rect = patches.Rectangle(
                (c, r),
                1,
                1,
                edgecolor="black",
                facecolor=CELL_COLORS[grid[r][c]]
            )

            ax.add_patch(rect)

            ax.text(
                c + 0.5,
                r + 0.5,
                f"{r},{c}",
                ha="center",
                va="center",
                fontsize=7,
                color="white"
            )

    ax.set_xlim(0, cfg.GRID_COLS)
    ax.set_ylim(0, cfg.GRID_ROWS)

    ax.invert_yaxis()
    ax.axis("off")

    fig.savefig(filename)
    plt.close(fig)


# -----------------------------
# SAVE GROUND TRUTH PATH
# -----------------------------
def save_ground_truth(grid, path, filename):

    fig, ax = plt.subplots(figsize=(6, 6))

    for r in range(cfg.GRID_ROWS):
        for c in range(cfg.GRID_COLS):

            rect = patches.Rectangle(
                (c, r),
                1,
                1,
                edgecolor="black",
                facecolor=CELL_COLORS[grid[r][c]]
            )

            ax.add_patch(rect)

    # draw trajectory
    xs = [c + 0.5 for r, c in path]
    ys = [r + 0.5 for r, c in path]

    ax.plot(xs, ys, color="black", linewidth=2)

    ax.set_xlim(0, cfg.GRID_COLS)
    ax.set_ylim(0, cfg.GRID_ROWS)

    ax.invert_yaxis()
    ax.axis("off")

    fig.savefig(filename)
    plt.close(fig)


# -----------------------------
# PRINT GRID WITH CELL IDS
# -----------------------------
def print_grid(grid):

    print("\nGRID WITH CELL TYPES:\n")

    for r in range(cfg.GRID_ROWS):
        row = []
        for c in range(cfg.GRID_COLS):
            row.append(f"{grid[r][c]}({r},{c})")
        print(" ".join(row))


# -----------------------------
# MAIN ENTRY
# -----------------------------
def main():

    print("\n--- Oracle Grid Simulation ---")

    # 9.1 Take parameters from config
    print(f"\nGrid size: {cfg.GRID_ROWS} x {cfg.GRID_COLS}")
    print(f"Start: {cfg.START}  Goal: {cfg.GOAL}")

    # build environment
    grid, ground_truth_path, anchor1, anchor2 = build_grid()

    print("\nAnchor Cells:")
    print("Anchor 1:", anchor1)
    print("Anchor 2:", anchor2)

    # 9.2 Print cell IDs and save trajectory image
    print_grid(grid)

    save_ground_truth(
        grid,
        ground_truth_path,
        "ground_truth_trajectory.png"
    )

    print("\nSaved ground truth trajectory image.")

    # 9.3 Save full grid PNG
    save_grid_png(
        grid,
        "initial_grid.png"
    )

    print("Saved initial grid image.")

    # 9.4 Run agent search
    print("\nRunning Oracle agent...")

    agent_path = oracle_search(grid)

    if agent_path is None:
        print("No valid path found.")
        return

    print("Agent path found.")

    print("\nAnchor in Path Check:")
    print(anchor1 in ground_truth_path)
    print(anchor2 in ground_truth_path)

    # 9.5 Render animation and save frames
    animate(grid, agent_path)


if __name__ == "__main__":
    main()