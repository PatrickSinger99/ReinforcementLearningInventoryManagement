from matplotlib import pyplot as plt

hyperbolic = []
linear = [1]

for i in range(26):
    hyperbolic.append(1/(i + 1))
    linear.append(1-(i+1)/26)
linear.pop(-1)
print(hyperbolic)
print(linear)

plt.plot(hyperbolic, label="Hyperbolic reward function", color="#66C2A5")
plt.plot(linear, label="Linear reward function", linestyle=":", color="#FC8D62")
plt.legend()
plt.ylabel("Reward")
plt.xlabel("Inventory level")
plt.xlim([0, 25])
plt.ylim([0, 1])
plt.title("Comparison of a linear and hyperbolic reward function")
plt.show()
