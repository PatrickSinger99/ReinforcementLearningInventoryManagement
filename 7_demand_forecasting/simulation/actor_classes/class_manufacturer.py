

"""Class: Manufacturer"""


class Manufacturer:
    def __init__(self, production_capacity_per_step):
        # Identification
        self._name = "manufacturer"

        # Parameters
        self._production_capacity_per_step = production_capacity_per_step
        self._inventory_amount = 100
        self._inventory_limit = 100

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

    def get_production_capacity(self):
        return self._production_capacity_per_step

    def set_production_capacity(self, new_capacity):
        self._production_capacity_per_step = new_capacity

    def get_inventory_amount(self):
        return self._inventory_amount

    def get_inventory_limit(self):
        return self._inventory_limit

    # Method can be used to eighter add/remove a certain amount from the inventory, or to overwrite it with a set value
    def set_inventory_amount(self, total_amount=None, add=0, remove=0):
        if total_amount is not None:
            self._inventory_amount = int(total_amount)

        else:
            self._inventory_amount += add
            self._inventory_amount -= remove

        # Check if inventory exceeds max amount
        if self._inventory_amount > self._inventory_limit:
            self._inventory_amount = self._inventory_limit

        # Check if inventory falls below 0 and correct
        if self._inventory_amount < 0:
            self._inventory_amount = 0

    # Add to inventory based on production rate
    def step(self):
        self.set_inventory_amount(add=self._production_capacity_per_step)
