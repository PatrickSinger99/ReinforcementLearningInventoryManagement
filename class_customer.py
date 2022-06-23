class Customer:
    id_count = 0

    def __init__(self):
        # ID & name assignment
        self._id = Customer.id_count
        Customer.id_count += 1
        self._name = "customer_" + str(Customer.id_count)

        self._demand_per_step = 1

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

