import tkinter as tk
import numpy as np
from random import randint
import time

# Global variable for dictionary with coordinates for the final route
final_route_coords = {}


class Environment(tk.Tk, object):
    def __init__(self, start_x, start_y, finish_x, finish_y, height, width, pixels):
        super(Environment, self).__init__()

        # Setting the sizes for the environment
        self.pixels = pixels  # pixels
        self.env_height = height  # grid height
        self.env_width = width  # grid width

        # Start, Agent and finish coordinates
        self.start_pnt = {
            "x": int(start_x),
            "y": int(start_y)
        }
        self.agent_pnt = {
            "x": int(start_x),
            "y": int(start_y)
        }
        self.flag_pnt = {
            "x": int(finish_x),
            "y": int(finish_y)
        }

        # Obstacles info
        self.obstacle_amount = int((self.env_height * self.env_width) / 100 * 30)
        self.o = np.array([self.pixels / 2, self.pixels / 2])
        self.obstacles = {  # Creating dictionary for holding Coordinates of Obstacles
            "x": [],
            "y": []
        }
        self.coords_obstacles = {  # Hold info obout 4 corners of a obstacle
            "x0": [],
            "x1": [],
            "y0": [],
            "y1": []
        }

        # Setting up actions
        self.action_space = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.action_space)

        # Drawing window
        self.canvas_widget = tk.Canvas(self, bg='oldlace',
                                       height=self.env_height * self.pixels,
                                       width=self.env_width * self.pixels)
        self.title('Learning...')
        self.geometry('{0}x{1}'.format(self.env_height * self.pixels, self.env_width * self.pixels))
        self.build_environment()

        # Dictionaries to draw the final route
        self.d = {}
        self.f = {}

        # Key for the dictionaries
        self.key = 0

        # Writing the final dictionary first time
        self.is_first_time = True

        # Showing the steps for longest found route
        self.longest_route = 0

        # Showing the steps for the shortest route
        self.shortest_route = 0

    # Checks for new coordinates are exist in obstacles
    def is_coordinate_exists(self, temp_x, temp_y, count):
        for i in range(count):
            x = self.obstacles['x'][i]
            y = self.obstacles['y'][i]
            if temp_x == x and temp_y == y:
                return False

        # checks for new coordinates are same with start or finish
        if (temp_x == self.start_pnt['x'] and temp_y == self.start_pnt['y']) or \
                (temp_x == self.flag_pnt['x'] and temp_y == self.flag_pnt['y']):
            return False

        return True

    # Generate random coordinates for creating obstacles
    def generate_coordinates(self):
        number_range = self.env_height - 1

        for i in range(self.obstacle_amount):
            temp_x = randint(0, number_range)
            temp_y = randint(0, number_range)

            size = len(self.obstacles['x']) - 1
            if self.is_coordinate_exists(temp_x, temp_y, size):
                self.obstacles['x'].append(temp_x)
                self.obstacles['y'].append(temp_y)
                print('x: ' + str(temp_x) + ' y: ' + str(temp_y))

            else:
                self.obstacle_amount += 1

    # Write coordinates to engel.txt as (x, y, color)
    def write_to_file(self):
        file = open("engel.txt", "w")

        width = self.env_width - 1
        height = self.env_height - 1
        for i in range(width):
            for j in range(height):
                # Check for point is start
                if i == self.start_pnt['x'] and j == self.start_pnt['y']:
                    file.write('(' + str(self.start_pnt['x']) + ',' + str(self.start_pnt['y']) + ',' + 'Blue' + ')\n')

                # Check for point is flag
                elif i == self.flag_pnt['x'] and j == self.flag_pnt['y']:
                    file.write('(' + str(self.flag_pnt['x']) + ',' + str(self.flag_pnt['y']) + ',' + 'Green' + ')\n')

                # Else is empty space
                else:
                    file.write('(' + str(i) + ',' + str(j) + ',' + 'White' + ')\n')

        size = len(self.obstacles['x'])
        for i in range(size):
            file.write('(' + str(self.obstacles['x'][i]) + ',' + str(self.obstacles['y'][i]) + ',' + 'Gray' + ')\n')

        file.close()

    # Draw obstacles to screen and save coordinates
    def create_obstacles(self):
        obstacle_amount = len(self.obstacles['x'])
        for i in range(obstacle_amount):
            x = self.obstacles['x'][i]
            y = self.obstacles['y'][i]

            # Defining center of obstacle
            obstacle_center = self.o + np.array([self.pixels * x, self.pixels * y])
            # building obstacle
            self.obstacle = self.canvas_widget.create_rectangle(
                obstacle_center[0] - self.pixels / 2, obstacle_center[1] - self.pixels / 2,  # Top left corner
                obstacle_center[0] + 10, obstacle_center[1] + self.pixels / 2,  # Bottom right corner
                outline='black', fill='grey')

            # Saving the coordinates of obstacle according to the size of agent
            # In order to fit the coordinates of the agent
            self.coords_obstacles['x0'].append(self.canvas_widget.coords(self.obstacle)[0] + 3)
            self.coords_obstacles['x1'].append(self.canvas_widget.coords(self.obstacle)[1] + 3)
            self.coords_obstacles['y0'].append(self.canvas_widget.coords(self.obstacle)[2] - 3)
            self.coords_obstacles['y1'].append(self.canvas_widget.coords(self.obstacle)[3] - 3)

    def build_environment(self):
        # Create Grid Lines
        for column in range(0, self.env_width * self.pixels, self.pixels):
            x0, y0, x1, y1 = column, 0, column, self.env_height * self.pixels
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='black')
        for row in range(0, self.env_height * self.pixels, self.pixels):
            x0, y0, x1, y1 = 0, row, self.env_height * self.pixels, row
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='black')

        # Generate random numbers between boundaries
        self.generate_coordinates()

        # Write coordinates to file
        self.write_to_file()

        # Draw obstacles
        self.create_obstacles()

        # Start Point - blue rectangle
        start_center = self.o + np.array([self.pixels * self.start_pnt['x'], self.pixels * self.start_pnt['y']])
        # Building the flag
        self.start_pnt = self.canvas_widget.create_rectangle(
            start_center[0] - 10, start_center[1] - 10,  # Top left corner
            start_center[0] + 10, start_center[1] + 10,  # Bottom right corner
            outline='grey', fill='blue')

        # Creating an agent of Mobile Robot - red dot
        agent_center = start_center
        self.agent = self.canvas_widget.create_oval(
            agent_center[0] - 7, agent_center[1] - 7,
            agent_center[0] + 7, agent_center[1] + 7,
            outline='red', fill='red')

        # Final Point - green rectangle
        flag_center = self.o + np.array([self.pixels * self.flag_pnt['x'], self.pixels * self.flag_pnt['y']])
        # Building the flag
        self.flag = self.canvas_widget.create_rectangle(
            flag_center[0] - 10, flag_center[1] - 10,  # Top left corner
            flag_center[0] + 10, flag_center[1] + 10,  # Bottom right corner
            outline='grey', fill='lawngreen')
        # Saving the coordinates of the final point according to the size of agent
        # In order to fit the coordinates of the agent
        self.coords_flag = [self.canvas_widget.coords(self.flag)[0] + 3,
                            self.canvas_widget.coords(self.flag)[1] + 3,
                            self.canvas_widget.coords(self.flag)[2] - 3,
                            self.canvas_widget.coords(self.flag)[3] - 3]

        self.canvas_widget.pack()

    # Function to reset the environment and start new Episode
    def reset(self):
        self.update()
        # time.sleep(0.5)

        # Updating agent
        self.canvas_widget.delete(self.agent)

        agent_center = self.o + np.array([self.pixels * self.agent_pnt['x'], self.pixels * self.agent_pnt['y']])
        self.agent = self.canvas_widget.create_oval(
            agent_center[0] - 7, agent_center[1] - 7,
            agent_center[0] + 7, agent_center[1] + 7,
            outline='red', fill='red')

        # Clearing the dictionary and the i
        self.d = {}
        self.key = 0

        # Return observation
        return self.canvas_widget.coords(self.agent)

    # Function to get the next observation and reward by doing next step
    def step(self, action):
        # Current state of the agent
        global reward, done
        state = self.canvas_widget.coords(self.agent)
        base_action = np.array([0, 0])

        # Updating next state according to the action
        # Action 'up'
        if action == 0:
            if state[1] >= self.pixels:
                base_action[1] -= self.pixels
        # Action 'down'
        elif action == 1:
            if state[1] < (self.env_height - 1) * self.pixels:
                base_action[1] += self.pixels
        # Action right
        elif action == 2:
            if state[0] < (self.env_width - 1) * self.pixels:
                base_action[0] += self.pixels
        # Action left
        elif action == 3:
            if state[0] >= self.pixels:
                base_action[0] -= self.pixels

        # Moving the agent according to the action
        self.canvas_widget.move(self.agent, base_action[0], base_action[1])

        # Writing in the dictionary coordinates of found route
        self.d[self.key] = self.canvas_widget.coords(self.agent)

        # Updating next state
        next_state = self.d[self.key]

        # Updating key for the dictionary
        self.key += 1

        # Calculating the reward for the agent
        if next_state == self.coords_flag:
            # time.sleep(0.1)
            reward = 5
            done = True
            next_state = 'goal'

            # Filling the dictionary first time
            if self.is_first_time:
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]
                self.is_first_time = False
                self.longest_route = len(self.d)
                self.shortest_route = len(self.d)

            # Checking if the currently found route is shorter
            if len(self.d) < len(self.f):
                # Saving the number of steps for the shortest route
                self.shortest_route = len(self.d)
                # Clearing the dictionary for the final route
                self.f = {}
                # Reassigning the dictionary
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]

            # Saving the number of steps for the longest route
            if len(self.d) > self.longest_route:
                self.longest_route = len(self.d)

        size = len(self.obstacles['x'])
        for i in range(size):
            coords_obstacle = [self.coords_obstacles['x0'][i],
                               self.coords_obstacles['x1'][i],
                               self.coords_obstacles['y0'][i],
                               self.coords_obstacles['y1'][i]
                               ]
            if next_state == coords_obstacle:
                reward = -5
                done = True
                next_state = 'obstacle'

                # Clearing the dictionary and the i
                self.d = {}
                self.key = 0

                break

        else:
            reward = 0
            done = False

        return next_state, reward, done

    # Function to refresh the environment
    def render(self):
        # time.sleep(0.03)
        self.update()

    # Function to show the found route
    def final(self):
        # Deleting the agent at the end
        self.canvas_widget.delete(self.agent)

        # Showing the number of steps
        print('The shortest route:', self.shortest_route)
        print('The longest route:', self.longest_route)

        # Filling the route
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            print(self.f[j])
            self.track = self.canvas_widget.create_oval(
                self.f[j][0] - 3 + self.o[0] - 4, self.f[j][1] - 3 + self.o[1] - 4,
                self.f[j][0] - 3 + self.o[0] + 4, self.f[j][1] - 3 + self.o[1] + 4,
                fill='blue', outline='blue')
            # Writing the final route in the global variable a
            final_route_coords[j] = self.f[j]


# Returning the final dictionary with route coordinates for agent.py
def final_states():
    return final_route_coords


# Main for testing path
if __name__ == '__main__':
    env = Environment(0, 10, 49, 40, 20, 20, 20)
    env.mainloop()
