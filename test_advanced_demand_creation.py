from matplotlib import pyplot as plt
import numpy as np
import random

demand = 5
demand_fluctuation = 3
sim_length = 100
curve_interval = 1


def calculate_demand_path():
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


path_calc = calculate_demand_path()
# params = path_calc["function_parameters"]
params = {'long_range': 0.06, 'long_range_amplitude': 3, 'mid_range': 0.25, 'mid_range_amplitude': 0.61, 'random_start': 5.4}
demand_path = path_calc["demand_path"]

x = np.linspace(0, sim_length, sim_length*10)
y = demand + ((params["long_range_amplitude"] * np.sin(params["long_range"]*x-params["random_start"]))
              - params["mid_range_amplitude"] * np.sin(params["mid_range"]*x))

print(params)

plt.plot(x, y)
plt.plot(demand_path, "o")
plt.ylim(0, 10)
plt.show()