from matplotlib import pyplot as plt

warehouse_1 = [0, 9, 8, 7, 5, 10, 9, 6, 5, 10, 9, 8, 7, 5, 12, 11, 10, 9, 7, 5, 3, 10, 7, 4, 1, 0, 6, 5, 12, 11, 8, 5, 3, 1, 7, 6, 11, 9, 8, 5, 4]

action_1 = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]


def convert_to_marker_pos(action):
    return_list = []
    i = 0
    for entry in action:
        if entry == 1:
            return_list.append(i)
        i += 1
    return return_list


plt.rcParams["figure.figsize"] = (7, 4.2)

plt.plot(warehouse_1, "-bo", label="Agent reorder point", markevery=convert_to_marker_pos(action_1), color="#66C2A5")
plt.legend()
plt.ylabel("Inventory Level")
plt.xlabel("Round")
plt.xlim([1, 40])
plt.ylim([0, 30])
plt.title("Simulation with stochastic lead times & stochastic demand")

plt.tight_layout(pad=1)
plt.show()

"""
Both after 50000 training steps a 1250 generations
Demand 1-3, Lead time 1-3
Convegence
PPO
"""
