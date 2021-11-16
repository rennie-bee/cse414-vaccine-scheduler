import sys
from ..scheduler.util.Util import Util
import pymssql

class Caregiver:
    def __init__(self, username, password):
        self.username = username
        self.salt = Util.generate_salt();
        self.hash = Util.generate_hash(password, self.salt)


    def __init__(self, username, salt, hash):
        self.username = username
        self.salt = salt
        self.hash = hash


    # getters
    def get_username(self):
        return self.username


    def get_salt(self):
        return self.salt


    def get_hash(self):
        return self.hash


    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_caregivers = "INSERT INTO Caregivers VALUES (%s, %b, %b)"
        try:
            cursor.execute(add_caregivers, (self.username, self.salt, self.hash))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.error as db_err:
            print("Error occurred when insert Vaccines")
        cm.close_connection()


    # Insert availability with parameter date d
    def upload_availability(self, d):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_availability  = "INSERT INTO Availabilities VALUES (%s , %s)"
        try:
            cursor.execute(update_vaccine_availability, (d, self.username))
            # you must call commit() to persist your data if you don't set autocommit to True
            conn.commit()
        except pymssql.error as db_err:
            print("Error occurred when updating caregiver availability")
        cm.close_connection()
