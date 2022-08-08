from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import matplotlib.font_manager

print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
matplotlib.font_manager.fontManager.addfont('C:\\Users\\patri\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')
plt.rcParams["font.family"] = "CMU Serif"

warehouse_1 = [0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0]
warehouse_2 = [0, 7, 4, 1, 8, 5, 12, 9, 6, 3, 0, 0, 0, 7, 4, 1, 0, 0, 0, 0, 0, 0, 7, 4, 1, 0, 0, 0, 0, 0, 0, 0, 7, 4, 1, 0, 0, 0, 0, 0, 0]
warehouse_cw = [0, 20, 10, 20, 0, 0, 0, 0, 10, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
manufacturer = [0, 0, 3, 6, 9, 12, 5, 8, 1, 4, 7, 10, 3, 6, 9, 12, 15, 8, 1, 4, 7, 0, 3, 6, 9, 12, 15, 8, 1, 4, 7, 10, 3, 6, 9, 12, 15, 8, 1, 4, 7]

action_1 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
action_2 = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
action_2_without_removed = [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
action_cw = [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0]


def convert_to_marker_pos(action):
    return_list = []
    i = 0
    for entry in action:
        if entry == 1:
            return_list.append(i)
        i += 1
    return return_list


reorder_marker = mlines.Line2D([], [], color='#66C2A5', marker='o', linestyle='None', label="Agent Reorder Point")
reorder_marker_cw = mlines.Line2D([], [], color='#FC8D62', marker='o', linestyle='None', label="Agent Reorder Point")

plt.rcParams["figure.figsize"] = (10, 6)

plt.subplot(2, 2, 1)
plt.plot(warehouse_1, "-bo", label="RW 1", markevery=convert_to_marker_pos(action_1), color="#66C2A5")
plt.legend(handles=[reorder_marker])
plt.ylabel("Inventory Level", fontsize=11)
# plt.xlabel("Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 25])
plt.title("Regional Warehouse 1", fontsize=14)

plt.subplot(2, 2, 2)
plt.plot(warehouse_2, "-bo", label="RW 2", markevery=convert_to_marker_pos(action_2_without_removed), color="#66C2A5")
# plt.legend(handles=[reorder_marker])
# plt.ylabel("Inventory Level")
# plt.xlabel("Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 25])
plt.title("Regional Warehouse 2", fontsize=14)

plt.subplot(2, 2, 3)
plt.plot(warehouse_cw, label="CW", color="#FC8D62")
# plt.legend(handles=[reorder_marker_cw])
plt.ylabel("Inventory Level", fontsize=11)
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([-1, 40])
plt.title("Central Warehouse", fontsize=14)

plt.subplot(2, 2, 4)
plt.plot(manufacturer, label="Manufacturer", color="#8DA0CB")
# plt.ylabel("Inventory Level")
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 40])
plt.title("Manufacturer", fontsize=14)


plt.suptitle("Simulation with Production Deficit and RW Prioritization", fontsize=16)
plt.tight_layout(pad=1)
plt.show()

"""
PPO
lead time 2
100000 training steps 
"""
