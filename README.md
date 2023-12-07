# Vaccine Scheduler Platform

## Background
A python-based platform enabling patients to book vaccination appointments with caregivers from hospitals. The application is developed using Pymssql and utilizes Microsoft Azure as the storage engine.
* Patients: these are customers that want to receive the vaccine.
* Caregivers: these are employees of the health organization administering the vaccines.
* Vaccines: these are vaccine doses in the health organization’s inventory of medical supplies that are on hand and ready to be given to the patients.



## Functionalities
- create_patient (username, password)
- create_caregiver (username, password)
- login_patient (username, password)
- login_caregiver (username, password)
- search_caregiver_schedule (date)
- reserve (date, vaccine)
- upload_availability (date)
- cancel (appointment_id)
- add_doses (vaccine, number)
- show_appointments
- logout
- quit
