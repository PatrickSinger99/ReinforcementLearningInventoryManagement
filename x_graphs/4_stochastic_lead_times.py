from matplotlib import pyplot as plt
import matplotlib.font_manager
import matplotlib.lines as mlines

print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
matplotlib.font_manager.fontManager.addfont('C:\\Users\\patri\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')
plt.rcParams["font.family"] = "CMU Serif"

warehouse_1 = [0, 8, 6, 4, 2, 8, 6, 4, 2, 8, 6, 4, 2, 0, 0, 6, 4, 2, 8, 6, 4, 2, 0, 0, 6, 4, 2, 0, 6, 4, 2, 0, 6, 4, 10, 8, 6, 4, 2, 0, 0]

action_1 = [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0]


def convert_to_marker_pos(action):
    return_list = []
    i = 0
    for entry in action:
        if entry == 1:
            return_list.append(i)
        i += 1
    return return_list

reorder_marker = mlines.Line2D([],[], color='#66C2A5', marker='o', linestyle='None', label="Agent Reorder Point")
plt.rcParams["figure.figsize"] = (7, 4.2)

plt.plot(warehouse_1, "-bo", label="Agent reorder point", markevery=convert_to_marker_pos(action_1), color="#66C2A5")
plt.legend(handles=[reorder_marker])
plt.ylabel("Inventory Level", fontsize=11)
plt.xlabel("Simulation Round", fontsize=11)
plt.xlim([1, 40])
plt.ylim([0, 30])
plt.title("Simulation with Stochastic Lead Times / Range 1-3", fontsize=16)

plt.tight_layout(pad=1)
plt.show()

"""
after 30000 training steps
Demand 2, Lead time 1-3
Convegence
PPO
"""
