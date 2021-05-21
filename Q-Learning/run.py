from path import Environment
from agent import QLearningTable
import tkinter as tk


def update():
    # Resulted list for the plotting Episodes via Steps
    all_steps = []

    # Summed costs for all episodes in resulted list
    all_costs = []

    for episode in range(100000):
        # Initial Observation
        observation = env.reset()

        # Updating number of Steps for each Episode
        episode_steps = 0

        # Updating the cost for each episode
        episode_cost = 0

        while True:
            # Refreshing environment
            env.render()

            # agent chooses action based on observation
            action = agent.choose_action(str(observation))

            # agent takes an action and get the next observation and reward
            observation_, reward, done = env.step(action)

            # agent learns from this transition and calculating the cost
            episode_cost += agent.learn(str(observation), action, reward, str(observation_))

            # Swapping the observations - current and next
            observation = observation_

            # Calculating number of Steps in the current Episode
            episode_steps += 1

            # Break while loop when it is the end of current Episode
            # When agent reached the goal or obstacle
            if done:
                all_steps += [episode_steps]
                all_costs += [episode_cost]
                break

    # Showing the final route
    env.final()

    # Showing the Q-table with values for each action
    agent.print_q_table()

    # Plotting the results
    agent.plot_results(all_steps, all_costs)


# Start Window for setting the environment
text_fields = 'Start X', 'Start Y', 'Finish X', 'Finish Y', 'Width', 'Height', 'Pixel Size'

start_x = 0
start_y = 0
finish_x = 0
finish_y = 0
width = 0
height = 0
pixel_size = 0


def fetch_info(root, entries):
    global start_x
    global start_y
    global finish_x
    global finish_y
    global width
    global height
    global pixel_size

    start_x = int(entries[0][1].get())
    start_y = int(entries[1][1].get())
    finish_x = int(entries[2][1].get())
    finish_y = int(entries[3][1].get())
    width = int(entries[4][1].get())
    height = int(entries[5][1].get())
    pixel_size = int(entries[6][1].get())

    root.quit()


def create_form(root, fields) -> object:
    entries = []
    for field in fields:
        row = tk.Frame(root)
        text = tk.Label(row, width=10, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        text.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries


def settings_window():
    root = tk.Tk()

    root.title('Q-Learning')
    ents = create_form(root, text_fields)

    b1 = tk.Button(root, text='Go!',
                   width=10, height=2,
                   command=(lambda e=ents: fetch_info(root, e)))
    b1.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()


# Commands to be implemented after running this file
if __name__ == "__main__":
    # Calling for starting window
    settings_window()

    # Calling for the environment
    env = Environment(start_x, start_y, finish_x, finish_y, height, width, pixel_size)

    # Calling for main algorithm
    agent = QLearningTable(actions=list(range(env.n_actions)))

    # Running main loop with Episodes by calling the function update()
    env.after(1, update)
    env.mainloop()
