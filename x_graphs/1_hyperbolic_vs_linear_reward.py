from matplotlib import pyplot as plt
import numpy as np
import matplotlib.font_manager

print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))
matplotlib.font_manager.fontManager.addfont('C:\\Users\\patri\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')
plt.rcParams["font.family"] = "CMU Serif"

hyperbolic = []
linear = [1]

for i in range(26):
    hyperbolic.append(1/(i + 1))
    linear.append(1-(i+1)/26)
linear.pop(-1)
print(hyperbolic)
print(linear)

x = np.linspace(0, 25, 250)

hyperbolic = 1/(x+1)
print(hyperbolic)
plt.rcParams["figure.figsize"] = (10, 4.2)


plt.subplot(1, 2, 1)
plt.plot(x, hyperbolic, label="Hyperbolic", color="#66C2A5")
plt.plot(linear, label="Linear", color="#FC8D62")
plt.legend()
plt.ylabel("Reward", fontsize=11)
plt.xlabel("Inventory Level", fontsize=11)
plt.xlim([0, 25])
plt.ylim([0, 1])
plt.title("Reward Function", fontsize=14)

plt.subplot(1, 2, 2)

hyperbolic = [7, 6, 5, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3]
linear = [7, 6, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 10, 9, 8, 7, 11, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 2, 1, 0, 4, 8]

plt.plot(linear, label="With Linear Reward Function", color="#FC8D62")
plt.plot(hyperbolic, label="With Hyperbolic Reward Function", color="#66C2A5")

plt.legend()
plt.ylabel("Inventory level", fontsize=11)
plt.xlabel("Step", fontsize=11)
plt.xlim([0, 60])
plt.ylim([0, 25])
plt.title("Agent Decision Making", fontsize=14)

plt.suptitle("Comparison of a Linear and Hyperbolic Reward Function", fontsize=16)
plt.tight_layout(pad=1)
plt.show()

"""
Both after 50000 training steps a 800 generations
Both with 2 lead time, 1 demand per step
Convegence in both (dont get better with more steps)
"""
