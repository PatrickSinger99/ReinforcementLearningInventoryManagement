from abc import ABC
from class_customer import Customer


"""Abstract class: Warehouse"""


class Warehouse(ABC):
    id_count = 0

    def __init__(self, inventory_limit, start_inventory=False):
        # ID assignment
        self._id = Warehouse.id_count
        Warehouse.id_count += 1
        self._name = "unnnamed_warehouse"

        # Inventory
        self._inventory_limit = inventory_limit
        self._inventory_amount = start_inventory

        # Set starting inventory to 1/3 if no given value
        if self._inventory_amount is False:
            self._inventory_amount = int(self._inventory_limit/3)

        # Save start value for reset
        self._reset_inv_amount = self._inventory_amount

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = str(new_name)

    def get_inventory_amount(self):
        return self._inventory_amount

    def set_inventory_amount(self, new_amount):
        self._inventory_amount = int(new_amount)

        # Check if inventory exceeds max amount
        if self._inventory_amount > self._inventory_limit:
            self._inventory_amount = self._inventory_limit

        # Check if inventory falls below 0 and correct
        if self._inventory_amount < 0:
            self._inventory_amount = 0

    def reset(self):
        self._inventory_amount = self._reset_inv_amount # Set inventory to initial value


"""Class: Central Warehouse"""


class CentralWarehouse(Warehouse):
    instance_count = 0

    def __init__(self, inventory_limit):
        super().__init__(inventory_limit)
        CentralWarehouse.instance_count += 1
        self._name = "central_warehouse_" + str(CentralWarehouse.instance_count)

        self._connected_regional_warehouses = {}

    def add_regional_warehouse(self, rw):
        self._connected_regional_warehouses[rw.get_id()] = rw

    def shipment(self, recieving_rw_id, amount=5):
        # self._inventory_amount -= amount
        self._connected_regional_warehouses[recieving_rw_id].recieve_shipment(amount)

    def step(self):
        pass


"""Class: Regional Warehouse"""


class RegionalWarehouse(Warehouse):
    instance_count = 0

    def __init__(self, inventory_limit):
        super().__init__(inventory_limit)
        RegionalWarehouse.instance_count += 1
        self._name = "regional_warehouse_" + str(RegionalWarehouse.instance_count)

        self._lost_sales = 0  # Counts lost sales due to empty inventory

        # Initiate connections
        self._connected_central_warehouse = None
        self._customer = Customer()

    def add_central_warehouse(self, cw):
        self._connected_central_warehouse = cw

    def get_customer(self):
        return self._customer

    def get_lost_sales(self):
        return self._lost_sales

    def recieve_shipment(self, amount):
        self._inventory_amount += amount

        # Check if inventory exceeds max amount
        if self._inventory_amount > self._inventory_limit:
            self._inventory_amount = self._inventory_limit

    def step(self):
        self._inventory_amount -= self._customer.get_demand_per_step()

        # Count up lost sales if inv is below zero
        if self._inventory_amount < 0:
            self._lost_sales -= self._inventory_amount
            self._inventory_amount = 0

    def reset(self):
        self._inventory_amount = self._reset_inv_amount  # Set inventory to initial value
        self._lost_sales = 0


if __name__ == "__main__":
    c1 = CentralWarehouse()
    r1 = RegionalWarehouse()
    r2 = RegionalWarehouse()
    r3 = RegionalWarehouse()

    print(c1.get_id())
    print(r1.get_id())
    print(r2.get_id())
    print(r3.get_name())

