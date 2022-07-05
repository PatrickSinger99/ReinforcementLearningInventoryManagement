from simulation.actor_classes.class_warehouse import *
import time


"""Simulation class"""


class Simulation:
    def __init__(self, number_of_regional_wh=1, inventory_limit=30):

        # Instantiate Warehouses
        self._central_warehouse = CentralWarehouse(inventory_limit)  # Saved as class object
        self._regional_warehouses = {}  # Saved as {id: object, id2: object2}

        # Create regional warehouses
        for i in range(number_of_regional_wh):
            new_rw = RegionalWarehouse(inventory_limit)
            self._regional_warehouses[new_rw.get_id()] = new_rw

            # Add connections
            self._central_warehouse.add_regional_warehouse(new_rw)
            new_rw.add_central_warehouse(self._central_warehouse)

    def get_central_warehouse(self):
        return self._central_warehouse

    def get_regional_warehouses(self):
        return self._regional_warehouses

    # Print distribution network state
    def print_state(self):
        print("-"*60)  # Separator

        # Print central warehouse
        print(self._central_warehouse.get_name() + " ; Inventory:", self._central_warehouse.get_inventory_amount())
        print()

        # Print regional warehouses
        for rw in self._regional_warehouses:
            print(self._regional_warehouses[rw].get_name() + " ; Inventory:",
                  self._regional_warehouses[rw].get_inventory_amount(), "; Demand:",
                  self._regional_warehouses[rw].get_customer().get_demand_per_step(), "; Lost sales:",
                  self._regional_warehouses[rw].get_lost_sales())

        print("-" * 60)  # Separator

    def ship_from_central_to_regional_warehouse(self, regional_warehouse_id, amount):
        self._central_warehouse.shipment(regional_warehouse_id, amount)

    def step(self):
        # Step regional warehouses
        for rw in self._regional_warehouses:
            self._regional_warehouses[rw].step()

        # Step central warehouse
        self._central_warehouse.step()

    def reset(self):
        self._central_warehouse.reset()
        for wh in self._regional_warehouses:
            self._regional_warehouses[wh].reset()


if __name__ == "__main__":
    s1 = Simulation(3)
    s1.print_state()
    s1.ship_from_central_to_regional_warehouse(1, 100)

    for i in range(150):
        s1.step()
        s1.print_state()
        time.sleep(.1)
