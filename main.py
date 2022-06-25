from class_customer import *
from class_warehouse import *
import time


class Simulation:
    def __init__(self, num_rw=1):

        # Initiate Warehouses
        self._central_warehouse = CentralWarehouse()
        self._regional_warehouses = {}

        # Create regional warehouses
        for i in range(num_rw):
            new_rw = RegionalWarehouse()
            self._regional_warehouses[new_rw.get_id()] = new_rw

            # Add connections
            self._central_warehouse.add_regional_warehouse(new_rw)
            new_rw.add_central_warehouse(self._central_warehouse.get_id())

        # Parameters
        self._timestep = 0

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

    def step(self):
        # Step regional warehouses
        for rw in self._regional_warehouses:
            self._regional_warehouses[rw].step()

        # Step central warehouse
        self._central_warehouse.step()

        # Timestep
        self._timestep += 1


if __name__ == "__main__":
    s1 = Simulation(3)
    s1.print_state()
    s1.get_central_warehouse().shipment(2)

    for i in range(150):
        s1.step()
        s1.print_state()
        time.sleep(.1)
