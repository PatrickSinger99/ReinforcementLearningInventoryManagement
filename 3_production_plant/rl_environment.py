from simulation.simulation import *
import gym
import numpy as np
#from stable_baselines.common.policies import MlpPolicy
from stable_baselines3 import PPO


"""Reinforcement Learning Evironment class"""


class Environment(gym.Env):

    def __init__(self, number_of_regional_wh, rw_inventory_limit, cw_inventory_limit, demand, lead_time,
                 shipment_amount, manufacturer=False, sim_length=50):
        super().__init__()

        # Create distribution network simulation
        self.simulation = Simulation(number_of_regional_wh=number_of_regional_wh,
                                     rw_inventory_limit=rw_inventory_limit,
                                     cw_inventory_limit=cw_inventory_limit,
                                     customer_demand=demand,
                                     manufacturer=manufacturer)

        # Two possible actions per warehouse:
        # Action 0: Dont ship new products
        # Action 1: Ship new products
        self.action_space = gym.spaces.MultiDiscrete([2]*number_of_regional_wh)

        # Observation space is the inventory amount of the regional warehouse
        # Plus 1 because inventory of 0 is a possibility
        self.observation_space = gym.spaces.MultiDiscrete(np.array([rw_inventory_limit + 1]*number_of_regional_wh))

        # The state is the current inventory level
        state_list = []
        for rw_id in self.simulation.get_regional_warehouses():
            state_list.append(self.simulation.get_regional_warehouse_by_id(rw_id).get_inventory_amount())
        self.state = np.array(state_list)

        # Number of steps per simulation
        self.sim_length = sim_length
        self.total_steps = self.sim_length

        # Simulation parameters
        self.lead_time = lead_time
        self.number_of_rw = number_of_regional_wh
        self.shipment_amount = shipment_amount

        # Values for final evaluation
        self.total_lost_sales = 0
        self.total_reward_gained = 0
        self.total_shipments = 0

        self.total_reward = []

    def print_environment_information(self):
        print("Environment Information")
        print("-----------------------")
        print("Observation space:", self.observation_space)
        print("Action space:", self.action_space)
        print("Starting state:", self.state)
        print("_"*80)  # Separator

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

        # For every RW, send shipment if action = 1
        for rw_id in self.simulation.get_regional_warehouses():
            if action[rw_id - 1] == 1:
                self.simulation.start_shipment(rw_id=rw_id, amount=self.shipment_amount, lead_time=self.lead_time)
                self.total_shipments += 1

        # Update state from simulation (Simulation handels demand)
        for rw_id in self.simulation.get_regional_warehouses():
            self.state[rw_id - 1] = self.simulation.get_regional_warehouse_by_id(rw_id).get_inventory_amount()

        # Reward function based on inventory amount
        reward = 0
        for rw_id in self.simulation.get_regional_warehouses():
            if self.simulation.get_regional_warehouse_by_id(rw_id).get_lost_sales_last_round() != 0:
                rw_reward = -1
            elif self.state[rw_id - 1] == 0:  # elif necessary because cannot divide through zero
                rw_reward = 1
            else:
                rw_reward = 1/(self.state[rw_id - 1] + 1)  # Hyperbel
            reward += rw_reward
        reward /= self.number_of_rw

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
        step_info = {"Steps left:": self.total_steps, "Inventory:": self.state, "Action:": action,
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
    env = Environment(number_of_regional_wh=1,
                      rw_inventory_limit=49,
                      cw_inventory_limit=100,
                      demand=[1],
                      lead_time=2,
                      shipment_amount=10,
                      manufacturer=True)

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    
    # Reset environment for simulation
    state = env.reset()
    done = False

    # Run simulation with model
    while not done:
        action, _states = model.predict(state)
        state, reward, done, info = env.step(action)
        print(info)
        # env.simulation.print_state()
