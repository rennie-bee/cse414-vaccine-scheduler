class Vaccine:
    def __init__(self, vaccine_name, available_doses, required_doses):
        self.vaccine_name = vaccine_name
        self.required_doses = required_doses
        self.available_doses = available_doses

    # getters
    def get_vaccine_name(self):
        return self.vaccine_name

    def get_available_doses(self):
        return self.available_doses

    def get_required_doses(self):
        return self.required_doses

    # Increment the available doses
    def increase_available_doses(self, num):
        if num <= 0:
            ValueError("Argument cannot be negative!")
        self.available_doses += num

    # Decrement the available doses
    def decrease_available_doses(self, num):
        if self.availableDoses - num < 0:
            ValueError("Not enough available doses!")
        self.available_doses -= num

    def __str__(self):
        return f"(Vaccine Name: {self.vaccine_name}, Required Doses: {self.required_doses}, Available Doses: {self.available_doses})"