from simulation.simulation import *
import gym
import numpy as np
from stable_baselines3 import PPO
import random
import itertools


"""Reinforcement Learning Evironment class"""


class Environment(gym.Env):

    def __init__(self, number_of_regional_wh, rw_inventory_limit, cw_inventory_limit, demand, lead_time,
                 shipment_amount, cw_shipment_amount, manufacturer, mf_prod_capacity, shipment_var_cost_per_unit,
                 shipment_fixed_cost, inventory_holding_cost_multiplier, demand_fluctuation, lead_time_fluctuation,
                 cw_inventory_holding_cost_multiplier, customer_priorities, use_single_value_action_space=False,
                 sim_length=50):

        # Initiate gym.Env
        super().__init__()

        # Create distribution network simulation
        self.simulation = Simulation(number_of_regional_wh=number_of_regional_wh,
                                     rw_inventory_limit=rw_inventory_limit,
                                     cw_inventory_limit=cw_inventory_limit,
                                     customer_demand=demand,
                                     manufacturer=manufacturer,
                                     manufacturer_production_capacity=mf_prod_capacity,
                                     demand_fluctuation=demand_fluctuation,
                                     customer_priorities=customer_priorities)

        # Creation of action space
        # Per warehouse the number of action depends on the nuber of possible shipment amounts
        action_space = [len(shipment_amount)+1]*number_of_regional_wh
        if manufacturer:
            action_space += [2]

        # Convert to single action value if use_single_value_action_space is true
        if not use_single_value_action_space:
            self.action_space = gym.spaces.MultiDiscrete(action_space)
        else:
            self.action_conversion_dict = self.create_actions_conversion_dict(action_space)
            self.action_space = gym.spaces.Discrete(len(self.action_conversion_dict))

        # Observation space is the inventory amount of the regional warehouse
        obs_space = {
            # Inventory state of every regional warehouse (Plus 1 to size 1 because inventory of 0 is a possibility)
            "rw_inventories": gym.spaces.MultiDiscrete(np.array([rw_inventory_limit + 1]*number_of_regional_wh)),
            "next_arrival": gym.spaces.MultiDiscrete(np.array([lead_time + 1 + lead_time_fluctuation]*number_of_regional_wh)),
            "rw_amount_in_transit": gym.spaces.MultiDiscrete(np.array([max(shipment_amount) * (lead_time + lead_time_fluctuation) + 1] * number_of_regional_wh))
        }
        if manufacturer:
            # Inventory state of the central warehouse
            obs_space["cw_inventory"] = gym.spaces.Discrete(cw_inventory_limit + 1)
            obs_space["cw_next_arrival"] = gym.spaces.Discrete(lead_time + 1)
            obs_space["cw_amount_in_transit"] = gym.spaces.Discrete(cw_shipment_amount * (lead_time + lead_time_fluctuation) + 1)

        self.observation_space = gym.spaces.Dict(obs_space)

        # Number of steps per simulation
        self.sim_length = sim_length
        self.total_steps = self.sim_length
        self.current_round = 1

        # Simulation parameters
        self.lead_time = lead_time
        self.number_of_rw = number_of_regional_wh
        self.shipment_amount = shipment_amount
        self.cw_shipment_amount = cw_shipment_amount
        self.manufacturer = manufacturer
        self.shipment_var_cost_per_unit = shipment_var_cost_per_unit
        self.shipment_fixed_cost = shipment_fixed_cost
        self.inventory_holding_cost_multiplier = inventory_holding_cost_multiplier
        self.cw_inventory_holding_cost_multiplier = cw_inventory_holding_cost_multiplier
        self.lead_time_fluctuation = lead_time_fluctuation
        self.use_single_value_action_space = use_single_value_action_space

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
        rw_next_arrival_state_list = [0]*self.number_of_rw
        rw_total_amount_on_way_state_list = [0]*self.number_of_rw

        for rw_id in self.simulation.get_regional_warehouses():
            rw_inv_state_list.append(self.simulation.get_regional_warehouse_by_id(rw_id).get_inventory_amount())

            # Check shipments
            for active_shipments in self.simulation.get_all_active_shipments():
                if active_shipments["regional_warehouse"] == rw_id:
                    rw_total_amount_on_way_state_list[rw_id-1] += active_shipments["amount"]

                    # Check arrival
                    possible_next_shipment = active_shipments["arrival"] - self.simulation.get_round()
                    if rw_next_arrival_state_list[rw_id-1] == 0:
                        rw_next_arrival_state_list[rw_id-1] = possible_next_shipment
                    elif rw_next_arrival_state_list[rw_id-1] > possible_next_shipment:
                        rw_next_arrival_state_list[rw_id-1] = possible_next_shipment

        # Concat all components to list
        current_state = {"rw_inventories": np.array(rw_inv_state_list),
                         "next_arrival": np.array(rw_next_arrival_state_list),
                         "rw_amount_in_transit": np.array(rw_total_amount_on_way_state_list)
                         }

        if self.manufacturer:
            cw_next_arrival_state = 0
            cw_total_amount_in_transit = 0

            # np.intc used because DQN algorithm needs .space method not included in regular ints
            current_state["cw_inventory"] = np.intc(self.simulation.get_central_warehouse().get_inventory_amount())

            # Arrival date for cw shipments
            for shipment in self.simulation.get_all_active_cw_shipments():
                cw_total_amount_in_transit += shipment["amount"]

                possible_next_shipment = shipment["arrival"] - self.simulation.get_round()
                if cw_next_arrival_state == 0:
                    cw_next_arrival_state = possible_next_shipment
                elif cw_next_arrival_state > possible_next_shipment:
                    cw_next_arrival_state = possible_next_shipment

            current_state["cw_next_arrival"] = np.intc(cw_next_arrival_state)
            current_state["cw_amount_in_transit"] = np.intc(cw_total_amount_in_transit)

        return current_state

    def print_environment_information(self):
        print("Environment Information")
        print("-----------------------")
        print("-> Gym spaces:")
        print("Observation space:", self.observation_space)
        print("Action space:", self.action_space)
        print("Starting state:", self.state)
        print("\n-> Reward penalty per shipment size:")
        for size in self.shipment_amount:
            print("Shipment of " + str(size) + ": " +
                  str(round(self.shipment_fixed_cost + size * self.shipment_var_cost_per_unit, 2)))
        print("_"*80)  # Separator

    def create_actions_conversion_dict(self, action_space):
        actions_as_lists = []

        for entry in action_space:
            new_list = []
            for pos in range(entry):
                new_list.append(pos)
            actions_as_lists.append(new_list)

        actions_dict = {}
        all_pos_action_comb = list(itertools.product(*actions_as_lists))

        count = 0
        for action_combination in all_pos_action_comb:
            actions_dict[count] = list(action_combination)
            count += 1

        return actions_dict

    def convert_discrete_to_multi_discrete(self, discrete_action):
        return self.action_conversion_dict[discrete_action]

    def convert_nulti_discrete_to_discrete(self, multi_discrete_action):
        for entry in self.action_conversion_dict:
            if self.action_conversion_dict[entry] == multi_discrete_action:
                return entry

    def reset(self):
        self.total_steps = self.sim_length
        self.current_round = 1

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

        # convert single action value to multi
        if self.use_single_value_action_space:
            # print("Converted", action, "to", end=" ")
            if type(action) != int:
                action = action.item()
            action = self.convert_discrete_to_multi_discrete(action)
            # print(action)
        else:
            # Change action np array to list
            action = action.tolist()

        # Step simulation
        self.simulation.step()


        # For every RW, send shipment if action = 1
        for rw_id in self.simulation.get_regional_warehouses():
            if action[rw_id - 1] != 0:
                self.simulation.start_shipment(rw_id=rw_id, amount=self.shipment_amount[action[rw_id - 1]-1],
                                               lead_time=self.get_lead_time_with_fluctuation())
                self.total_shipments += 1

        # Shipment action for cw
        if self.simulation.get_manufacturer():
            if action[-1] == 1:
                self.simulation.start_cw_shipment(amount=self.cw_shipment_amount,
                                                  lead_time=self.get_lead_time_with_fluctuation())
                self.total_shipments += 1

        # Update state from simulation (Simulation handels demand)
        self.state = self.get_state()

        # Reward function based on inventory amount
        reward = 0
        # Check RWs
        for rw_id in self.simulation.get_regional_warehouses():
            if self.simulation.get_regional_warehouse_by_id(rw_id).get_lost_sales_last_round() != 0:
                # Negative reward based on the priorization of the RW customer
                rw_reward = -self.simulation.get_regional_warehouse_by_id(rw_id).get_customer().get_priority()
            else:
                rw_reward = self.inventory_holding_cost_multiplier/(self.state["rw_inventories"][rw_id - 1] + 1)  # Hyperbel

                # Shipping cost
                if action[rw_id - 1] != 0:
                    rw_reward -= self.shipment_fixed_cost + \
                                 self.shipment_amount[action[rw_id - 1]-1] * self.shipment_var_cost_per_unit
                    if rw_reward < -1:
                        rw_reward = -1

            reward += rw_reward

        # Check CW if manufacturer is enabled
        if self.simulation.get_manufacturer():
            reward += self.cw_inventory_holding_cost_multiplier/(self.state["cw_inventory"] + 1)

        # Calculate combined reward
        if self.simulation.get_manufacturer():
            reward /= self.number_of_rw + 1
        else:
            reward /= self.number_of_rw

        # Count up eval parameters
        self.total_reward_gained += reward
        for rw_id in self.simulation.get_regional_warehouses():
            self.total_lost_sales += self.simulation.get_regional_warehouse_by_id(rw_id).get_lost_sales_last_round()

        # Steps left
        self.total_steps -= 1
        if self.total_steps == 0:
            done = True
        else:
            done = False

        # Write info
        step_info = {"Round:": self.current_round, "RW Invs:": self.state["rw_inventories"].tolist(), "Shipments": self.state["rw_amount_in_transit"].tolist(),
                     "Action:": action, "Reward:": round(reward, 2)}

        if self.simulation.get_manufacturer():
            step_info["CW Inv:"] = self.state["cw_inventory"]
            step_info["Manufacturer:"] = self.simulation.get_manufacturer().get_inventory_amount()

        self.current_round += 1

        return self.state, reward, done, step_info

    def get_lead_time_with_fluctuation(self):
        new_lead_time = random.randint(self.lead_time - self.lead_time_fluctuation,
                                       self.lead_time + self.lead_time_fluctuation)
        if new_lead_time < 1:
            new_lead_time = 1

        return new_lead_time

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
