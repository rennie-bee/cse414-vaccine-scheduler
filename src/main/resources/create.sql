CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
)

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255),
    PRIMARY KEY (Time, Username),
    FOREIGN KEY (Username) REFERENCES Caregivers(Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Reservations (
    Id int IDENTITY(1,1),
    Time date,
    PatientName varchar(255),
    CaregiverName varchar(255),
    VaccineName varchar(255),
    PRIMARY KEY (Id),
    FOREIGN KEY (PatientName) REFERENCES Patients(Username),
    FOREIGN KEY (CaregiverName) REFERENCES Caregivers(Username),
    FOREIGN KEY (VaccineName) REFERENCES Vaccines(Name)
)


