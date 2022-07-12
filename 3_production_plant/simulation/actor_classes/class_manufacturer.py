class Manufacturer:
    def __init__(self):
        self._name = "manufacturer"
        self._production_capacity_per_step = 1
        self._inventory = 0

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

    def get_production_capacity(self):
        return self._production_capacity_per_step

    def set_production_capacity(self, new_capacity):
        self._production_capacity_per_step = new_capacity

    def get_inventory(self):
        return self._inventory

    def step(self):
        self._inventory += self._production_capacity_per_step

    def remove_from_inventory(self, amount):
        if self._inventory - amount < 0:
            return False
        else:
            self._inventory -= amount
            return True
