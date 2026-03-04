# Oracle Intelligent Agentic System
# AI Project Exercise 1


## Group Members
1. Anurag Padhy - 2023A3PS0301H

2. Khushal Vardhan Neeli - 2023B4A40680H

3. Harshit Verma - 2022A3PS0510H

## Project Overview
This project implements the **Oracle** agent, an intelligent system designed to navigate a $(M \times N)$ grid-type environment with varying hazards. 

## Scoring Logic & Optimization
The agent is designed to **minimize** the following cost function to reach the goal at the fastest possible speed:

$$Score = \frac{\text{Turn Units} + \text{Time Units}}{\text{Lives}}$$

- **Turn Units**: Every action (Walk, Jump, or Brick-wall bounce) adds $+1$ turn.
- **Time Units**: Walk = $2$ units, Jump = $3$ units.
- **Lives**: Agent starts with $4$. Stepping on Water (W) or Volcano (V) costs $1$ life.

The agent uses a **Priority Queue (Dijkstra-based approach)** to find the path that yields the lowest possible score while ensuring survival (Lives $> 0$).

## Key Features
- **Brick Wall "Bounce"**: Attempting to move into a Brick Wall (B) costs 1 turn and returns the agent to its previous position.
- **Visualizer**: Generates an animated `.gif` showing path history, using **curved purple arrows** for Jumps and **dotted red arrows** for damage.
- **Modular Architecture**: Strictly follows the required file structure (`config.py`, `grid_gen.py`, `agent.py`, `visualizer.py`, and `main.py`).

## Setup Instructions
1. Create and activate the environment, run the agent:
   ```bash
   conda create -n ai_test_env python=3.12
   conda activate ai_test_env
   pip install -r requirements.txt
   python main.py

