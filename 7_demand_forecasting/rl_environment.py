from simulation.simulation import *
import gym
import numpy as np
import random
import itertools


"""
Environment class
-----------------
@ number_of_regional_wh = Number of regional warehouses that will be simulated
@ rw_inventory_limit = The maximum amout of stock a regional warehouse can hold
@ cw_inventory_limit = The maximum amout of stock the central warehouse can hold
@ demand = List of demand values per RW. Needs one entry per RW
@ lead_time = Number of steps it takes a shipment to arrive at its destination
@ shipment_amount = List of possible shipment sizes that can be initiated
@ cw_shipment_amount = Shipment size of a shipment from the manufacturer to the CW
@ manufacturer = Determines, if a manufacturer and CW inventory depletion is simulated
@ mf_production_capacity = amount of product a MF can produce per round
@ shipment_var_cost_per_unit = Cost per product shipped. Will be multiplied by shipment size
@ shipment_fixed_cost = Fixed cost of one shipment. Not dependend on shipment size
@ inventory_holding_cost_multiplier = Determines the maximum reward a RW inventory can generate (Applied to all RWs)
@ demand_fluctuation = Determines the range the demand will fluctuate.
@ lead_time_fluctuation = Determines the range on which shipment times can fluctuate
@ cw_inventory_holding_cost_multiplier = Determines the maximum reward the CW inventory can generate
@ customer_priorities = List of priorities for the RWs. Needs one entry per RW
@ rw_inventory_holding_cost_drop_off = Determines the rate of which the reward drops off depending in RW stock
@ cw_inventory_holding_cost_drop_off = Determines the rate of which the reward drops off depending in CW stock
@ use_advanced_demand_simulation = A random demand curve/trend will be generated. Agent will recieve forecasts 
@ demand_curve_length_multiplier = Influences the length of the demand function
@ manufacturer_inventory_limit = Maximum inventory the manufacturer can hold
@ forecast_range = The number of future steps the agent recieves as a demand forecast
@ forecast_deviation_factor = Determines the accuracy drop-off of the forecast values depending how much in the future
@ use_single_value_action_space = Converts action space to discrete type. Needed by some RL algorithms
@ sim_length = The number of rounds played during one simulation
"""


