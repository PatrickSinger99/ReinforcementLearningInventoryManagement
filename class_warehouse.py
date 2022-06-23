from abc import ABC
from class_customer import Customer


"""Abstract class: Warehouse"""


class Warehouse(ABC):
    id_count = 0

    def __init__(self):
        # ID assignment
        self._id = Warehouse.id_count
        Warehouse.id_count += 1

        self._inventory_amount = 0
        self._name = "unnnamed_warehouse"

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


"""Class: Regional Warehouse"""


class RegionalWarehouse(Warehouse):
    instance_count = 0

    def __init__(self):
        super().__init__()
        RegionalWarehouse.instance_count += 1
        self._name = "regional_warehouse_" + str(RegionalWarehouse.instance_count)


if __name__ == "__main__":
    c1 = CentralWarehouse()
    r1 = RegionalWarehouse()
    r2 = RegionalWarehouse()
    r3 = RegionalWarehouse()

    print(c1.get_id())
    print(r1.get_id())
    print(r2.get_id())
    print(r3.get_name())

