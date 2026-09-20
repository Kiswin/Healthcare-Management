```sql
CREATE DATABASE healthcare_management;

USE healthcare_management;


-- ============================================================
-- PATIENTS TABLE
-- ============================================================

CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(15),
    address VARCHAR(255),
    blood_group VARCHAR(5),
    emergency_contact VARCHAR(15),
    registration_date DATE NOT NULL
);


-- ============================================================
-- DEPARTMENTS TABLE
-- ============================================================

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);


-- ============================================================
-- DOCTORS TABLE
-- ============================================================

CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    department_id INT,
    phone VARCHAR(15),
    consultation_fee DECIMAL(10,2)
);


-- ============================================================
-- APPOINTMENTS TABLE
-- ============================================================

CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    appointment_time TIME,
    status VARCHAR(20),
    reason VARCHAR(255)
);


-- ============================================================
-- MEDICAL RECORDS TABLE
-- ============================================================

CREATE TABLE medical_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    visit_date DATE,
    diagnosis VARCHAR(255),
    prescription TEXT,
    notes TEXT
);


-- ============================================================
-- BILLING TABLE
-- ============================================================

CREATE TABLE billing (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    appointment_id INT,
    bill_date DATE,
    consultation_fee DECIMAL(10,2),
    medicine_charge DECIMAL(10,2),
    test_charge DECIMAL(10,2),
    other_charge DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    payment_status VARCHAR(20)
);


-- ============================================================
-- SAMPLE DEPARTMENTS
-- ============================================================

INSERT INTO departments
(department_name, location)
VALUES
('General Medicine', 'Block A'),
('Cardiology', 'Block B'),
('Neurology', 'Block B'),
('Orthopedics', 'Block C'),
('Pediatrics', 'Block C');


-- ============================================================
-- SAMPLE DOCTORS
-- ============================================================

INSERT INTO doctors
(name, specialization, department_id, phone, consultation_fee)
VALUES
('Dr. Ravi Kumar', 'General Physician', 1, '9876543211', 500),
('Dr. Priya Sharma', 'Cardiologist', 2, '9876543212', 800),
('Dr. Arun Raj', 'Neurologist', 3, '9876543213', 1000),
('Dr. Meena Joseph', 'Orthopedic Surgeon', 4, '9876543214', 900),
('Dr. Anitha Thomas', 'Pediatrician', 5, '9876543215', 600);


-- ============================================================
-- SAMPLE PATIENT
-- ============================================================

INSERT INTO patients
(name, gender, date_of_birth, phone, address,
 blood_group, emergency_contact, registration_date)
VALUES
('Arun Kumar', 'Male', '2008-05-12', '9876543210',
 'Madurai', 'B+', '9876500000', '2026-08-26');


-- ============================================================
-- SAMPLE APPOINTMENT
-- ============================================================

INSERT INTO appointments
(patient_id, doctor_id, appointment_date,
 appointment_time, status, reason)
VALUES
(1, 2, '2026-08-27', '10:30:00',
 'Scheduled', 'Chest discomfort');


-- ============================================================
-- SAMPLE MEDICAL RECORD
-- ============================================================

INSERT INTO medical_records
(patient_id, doctor_id, visit_date,
 diagnosis, prescription, notes)
VALUES
(1, 2, '2026-08-27',
 'Chest discomfort',
 'Medication as prescribed',
 'Follow-up after 7 days');


-- ============================================================
-- SAMPLE BILL
-- ============================================================

INSERT INTO billing
(patient_id, appointment_id, bill_date,
 consultation_fee, medicine_charge, test_charge,
 other_charge, total_amount, payment_status)
VALUES
(1, 1, '2026-08-27',
 800.00, 350.00, 1200.00,
 0.00, 2350.00, 'Pending');
```
