from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import matplotlib.font_manager

print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
matplotlib.font_manager.fontManager.addfont('C:\\Users\\patri\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')
plt.rcParams["font.family"] = "CMU Serif"

warehouse_1 = [0, 14, 12, 10, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6]
warehouse_2 = [0, 12, 8, 4, 0, 6, 2, 8, 4, 0, 6, 2, 8, 4, 0, 6, 2, 8, 4, 0, 6, 2, 8, 4, 0, 6, 2, 8, 4, 0, 6, 2, 8, 4, 0, 6, 2, 8, 4, 0, 6, 2, 8, 4, 0, 6, 2, 8, 4, 0, 6]
warehouse_3 = [0, 13, 10, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
warehouse_cw = [0, 33, 33, 23, 13, 3, 28, 8, 23, 23, 38, 28, 18, 33, 23, 13, 38, 18, 8, 8, 23, 38, 53, 43, 33, 23, 23, 3, 18, 18, 33, 23, 13, 28, 18, 8, 33, 13, 3, 3, 18, 33, 48, 38, 28, 43, 43, 23, 13, 13, 28]
manufacturer = [0, 81, 96, 111, 101, 116, 106, 121, 111, 126, 141, 131, 146, 161, 151, 166, 181, 196, 175, 165, 155, 170, 185, 200, 200, 200, 175, 190, 175, 190, 200, 175, 190, 200, 175, 190, 200, 200, 175, 165, 155, 170, 185, 175, 190, 200, 200, 200, 175, 165, 155]

action_1 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]
action_2 = [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
action_3 = [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
action_cw = [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1]


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

plt.subplot2grid((2, 6), (0, 0), colspan=2)
plt.plot(warehouse_1, "-bo", label="RW 1", markevery=convert_to_marker_pos(action_1), color="#66C2A5")
plt.legend(handles=[reorder_marker])
plt.ylabel("Inventory Level", fontsize=11)
# plt.xlabel("Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 25])
plt.title("Regional Warehouse 1", fontsize=14)

plt.subplot2grid((2, 6), (0, 2), colspan=2)
plt.plot(warehouse_2, "-bo", label="RW 2", markevery=convert_to_marker_pos(action_2), color="#66C2A5")
# plt.legend(handles=[reorder_marker])
# plt.ylabel("Inventory Level")
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 25])
plt.title("Regional Warehouse 2", fontsize=14)

plt.subplot2grid((2, 6), (0, 4), colspan=2)
plt.plot(warehouse_3, "-bo", label="RW 3", markevery=convert_to_marker_pos(action_3), color="#66C2A5")
# plt.legend(handles=[reorder_marker])
# plt.ylabel("Inventory Level")
# plt.xlabel("Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 25])
plt.title("Regional Warehouse 3", fontsize=14)

plt.subplot2grid((2, 6), (1, 0), colspan=3)
plt.plot(warehouse_cw, "-bo", label="CW", markevery=convert_to_marker_pos(action_cw), color="#FC8D62")
plt.legend(handles=[reorder_marker_cw])
plt.ylabel("Inventory Level", fontsize=11)
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 100])
plt.title("Central Warehouse", fontsize=14)

plt.subplot2grid((2, 6), (1, 3), colspan=3)
plt.plot(manufacturer, label="Manufacturer", color="#8DA0CB")
# plt.ylabel("Inventory Level")
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 200])
plt.title("Manufacturer", fontsize=14)


plt.suptitle("Simulation with Multiple Regional Warehouses and Manufacturer", fontsize=16)
plt.tight_layout(pad=1)
plt.show()

"""
PPO
lead time 2
100000 training steps 
"""
