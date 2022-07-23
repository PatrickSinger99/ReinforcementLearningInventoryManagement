from simulation.actor_classes.class_warehouse import *
from simulation.actor_classes.class_manufacturer import *


"""Class: Simulation"""


class Simulation:
    def __init__(self, number_of_regional_wh=1,
                 rw_inventory_limit=30,
                 cw_inventory_limit=100,
                 customer_demand=[1],
                 manufacturer=False,
                 manufacturer_production_capacity=10,
                 demand_fluctuation=0,
                 customer_priorities=[1]
                 ):

        # Variables
        self._round = 1
        self._in_transit_shipments = []
        self._in_transit_cw_shipments = []
        self._priorities = self.calculate_priorities(customer_priorities)

        # Instantiate actors
        self._central_warehouse = CentralWarehouse(cw_inventory_limit)  # Saved as class object
        self._central_warehouse.set_id(1)
        self._regional_warehouses = {}  # Saved as {id: object, id2: object2}

        # Create regional warehouses
        rw_id_count = 1

        for i in range(number_of_regional_wh):
            new_rw = RegionalWarehouse(rw_inventory_limit)
            new_rw.set_id(rw_id_count)
            new_rw.get_customer().set_demand_per_step(customer_demand[i])
            new_rw.get_customer().set_demand_fluctuation(demand_fluctuation)
            new_rw.get_customer().set_priority(self._priorities[i])

            self._regional_warehouses[rw_id_count] = new_rw
            rw_id_count += 1

            # Add connections
            self._central_warehouse.add_regional_warehouse(new_rw)
            new_rw.add_central_warehouse(self._central_warehouse)

        # Create Manufacturer if set to True
        if manufacturer:
            self._manufacturer = Manufacturer(manufacturer_production_capacity)
        else:
            self._manufacturer = False

        # Info print
        print("Simulation created with the following parameters:")
        print("_"*80)
        self.print_state()

    def get_round(self):
        return self._round

    def get_central_warehouse(self):
        return self._central_warehouse

    def get_regional_warehouses(self):
        return self._regional_warehouses

    def get_regional_warehouse_by_id(self, rw_id):
        return self._regional_warehouses[rw_id]

    def get_manufacturer(self):
        return self._manufacturer

    def calculate_priorities(self, priorities):
        max_val = max(priorities)
        val = 1 / (max_val + 1)
        min_val = 1 - max_val * val

        new_prio = []
        for prio in priorities:
            new_prio.append(round(prio * val + min_val, 2))

        return new_prio

    # Print distribution network state
    def print_state(self):
        title = "Simulation | Round " + str(self._round)
        print(title + "\n" + "-"*(len(title)-1))

        print("-> Active shipments:")

        for shipment in self._in_transit_shipments:
            print("To:", self._regional_warehouses[shipment["regional_warehouse"]].get_name(),
                  "Arrival in round:", shipment["arrival"], "Amount:", shipment["amount"])
        if len(self._in_transit_shipments) == 0:
            print("No active shipments")

        print("\n-> Warehouses:")
        # Print central warehouse
        print(self._central_warehouse.get_name() + " ; Inventory:",
              self._central_warehouse.get_inventory_amount())

        # Print regional warehouses
        for rw in self._regional_warehouses:
            print(self._regional_warehouses[rw].get_name() + " ; ID:",
                  self._regional_warehouses[rw].get_id(), "; Inventory:",
                  self._regional_warehouses[rw].get_inventory_amount(), "; Demand:",
                  self._regional_warehouses[rw].get_customer().get_demand_per_step(), "; Priority:",
                  self._regional_warehouses[rw].get_customer().get_priority(), "; Lost sales:",
                  self._regional_warehouses[rw].get_lost_sales())

        if self._manufacturer:
            print("\n-> Production plant:")
            print(self._manufacturer.get_name() + " ; Production per step:",
                  self._manufacturer.get_production_capacity(), "; Inventory:",
                  self._manufacturer.get_inventory_amount())

        print("_" * 80)  # Separator

    # Starts a new shipment by creating a entry in the in_transit_shipments dictionary
    def start_shipment(self, rw_id, amount, lead_time):
        # Check if enough inventory in central warehouse
        if self._central_warehouse.get_inventory_amount() >= amount:
            # Create shipment
            self._in_transit_shipments.append({"regional_warehouse": rw_id,
                                               "amount": amount,
                                               "lead_time": lead_time,
                                               "arrival": self._round + lead_time})
            # Remove amount from central warehouse if manufacturer is modeled
            if self._manufacturer:
                self._central_warehouse.set_inventory_amount(remove=amount)

    # Finish a shipment by adding amount to recieving regional warehouse
    def finish_shipment(self, rw_id, amount):
        self._regional_warehouses[rw_id].set_inventory_amount(add=amount)

    # Start shipment for central warehouse
    def start_cw_shipment(self, amount, lead_time):
        # Check if amount is available at manufacturer
        if self._manufacturer.get_inventory_amount() >= amount:
            self._in_transit_cw_shipments.append({"amount": amount,
                                                  "lead_time": lead_time,
                                                  "arrival": self._round + lead_time})

            self._manufacturer.set_inventory_amount(remove=amount)

    # Finish shipment for central warehouse
    def finish_cw_shipment(self, amount):
        self._central_warehouse.set_inventory_amount(add=amount)

    # return all rw and cw shipments that are in transit
    def get_all_active_shipments(self):
        return self._in_transit_shipments

    def get_all_active_cw_shipments(self):
        return self._in_transit_cw_shipments

    # Step simulation
    # - Finish shipments

    def step(self):
        # Current round
        self._round += 1

        # List for later removement
        shipments_to_remove = []

        # Finish shipments, if delivery time reached
        for active_shipment in self._in_transit_shipments:
            if active_shipment["arrival"] == self._round:

                self.finish_shipment(rw_id=active_shipment["regional_warehouse"], amount=active_shipment["amount"])
                shipments_to_remove.append(active_shipment)

        # Remove finished shipments
        for shipment in shipments_to_remove:
            self._in_transit_shipments.remove(shipment)

        # List for later removement
        cw_shipments_to_remove = []

        # Finish cw shipments
        for active_shipment in self._in_transit_cw_shipments:
            if active_shipment["arrival"] == self._round:
                self.finish_cw_shipment(amount=active_shipment["amount"])
                cw_shipments_to_remove.append(active_shipment)

        # Remove finished shipments
        for shipment in cw_shipments_to_remove:
            self._in_transit_cw_shipments.remove(shipment)

        # Step regional warehouses
        for rw in self._regional_warehouses:
            self._regional_warehouses[rw].step()

        # Step Manufacturer
        if self._manufacturer:
            self._manufacturer.step()

    # Resets parameters back to initial values
    def reset(self):
        self._round = 1
        self._in_transit_shipments = []
        self._in_transit_cw_shipments = []

        self._central_warehouse.reset()
        for wh in self._regional_warehouses:
            self._regional_warehouses[wh].reset()
