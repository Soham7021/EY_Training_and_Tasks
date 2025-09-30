-- Step 1: Create the Database
CREATE DATABASE HospitalDB;
USE HospitalDB;

-- Step 2: Create Patients Table
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    gender CHAR(1),
    city VARCHAR(50)
);

-- Step 3: Create Doctors Table
CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(50),
    specialization VARCHAR(50),
    experience INT
);

-- Step 4: Create Appointments Table
CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

-- Step 5: Create MedicalRecords Table
CREATE TABLE MedicalRecords (
    record_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    diagnosis VARCHAR(100),
    treatment VARCHAR(100),
    date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

-- Step 6: Create Billing Table
CREATE TABLE Billing (
    bill_id INT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10,2),
    bill_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);
