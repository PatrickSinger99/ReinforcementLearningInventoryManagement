from matplotlib import pyplot as plt
import matplotlib.font_manager
import matplotlib.lines as mlines

print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
matplotlib.font_manager.fontManager.addfont('C:\\Users\\patri\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')
plt.rcParams["font.family"] = "CMU Serif"

warehouse_1 = [0, 9, 9, 8, 6, 6, 5, 4, 2, 2, 1, 1, 1, 0, 8, 6, 6, 6, 4, 3, 3, 3, 3, 12, 10, 9, 7, 7, 5, 5, 3, 1, 0, 0, 9, 8, 7, 5, 4, 3, 1]
warehouse_2 = [0, 9, 7, 4, 3, 1, 10, 8, 6, 3, 0, 8, 7, 4, 2, 9, 6, 3, 0, 0, 7, 5, 2, 1, 8, 5, 4, 2, 11, 8, 5, 4, 3, 10, 7, 4, 3, 2, 9, 8, 5]

action_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
action_2 = [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]


def convert_to_marker_pos(action):
    return_list = []
    i = 0
    for entry in action:
        if entry == 1:
            return_list.append(i)
        i += 1
    return return_list


plt.rcParams["figure.figsize"] = (10, 3.2)
reorder_marker = mlines.Line2D([],[], color='#66C2A5', marker='o', linestyle='None', label="Agent Reorder Point")

plt.subplot(1, 2, 1)
plt.plot(warehouse_1, "-bo", label="Agent reorder point", markevery=convert_to_marker_pos(action_1), color="#66C2A5")
plt.legend(handles=[reorder_marker])
plt.ylabel("Inventory Level", fontsize=11)
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 25])
plt.title("Warehouse 1 / Demand Range 0-2", fontsize=14)

plt.subplot(1, 2, 2)
plt.plot(warehouse_2, "-bo", label="Agent reorder point", markevery=convert_to_marker_pos(action_2), color="#66C2A5")
# plt.legend()
# plt.ylabel("Inventory Level")
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 25])
plt.title("Warehouse 2 / Demand Range 1-3", fontsize=14)

plt.suptitle("Simulation with Different Stochastic Demands per RW", fontsize=16)
plt.tight_layout(pad=1)
plt.show()

"""
Both after 60000 training steps a 1500 generations
Both with 3 lead time, RW1 with demand range 0-2, RW2 with demand range 1-3
Convegence in both (dont get better with more steps)
A2C
"""
