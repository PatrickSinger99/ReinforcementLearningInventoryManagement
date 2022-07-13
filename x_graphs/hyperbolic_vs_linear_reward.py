from matplotlib import pyplot as plt

hyperbolic = []
linear = [1]

for i in range(26):
    hyperbolic.append(1/(i + 1))
    linear.append(1-(i+1)/26)
linear.pop(-1)
print(hyperbolic)
print(linear)

plt.rcParams["figure.figsize"] = (10, 4.2)

plt.subplot(1, 2, 1)
plt.plot(hyperbolic, "-bo", label="Hyperbolic Reward Function", color="#66C2A5")
plt.plot(linear, "--bo", label="Linear Reward Function", linestyle=":", color="#FC8D62")
plt.legend()
plt.ylabel("Reward")
plt.xlabel("Inventory level")
plt.xlim([0, 25])
plt.ylim([0, 1])
plt.title("Reward Function")

plt.subplot(1, 2, 2)

hyperbolic = [7, 6, 5, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3]
linear = [7, 6, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 10, 9, 8, 7, 11, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 2, 1, 0, 4, 8]


plt.plot(hyperbolic, label="With Hyperbolic Reward", color="#66C2A5", linewidth=2)
plt.plot(linear, label="With Linear Reward", linestyle=":", color="#FC8D62", linewidth=2)
plt.legend()
plt.ylabel("Inventory level")
plt.xlabel("Step")
plt.xlim([0, 60])
plt.ylim([0, 25])
plt.title("Agent Decision Making")

plt.suptitle("Comparison of a Linear and Hyperbolic Reward Function", fontsize=15)
plt.tight_layout(pad=1)
plt.show()

"""
Both after 50000 training steps a 800 generations
Both with 2 lead time, 1 demand per step
Convegence in both (dont get better with more steps)
"""
