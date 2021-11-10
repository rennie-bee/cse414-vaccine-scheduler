import sys
sys.path.append("./model/*")

from model.Vaccine import Vaccine

def login():
  '''
  TODO: add logic for logging in
  case 0: invalid login credentials, re-try
  case 1: user is a patient, display the corresponding commands and wait for input
  case 2: user is a caregiver, display the corresponding commands and wait for input
  '''
  pass

def create_account():
  '''
  TODO: add logic for creating an account
  once we'v e created the user, we can go back to processing create and login again
  '''
  process_create_and_login()

def process_create_and_login():
    stop = False
    while not stop:
        print()
        print(" *** Please enter one of the following commands *** ")
        print("> Create")
        print("> Login")
        print("> Quit")
        print()
        response = ""
        print("> Enter: ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Type in a valid argument")
            break
      
        response = response.lower()
        if response == "create":
            create_account()
        elif response == "login":
            login()
        elif response == "quit":
            print("Thank you for using the scheduler, Goodbye!")
            stop = True
        else:
            print("Invalid Argument")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''
    vaccine_map = {}
    pfizer = Vaccine("Pfizer", 2, 33)
    moderna = Vaccine("Moderna", 2, 44)
    jj = Vaccine("Johnson & Johnson", 1, 7)

    vaccine_map["Pfizer"] = pfizer
    vaccine_map["Moderna"] = moderna
    vaccine_map["Johnson & Johnson"] = jj

    # start command line 
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    process_create_and_login()
  
