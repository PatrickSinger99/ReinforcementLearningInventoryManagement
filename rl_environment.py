from simulation.simulation import *
import gym
import numpy as np
from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO2


"""Reinforcement Learning Evironment class"""


class Environment(gym.Env):

    def __init__(self, number_of_regional_wh, rw_inventory_limit, cw_inventory_limit, demand, lead_time, sim_length=50):
        super().__init__()

        # Create distribution network simulation
        self.simulation = Simulation(number_of_regional_wh=number_of_regional_wh,
                                     rw_inventory_limit=rw_inventory_limit,
                                     cw_inventory_limit=cw_inventory_limit,
                                     customer_demand=demand)

        # Two possible actions:
        # Action 0: Dont ship new products
        # Action 1: Ship new products
        self.action_space = gym.spaces.Discrete(2)

        # Observation space is the inventory amount of the regional warehouse
        # Plus 1 because inventory of 0 is a possibility
        self.observation_space = gym.spaces.Discrete(rw_inventory_limit + 1)

        # The state is the current inventory level
        self.state = np.array([self.simulation.get_regional_warehouse_by_id(1).get_inventory_amount()])

        # Number of steps per simulation
        self.sim_length = sim_length
        self.total_steps = self.sim_length

        self.lead_time = lead_time

    def reset(self):
        self.total_steps = self.sim_length

        # Reset simulation
        self.simulation.reset()

        # Returns value that is within observation space
        return self.state[0]

    def step(self, action):
        # Step simulation
        self.simulation.step()

        # Send shipment if action = 1
        if action == 1:
            self.simulation.start_shipment(rw_id=1, amount=5, lead_time=self.lead_time)

        # Dummy reward function
        if self.state[0] == 0:
            reward = -1
        else:
            reward = 1/self.state[0]  # Hyperbel

        # Update state from simulation (Simulation handels demand)
        self.state[0] = self.simulation.get_regional_warehouses()[1].get_inventory_amount()

        # Steps left
        self.total_steps -= 1
        if self.total_steps == 0:
            done = True
        else:
            done = False

        # Write info
        step_info = {"Steps left:": self.total_steps, "Inventory:": self.state[0], "Action:": action,
                     "Reward:": round(reward, 2)}

        return self.state[0], reward, done, step_info


if __name__ == "__main__":

    # Display Q-Values
    """
    action_space_size = env.action_space.n
    state_space_size = env.observation_space.n
    q_table = np.zeros((state_space_size, action_space_size))
    print(q_table)
    """

    # Create and train model
    env = Environment(1, 49, 100, 2, 3)
    model = PPO2(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=100000)

    # Reset environment for simulation
    state = env.reset()
    done = False

    # Run simulation with model
    while not done:
        action, _states = model.predict(state)
        state, reward, done, info = env.step(action)
        print(info)
        # env.simulation.print_state()
