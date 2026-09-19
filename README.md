# Healthcare Management System

A **Python and MySQL-based Healthcare Management System** designed to manage patients, doctors, appointments, medical records, billing, and reports through a simple command-line interface.

## Project Overview

The Healthcare Management System demonstrates how **Python programming and MySQL database management** can be combined to build a practical real-world application.

The system allows healthcare staff to maintain organized records and perform common operations such as adding, searching, updating, and deleting information.

## Features

* Patient registration and management
* Doctor management
* Department-based doctor records
* Appointment booking and management
* Medical record management
* Billing and automatic total calculation
* Patient, doctor, appointment, medical record, and billing reports
* Search functionality
* Update and delete operations
* MySQL database integration
* Input validation and error handling
* Command-line interface with menu-based navigation

## Modules

### 1. Patient Management

* Register new patients
* View all patients
* Search patients by ID or name
* Update patient information
* Delete patient records

### 2. Doctor Management

* Add doctors
* View doctors
* Search doctors by ID or name
* Update doctor information
* Assign doctors to departments
* Delete doctor records

### 3. Appointment Management

* Book appointments
* View appointments
* Search appointments
* Update appointment details
* Cancel appointments
* Maintain appointment status

### 4. Medical Records

* Add medical records
* Record diagnosis and prescriptions
* Store visit notes
* Search medical records
* Update and delete records

### 5. Billing

* Create bills
* Calculate total charges
* Track consultation, medicine, test, and other charges
* Track payment status
* Search and update bills
* Generate billing summaries

### 6. Reports

The system generates reports using SQL queries and aggregate functions, including:

* Total number of patients
* Patients by gender and blood group
* Total doctors
* Doctors by department
* Average consultation fee
* Appointments by status
* Appointments by doctor
* Medical records by doctor and diagnosis
* Total billing amount
* Paid and pending amounts

## Technologies Used

| Technology             | Purpose                                          |
| ---------------------- | ------------------------------------------------ |
| Python                 | Application logic and command-line interface     |
| MySQL                  | Database management                              |
| MySQL Connector/Python | Connecting Python with MySQL                     |
| SQL                    | Data storage, retrieval, updating, and reporting |

## SQL Concepts Used

This project demonstrates several important SQL concepts:

* `CREATE DATABASE`
* `CREATE TABLE`
* `INSERT`
* `SELECT`
* `WHERE`
* `LIKE`
* `UPDATE`
* `DELETE`
* `ORDER BY`
* `GROUP BY`
* Aggregate functions such as `COUNT()`, `SUM()`, and `AVG()`
* `JOIN`

## Database Structure

The database contains the following tables:

```text
healthcare_management
│
├── patients
├── departments
├── doctors
├── appointments
├── medical_records
└── billing
```

Relationships between records are maintained using their corresponding IDs and SQL `JOIN` operations.

## Requirements

* Python 3
* MySQL Server
* MySQL Connector/Python

Install the MySQL connector using:

```bash
pip install mysql-connector-python
```

## Setup

### 1. Create the Database

Open MySQL and create the database:

```sql
CREATE DATABASE healthcare_management;
```

### 2. Create the Tables

Run the SQL commands provided in `database.sql`.

### 3. Configure MySQL

Update the connection details in `healthcare_management.py`:

```python
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="healthcare_management"
)
```

### 4. Run the Program

From the project directory:

```bash
python3 healthcare_management.py
```

## Main Menu

```text
============================================================
          HEALTHCARE MANAGEMENT SYSTEM
============================================================

1. Patient Management
2. Doctor Management
3. Appointment Management
4. Medical Records
5. Billing
6. Reports
7. Exit
```

## Project Objectives

* To develop a practical database management application.
* To understand Python-MySQL connectivity.
* To apply SQL queries in a real-world scenario.
* To practice CRUD operations.
* To demonstrate the use of functions, loops, conditional statements, and exception handling.
* To generate meaningful reports from stored data.

## Future Improvements

Possible future enhancements include:

* Graphical User Interface
* User authentication and role-based access
* Appointment conflict detection
* Automated database backups
* PDF invoice generation
* Advanced reporting and analytics
* Improved input validation
* Web-based interface

## Author

**Kiswin**

Class 12 Student
Python & MySQL Academic Project

## Disclaimer

This project is developed for **educational and academic purposes**. It is a demonstration of database management and Python programming concepts and is not intended for use as a production healthcare system.
