```python
import mysql.connector
import os
from datetime import datetime

# DATABASE CONNECTION
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="healthcare_management"
)
cur = con.cursor()

# GENERAL FUNCTIONS
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header(location):
    clear_screen()
    print("=" * 60)
    print("          HEALTHCARE MANAGEMENT SYSTEM")
    print("          > " + location)
    print("=" * 60)

def pause():
    input("\nPress Enter to continue...")

# DATE AND TIME FORMATTING
def get_date(prompt):
    while True:
        value = input(prompt)
        if len(value) == 8 and value.isdigit():
            try:
                return datetime.strptime(value, "%d%m%Y").strftime("%Y-%m-%d")
            except ValueError:
                print("\nInvalid date. Please try again.")
        else:
            print("\nPlease enter exactly 8 digits.")

def get_time(prompt):
    while True:
        value = input(prompt)
        if len(value) == 6 and value.isdigit():
            try:
                return datetime.strptime(value, "%H%M%S").strftime("%H:%M:%S")
            except ValueError:
                print("\nInvalid time. Please try again.")
        else:
            print("\nPlease enter exactly 6 digits.")

# PATIENT MANAGEMENT
def patient_menu():
    while True:
        show_header("PATIENT MANAGEMENT")
        print("1. Register New Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Back to Main Menu")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            update_patient()
        elif choice == "5":
            delete_patient()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice.")
            pause()

# ADD PATIENT
def add_patient():
    show_header("PATIENT MANAGEMENT > REGISTER PATIENT")
    print("Enter Patient Details")
    print("-" * 60)

    name = input("Patient Name       : ")
    gender = input("Gender             : ")
    date_of_birth = get_date("Date of Birth (DDMMYYYY): ")
    phone = input("Phone Number       : ")
    address = input("Address            : ")
    blood_group = input("Blood Group        : ")
    emergency_contact = input("Emergency Contact  : ")
    registration_date = get_date("Registration Date (DDMMYYYY): ")

    query = """
    INSERT INTO patients
    (name, gender, date_of_birth, phone, address,
     blood_group, emergency_contact, registration_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        name, gender, date_of_birth, phone, address,
        blood_group, emergency_contact, registration_date
    )

    try:
        cur.execute(query, values)
        con.commit()
        patient_id = cur.lastrowid
        print("\nPatient registered successfully!")
        print("Patient ID:", patient_id)
    except mysql.connector.Error as err:
        print("\nError registering patient.")
        print("Error:", err)
    pause()

# VIEW PATIENTS
def view_patients():
    show_header("PATIENT MANAGEMENT > VIEW PATIENTS")
    cur.execute("SELECT * FROM patients ORDER BY patient_id")
    records = cur.fetchall()

    if len(records) == 0:
        print("No patients found.")
    else:
        print("PATIENT LIST")
        print("-" * 95)
        print(
            f"{'ID':<5}"
            f"{'NAME':<20}"
            f"{'GENDER':<10}"
            f"{'DOB':<12}"
            f"{'PHONE':<13}"
            f"{'BLOOD':<8}"
            f"{'REG DATE':<12}"
        )
        print("-" * 95)

        for record in records:
            print(
                f"{record[0]:<5}"
                f"{record[1]:<20}"
                f"{record[2]:<10}"
                f"{str(record[3]):<12}"
                f"{record[4]:<13}"
                f"{record[6]:<8}"
                f"{str(record[8]):<12}"
            )
        print("-" * 95)
    pause()

# SEARCH PATIENT
def search_patient():
    show_header("PATIENT MANAGEMENT > SEARCH PATIENT")
    print("1. Search by Patient ID")
    print("2. Search by Patient Name")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        patient_id = input("\nEnter Patient ID: ")
        query = """
        SELECT *
        FROM patients
        WHERE patient_id = %s
        """
        cur.execute(query, (patient_id,))
    elif choice == "2":
        name = input("\nEnter Patient Name: ")
        query = """
        SELECT *
        FROM patients
        WHERE name LIKE %s
        """
        cur.execute(query, ("%" + name + "%",))
    else:
        print("\nInvalid choice.")
        pause()
        return

    records = cur.fetchall()

    if len(records) == 0:
        print("\nNo patient found.")
    else:
        print("\nPATIENT DETAILS")
        print("-" * 60)

        for record in records:
            print("Patient ID        :", record[0])
            print("Name              :", record[1])
            print("Gender            :", record[2])
            print("Date of Birth     :", record[3])
            print("Phone             :", record[4])
            print("Address           :", record[5])
            print("Blood Group       :", record[6])
            print("Emergency Contact :", record[7])
            print("Registration Date :", record[8])
            print("-" * 60)
    pause()

# UPDATE PATIENT
def update_patient():
    show_header("PATIENT MANAGEMENT > UPDATE PATIENT")
    patient_id = input("Enter Patient ID: ")

    cur.execute(
        "SELECT * FROM patients WHERE patient_id = %s",
        (patient_id,)
    )
    record = cur.fetchone()

    if record is None:
        print("\nPatient not found.")
        pause()
        return

    print("\nPatient found:")
    print("-" * 50)
    print("Patient ID   :", record[0])
    print("Name         :", record[1])
    print("Gender       :", record[2])
    print("Date of Birth:", record[3])
    print("Phone        :", record[4])
    print("Address      :", record[5])
    print("Blood Group  :", record[6])
    print("Emergency    :", record[7])
    print("-" * 50)

    print("\nWhat do you want to update?")
    print("1. Name")
    print("2. Gender")
    print("3. Date of Birth")
    print("4. Phone Number")
    print("5. Address")
    print("6. Blood Group")
    print("7. Emergency Contact")
    print("8. Cancel")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        new_value = input("Enter new name: ")
        query = """
        UPDATE patients
        SET name = %s
        WHERE patient_id = %s
        """
    elif choice == "2":
        new_value = input("Enter new gender: ")
        query = """
        UPDATE patients
        SET gender = %s
        WHERE patient_id = %s
        """
    elif choice == "3":
        new_value = get_date("Enter new date of birth (DDMMYYYY): ")
        query = """
        UPDATE patients
        SET date_of_birth = %s
        WHERE patient_id = %s
        """
    elif choice == "4":
        new_value = input("Enter new phone number: ")
        query = """
        UPDATE patients
        SET phone = %s
        WHERE patient_id = %s
        """
    elif choice == "5":
        new_value = input("Enter new address: ")
        query = """
        UPDATE patients
        SET address = %s
        WHERE patient_id = %s
        """
    elif choice == "6":
        new_value = input("Enter new blood group: ")
        query = """
        UPDATE patients
        SET blood_group = %s
        WHERE patient_id = %s
        """
    elif choice == "7":
        new_value = input("Enter new emergency contact: ")
        query = """
        UPDATE patients
        SET emergency_contact = %s
        WHERE patient_id = %s
        """
    elif choice == "8":
        return
    else:
        print("\nInvalid choice.")
        pause()
        return

    try:
        cur.execute(query, (new_value, patient_id))
        con.commit()
        print("\nPatient information updated successfully!")
    except mysql.connector.Error as err:
        print("\nError updating patient.")
        print("Error:", err)
    pause()

# DELETE PATIENT
def delete_patient():
    show_header("PATIENT MANAGEMENT > DELETE PATIENT")
    patient_id = input("Enter Patient ID: ")

    cur.execute(
        "SELECT * FROM patients WHERE patient_id = %s",
        (patient_id,)
    )
    record = cur.fetchone()

    if record is None:
        print("\nPatient not found.")
        pause()
        return

    print("\nPatient found:")
    print("-" * 50)
    print("Patient ID        :", record[0])
    print("Name              :", record[1])
    print("Gender            :", record[2])
    print("Date of Birth     :", record[3])
    print("Phone             :", record[4])
    print("Address           :", record[5])
    print("Blood Group       :", record[6])
    print("Emergency Contact :", record[7])
    print("Registration Date :", record[8])
    print("-" * 50)

    cur.execute(
        """
        SELECT COUNT(*)
        FROM appointments
        WHERE patient_id = %s
        """,
        (patient_id,)
    )
    appointment_count = cur.fetchone()[0]

    if appointment_count > 0:
        print("\nThis patient has", appointment_count, "appointment(s).")
        print("Delete or cancel the appointments before deleting the patient.")
        pause()
        return

    confirm = input(
        "\nAre you sure you want to delete this patient? (Y/N): "
    )

    if confirm.upper() == "Y":
        try:
            cur.execute(
                "DELETE FROM patients WHERE patient_id = %s",
                (patient_id,)
            )
            con.commit()
            print("\nPatient deleted successfully!")
        except mysql.connector.Error as err:
            print("\nError deleting patient.")
            print("Error:", err)
    else:
        print("\nDeletion cancelled.")
    pause()

# DEPARTMENT MANAGEMENT
def department_menu():
    while True:
        show_header("DEPARTMENT MANAGEMENT")
        print("1. Add Department")
        print("2. View All Departments")
        print("3. Search Department")
        print("4. Update Department")
        print("5. Delete Department")
        print("6. Back to Main Menu")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_department()
        elif choice == "2":
            view_departments()
        elif choice == "3":
            search_department()
        elif choice == "4":
            update_department()
        elif choice == "5":
            delete_department()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice.")
            pause()

# ADD DEPARTMENT
def add_department():
    show_header("DEPARTMENT MANAGEMENT > ADD DEPARTMENT")
    print("Enter Department Details")
    print("-" * 60)

    department_name = input("Department Name : ")
    location = input("Location         : ")

    query = """
    INSERT INTO departments
    (department_name, location)
    VALUES (%s, %s)
    """

    try:
        cur.execute(query, (department_name, location))
        con.commit()
        department_id = cur.lastrowid
        print("\nDepartment added successfully!")
        print("Department ID:", department_id)
    except mysql.connector.Error as err:
        print("\nError adding department.")
        print("Error:", err)
    pause()

# VIEW DEPARTMENTS
def view_departments():
    show_header("DEPARTMENT MANAGEMENT > VIEW DEPARTMENTS")
    cur.execute("""
        SELECT *
        FROM departments
        ORDER BY department_id
    """)
    records = cur.fetchall()

    if len(records) == 0:
        print("No departments found.")
    else:
        print("DEPARTMENT LIST")
        print("-" * 60)
        print(
            f"{'ID':<5}"
            f"{'DEPARTMENT':<30}"
            f"{'LOCATION':<20}"
        )
        print("-" * 60)

        for record in records:
            print(
                f"{record[0]:<5}"
                f"{record[1]:<30}"
                f"{record[2]:<20}"
            )
        print("-" * 60)
    pause()

# SEARCH DEPARTMENT
def search_department():
    show_header("DEPARTMENT MANAGEMENT > SEARCH DEPARTMENT")
    print("1. Search by Department ID")
    print("2. Search by Department Name")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        department_id = input("\nEnter Department ID: ")
        query = """
        SELECT *
        FROM departments
        WHERE department_id = %s
        """
        cur.execute(query, (department_id,))
    elif choice == "2":
        name = input("\nEnter Department Name: ")
        query = """
        SELECT *
        FROM departments
        WHERE department_name LIKE %s
        """
        cur.execute(query, ("%" + name + "%",))
    else:
        print("\nInvalid choice.")
        pause()
        return

    records = cur.fetchall()

    if len(records) == 0:
        print("\nNo department found.")
    else:
        print("\nDEPARTMENT DETAILS")
        print("-" * 50)

        for record in records:
            print("Department ID   :", record[0])
            print("Department Name :", record[1])
            print("Location        :", record[2])
            print("-" * 50)
    pause()

# UPDATE DEPARTMENT
def update_department():
    show_header("DEPARTMENT MANAGEMENT > UPDATE DEPARTMENT")
    department_id = input("Enter Department ID: ")

    cur.execute("""
        SELECT *
        FROM departments
        WHERE department_id = %s
    """, (department_id,))
    record = cur.fetchone()

    if record is None:
        print("\nDepartment not found.")
        pause()
        return

    print("\nDepartment found:")
    print("-" * 50)
    print("Department ID   :", record[0])
    print("Department Name :", record[1])
    print("Location        :", record[2])
    print("-" * 50)

    print("\nWhat do you want to update?")
    print("1. Department Name")
    print("2. Location")
    print("3. Cancel")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        new_value = input("Enter new department name: ")
        query = """
        UPDATE departments
        SET department_name = %s
        WHERE department_id = %s
        """
    elif choice == "2":
        new_value = input("Enter new location: ")
        query = """
        UPDATE departments
        SET location = %s
        WHERE department_id = %s
        """
    elif choice == "3":
        return
    else:
        print("\nInvalid choice.")
        pause()
        return

    try:
        cur.execute(query, (new_value, department_id))
        con.commit()
        print("\nDepartment updated successfully!")
    except mysql.connector.Error as err:
        print("\nError updating department.")
        print("Error:", err)
    pause()

# DELETE DEPARTMENT
def delete_department():
    show_header("DEPARTMENT MANAGEMENT > DELETE DEPARTMENT")
    department_id = input("Enter Department ID: ")

    cur.execute("""
        SELECT *
        FROM departments
        WHERE department_id = %s
    """, (department_id,))
    record = cur.fetchone()

    if record is None:
        print("\nDepartment not found.")
        pause()
        return

    print("\nDepartment found:")
    print("-" * 50)
    print("Department ID   :", record[0])
    print("Department Name :", record[1])
    print("Location        :", record[2])
    print("-" * 50)

    cur.execute("""
        SELECT COUNT(*)
        FROM doctors
        WHERE department_id = %s
    """, (department_id,))
    doctor_count = cur.fetchone()[0]

    if doctor_count > 0:
        print("\nThis department has", doctor_count, "doctor(s).")
        print("Change or remove the doctors before deleting the department.")
        pause()
        return

    confirm = input(
        "\nAre you sure you want to delete this department? (Y/N): "
    )

    if confirm.upper() == "Y":
        try:
            cur.execute(
                "DELETE FROM departments WHERE department_id = %s",
                (department_id,)
            )
            con.commit()
            print("\nDepartment deleted successfully!")
        except mysql.connector.Error as err:
            print("\nError deleting department.")
            print("Error:", err)
    else:
        print("\nDeletion cancelled.")
    pause()

# DOCTOR MANAGEMENT
def doctor_menu():
    while True:
        show_header("DOCTOR MANAGEMENT")
        print("1. Add New Doctor")
        print("2. View All Doctors")
        print("3. Search Doctor")
        print("4. Update Doctor")
        print("5. Delete Doctor")
        print("6. Back to Main Menu")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_doctor()
        elif choice == "2":
            view_doctors()
        elif choice == "3":
            search_doctor()
        elif choice == "4":
            update_doctor()
        elif choice == "5":
            delete_doctor()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice.")
            pause()

# ADD DOCTOR
def add_doctor():
    show_header("DOCTOR MANAGEMENT > ADD DOCTOR")
    print("Enter Doctor Details")
    print("-" * 60)

    name = input("Doctor Name       : ")
    specialization = input("Specialization     : ")

    print("\nAvailable Departments")
    print("-" * 50)

    cur.execute("""
        SELECT department_id, department_name
        FROM departments
        ORDER BY department_id
    """)
    records = cur.fetchall()

    if len(records) == 0:
        print("No departments found.")
        pause()
        return

    for record in records:
        print(record[0], "-", record[1])

    while True:
        department_id = input("\nEnter Department ID: ")
        cur.execute("""
            SELECT *
            FROM departments
            WHERE department_id = %s
        """, (department_id,))
        department = cur.fetchone()

        if department is not None:
            break

        print("\nDepartment not found. Please try again.")

    phone = input("Phone Number       : ")
    consultation_fee = input("Consultation Fee   : ")

    query = """
    INSERT INTO doctors
    (name, specialization, department_id,
     phone, consultation_fee)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        name, specialization, department_id,
        phone, consultation_fee
    )

    try:
        cur.execute(query, values)
        con.commit()
        doctor_id = cur.lastrowid
        print("\nDoctor added successfully!")
        print("Doctor ID:", doctor_id)
    except mysql.connector.Error as err:
        print("\nError adding doctor.")
        print("Error:", err)
    pause()

# VIEW DOCTORS
def view_doctors():
    show_header("DOCTOR MANAGEMENT > VIEW DOCTORS")

    query = """
    SELECT doctors.doctor_id, doctors.name,
           doctors.specialization, departments.department_name,
           doctors.phone, doctors.consultation_fee
    FROM doctors
    JOIN departments
        ON doctors.department_id = departments.department_id
    ORDER BY doctors.doctor_id
    """
    cur.execute(query)
    records = cur.fetchall()

    if len(records) == 0:
        print("No doctors found.")
    else:
        print("DOCTOR LIST")
        print("-" * 100)
        print(
            f"{'ID':<5}"
            f"{'NAME':<20}"
            f"{'SPECIALIZATION':<22}"
            f"{'DEPARTMENT':<18}"
            f"{'PHONE':<13}"
            f"{'FEE':<10}"
        )
        print("-" * 100)

        for record in records:
            print(
                f"{record[0]:<5}"
                f"{record[1]:<20}"
                f"{record[2]:<22}"
                f"{record[3]:<18}"
                f"{record[4]:<13}"
                f"{record[5]:<10}"
            )
        print("-" * 100)
    pause()

# SEARCH DOCTOR
def search_doctor():
    show_header("DOCTOR MANAGEMENT > SEARCH DOCTOR")
    print("1. Search by Doctor ID")
    print("2. Search by Doctor Name")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        doctor_id = input("\nEnter Doctor ID: ")
        query = """
        SELECT doctors.doctor_id, doctors.name,
               doctors.specialization, departments.department_name,
               doctors.phone, doctors.consultation_fee
        FROM doctors
        JOIN departments
            ON doctors.department_id = departments.department_id
        WHERE doctors.doctor_id = %s
        """
        cur.execute(query, (doctor_id,))
    elif choice == "2":
        name = input("\nEnter Doctor Name: ")
        query = """
        SELECT doctors.doctor_id, doctors.name,
               doctors.specialization, departments.department_name,
               doctors.phone, doctors.consultation_fee
        FROM doctors
        JOIN departments
            ON doctors.department_id = departments.department_id
        WHERE doctors.name LIKE %s
        """
        cur.execute(query, ("%" + name + "%",))
    else:
        print("\nInvalid choice.")
        pause()
        return

    records = cur.fetchall()

    if len(records) == 0:
        print("\nNo doctor found.")
    else:
        print("\nDOCTOR DETAILS")
        print("-" * 60)

        for record in records:
            print("Doctor ID        :", record[0])
            print("Name             :", record[1])
            print("Specialization   :", record[2])
            print("Department       :", record[3])
            print("Phone            :", record[4])
            print("Consultation Fee :", record[5])
            print("-" * 60)
    pause()

# UPDATE DOCTOR
def update_doctor():
    show_header("DOCTOR MANAGEMENT > UPDATE DOCTOR")
    doctor_id = input("Enter Doctor ID: ")

    query = """
    SELECT doctors.doctor_id, doctors.name,
           doctors.specialization, departments.department_name,
           doctors.phone, doctors.consultation_fee
    FROM doctors
    JOIN departments
        ON doctors.department_id = departments.department_id
    WHERE doctors.doctor_id = %s
    """
    cur.execute(query, (doctor_id,))
    record = cur.fetchone()

    if record is None:
        print("\nDoctor not found.")
        pause()
        return

    print("\nDoctor found:")
    print("-" * 60)
    print("Doctor ID        :", record[0])
    print("Name             :", record[1])
    print("Specialization   :", record[2])
    print("Department       :", record[3])
    print("Phone            :", record[4])
    print("Consultation Fee :", record[5])
    print("-" * 60)

    print("\nWhat do you want to update?")
    print("1. Name")
    print("2. Specialization")
    print("3. Department")
    print("4. Phone Number")
    print("5. Consultation Fee")
    print("6. Cancel")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        new_value = input("Enter new doctor name: ")
        query = """
        UPDATE doctors
        SET name = %s
        WHERE doctor_id = %s
        """
    elif choice == "2":
        new_value = input("Enter new specialization: ")
        query = """
        UPDATE doctors
        SET specialization = %s
        WHERE doctor_id = %s
        """
    elif choice == "3":
        print("\nAvailable Departments")
        print("-" * 40)

        cur.execute("""
            SELECT department_id, department_name
            FROM departments
            ORDER BY department_id
        """)
        records = cur.fetchall()

        for department in records:
            print(department[0], "-", department[1])

        while True:
            new_value = input("\nEnter new Department ID: ")
            cur.execute("""
                SELECT *
                FROM departments
                WHERE department_id = %s
            """, (new_value,))
            department = cur.fetchone()

            if department is not None:
                break

            print("\nDepartment not found. Please try again.")

        query = """
        UPDATE doctors
        SET department_id = %s
        WHERE doctor_id = %s
        """
    elif choice == "4":
        new_value = input("Enter new phone number: ")
        query = """
        UPDATE doctors
        SET phone = %s
        WHERE doctor_id = %s
        """
    elif choice == "5":
        new_value = input("Enter new consultation fee: ")
        query = """
        UPDATE doctors
        SET consultation_fee = %s
        WHERE doctor_id = %s
        """
    elif choice == "6":
        return
    else:
        print("\nInvalid choice.")
        pause()
        return

    try:
        cur.execute(query, (new_value, doctor_id))
        con.commit()
        print("\nDoctor information updated successfully!")
    except mysql.connector.Error as err:
        print("\nError updating doctor.")
        print("Error:", err)
    pause()

# DELETE DOCTOR
def delete_doctor():
    show_header("DOCTOR MANAGEMENT > DELETE DOCTOR")
    doctor_id = input("Enter Doctor ID: ")

    cur.execute(
        "SELECT * FROM doctors WHERE doctor_id = %s",
        (doctor_id,)
    )
    record = cur.fetchone()

    if record is None:
        print("\nDoctor not found.")
        pause()
        return

    print("\nDoctor found:")
    print("-" * 50)
    print("Doctor ID        :", record[0])
    print("Name             :", record[1])
    print("Specialization   :", record[2])
    print("Department ID    :", record[3])
    print("Phone            :", record[4])
    print("Consultation Fee :", record[5])
    print("-" * 50)

    cur.execute("""
        SELECT COUNT(*)
        FROM appointments
        WHERE doctor_id = %s
    """, (doctor_id,))
    appointment_count = cur.fetchone()[0]

    if appointment_count > 0:
        print("\nThis doctor has", appointment_count, "appointment(s).")
        print("Cancel or change those appointments before deleting the doctor.")
        pause()
        return

    confirm = input(
        "\nAre you sure you want to delete this doctor? (Y/N): "
    )

    if confirm.upper() == "Y":
        try:
            cur.execute(
                "DELETE FROM doctors WHERE doctor_id = %s",
                (doctor_id,)
            )
            con.commit()
            print("\nDoctor deleted successfully!")
        except mysql.connector.Error as err:
            print("\nError deleting doctor.")
            print("Error:", err)
    else:
        print("\nDeletion cancelled.")
    pause()

# APPOINTMENT MANAGEMENT
def appointment_menu():
    while True:
        show_header("APPOINTMENT MANAGEMENT")
        print("1. Book New Appointment")
        print("2. View All Appointments")
        print("3. Search Appointment")
        print("4. Update Appointment")
        print("5. Cancel Appointment")
        print("6. Back to Main Menu")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_appointment()
        elif choice == "2":
            view_appointments()
        elif choice == "3":
            search_appointment()
        elif choice == "4":
            update_appointment()
        elif choice == "5":
            delete_appointment()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice.")
            pause()

# ADD APPOINTMENT
def add_appointment():
    show_header("APPOINTMENT MANAGEMENT > BOOK APPOINTMENT")
    print("Enter Appointment Details")
    print("-" * 60)

    print("\nAvailable Patients")
    print("-" * 40)

    cur.execute("""
        SELECT patient_id, name
        FROM patients
        ORDER BY patient_id
    """)
    records = cur.fetchall()

    if len(records) == 0:
        print("No patients found.")
        pause()
        return

    for record in records:
        print(record[0], "-", record[1])

    while True:
        patient_id = input("\nEnter Patient ID: ")
        cur.execute("""
            SELECT *
            FROM patients
            WHERE patient_id = %s
        """, (patient_id,))
        patient = cur.fetchone()

        if patient is not None:
            break

        print("\nPatient not found. Please try again.")

    print("\nAvailable Doctors")
    print("-" * 60)

    query = """
    SELECT doctors.doctor_id, doctors.name,
           doctors.specialization, departments.department_name
    FROM doctors
    JOIN departments
        ON doctors.department_id = departments.department_id
    ORDER BY doctors.doctor_id
    """
    cur.execute(query)
    records = cur.fetchall()

    if len(records) == 0:
        print("No doctors found.")
        pause()
        return

    for record in records:
        print(
            record[0], "-", record[1],
            "|", record[2], "|", record[3]
        )

    while True:
        doctor_id = input("\nEnter Doctor ID: ")
        cur.execute("""
            SELECT *
            FROM doctors
            WHERE doctor_id = %s
        """, (doctor_id,))
        doctor = cur.fetchone()

        if doctor is not None:
            break

        print("\nDoctor not found. Please try again.")

    appointment_date = get_date(
        "\nAppointment Date (DDMMYYYY): "
    )
    appointment_time = get_time(
        "Appointment Time (HHMMSS): "
    )
    reason = input("Reason for Appointment: ")
    status = "Scheduled"

    query = """
    INSERT INTO appointments
    (patient_id, doctor_id, appointment_date,
     appointment_time, status, reason)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        patient_id, doctor_id, appointment_date,
        appointment_time, status, reason
    )

    try:
        cur.execute(query, values)
        con.commit()
        appointment_id = cur.lastrowid
        print("\nAppointment booked successfully!")
        print("Appointment ID:", appointment_id)
    except mysql.connector.Error as err:
        print("\nError booking appointment.")
        print("Error:", err)
    pause()

# VIEW APPOINTMENTS
def view_appointments():
    show_header("APPOINTMENT MANAGEMENT > VIEW APPOINTMENTS")

    query = """
    SELECT appointments.appointment_id,
           patients.name AS patient_name,
           doctors.name AS doctor_name,
           appointments.appointment_date,
           appointments.appointment_time,
           appointments.status
    FROM appointments
    JOIN patients
        ON appointments.patient_id = patients.patient_id
    JOIN doctors
        ON appointments.doctor_id = doctors.doctor_id
    ORDER BY appointments.appointment_date,
             appointments.appointment_time
    """
    cur.execute(query)
    records = cur.fetchall()

    if len(records) == 0:
        print("No appointments found.")
    else:
        print("APPOINTMENT LIST")
        print("-" * 105)
        print(
            f"{'ID':<5}"
            f"{'PATIENT':<20}"
            f"{'DOCTOR':<20}"
            f"{'DATE':<12}"
            f"{'TIME':<10}"
            f"{'STATUS':<15}"
        )
        print("-" * 105)

        for record in records:
            print(
                f"{record[0]:<5}"
                f"{record[1]:<20}"
                f"{record[2]:<20}"
                f"{str(record[3]):<12}"
                f"{str(record[4]):<10}"
                f"{record[5]:<15}"
            )
        print("-" * 105)
    pause()

# SEARCH APPOINTMENT
def search_appointment():
    show_header("APPOINTMENT MANAGEMENT > SEARCH APPOINTMENT")
    print("1. Search by Appointment ID")
    print("2. Search by Patient Name")
    print("3. Search by Doctor Name")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        appointment_id = input("\nEnter Appointment ID: ")
        query = """
        SELECT appointments.appointment_id,
               patients.name AS patient_name,
               doctors.name AS doctor_name,
               appointments.appointment_date,
               appointments.appointment_time,
               appointments.status,
               appointments.reason
        FROM appointments
        JOIN patients
            ON appointments.patient_id = patients.patient_id
        JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
        WHERE appointments.appointment_id = %s
        """
        cur.execute(query, (appointment_id,))
    elif choice == "2":
        name = input("\nEnter Patient Name: ")
        query = """
        SELECT appointments.appointment_id,
               patients.name AS patient_name,
               doctors.name AS doctor_name,
               appointments.appointment_date,
               appointments.appointment_time,
               appointments.status,
               appointments.reason
        FROM appointments
        JOIN patients
            ON appointments.patient_id = patients.patient_id
        JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
        WHERE patients.name LIKE %s
        ORDER BY appointments.appointment_date
        """
        cur.execute(query, ("%" + name + "%",))
    elif choice == "3":
        name = input("\nEnter Doctor Name: ")
        query = """
        SELECT appointments.appointment_id,
               patients.name AS patient_name,
               doctors.name AS doctor_name,
               appointments.appointment_date,
               appointments.appointment_time,
               appointments.status,
               appointments.reason
        FROM appointments
        JOIN patients
            ON appointments.patient_id = patients.patient_id
        JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
        WHERE doctors.name LIKE %s
        ORDER BY appointments.appointment_date
        """
        cur.execute(query, ("%" + name + "%",))
    else:
        print("\nInvalid choice.")
        pause()
        return

    records = cur.fetchall()

    if len(records) == 0:
        print("\nNo appointment found.")
    else:
        print("\nAPPOINTMENT DETAILS")
        print("-" * 60)

        for record in records:
            print("Appointment ID :", record[0])
            print("Patient        :", record[1])
            print("Doctor         :", record[2])
            print("Date           :", record[3])
            print("Time           :", record[4])
            print("Status         :", record[5])
            print("Reason         :", record[6])
            print("-" * 60)
    pause()

# UPDATE APPOINTMENT
def update_appointment():
    show_header("APPOINTMENT MANAGEMENT > UPDATE APPOINTMENT")
    appointment_id = input("Enter Appointment ID: ")

    query = """
    SELECT appointments.appointment_id,
           patients.name AS patient_name,
           doctors.name AS doctor_name,
           appointments.appointment_date,
           appointments.appointment_time,
           appointments.status,
           appointments.reason
    FROM appointments
    JOIN patients
        ON appointments.patient_id = patients.patient_id
    JOIN doctors
        ON appointments.doctor_id = doctors.doctor_id
    WHERE appointments.appointment_id = %s
    """
    cur.execute(query, (appointment_id,))
    record = cur.fetchone()

    if record is None:
        print("\nAppointment not found.")
        pause()
        return

    print("\nAppointment found:")
    print("-" * 60)
    print("Appointment ID :", record[0])
    print("Patient        :", record[1])
    print("Doctor         :", record[2])
    print("Date           :", record[3])
    print("Time           :", record[4])
    print("Status         :", record[5])
    print("Reason         :", record[6])
    print("-" * 60)

    print("\nWhat do you want to update?")
    print("1. Appointment Date")
    print("2. Appointment Time")
    print("3. Doctor")
    print("4. Status")
    print("5. Reason")
    print("6. Cancel")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        new_value = get_date(
            "Enter new appointment date (DDMMYYYY): "
        )
        query = """
        UPDATE appointments
        SET appointment_date = %s
        WHERE appointment_id = %s
        """
    elif choice == "2":
        new_value = get_time(
            "Enter new appointment time (HHMMSS): "
        )
        query = """
        UPDATE appointments
        SET appointment_time = %s
        WHERE appointment_id = %s
        """
    elif choice == "3":
        print("\nAvailable Doctors")
        print("-" * 60)

        query = """
        SELECT doctors.doctor_id, doctors.name,
               doctors.specialization, departments.department_name
        FROM doctors
        JOIN departments
            ON doctors.department_id = departments.department_id
        ORDER BY doctors.doctor_id
        """
        cur.execute(query)
        records = cur.fetchall()

        for doctor in records:
            print(
                doctor[0], "-", doctor[1],
                "|", doctor[2], "|", doctor[3]
            )

        while True:
            new_value = input("\nEnter new Doctor ID: ")
            cur.execute("""
                SELECT *
                FROM doctors
                WHERE doctor_id = %s
            """, (new_value,))
            doctor = cur.fetchone()

            if doctor is not None:
                break

            print("\nDoctor not found. Please try again.")

        query = """
        UPDATE appointments
        SET doctor_id = %s
        WHERE appointment_id = %s
        """
    elif choice == "4":
        print("\nAppointment Status")
        print("-" * 30)
        print("1. Scheduled")
        print("2. Completed")
        print("3. Cancelled")
        status_choice = input("\nEnter status choice: ")

        if status_choice == "1":
            new_value = "Scheduled"
        elif status_choice == "2":
            new_value = "Completed"
        elif status_choice == "3":
            new_value = "Cancelled"
        else:
            print("\nInvalid status.")
            pause()
            return

        query = """
        UPDATE appointments
        SET status = %s
        WHERE appointment_id = %s
        """
    elif choice == "5":
        new_value = input("Enter new reason: ")
        query = """
        UPDATE appointments
        SET reason = %s
        WHERE appointment_id = %s
        """
    elif choice == "6":
        return
    else:
        print("\nInvalid choice.")
        pause()
        return

    try:
        cur.execute(query, (new_value, appointment_id))
        con.commit()
        print("\nAppointment updated successfully!")
    except mysql.connector.Error as err:
        print("\nError updating appointment.")
        print("Error:", err)
    pause()

# CANCEL APPOINTMENT
def delete_appointment():
    show_header("APPOINTMENT MANAGEMENT > CANCEL APPOINTMENT")
    appointment_id = input("Enter Appointment ID: ")

    query = """
    SELECT appointments.appointment_id,
           patients.name AS patient_name,
           doctors.name AS doctor_name,
           appointments.appointment_date,
           appointments.appointment_time,
           appointments.status,
           appointments.reason
    FROM appointments
    JOIN patients
        ON appointments.patient_id = patients.patient_id
    JOIN doctors
        ON appointments.doctor_id = doctors.doctor_id
    WHERE appointments.appointment_id = %s
    """
    cur.execute(query, (appointment_id,))
    record = cur.fetchone()

    if record is None:
        print("\nAppointment not found.")
        pause()
        return

    print("\nAppointment found:")
    print("-" * 60)
    print("Appointment ID :", record[0])
    print("Patient        :", record[1])
    print("Doctor         :", record[2])
    print("Date           :", record[3])
    print("Time           :", record[4])
    print("Status         :", record[5])
    print("Reason         :", record[6])
    print("-" * 60)

    if record[5] == "Cancelled":
        print("\nThis appointment is already cancelled.")
        pause()
        return

    confirm = input(
        "\nAre you sure you want to cancel this appointment? (Y/N): "
    )

    if confirm.upper() == "Y":
        try:
            query = """
            UPDATE appointments
            SET status = 'Cancelled'
            WHERE appointment_id = %s
            """
            cur.execute(query, (appointment_id,))
            con.commit()
            print("\nAppointment cancelled successfully!")
        except mysql.connector.Error as err:
            print("\nError cancelling appointment.")
            print("Error:", err)
    else:
        print("\nCancellation cancelled.")
    pause()

# MAIN MENU
def main_menu():
    while True:
        show_header("MAIN MENU")
        print("1. Patient Management")
        print("2. Department Management")
        print("3. Doctor Management")
        print("4. Appointment Management")
        print("5. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            patient_menu()
        elif choice == "2":
            department_menu()
        elif choice == "3":
            doctor_menu()
        elif choice == "4":
            appointment_menu()
        elif choice == "5":
            print("\nThank you for using Healthcare Management System.")
            break
        else:
            print("\nInvalid choice.")
            pause()

# PROGRAM START
main_menu()
cur.close()
con.close()
```
