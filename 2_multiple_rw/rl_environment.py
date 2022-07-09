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

        # Two possible actions per warehouse:
        # Action 0: Dont ship new products
        # Action 1: Ship new products
        self.action_space = gym.spaces.MultiDiscrete([2]*number_of_regional_wh)
        print(self.action_space)
        # Observation space is the inventory amount of the regional warehouse
        # Plus 1 because inventory of 0 is a possibility
        self.observation_space = gym.spaces.MultiDiscrete(np.array([rw_inventory_limit + 1]*number_of_regional_wh))
        print(self.observation_space)

        # The state is the current inventory level
        state_list = []
        for rw_id in self.simulation.get_regional_warehouses():
            state_list.append(self.simulation.get_regional_warehouse_by_id(rw_id).get_inventory_amount())
        self.state = np.array(state_list)
        print(self.state)

        # Number of steps per simulation
        self.sim_length = sim_length
        self.total_steps = self.sim_length

        # Simulation parameters
        self.lead_time = lead_time
        self.number_of_rw = number_of_regional_wh

        # Values for final evaluation
        self.total_lost_sales = 0
        self.total_reward_gained = 0
        self.total_shipments = 0

        self.total_reward = []

    def reset(self):
        self.total_steps = self.sim_length

        # Reset simulation
        self.simulation.reset()

        self.total_reward.append(self.total_reward_gained)

        # Reset values for final evaluation
        self.total_lost_sales = 0
        self.total_reward_gained = 0
        self.total_shipments = 0

        # Returns value that is within observation space
        return np.array([0]*self.number_of_rw)

    def step(self, action):
        # Step simulation
        self.simulation.step()

        # Send shipment if action = 1
        if action[0] == 1:
            self.simulation.start_shipment(rw_id=1, amount=5, lead_time=self.lead_time)
            self.total_shipments += 1

        # Update state from simulation (Simulation handels demand)
        for rw in self.simulation.get_regional_warehouses():
            self.state[rw - 1] = self.simulation.get_regional_warehouse_by_id(rw).get_inventory_amount()

        # Dummy reward function
        if self.simulation.get_regional_warehouse_by_id(1).get_lost_sales_last_round() != 0:
            reward = -1
        elif self.state[0] == 0:
            reward = 1
        else:
            reward = 1/(self.state[0] + 1)  # Hyperbel

        # Count up eval parameters
        self.total_reward_gained += reward
        self.total_lost_sales += self.simulation.get_regional_warehouse_by_id(1).get_lost_sales_last_round()

        # Steps left
        self.total_steps -= 1
        if self.total_steps == 0:
            done = True
        else:
            done = False

        # Write info
        step_info = {"Steps left:": self.total_steps, "Inventory:": self.state[0], "Action:": action,
                     "Reward:": round(reward, 2)}

        return self.state, reward, done, step_info

    def evaluation_parameters(self):
        return {"total_shipments": self.total_shipments,
                "total_lost_sales": self.total_lost_sales,
                "total_reward_gained": round(self.total_reward_gained, 2)}


if __name__ == "__main__":

    # Display Q-Values
    """
    action_space_size = env.action_space.n
    state_space_size = env.observation_space.n
    q_table = np.zeros((state_space_size, action_space_size))
    print(q_table)
    """

    # Create and train model
    env = Environment(2, 49, 100, 1, 2)
    model = PPO2(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=30000)
    
    # Reset environment for simulation
    state = env.reset()
    done = False

    # Run simulation with model
    while not done:
        action, _states = model.predict(state)
        state, reward, done, info = env.step(action)
        print(info)
        print(env.simulation.print_state())
        # env.simulation.print_state()