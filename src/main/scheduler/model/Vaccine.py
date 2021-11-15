import sys
from ..scheduler.db.ConnectionManager import ConnectionManager
import pymssql

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


    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_doses = "INSERT INTO VACCINES VALUES (%s, %d)"
        try:
            cursor.execute(add_doses, (self.vaccine_name, self.available_doses))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.error as db_err:
            print("Error occurred when insert Vaccines")
        cm.close_connection()


    # Increment the available doses
    def increase_available_doses(self, num):
        if num <= 0:
            ValueError("Argument cannot be negative!")
        self.available_doses += num

        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        update_vaccine_availability  = "UPDATE vaccines SET Doses = %d WHERE name = %s"
        try:
            cursor.execute(update_vaccine_availability, (self.available_doses, self.vaccine_name))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.error as db_err:
            print("Error occurred when updating vaccine availability")
        cm.close_connection()


    # Decrement the available doses
    def decrease_available_doses(self, num):
        if self.available_doses - num < 0:
            ValueError("Not enough available doses!")
        self.available_doses -= num

        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        update_vaccine_availability  = "UPDATE vaccines SET Doses = %d WHERE name = %s"
        try:
            cursor.execute(update_vaccine_availability, (self.available_doses, self.vaccine_name))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.error as db_err:
            print("Error occurred when updating vaccine availability")
        cm.close_connection()


    def __str__(self):
        return f"(Vaccine Name: {self.vaccine_name}, Required Doses: {self.required_doses}, Available Doses: {self.available_doses})"
