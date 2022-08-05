from matplotlib import pyplot as plt
import numpy as np
import random
import matplotlib.font_manager

print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
matplotlib.font_manager.fontManager.addfont('C:\\Users\\patri\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')
plt.rcParams["font.family"] = "CMU Serif"

sim_length = 100
curve_interval = 1


def get_forecasts(current_round, demand, params, forecast_range, forecast_deviation_factor=1.0):
    true_forecast_values = []
    deviating_forecast_values = []
    final_deviating_forecast_values = []
    tamps = []

    for x in range(forecast_range):
        days_in_future = x
        x += current_round + 1
        function_value = demand + ((params["long_range_amplitude"] * np.sin(params["long_range"]*x-params["random_start"])) - params["mid_range_amplitude"] * np.sin(params["mid_range"]*x))

        true_forecast_values.append(function_value)
        tamper_value = (demand*forecast_deviation_factor/forecast_range) * days_in_future
        deviating_forecast_values.append(function_value + random.uniform(-tamper_value, tamper_value))
        tamps.append(tamper_value)
    for value in deviating_forecast_values:
        final_deviating_forecast_values.append(int(round(value, 0)))

    return {"deviating_forecast_values": final_deviating_forecast_values,
            "float_deviating_forecast_values": deviating_forecast_values,
            "true_forecast_values": true_forecast_values,
            "tamps": tamps}

plt.rcParams["figure.figsize"] = (7, 4.2)
demand1 = 6

x = np.linspace(0, sim_length, sim_length*10)


params = {'long_range': 0.14, 'long_range_amplitude': 2, 'mid_range': 0.17, 'mid_range_amplitude': 0.38, 'random_start': 8.87}

y1 = demand1 + ((params["long_range_amplitude"] * np.sin(params["long_range"]*x-params["random_start"]))
              - params["mid_range_amplitude"] * np.sin(params["mid_range"]*x))

dic = get_forecasts(0, demand1, params, 100, 1)
forecasts = dic["float_deviating_forecast_values"]
trues = dic["true_forecast_values"]
distortion = dic["tamps"]

upper_bound = []
lower_bound = []

for i in range(51):
    upper_bound.append(trues[i]+distortion[i])
    lower_bound.append(trues[i]-distortion[i])

plt.plot(x, y1, color="#66C2A5", label="True Demand", linewidth=3)

plt.plot([0] + upper_bound, "--", color="#66C2A5", alpha=0.5, label="Forecasting Range")
plt.plot([0] + lower_bound, "--", color="#66C2A5", alpha=0.5)

plt.plot([0] + forecasts, "o", color="#FC8D62", label="Chosen Forecast Values")
plt.legend(loc="lower left")
plt.ylabel("Demand", fontsize=11)
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 50])
plt.ylim([0, 10])
plt.title("Forecast Creation for One Customer", fontsize=16)
plt.show()