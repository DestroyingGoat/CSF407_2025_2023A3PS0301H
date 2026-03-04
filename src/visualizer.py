# visualizer.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import os
import shutil
import config as cfg


COLORS = {
    "L": "green",
    "V": "red",
    "W": "blue",
    "B": "gray"
}

FRAME_DIR = "frames"


def draw_grid(ax, grid):

    for r in range(cfg.GRID_ROWS):
        for c in range(cfg.GRID_COLS):

            rect = patches.Rectangle(
                (c, r),
                1,
                1,
                edgecolor="black",
                facecolor=COLORS[grid[r][c]]
            )

            ax.add_patch(rect)


def draw_arrow(ax, start, end, mode, damaged):
    r1, c1 = start
    r2, c2 = end

    color = "black"
    style = "-"
    conn = "arc3,rad=0" # Default straight

    if mode == "jump":
        color = "purple"
        conn = "arc3,rad=0.3" # Requirement 8: Curved jump

    if damaged:
        color = "red"
        style = "--" # Requirement 8: Dotted/dashed for limping

    ax.annotate(
        "",
        xy=(c2 + 0.5, r2 + 0.5),
        xytext=(c1 + 0.5, r1 + 0.5),
        arrowprops=dict(
            arrowstyle="->",
            color=color,
            linestyle=style,
            connectionstyle=conn, # Apply the curve here
            lw=2
        )
    )


def animate(grid, agent_path):
    # FIXED: Ensure these are indented exactly 4 spaces
    if os.path.exists(FRAME_DIR):
        shutil.rmtree(FRAME_DIR)
    
    os.makedirs(FRAME_DIR)

    history = []
    prev = cfg.START
    lives = cfg.MAX_LIVES
    turns = 0
    time = 0

    for step, (r, c, mode, life_after) in enumerate(agent_path):
        fig, ax = plt.subplots(figsize=(6, 6))
        draw_grid(ax, grid)

        damaged = life_after < lives
        history.append((prev, (r, c), mode, damaged))

        # draw entire path history
        for s, e, m, d in history:
            draw_arrow(ax, s, e, m, d)

        if damaged:
            ax.text(c + 0.3, r + 0.7, "✗", fontsize=16, color="red")

        lives = life_after
        turns += 1

        if mode == "walk":
            time += cfg.WALK_TIME
        else:
            time += cfg.JUMP_TIME

        # Requirement 7: Optimized score calculation
        score = (turns + time) / max(1, lives)

        # Requirement 9.5: Update values on screen
        ax.set_title(
            f"Lives: {lives} | Turns: {turns} | Time: {time} | Score: {score:.2f}"
        )

        ax.set_xlim(0, cfg.GRID_COLS)
        ax.set_ylim(0, cfg.GRID_ROWS)
        ax.invert_yaxis()
        ax.axis("off")

        fig.savefig(f"{FRAME_DIR}/frame_{step}.png")
        plt.close(fig)
        prev = (r, c)

    create_gif()


def create_gif():

    images = []

    files = sorted(
        os.listdir(FRAME_DIR),
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )

    for f in files:
        images.append(imageio.imread(f"{FRAME_DIR}/{f}"))

    imageio.mimsave(
        "oracle_simulation.gif",
        images,
        fps=1
    )

    print("Simulation saved as oracle_simulation.gif")