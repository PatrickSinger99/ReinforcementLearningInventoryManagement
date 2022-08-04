from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import matplotlib.font_manager

print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
matplotlib.font_manager.fontManager.addfont('C:\\Users\\patri\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')
plt.rcParams["font.family"] = "CMU Serif"

warehouse_1 = [0, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 7, 6, 5, 4, 3, 2, 1, 0, 7, 6, 5, 4, 3, 2, 1, 0, 7]
warehouse_2 = [0, 11, 9, 7, 5, 3, 1, 7, 5, 3, 1, 7, 5, 3, 1, 7, 5, 3, 9, 15, 13, 11, 9, 7, 5, 3, 1, 7, 5, 3, 1]
warehouse_3 = [0, 10, 7, 4, 1, 6, 3, 0, 5, 2, 7, 4, 1, 6, 3, 0, 5, 2, 7, 4, 1, 6, 3, 0, 5, 2, 7, 4, 1, 6, 3]

action_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
action_2 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
action_3 = [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1]


def convert_to_marker_pos(action):
    return_list = []
    i = 0
    for entry in action:
        if entry == 1:
            return_list.append(i)
        i += 1
    return return_list


reorder_marker = mlines.Line2D([],[], color='#66C2A5', marker='o', linestyle='None', label="Agent Reorder Point")

plt.rcParams["figure.figsize"] = (10, 4.2)

plt.subplot(1, 3, 1)
plt.plot(warehouse_1, "-bo", label="Reorder point", markevery=convert_to_marker_pos(action_1), color="#66C2A5")
plt.legend(handles=[reorder_marker])
plt.ylabel("Inventory Level")
#plt.xlabel("Round")
plt.xlim([1, 30])
plt.ylim([0, 25])
plt.title("Regional Warehouse 1")

plt.subplot(1, 3, 2)
plt.plot(warehouse_2, "-bo", label="Inventory with demand of 2", markevery=convert_to_marker_pos(action_2), color="#66C2A5")
#plt.legend(handles=[reorder_marker])

plt.xlabel("Simulation Round")
plt.xlim([1, 30])
plt.ylim([0, 25])
plt.title("Regional Warehouse 2")

plt.subplot(1, 3, 3)
plt.plot(warehouse_3, "-bo", label="Inventory with demand of 3", markevery=convert_to_marker_pos(action_3), color="#66C2A5")
#plt.legend(handles=[reorder_marker])

#plt.xlabel("Round")
plt.xlim([1, 30])
plt.ylim([0, 25])
plt.title("Regional Warehouse 3")
plt.suptitle("Simulation with three Regional Warehouses", fontsize=15)
plt.tight_layout(pad=1)
plt.show()

"""
PPO
lead time 2
60000 training steps 
"""
