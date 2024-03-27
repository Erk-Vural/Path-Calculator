# Q-Learning Path Calculator

The Q-Learning Path Calculator is a Python-based application that utilizes Q-learning to find the shortest path for a robot on a given maze. Q-learning is a reinforcement learning algorithm that learns an optimal policy by interacting with an environment and receiving rewards for its actions.

## Features

- **Q-Learning Algorithm**: Utilizes Q-learning to find the shortest path for a robot on a maze.
- **Maze Representation**: Represents the maze as a grid with obstacles and goal positions.
- **Customizable Maze**: Allows users to define their own maze configurations.
- **Shortest Path Calculation**: Finds the shortest path from the starting position to the goal position using Q-learning.

## Technologies Used

- Python
- NumPy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/q-learning-path-calculator.git
   ```

2. Install dependencies:
   ```bash
   pip install numpy
   ```

3. Run the Python script:
   ```bash
   python q_learning_path_calculator.py
   ```

## Usage

1. Define the maze configuration in the `maze.txt` file. Use the following symbols:
   - `S`: Starting position
   - `G`: Goal position
   - `O`: Obstacle
   - `.`: Open path

2. Run the script and observe the robot finding the shortest path using Q-learning.

## Customization

- Modify the `maze.txt` file to define custom maze configurations.
- Adjust the Q-learning parameters and hyperparameters in the Python script (`q_learning_path_calculator.py`) for different maze environments.
