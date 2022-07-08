class Customer:
    id_count = 0

    def __init__(self, demand_per_step=1):
        # ID & name assignment
        self._id = Customer.id_count
        Customer.id_count += 1
        self._name = "customer_" + str(Customer.id_count)

        self._demand_per_step = demand_per_step

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
