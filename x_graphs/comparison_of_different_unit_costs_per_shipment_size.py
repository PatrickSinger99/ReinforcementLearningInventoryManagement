from matplotlib import pyplot as plt

low_fix, high_fix = .25, .5
high_var, low_var = .05, .02

option_1 = []
option_2 = []

for i in range(26):
    option_1.append(low_fix + high_var*(i+1))
    option_2.append(high_fix + low_var*(i+1))

print(option_1)
print(option_2)

plt.rcParams["figure.figsize"] = (10, 4.2)

plt.subplot(1, 2, 1)
plt.plot(option_1, label="Szenario 1: Low Fixed Costs / High Variable Costs", color="#66C2A5")
plt.plot(option_2, label="Szenario 2: High Fixed Costs / Low Variable Costs", color="#FC8D62")
plt.legend()
plt.ylabel("Reward Penalty")
plt.xlabel("Shipment Amount")
plt.xlim([0, 15])
plt.ylim([0, 1.5])
plt.title("Shiping Costs")

plt.subplot(1, 2, 2)

option_1 = [0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0, 8, 6, 4, 2, 0]
option_2 = [0, 8, 6, 4, 2, 0, 4, 2, 0, 4, 2, 0, 4, 2, 0, 4, 2, 0, 4, 2, 0, 4, 2, 0, 4, 2]
# [8, 6, 4, 2, 0, 10, 8, 6, 4, 2, 0, 10, 8, 6, 4, 2, 0, 10, 8, 6, 4, 2, 0, 10, 8]
plt.plot(option_1, label="Szenario 1: Low Fixed Costs / High Variable Costs", color="#66C2A5", linewidth=2)
plt.plot(option_2, label="Szenario 2: High Fixed Costs / Low Variable Costs", color="#FC8D62", linewidth=2)
plt.legend()
plt.ylabel("Inventory level")
plt.xlabel("Step")
plt.xlim([1, 25])
plt.ylim([0, 25])
plt.title("Agent Decision Making")

plt.suptitle("Comparison of Different Shipping Cost Allocations", fontsize=15)
plt.tight_layout(pad=1)
plt.show()

"""
Both after 50000 training steps a 2000 generations
Both with 2 lead time, 2 demand per step
inventory_holding_cost_multiplier of .5
Options for shipment size of 4 or 10
Convegence in both (dont get better with more steps)
"""
