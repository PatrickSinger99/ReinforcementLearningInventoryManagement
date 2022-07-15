from simulation.simulation import *
import gym
import numpy as np
from stable_baselines3 import PPO


"""Reinforcement Learning Evironment class"""


class Environment(gym.Env):

    def __init__(self, number_of_regional_wh, rw_inventory_limit, cw_inventory_limit, demand, lead_time,
                 shipment_amount, cw_shipment_amount, manufacturer, mf_prod_capacity, max_min_price_per_unit,
                 price_multiplier, sim_length=50):
        super().__init__()

        # Create distribution network simulation
        self.simulation = Simulation(number_of_regional_wh=number_of_regional_wh,
                                     rw_inventory_limit=rw_inventory_limit,
                                     cw_inventory_limit=cw_inventory_limit,
                                     customer_demand=demand,
                                     manufacturer=manufacturer,
                                     manufacturer_production_capacity=mf_prod_capacity)

        # Creation of action space
        # Per warehouse the number of action depends on the nuber of possible shipment amounts
        action_space = [len(shipment_amount)+1]*number_of_regional_wh
        if manufacturer:
            action_space += [2]

        self.action_space = gym.spaces.MultiDiscrete(action_space)

        # Observation space is the inventory amount of the regional warehouse
        obs_space = {
            # Inventory state of every regional warehouse (Plus 1 to size 1 because inventory of 0 is a possibility)
            "rw_inventories": gym.spaces.MultiDiscrete(np.array([rw_inventory_limit + 1]*number_of_regional_wh)),
            "shipments": gym.spaces.MultiDiscrete(np.array([2]*number_of_regional_wh))
        }
        if manufacturer:
            # Inventory state of the central warehouse
            obs_space["cw_inventory"] = gym.spaces.Discrete(cw_inventory_limit + 1)

        self.observation_space = gym.spaces.Dict(obs_space)

        # Number of steps per simulation
        self.sim_length = sim_length
        self.total_steps = self.sim_length

        # Simulation parameters
        self.lead_time = lead_time
        self.number_of_rw = number_of_regional_wh
        self.shipment_amount = shipment_amount
        self.cw_shipment_amount = cw_shipment_amount
        self.manufacturer = manufacturer
        self.max_min_price_per_unit = max_min_price_per_unit
        self.price_multiplier = price_multiplier

        # Set initial state
        self.state = self.get_state()

        # Values for final evaluation
        self.total_lost_sales = 0
        self.total_reward_gained = 0
        self.total_shipments = 0

        self.total_reward = []

    def get_state(self):
        # Build state component regional warehouse inventories
        rw_inv_state_list = []
        rw_shipment_state_list = []
        for rw_id in self.simulation.get_regional_warehouses():
            rw_inv_state_list.append(self.simulation.get_regional_warehouse_by_id(rw_id).get_inventory_amount())

            # Check shipments
            found_shipment = False
            for active_shipments in self.simulation.get_all_active_shipments():
                if active_shipments["regional_warehouse"] == rw_id:
                    rw_shipment_state_list.append(1)
                    found_shipment = True
                    break
            if not found_shipment:
                rw_shipment_state_list.append(0)

        # Concat all components to list
        current_state = {"rw_inventories": np.array(rw_inv_state_list),
                         "shipments": np.array(rw_shipment_state_list)
                         }

        if self.manufacturer:
            current_state["cw_inventory"] = self.simulation.get_central_warehouse().get_inventory_amount()

        return current_state

    def calc_price_per_unit(self, amount):
        if len(self.shipment_amount) > 1:
            max_price = self.max_min_price_per_unit[0]
            min_price = self.max_min_price_per_unit[1]
            max_amount = max(self.shipment_amount)

            return round(max_price - (amount - 1) * ((max_price - min_price) / (max_amount - 1)), 2)

        else:
            return 1

    def print_environment_information(self):
        print("Environment Information")
        print("-----------------------")
        print("Observation space:", self.observation_space)
        print("Action space:", self.action_space)
        print("Starting state:", self.state)
        print("Reward penalty per unit shipped:")
        print("Max = " + str(round(self.max_min_price_per_unit[0]*self.price_multiplier, 2)))
        print("Min = " + str(round(self.max_min_price_per_unit[1]*self.price_multiplier, 2)))
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
        return self.get_state()

    def step(self, action):
        # Change action np array to list
        action = action.tolist()

        # Step simulation
        self.simulation.step()

        # For every RW, send shipment if action = 1
        for rw_id in self.simulation.get_regional_warehouses():
            if action[rw_id - 1] != 0:
                self.simulation.start_shipment(rw_id=rw_id, amount=self.shipment_amount[action[rw_id - 1]-1], lead_time=self.lead_time)
                self.total_shipments += 1

        # Shipment action for cw
        if self.simulation.get_manufacturer():
            if action[-1] == 1:
                self.simulation.start_cw_shipment(amount=self.cw_shipment_amount, lead_time=self.lead_time)
                self.total_shipments += 1

        # Update state from simulation (Simulation handels demand)
        self.state = self.get_state()

        # Reward function based on inventory amount
        reward = 0
        # Check RWs
        for rw_id in self.simulation.get_regional_warehouses():
            if self.simulation.get_regional_warehouse_by_id(rw_id).get_lost_sales_last_round() != 0:
                rw_reward = -1
            else:
                rw_reward = 1/(self.state["rw_inventories"][rw_id - 1] + 1)  # Hyperbel

                # Shipping cost
                if action[rw_id - 1] != 0:
                    print("lost:", self.price_multiplier * self.shipment_amount[action[rw_id - 1]-1] * self.calc_price_per_unit(self.shipment_amount[action[rw_id - 1]-1]))
                    rw_reward -= self.price_multiplier * self.shipment_amount[action[rw_id - 1]-1] * self.calc_price_per_unit(self.shipment_amount[action[rw_id - 1]-1])
                    if rw_reward < -1:
                        rw_reward = -1

            reward += rw_reward

        # Check CW if manufacturer is enabled
        if self.simulation.get_manufacturer():
            reward += .25/(self.state["cw_inventory"] + 1)

        # Calculate combined reward
        if self.simulation.get_manufacturer():
            reward /= self.number_of_rw + 1
        else:
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
        step_info = {"Steps left:": self.total_steps, "RW Invs:": self.state["rw_inventories"].tolist(), "Shipments": self.state["shipments"].tolist(),
                     "Action:": action, "Reward:": round(reward, 2)}

        if self.simulation.get_manufacturer():
            step_info["CW Inv:"] = self.state["cw_inventory"]
            step_info["Manufacturer:"] = self.simulation.get_manufacturer().get_inventory_amount()

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
                      manufacturer=True,
                      cw_shipment_amount=10,
                      mf_prod_capacity=10)

    model = PPO("MultiInputPolicy", env, verbose=1)
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
