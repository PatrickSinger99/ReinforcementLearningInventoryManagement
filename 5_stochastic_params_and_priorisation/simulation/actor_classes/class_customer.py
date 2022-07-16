import random


class Customer:
    id_count = 0

    def __init__(self, demand_per_step=1, demand_fluctuation=0):
        # ID & name assignment
        self._id = Customer.id_count
        Customer.id_count += 1
        self._name = "customer_" + str(Customer.id_count)

        self._demand_per_step = demand_per_step
        self._demand_fluctuation = demand_fluctuation

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

    def set_demand_per_step(self, new_demand):
        self._demand_per_step = new_demand

    def get_demand_per_step(self):
        return self._demand_per_step

    def get_demand_with_fluctuation(self):
        new_demand = random.randint(self._demand_per_step - self._demand_fluctuation,
                                    self._demand_per_step + self._demand_fluctuation)
        if new_demand < 0:
            new_demand = 0

        return new_demand

    def get_demand_fluctuation(self):
        return self._demand_fluctuation

    def set_demand_fluctuation(self, new_fluctuation):
        self._demand_fluctuation = new_fluctuation