class Environment(gym.Env):

    def __init__(self, number_of_regional_wh, rw_inventory_limit, cw_inventory_limit, demand, lead_time,
                 shipment_amount, manufacturer, shipment_var_cost_per_unit, shipment_fixed_cost, demand_fluctuation,
                 lead_time_fluctuation, customer_priorities, cw_shipment_amount=20, mf_prod_capacity=20,
                 inventory_holding_cost_multiplier=1, cw_inventory_holding_cost_multiplier=.5,
                 rw_inventory_holding_cost_drop_off=1, cw_inventory_holding_cost_drop_off=.25,
                 manufacturer_inventory_limit=200, forecast_range=10, forecast_deviation_factor=1,
                 use_advanced_demand_simulation=False, demand_curve_length_multiplier=1, new_demand_curve_on_reset=True,
                 use_single_value_action_space=False, sim_length=50):

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
                                     customer_priorities=customer_priorities,
                                     sim_length=sim_length,
                                     use_predefined_demand=use_advanced_demand_simulation,
                                     demand_curve_length_multiplier=demand_curve_length_multiplier,
                                     manufacturer_inventory_limit=manufacturer_inventory_limit,
                                     new_demand_curve_on_reset=new_demand_curve_on_reset)

        """Action Space"""

        # Per warehouse the number of action depends on the number of possible shipment amounts
        action_space = [len(shipment_amount)+1]*number_of_regional_wh
        if manufacturer:
            action_space += [2]

        # Convert to single action value if use_single_value_action_space is true
        if not use_single_value_action_space:
            self.action_space = gym.spaces.MultiDiscrete(action_space)
        else:
            self.action_conversion_dict = self.create_actions_conversion_dict(action_space)
            self.action_space = gym.spaces.Discrete(len(self.action_conversion_dict))

        """Observation Space"""

        obs_space = {
            # Inventory state of every regional warehouse (Plus 1 to size 1 because inventory of 0 is a possibility)
            "rw_inventories": gym.spaces.MultiDiscrete(np.array([rw_inventory_limit + 1]*number_of_regional_wh)),
            "shipments": gym.spaces.MultiDiscrete(np.array([2]*number_of_regional_wh)),
            "next_arrival": gym.spaces.MultiDiscrete(np.array([lead_time + 1 + lead_time_fluctuation]*number_of_regional_wh)),
            "rw_amount_in_transit": gym.spaces.MultiDiscrete(np.array([max(shipment_amount) * (lead_time + lead_time_fluctuation) + 1] * number_of_regional_wh))
        }
        if manufacturer:
            # Inventory state of the central warehouse
            obs_space["cw_inventory"] = gym.spaces.Discrete(cw_inventory_limit + 1)
            obs_space["cw_shipment"] = gym.spaces.Discrete(2)
            obs_space["cw_next_arrival"] = gym.spaces.Discrete(lead_time + 1 + lead_time_fluctuation)
            obs_space["cw_amount_in_transit"] = gym.spaces.Discrete(cw_shipment_amount * (lead_time + lead_time_fluctuation) + 1)

        if use_advanced_demand_simulation:
            # Set parameters for forecasts
            self.max_possible_forecast = max(demand) * 2 + demand_fluctuation  # Value needed for space range generation
            self.forecast_range = forecast_range
            self.forecast_deviation_factor = forecast_deviation_factor

            # Expand observation space with Box shape representing forecasts for each RW
            obs_space["forecasts"] = gym.spaces.Box(0, self.max_possible_forecast, shape=(number_of_regional_wh, self.forecast_range))

        self.observation_space = gym.spaces.Dict(obs_space)

        """Environment Parameters"""

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
        self.use_advanced_demand_simulation = use_advanced_demand_simulation

        # Reward drop-off
        self.rw_inventory_holding_cost_drop_off = rw_inventory_holding_cost_drop_off
        self.cw_inventory_holding_cost_drop_off = cw_inventory_holding_cost_drop_off

        # Set initial state
        self.state = self.get_state()

        # Values for final evaluation
        self.total_lost_sales = 0
        self.total_reward_gained = 0
        self.total_shipments = 0

        # Saves total rewards over multiple episodes. Not affected by resets
        self.total_reward = []

    """Creates new state dictionary. Fetches changes in the simulation"""
    def get_state(self):
        # Build state component regional warehouse inventories
        rw_inv_state_list = []
        rw_shipment_state_list = [0]*self.number_of_rw
        rw_next_arrival_state_list = [0]*self.number_of_rw
        rw_total_amount_on_way_state_list = [0]*self.number_of_rw

        for rw_id in self.simulation.get_regional_warehouses():
            rw_inv_state_list.append(self.simulation.get_regional_warehouse_by_id(rw_id).get_inventory_amount())

            # Check shipments
            for active_shipments in self.simulation.get_all_active_shipments():
                if active_shipments["regional_warehouse"] == rw_id:
                    rw_shipment_state_list[rw_id-1] = 1
                    rw_total_amount_on_way_state_list[rw_id-1] += active_shipments["amount"]

                    # Check arrival
                    possible_next_shipment = active_shipments["arrival"] - self.simulation.get_round()
                    if rw_next_arrival_state_list[rw_id-1] == 0:
                        rw_next_arrival_state_list[rw_id-1] = possible_next_shipment
                    elif rw_next_arrival_state_list[rw_id-1] > possible_next_shipment:
                        rw_next_arrival_state_list[rw_id-1] = possible_next_shipment

        # Concat all components to list
        current_state = {"rw_inventories": np.array(rw_inv_state_list),
                         "shipments": np.array(rw_shipment_state_list),
                         "next_arrival": np.array(rw_next_arrival_state_list),
                         "rw_amount_in_transit": np.array(rw_total_amount_on_way_state_list)
                         }

        # Add manufacturer states if manufacturer is enabled
        if self.manufacturer:
            cw_next_arrival_state = 0
            cw_total_amount_in_transit = 0

            # np.intc used because DQN algorithm needs .space method not included in regular ints
            current_state["cw_inventory"] = np.intc(self.simulation.get_central_warehouse().get_inventory_amount())
            if len(self.simulation.get_all_active_cw_shipments()) == 0:
                current_state["cw_shipment"] = np.intc(0)
            else:
                current_state["cw_shipment"] = np.intc(1)

                # Arrival date for cw shipments
                for shipment in self.simulation.get_all_active_cw_shipments():
                    cw_total_amount_in_transit += shipment["amount"]

                    # Determine next shipment
                    possible_next_shipment = shipment["arrival"] - self.simulation.get_round()
                    if cw_next_arrival_state == 0:
                        cw_next_arrival_state = possible_next_shipment
                    elif cw_next_arrival_state > possible_next_shipment:
                        cw_next_arrival_state = possible_next_shipment

            current_state["cw_next_arrival"] = np.intc(cw_next_arrival_state)
            current_state["cw_amount_in_transit"] = np.intc(cw_total_amount_in_transit)

        # Add forecasts to state, if advanced demand simulation is enabled
        if self.use_advanced_demand_simulation:

            forecast_array = []  # Will become 2D array including all forecasts

            for rw_id in self.simulation.get_regional_warehouses():

                # Parameters for Forecasting calculation
                rw_demand_params = self.simulation.get_predefined_demand_parameters()[rw_id - 1]
                rw_strd_demand = self.simulation.get_regional_warehouse_by_id(rw_id).get_customer().get_demand_per_step()

                # Forecast calculation
                forecast_dict = self.get_forecasts(self.simulation.get_round() - 2, rw_strd_demand, rw_demand_params,
                                                   self.forecast_range, self.forecast_deviation_factor)

                # Forecast values for one RW
                forecast_values = forecast_dict["deviating_forecast_values"]
                float_forecast_values = forecast_dict["float_deviating_forecast_values"]

                forecast_array.append(float_forecast_values)

            # Add all forecasts to state
            forecast_array = np.array(forecast_array)
            current_state["forecasts"] = forecast_array

        return current_state

    # Calculates forecasts for one Demand trend and given step
    def get_forecasts(self, current_round, demand, params, forecast_range, forecast_deviation_factor=1.0):
        true_forecast_values = []
        deviating_forecast_values = []
        final_deviating_forecast_values = []

        # Calculate one forecast value per step in the future
        for x in range(forecast_range):
            days_in_future = x
            x += current_round + 1
            function_value = demand + ((params["long_range_amplitude"]
                                       * np.sin(params["long_range"] * x - params["random_start"]))
                                       - params["mid_range_amplitude"] * np.sin(params["mid_range"] * x))

            # Fill forecast lists
            true_forecast_values.append(function_value)
            tamper_value = (demand * forecast_deviation_factor / forecast_range) * days_in_future
            deviating_forecast_values.append(function_value + random.uniform(-tamper_value, tamper_value))

        # Check if calculated value is out of bounds
        for value in deviating_forecast_values:
            val_to_append = int(round(value, 0))
            if val_to_append < 0:
                val_to_append = 0
            elif val_to_append > self.max_possible_forecast:
                val_to_append = self.max_possible_forecast

            final_deviating_forecast_values.append(val_to_append)

        return {"deviating_forecast_values": final_deviating_forecast_values,
                "float_deviating_forecast_values": deviating_forecast_values,
                "true_forecast_values": true_forecast_values}

    # Prints all environment specifications
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

    # Create list that is used for action space conversion
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

    # Converts single action value to list
    def convert_discrete_to_multi_discrete(self, discrete_action):
        return self.action_conversion_dict[discrete_action]

    # Converts action list to single value
    def convert_nulti_discrete_to_discrete(self, multi_discrete_action):
        for entry in self.action_conversion_dict:
            if self.action_conversion_dict[entry] == multi_discrete_action:
                return entry

    """
    Reset Method
    ------------
    - Resets values of simulation class instance
    - Resets evaluation parameters
    - Adds up total reward value
    
    @ returns state
    """
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

    """
    Step Method
    -----------
    1. Converts action space if necessary
    2. Steps simulation class instance
    3. Create RW and CW shipments based on agent action
    4. Calculate reward based on inventory amounts and new shipment initializations
    5. Count up evaluation parameters
     
    @return new state, reward, done/not done, user information about step
    """

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

        # Reward function based on inventory amounts and started shipments
        reward = 0
        # Check RWs
        for rw_id in self.simulation.get_regional_warehouses():
            if self.simulation.get_regional_warehouse_by_id(rw_id).get_lost_sales_last_round() != 0:
                # Negative reward based on the priorization of the RW customer
                rw_reward = -self.simulation.get_regional_warehouse_by_id(rw_id).get_customer().get_priority()
            else:
                rw_reward = self.inventory_holding_cost_multiplier/(self.state["rw_inventories"][rw_id - 1]*self.rw_inventory_holding_cost_drop_off + 1)  # Hyperbel

                # Shipping cost
                if action[rw_id - 1] != 0:
                    rw_reward -= self.shipment_fixed_cost + \
                                 self.shipment_amount[action[rw_id - 1]-1] * self.shipment_var_cost_per_unit
                    if rw_reward < -1:
                        rw_reward = -1

            reward += rw_reward

        # Check CW if manufacturer is enabled
        if self.simulation.get_manufacturer():
            cw_reward = self.cw_inventory_holding_cost_multiplier/(self.state["cw_inventory"]*self.cw_inventory_holding_cost_drop_off + 1)
            # Add shipping cost

            reward += cw_reward

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
        step_info = {"Round:": self.current_round, "RW Invs:": self.state["rw_inventories"].tolist(), "Shipments": self.state["shipments"].tolist(),
                     "Action:": action, "Reward:": round(reward, 2)}

        # Add manufacturer info if enabled
        if self.simulation.get_manufacturer():
            step_info["CW Inv:"] = self.state["cw_inventory"]
            step_info["Manufacturer:"] = self.simulation.get_manufacturer().get_inventory_amount()

        self.current_round += 1

        return self.state, reward, done, step_info

    # Determine a lead time with the fluctuation parameter
    def get_lead_time_with_fluctuation(self):
        new_lead_time = random.randint(self.lead_time - self.lead_time_fluctuation,
                                       self.lead_time + self.lead_time_fluctuation)
        if new_lead_time < 1:
            new_lead_time = 1

        return new_lead_time

    # Return all eval parameters
    def evaluation_parameters(self):
        return {"total_shipments": self.total_shipments,
                "total_lost_sales": self.total_lost_sales,
                "total_reward_gained": round(self.total_reward_gained, 2)}
