import numpy as np
import random
from matplotlib import pyplot as plt


params = {'long_range': 0.06, 'long_range_amplitude': 3, 'mid_range': 0.25, 'mid_range_amplitude': 0.61, 'random_start': 5.4}
demand = 5
current_round = 0


def get_forecasts(current_round, demand, params, forecast_range, forecast_deviation_factor=1.0):
    true_forecast_values = []
    deviating_forecast_values = []
    final_deviating_forecast_values = []

    for x in range(forecast_range):
        days_in_future = x
        x += current_round + 1
        function_value = demand + ((params["long_range_amplitude"] * np.sin(params["long_range"]*x-params["random_start"])) - params["mid_range_amplitude"] * np.sin(params["mid_range"]*x))

        true_forecast_values.append(function_value)
        tamper_value = (demand*forecast_deviation_factor/forecast_range) * days_in_future
        deviating_forecast_values.append(function_value + random.uniform(-tamper_value, tamper_value))

    for value in deviating_forecast_values:
        final_deviating_forecast_values.append(int(round(value, 0)))

    """
    plt.plot(true_forecast_values)
    plt.plot(deviating_forecast_values)
    plt.plot(rounded_deviating_forecast_values)
    plt.show()
    """

    return {"deviating_forecast_values": final_deviating_forecast_values,
            "float_deviating_forecast_values": deviating_forecast_values,
            "true_forecast_values": true_forecast_values}


get_forecasts(current_round, demand, params, 20, .5)
