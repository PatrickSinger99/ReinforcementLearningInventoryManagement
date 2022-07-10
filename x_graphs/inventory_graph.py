from matplotlib import pyplot as plt

hyperbolic = [7, 6, 5, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3]
linear = [7, 6, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 10, 9, 8, 7, 11, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 7, 6, 10, 9, 8, 7, 6, 5, 4, 3, 7, 6, 5, 4, 3, 2, 1, 0, 4, 8]


plt.plot(hyperbolic, label="Hyperbolic reward function", color="#66C2A5")
plt.plot(linear, label="Linear reward function", linestyle=":", color="#FC8D62")
plt.legend()
plt.ylabel("Reward")
plt.xlabel("Inventory level")
plt.xlim([0, 60])
plt.ylim([0, 25])
plt.title("Comparison of a linear and hyperbolic reward function")
plt.show()

"""
Both after 50000 training steps a 800 generations
Both with 2 lead time, 1 demand per step
Convegence in both (dont get better with more steps)
"""