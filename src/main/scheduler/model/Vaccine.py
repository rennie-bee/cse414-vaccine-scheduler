class Vaccine:
    def __init__(self, builder):
        self.vaccineName = builder.vaccineName
        self.availableDoses = builder.availableDoses
        self.requiredDoses = builder.requiredDoses

    # getters
    def getVaccineName() -> String:
        return self.vaccineName

    def getAvailableDoses() -> int:
        return self.availableDoses

    def getRequiredDoses() -> int:
        return self.requiredDoses

    # Increment the available doses
    def increaseAvailableDoses(num):
        if num <= 0:
            throw ValueError("Argument cannot be negative!")
        self.availableDoses += num

    # Decrement the available doses
    def decreaseAvailableDoses(num):
        if self.availableDoses - num < 0:
            throw ValueError("Not enough available doses!")
        self.availableDoses -= num

    def __str__():
          return "Vaccine{" +
            "vaccineName='" + str(self.vaccineName) + '\'' +
            ", requiredDoses=" + str(self.requiredDoses) +
            ", availableDoses=" + str(self.availableDoses) +
            "}"

    class VaccineBuilder:
        def __init__(self, vaccineName, requiredDoses):
            self.vaccineName = vaccineName
            self.requiredDoses = requiredDoses

        def availableDoses(availableDoses):
            self.availableDoses = availableDoses
            return self

        def build():
            return Vaccine(self)
