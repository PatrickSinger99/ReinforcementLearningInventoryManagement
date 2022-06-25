from abc import ABC
from class_customer import Customer


"""Abstract class: Warehouse"""


class Warehouse(ABC):
    id_count = 0

    def __init__(self, start_inventory=100):
        # ID assignment
        self._id = Warehouse.id_count
        Warehouse.id_count += 1
        self._name = "unnnamed_warehouse"

        # Inventory
        self._inventory_amount = start_inventory

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


"""Class: Central Warehouse"""


class CentralWarehouse(Warehouse):
    instance_count = 0

    def __init__(self):
        super().__init__()
        CentralWarehouse.instance_count += 1
        self._name = "central_warehouse_" + str(CentralWarehouse.instance_count)

        self._connected_regional_warehouses = {}

    def add_regional_warehouse(self, rw):
        self._connected_regional_warehouses[rw.get_id()] = rw

    def shipment(self, recieving_rw_id, amount=10):
        # self._inventory_amount -= amount
        self._connected_regional_warehouses[recieving_rw_id].recieve_shipment(amount)

    def step(self):
        pass


"""Class: Regional Warehouse"""


class RegionalWarehouse(Warehouse):
    instance_count = 0

    def __init__(self):
        super().__init__()
        RegionalWarehouse.instance_count += 1
        self._name = "regional_warehouse_" + str(RegionalWarehouse.instance_count)

        self._lost_sales = 0  # Counts lost sales due to empty inventory

        # Initiate connections
        self._connected_central_warehouse = None
        self._customer = Customer()

    def add_central_warehouse(self, cw_id):
        self._connected_central_warehouse = cw_id

    def get_customer(self):
        return self._customer

    def get_lost_sales(self):
        return self._lost_sales

    def recieve_shipment(self, amount):
        self._inventory_amount += amount

    def step(self):
        self._inventory_amount -= self._customer.get_demand_per_step()

        # Count up lost sales if inv is below zero
        if self._inventory_amount < 0:
            self._lost_sales -= self._inventory_amount
            self._inventory_amount = 0


if __name__ == "__main__":
    c1 = CentralWarehouse()
    r1 = RegionalWarehouse()
    r2 = RegionalWarehouse()
    r3 = RegionalWarehouse()

    print(c1.get_id())
    print(r1.get_id())
    print(r2.get_id())
    print(r3.get_name())

