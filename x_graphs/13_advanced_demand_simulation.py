from matplotlib import pyplot as plt
import numpy as np
import random

sim_length = 100
curve_interval = 1


def calculate_demand_path(demand, demand_fluctuation):
    # Get random values for function parameters
    long_range = round(random.uniform(curve_interval*.02, curve_interval*.1), 2)
    long_range_amplitude = demand_fluctuation
    mid_range = round(random.uniform(curve_interval*.1, curve_interval*.3), 2)
    mid_range_amplitude = round(random.uniform(.3, 1), 2)
    random_start = round(random.uniform(0, 1 / long_range), 2)

    # Save function parameters
    function_parameters = {"long_range": long_range, "long_range_amplitude": long_range_amplitude,
                           "mid_range": mid_range, "mid_range_amplitude": mid_range_amplitude,
                           "random_start": random_start}

    demand_path = []
    for x in range(sim_length):
        demand_function = demand + ((long_range_amplitude * np.sin(long_range*x-random_start)) - mid_range_amplitude * np.sin(mid_range*x))
        demand_path.append(round(demand_function, 0))

    return {"demand_path": demand_path, "function_parameters": function_parameters}

plt.rcParams["figure.figsize"] = (7, 4.2)
demand1 = 4
demand2 = 6
demand3 = 6

demand_fluctuation1 = 2
demand_fluctuation2 = 3
demand_fluctuation3 = 1

x = np.linspace(0, sim_length, sim_length*10)

# params = calculate_demand_path(demand1, demand_fluctuation1)["function_parameters"]
params = {'long_range': 0.05, 'long_range_amplitude': 2, 'mid_range': 0.25, 'mid_range_amplitude': 0.41, 'random_start': 3.28}
y1 = demand1 + ((params["long_range_amplitude"] * np.sin(params["long_range"]*x-params["random_start"]))
              - params["mid_range_amplitude"] * np.sin(params["mid_range"]*x))

print(params)

# params = calculate_demand_path(demand2, demand_fluctuation2)["function_parameters"]
params = {'long_range': 0.06, 'long_range_amplitude': 3, 'mid_range': 0.21, 'mid_range_amplitude': 0.85, 'random_start': 2.4}
y2 = demand2 + ((params["long_range_amplitude"] * np.sin(params["long_range"]*x-params["random_start"]))
              - params["mid_range_amplitude"] * np.sin(params["mid_range"]*x))

print(params)

# params = calculate_demand_path(demand3, demand_fluctuation3)["function_parameters"]
params = {'long_range': 0.07, 'long_range_amplitude': 1, 'mid_range': 0.16, 'mid_range_amplitude': 0.35, 'random_start': 11.77}
y3 = demand3 + ((params["long_range_amplitude"] * np.sin(params["long_range"]*x-params["random_start"]))
              - params["mid_range_amplitude"] * np.sin(params["mid_range"]*x))

print(params)

plt.plot(x, y1, color="#FC8D62", label="Demand: 6; Fluctuation: 4")
plt.plot(x, y2, color="#66C2A5", label="Demand: 4; Fluctuation: 2")
plt.plot(x, y3, color="#8DA0CB", label="Demand: 6; Fluctuation: 1")
plt.legend()
plt.ylabel("Demand")
plt.xlabel("Simulation Round")
plt.xlim([1, 100])
plt.ylim([0, 10])
plt.title("Created Demand Trend Examples")
plt.show()