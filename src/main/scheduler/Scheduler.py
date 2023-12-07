from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime
import re

'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None

def is_strong_password(password):
    if len(password) < 8:
        print("Password length should be at least 8")
        return False
    if not any(char.isupper() for char in password) or not any(char.islower() for char in password):
        print("Password should contain both upper and lower cases")
        return False
    if not any(char.isdigit() for char in password):
        print("Password should contain digit")
        return False
    if not re.search(r'[!@#?]', password):
        print("Password should contain any of !@#?")
        return False
    return True

def create_patient(tokens):
    """
    TODO: Part 1
    """
    # create patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    patient_name = tokens[1]
    patient_pwd = tokens[2]
    if not is_strong_password(password=patient_pwd):
        return
    if username_exists_patient(patient_name):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    pwd_hash = Util.generate_hash(patient_pwd, salt)
    # create the patient
    patient = Patient(patient_name, salt=salt, hash=pwd_hash)

    # save to patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create patient.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create patient.")
        print(e)
        return
    print("Created patient: ", patient_name)


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    if not is_strong_password(password=password):
        return
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create caregiver object
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_patient(patient_name):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, patient_name)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking patient's name")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking patient's name")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    """
    TODO: Part 1
    """
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_patient is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(
            username=username,
            password=password
        ).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    TODO: Part 2
    """
    # search_caregiver_schedule <date>
    global current_patient, current_caregiver
    if current_patient is None and current_caregiver is None:
        print("Please login as a patient/caregiver first!")
        return

    if len(tokens) != 2:
        print("please try again!")

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)
        dt = datetime.datetime(year, month, day)

        sentence1 = """
                SELECT Username
                FROM [dbo].[Availabilities] A
                WHERE A.Time = %s
                ORDER BY A.Username"""
        sentence2 = """
                SELECT Name, Doses
                FROM [dbo].[Vaccines] V
                """

        cursor.execute(sentence1, dt)
        for row in cursor:
            print(f"Available caregivers for date {dt}:")
            print(f"{row['Username']}") is not None
        
        cursor.execute(sentence2)
        for row in cursor:
            print(f"Available vaccine and doses:")
            print(f"{row['Doses']} in {row['Name']}") is not None

    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()

def reserve(tokens):
    """
    TODO: Part 2
    """
    if len(tokens) != 3:
        print("Please try again!")
        return
    
    global current_patient, current_caregiver
    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return
    if current_patient is None:
        print("Please login as a patient!")
        return
    
    date = tokens[1]
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    dt = datetime.datetime(year, month, day)
    vaccine_name = tokens[2]
    try:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)
        vac = None
        
        # Return if no available doses for current vaccine.
        sentence1 = """
                SELECT name, doses
                FROM Vaccines V
                WHERE V.name = %s"""
        cursor.execute(sentence1, vaccine_name)
        for row in cursor:
            if row['doses'] < 1:
                print("Not enough available doses!")
                return
            else:
                vac = Vaccine(row["name"], row["doses"]).get()

        # Return if no available doctors or doctors' availabilites are filled up.   
        sentence2 = """
                SELECT TOP 1 Username
                FROM Availabilities a
                LEFT JOIN Reservations r ON a.Username = r.CaregiverName AND a.Time = r.Time
                WHERE a.Time = %s AND r.Id IS NULL"""
        cursor.execute(sentence2, dt)
        # print("Filter Accomplish")
        for row in cursor:
            if row['Username'] is None:
                print("No Caregiver is available!")
                return
            else:
                print("Conditions satisfied. Start Reservation")
                # Decrease one available dose for current vaccine 
                vac.decrease_available_doses(1)
                # Record the reservation details
                add_reservation = """
                                INSERT INTO reservations
                                VALUES(%s, %s, %s, %s)"""
                cursor.execute(
                    add_reservation, 
                    (dt, 
                    current_patient.username,
                    row['Username'],
                    vac.vaccine_name)
                )
                conn.commit()
                print(f"Successfully Reserved with {row['Username']}! Received vaccination {vac.vaccine_name} on {dt}!")
    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()



def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra Credit
    """

    pass


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    '''
    TODO: Part 2
    '''
    global current_patient, current_caregiver
    if len(tokens) != 1:
        print("Please try again!")
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    else:
        try:
            cm = ConnectionManager()
            conn = cm.create_connection()
            cursor = conn.cursor(as_dict=True)
            if current_caregiver is not None:
                # print the appointment ID, vaccine name, date, and patient name. Order by the appointment ID        
                str1 = """
                    SELECT Id, VaccineName, Time, PatientName FROM Reservations R 
                    WHERE R.CaregiverName = %s
                    ORDER BY R.Id"""
                print("Appointment ID | Vaccine | Date | Patient Name")
                cursor.execute(str1, current_caregiver.username)
                for row in cursor:
                    print(f"{row['Id']} | {row['VaccineName']} | {row['Time']} | {row['PatientName']}")
            else:
                # print the appointment ID, vaccine name, date, and caregiver name. Order by the appointment ID
                str2 = """
                    SELECT Id, VaccineName, Time, CaregiverName FROM Reservations R 
                    WHERE R.PatientName = %s
                    ORDER BY R.Id"""
                print("Appointment ID | Vaccine | Date | Caregiver Name")
                cursor.execute(str2, current_patient.username)
                for row in cursor:
                    print(f"{row['Id']} | {row['VaccineName']} | {row['Time']} | {row['CaregiverName']}")
        except pymssql.Error as e:
            print("Please try again!")
            print("Db-Error:", e)
            quit()
        except ValueError:
            print("Please try again!")
            return
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
            return


def logout(tokens):
    """
    TODO: Part 2
    """
    global current_patient, current_caregiver
    if len(tokens) != 1:
        print("Please try again!")
    if current_patient is not None:
        current_patient = None
    elif current_caregiver is not None:
        current_caregiver = None
    else:
        print("Please login first.")
        return
    print("Successfully logged out!")


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        # response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == cancel:
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
