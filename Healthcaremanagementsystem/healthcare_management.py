import mysql.connector
import os
from datetime import datetime

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="healthcare_management"
)

cur = con.cursor()


# --------------------------------------------------
# SCREEN FUNCTIONS
# --------------------------------------------------

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


# --------------------------------------------------
# PATIENT MANAGEMENT
# --------------------------------------------------

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


# --------------------------------------------------
# PATIENT FUNCTIONS
# --------------------------------------------------

def add_patient():

    show_header("PATIENT MANAGEMENT > REGISTER PATIENT")

    print("Enter Patient Details")
    print("-" * 60)

    name = input("Patient Name       : ")
    gender = input("Gender             : ")

    # Get Date of Birth
    while True:

        date_of_birth = input(
            "Date of Birth (DD-MM-YYYY): "
        )

        try:

            date_of_birth = datetime.strptime(
                date_of_birth,
                "%d-%m-%Y"
            ).strftime("%Y-%m-%d")

            break

        except ValueError:

            print(
                "\nInvalid date format."
                "\nPlease enter the date like 23-08-2008."
            )

    phone = input("Phone Number       : ")
    address = input("Address            : ")
    blood_group = input("Blood Group        : ")
    emergency_contact = input("Emergency Contact  : ")

    # Get Registration Date
    while True:

        registration_date = input(
            "Registration Date (DD-MM-YYYY): "
        )

        try:

            registration_date = datetime.strptime(
                registration_date,
                "%d-%m-%Y"
            ).strftime("%Y-%m-%d")

            break

        except ValueError:

            print(
                "\nInvalid date format."
                "\nPlease enter the date like 03-09-2026."
            )

    query = """
    INSERT INTO patients
    (name, gender, date_of_birth, phone, address,
     blood_group, emergency_contact, registration_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        name,
        gender,
        date_of_birth,
        phone,
        address,
        blood_group,
        emergency_contact,
        registration_date
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

def view_patients():

    show_header("PATIENT MANAGEMENT > VIEW PATIENTS")

    cur.execute("SELECT * FROM patients")

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
def search_patient():

    show_header("PATIENT MANAGEMENT > SEARCH PATIENT")

    print("1. Search by Patient ID")
    print("2. Search by Patient Name")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        patient_id = input("\nEnter Patient ID: ")

        query = "SELECT * FROM patients WHERE patient_id = %s"

        cur.execute(query, (patient_id,))

    elif choice == "2":

        name = input("\nEnter Patient Name: ")

        query = "SELECT * FROM patients WHERE name LIKE %s"

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

def update_patient():

    show_header("PATIENT MANAGEMENT > UPDATE PATIENT")

    patient_id = input("Enter Patient ID: ")

    # Check whether patient exists
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
    print("Patient ID  :", record[0])
    print("Name        :", record[1])
    print("Gender      :", record[2])
    print("Date of Birth:", record[3])
    print("Phone       :", record[4])
    print("Address     :", record[5])
    print("Blood Group :", record[6])
    print("Emergency   :", record[7])
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

        query = "UPDATE patients SET name = %s WHERE patient_id = %s"

    elif choice == "2":

        new_value = input("Enter new gender: ")

        query = "UPDATE patients SET gender = %s WHERE patient_id = %s"

    elif choice == "3":

        new_value = input("Enter new date of birth (YYYY-MM-DD): ")

        query = "UPDATE patients SET date_of_birth = %s WHERE patient_id = %s"

    elif choice == "4":

        new_value = input("Enter new phone number: ")

        query = "UPDATE patients SET phone = %s WHERE patient_id = %s"

    elif choice == "5":

        new_value = input("Enter new address: ")

        query = "UPDATE patients SET address = %s WHERE patient_id = %s"

    elif choice == "6":

        new_value = input("Enter new blood group: ")

        query = "UPDATE patients SET blood_group = %s WHERE patient_id = %s"

    elif choice == "7":

        new_value = input("Enter new emergency contact: ")

        query = "UPDATE patients SET emergency_contact = %s WHERE patient_id = %s"

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
def delete_patient():

    show_header("PATIENT MANAGEMENT > DELETE PATIENT")

    patient_id = input("Enter Patient ID: ")

    # Check whether patient exists
    cur.execute(
        "SELECT * FROM patients WHERE patient_id = %s",
        (patient_id,)
    )

    record = cur.fetchone()

    if record is None:

        print("\nPatient not found.")
        pause()
        return

    # Display patient details
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

    # Ask for confirmation
    confirm = input("\nAre you sure you want to delete this patient? (Y/N): ")

    if confirm.upper() == "Y":

        try:

            query = "DELETE FROM patients WHERE patient_id = %s"

            cur.execute(query, (patient_id,))
            con.commit()

            print("\nPatient deleted successfully!")

        except mysql.connector.Error as err:

            print("\nError deleting patient.")
            print("Error:", err)

    else:

        print("\nDeletion cancelled.")

    pause()
# --------------------------------------------------
# OTHER MENUS
# --------------------------------------------------

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

def add_doctor():

    show_header("DOCTOR MANAGEMENT > ADD DOCTOR")

    print("Enter Doctor Details")
    print("-" * 60)

    name = input("Doctor Name       : ")
    specialization = input("Specialization     : ")
    department_id = input("Department ID      : ")
    phone = input("Phone Number       : ")
    consultation_fee = input("Consultation Fee   : ")

    query = """
    INSERT INTO doctors
    (name, specialization, department_id, phone, consultation_fee)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        name,
        specialization,
        department_id,
        phone,
        consultation_fee
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
def view_doctors():

    show_header("DOCTOR MANAGEMENT > VIEW DOCTORS")

    query = """
    SELECT
        doctors.doctor_id,
        doctors.name,
        doctors.specialization,
        departments.department_name,
        doctors.phone,
        doctors.consultation_fee
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
def search_doctor():

    show_header("DOCTOR MANAGEMENT > SEARCH DOCTOR")

    print("1. Search by Doctor ID")
    print("2. Search by Doctor Name")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        doctor_id = input("\nEnter Doctor ID: ")

        query = """
        SELECT
            doctors.doctor_id,
            doctors.name,
            doctors.specialization,
            departments.department_name,
            doctors.phone,
            doctors.consultation_fee
        FROM doctors
        JOIN departments
            ON doctors.department_id = departments.department_id
        WHERE doctors.doctor_id = %s
        """

        cur.execute(query, (doctor_id,))

    elif choice == "2":

        name = input("\nEnter Doctor Name: ")

        query = """
        SELECT
            doctors.doctor_id,
            doctors.name,
            doctors.specialization,
            departments.department_name,
            doctors.phone,
            doctors.consultation_fee
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
def update_doctor():

    show_header("DOCTOR MANAGEMENT > UPDATE DOCTOR")

    doctor_id = input("Enter Doctor ID: ")

    # Check whether doctor exists
    query = """
    SELECT
        doctors.doctor_id,
        doctors.name,
        doctors.specialization,
        departments.department_name,
        doctors.phone,
        doctors.consultation_fee
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

    # Display current details
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

        cur.execute(
            "SELECT department_id, department_name FROM departments"
        )

        records = cur.fetchall()

        for department in records:
            print(department[0], "-", department[1])

        new_value = input("\nEnter new Department ID: ")

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
def delete_doctor():

    show_header("DOCTOR MANAGEMENT > DELETE DOCTOR")

    doctor_id = input("Enter Doctor ID: ")

    # Check whether doctor exists
    cur.execute(
        "SELECT * FROM doctors WHERE doctor_id = %s",
        (doctor_id,)
    )

    record = cur.fetchone()

    if record is None:

        print("\nDoctor not found.")
        pause()
        return

    # Display doctor details
    print("\nDoctor found:")
    print("-" * 50)
    print("Doctor ID        :", record[0])
    print("Name             :", record[1])
    print("Specialization   :", record[2])
    print("Department ID    :", record[3])
    print("Phone            :", record[4])
    print("Consultation Fee :", record[5])
    print("-" * 50)

    # Ask for confirmation
    confirm = input("\nAre you sure you want to delete this doctor? (Y/N): ")

    if confirm.upper() == "Y":

        try:

            query = "DELETE FROM doctors WHERE doctor_id = %s"

            cur.execute(query, (doctor_id,))
            con.commit()

            print("\nDoctor deleted successfully!")

        except mysql.connector.Error as err:

            print("\nError deleting doctor.")
            print("Error:", err)

    else:

        print("\nDeletion cancelled.")

    pause()

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
def add_appointment():

    show_header("APPOINTMENT MANAGEMENT > BOOK APPOINTMENT")

    print("Enter Appointment Details")
    print("-" * 60)

    # Show patients
    print("\nAvailable Patients")
    print("-" * 40)

    cur.execute(
        "SELECT patient_id, name FROM patients ORDER BY patient_id"
    )

    records = cur.fetchall()

    for record in records:
        print(record[0], "-", record[1])

    patient_id = input("\nEnter Patient ID: ")

    # Check patient
    cur.execute(
        "SELECT * FROM patients WHERE patient_id = %s",
        (patient_id,)
    )

    patient = cur.fetchone()

    if patient is None:

        print("\nPatient not found.")
        pause()
        return

    # Show doctors
    print("\nAvailable Doctors")
    print("-" * 50)

    query = """
    SELECT
        doctors.doctor_id,
        doctors.name,
        doctors.specialization,
        departments.department_name
    FROM doctors
    JOIN departments
        ON doctors.department_id = departments.department_id
    ORDER BY doctors.doctor_id
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            "-",
            record[1],
            "|",
            record[2],
            "|",
            record[3]
        )

    doctor_id = input("\nEnter Doctor ID: ")

    # Check doctor
    cur.execute(
        "SELECT * FROM doctors WHERE doctor_id = %s",
        (doctor_id,)
    )

    doctor = cur.fetchone()

    if doctor is None:

        print("\nDoctor not found.")
        pause()
        return

    appointment_date = input(
        "Appointment Date (YYYY-MM-DD): "
    )

    appointment_time = input(
        "Appointment Time (HH:MM:SS): "
    )

    status = "Scheduled"

    reason = input("Reason for Appointment: ")

    query = """
    INSERT INTO appointments
    (patient_id, doctor_id, appointment_date,
     appointment_time, status, reason)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status,
        reason
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


def view_appointments():

    show_header("APPOINTMENT MANAGEMENT > VIEW APPOINTMENTS")

    query = """
    SELECT
        appointments.appointment_id,
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
def search_appointment():

    show_header("APPOINTMENT MANAGEMENT > SEARCH APPOINTMENT")

    print("1. Search by Appointment ID")
    print("2. Search by Patient Name")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        appointment_id = input("\nEnter Appointment ID: ")

        query = """
        SELECT
            appointments.appointment_id,
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
        SELECT
            appointments.appointment_id,
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

def update_appointment():

    show_header("APPOINTMENT MANAGEMENT > UPDATE APPOINTMENT")

    appointment_id = input("Enter Appointment ID: ")

    # Check whether appointment exists
    query = """
    SELECT
        appointments.appointment_id,
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

    # Display current details
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

        new_value = input(
            "Enter new appointment date (YYYY-MM-DD): "
        )

        query = """
        UPDATE appointments
        SET appointment_date = %s
        WHERE appointment_id = %s
        """

    elif choice == "2":

        new_value = input(
            "Enter new appointment time (HH:MM:SS): "
        )

        query = """
        UPDATE appointments
        SET appointment_time = %s
        WHERE appointment_id = %s
        """

    elif choice == "3":

        print("\nAvailable Doctors")
        print("-" * 50)

        query = """
        SELECT
            doctors.doctor_id,
            doctors.name,
            doctors.specialization
        FROM doctors
        ORDER BY doctors.doctor_id
        """

        cur.execute(query)

        records = cur.fetchall()

        for doctor in records:

            print(
                doctor[0],
                "-",
                doctor[1],
                "|",
                doctor[2]
            )

        new_value = input("\nEnter new Doctor ID: ")

        # Check doctor
        cur.execute(
            "SELECT * FROM doctors WHERE doctor_id = %s",
            (new_value,)
        )

        doctor = cur.fetchone()

        if doctor is None:

            print("\nDoctor not found.")
            pause()
            return

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
def delete_appointment():

    show_header("APPOINTMENT MANAGEMENT > CANCEL APPOINTMENT")

    appointment_id = input("Enter Appointment ID: ")

    # Check whether appointment exists
    query = """
    SELECT
        appointments.appointment_id,
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

# ============================================================
# MEDICAL RECORDS
# ============================================================

def medical_record_menu():

    while True:

        show_header("MEDICAL RECORDS")

        print("1. Add Medical Record")
        print("2. View All Medical Records")
        print("3. Search Medical Record")
        print("4. Update Medical Record")
        print("5. Delete Medical Record")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_medical_record()

        elif choice == "2":
            view_medical_records()

        elif choice == "3":
            search_medical_record()

        elif choice == "4":
            update_medical_record()

        elif choice == "5":
            delete_medical_record()

        elif choice == "6":
            break

        else:
            print("\nInvalid choice.")
            pause()


# ============================================================
# ADD MEDICAL RECORD
# ============================================================

def add_medical_record():

    show_header("MEDICAL RECORDS > ADD MEDICAL RECORD")

    print("Enter Medical Record Details")
    print("-" * 60)

    # Show patients
    print("\nAvailable Patients")
    print("-" * 40)

    cur.execute(
        "SELECT patient_id, name FROM patients ORDER BY patient_id"
    )

    records = cur.fetchall()

    if len(records) == 0:

        print("No patients found.")
        pause()
        return

    for record in records:
        print(record[0], "-", record[1])

    patient_id = input("\nEnter Patient ID: ")

    # Check patient
    cur.execute(
        "SELECT * FROM patients WHERE patient_id = %s",
        (patient_id,)
    )

    patient = cur.fetchone()

    if patient is None:

        print("\nPatient not found.")
        pause()
        return

    # Show doctors
    print("\nAvailable Doctors")
    print("-" * 50)

    query = """
    SELECT
        doctor_id,
        name,
        specialization
    FROM doctors
    ORDER BY doctor_id
    """

    cur.execute(query)

    records = cur.fetchall()

    if len(records) == 0:

        print("No doctors found.")
        pause()
        return

    for record in records:

        print(
            record[0],
            "-",
            record[1],
            "|",
            record[2]
        )

    doctor_id = input("\nEnter Doctor ID: ")

    # Check doctor
    cur.execute(
        "SELECT * FROM doctors WHERE doctor_id = %s",
        (doctor_id,)
    )

    doctor = cur.fetchone()

    if doctor is None:

        print("\nDoctor not found.")
        pause()
        return

    # Visit date
    while True:

        visit_date = input(
            "\nVisit Date (DD-MM-YYYY): "
        )

        try:

            visit_date = datetime.strptime(
                visit_date,
                "%d-%m-%Y"
            ).strftime("%Y-%m-%d")

            break

        except ValueError:

            print(
                "Invalid date."
                "\nPlease enter the date like 03-09-2026."
            )

    diagnosis = input("Diagnosis: ")

    prescription = input("Prescription: ")

    notes = input("Additional Notes: ")

    query = """
    INSERT INTO medical_records
    (patient_id, doctor_id, visit_date,
     diagnosis, prescription, notes)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        patient_id,
        doctor_id,
        visit_date,
        diagnosis,
        prescription,
        notes
    )

    try:

        cur.execute(query, values)
        con.commit()

        record_id = cur.lastrowid

        print("\nMedical record added successfully!")
        print("Record ID:", record_id)

    except mysql.connector.Error as err:

        print("\nError adding medical record.")
        print("Error:", err)

    pause()


# ============================================================
# VIEW ALL MEDICAL RECORDS
# ============================================================

def view_medical_records():

    show_header("MEDICAL RECORDS > VIEW MEDICAL RECORDS")

    query = """
    SELECT
        medical_records.record_id,
        patients.name AS patient_name,
        doctors.name AS doctor_name,
        medical_records.visit_date,
        medical_records.diagnosis
    FROM medical_records
    JOIN patients
        ON medical_records.patient_id = patients.patient_id
    JOIN doctors
        ON medical_records.doctor_id = doctors.doctor_id
    ORDER BY medical_records.visit_date DESC
    """

    cur.execute(query)

    records = cur.fetchall()

    if len(records) == 0:

        print("No medical records found.")

    else:

        print("MEDICAL RECORD LIST")
        print("-" * 100)

        print(
            f"{'ID':<5}"
            f"{'PATIENT':<22}"
            f"{'DOCTOR':<22}"
            f"{'VISIT DATE':<15}"
            f"{'DIAGNOSIS':<30}"
        )

        print("-" * 100)

        for record in records:

            print(
                f"{record[0]:<5}"
                f"{record[1]:<22}"
                f"{record[2]:<22}"
                f"{str(record[3]):<15}"
                f"{record[4]:<30}"
            )

        print("-" * 100)

    pause()


# ============================================================
# SEARCH MEDICAL RECORD
# ============================================================

def search_medical_record():

    show_header("MEDICAL RECORDS > SEARCH MEDICAL RECORD")

    print("1. Search by Record ID")
    print("2. Search by Patient Name")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        record_id = input("\nEnter Record ID: ")

        query = """
        SELECT
            medical_records.record_id,
            patients.name AS patient_name,
            doctors.name AS doctor_name,
            medical_records.visit_date,
            medical_records.diagnosis,
            medical_records.prescription,
            medical_records.notes
        FROM medical_records
        JOIN patients
            ON medical_records.patient_id = patients.patient_id
        JOIN doctors
            ON medical_records.doctor_id = doctors.doctor_id
        WHERE medical_records.record_id = %s
        """

        cur.execute(query, (record_id,))

    elif choice == "2":

        name = input("\nEnter Patient Name: ")

        query = """
        SELECT
            medical_records.record_id,
            patients.name AS patient_name,
            doctors.name AS doctor_name,
            medical_records.visit_date,
            medical_records.diagnosis,
            medical_records.prescription,
            medical_records.notes
        FROM medical_records
        JOIN patients
            ON medical_records.patient_id = patients.patient_id
        JOIN doctors
            ON medical_records.doctor_id = doctors.doctor_id
        WHERE patients.name LIKE %s
        ORDER BY medical_records.visit_date DESC
        """

        cur.execute(query, ("%" + name + "%",))

    else:

        print("\nInvalid choice.")
        pause()
        return

    records = cur.fetchall()

    if len(records) == 0:

        print("\nNo medical record found.")

    else:

        print("\nMEDICAL RECORD DETAILS")
        print("-" * 60)

        for record in records:

            print("Record ID     :", record[0])
            print("Patient       :", record[1])
            print("Doctor        :", record[2])
            print("Visit Date    :", record[3])
            print("Diagnosis     :", record[4])
            print("Prescription  :", record[5])
            print("Notes         :", record[6])

            print("-" * 60)

    pause()


# ============================================================
# UPDATE MEDICAL RECORD
# ============================================================

def update_medical_record():

    show_header("MEDICAL RECORDS > UPDATE MEDICAL RECORD")

    record_id = input("Enter Record ID: ")

    query = """
    SELECT
        medical_records.record_id,
        patients.name AS patient_name,
        doctors.name AS doctor_name,
        medical_records.visit_date,
        medical_records.diagnosis,
        medical_records.prescription,
        medical_records.notes
    FROM medical_records
    JOIN patients
        ON medical_records.patient_id = patients.patient_id
    JOIN doctors
        ON medical_records.doctor_id = doctors.doctor_id
    WHERE medical_records.record_id = %s
    """

    cur.execute(query, (record_id,))

    record = cur.fetchone()

    if record is None:

        print("\nMedical record not found.")
        pause()
        return

    print("\nMedical Record Found")
    print("-" * 60)
    print("Record ID     :", record[0])
    print("Patient       :", record[1])
    print("Doctor        :", record[2])
    print("Visit Date    :", record[3])
    print("Diagnosis     :", record[4])
    print("Prescription  :", record[5])
    print("Notes         :", record[6])
    print("-" * 60)

    print("\nWhat do you want to update?")
    print("1. Visit Date")
    print("2. Diagnosis")
    print("3. Prescription")
    print("4. Notes")
    print("5. Doctor")
    print("6. Cancel")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        while True:

            new_value = input(
                "Enter new visit date (DD-MM-YYYY): "
            )

            try:

                new_value = datetime.strptime(
                    new_value,
                    "%d-%m-%Y"
                ).strftime("%Y-%m-%d")

                break

            except ValueError:

                print(
                    "Invalid date."
                    "\nPlease enter the date like 03-09-2026."
                )

        query = """
        UPDATE medical_records
        SET visit_date = %s
        WHERE record_id = %s
        """

    elif choice == "2":

        new_value = input("Enter new diagnosis: ")

        query = """
        UPDATE medical_records
        SET diagnosis = %s
        WHERE record_id = %s
        """

    elif choice == "3":

        new_value = input("Enter new prescription: ")

        query = """
        UPDATE medical_records
        SET prescription = %s
        WHERE record_id = %s
        """

    elif choice == "4":

        new_value = input("Enter new notes: ")

        query = """
        UPDATE medical_records
        SET notes = %s
        WHERE record_id = %s
        """

    elif choice == "5":

        print("\nAvailable Doctors")
        print("-" * 50)

        cur.execute(
            """
            SELECT doctor_id, name, specialization
            FROM doctors
            ORDER BY doctor_id
            """
        )

        records = cur.fetchall()

        for doctor in records:

            print(
                doctor[0],
                "-",
                doctor[1],
                "|",
                doctor[2]
            )

        new_value = input("\nEnter new Doctor ID: ")

        cur.execute(
            "SELECT * FROM doctors WHERE doctor_id = %s",
            (new_value,)
        )

        doctor = cur.fetchone()

        if doctor is None:

            print("\nDoctor not found.")
            pause()
            return

        query = """
        UPDATE medical_records
        SET doctor_id = %s
        WHERE record_id = %s
        """

    elif choice == "6":

        return

    else:

        print("\nInvalid choice.")
        pause()
        return

    try:

        cur.execute(query, (new_value, record_id))
        con.commit()

        print("\nMedical record updated successfully!")

    except mysql.connector.Error as err:

        print("\nError updating medical record.")
        print("Error:", err)

    pause()


# ============================================================
# DELETE MEDICAL RECORD
# ============================================================

def delete_medical_record():

    show_header("MEDICAL RECORDS > DELETE MEDICAL RECORD")

    record_id = input("Enter Record ID: ")

    cur.execute(
        "SELECT * FROM medical_records WHERE record_id = %s",
        (record_id,)
    )

    record = cur.fetchone()

    if record is None:

        print("\nMedical record not found.")
        pause()
        return

    print("\nMedical Record Found")
    print("-" * 50)
    print("Record ID    :", record[0])
    print("Patient ID   :", record[1])
    print("Doctor ID    :", record[2])
    print("Visit Date   :", record[3])
    print("Diagnosis    :", record[4])
    print("Prescription :", record[5])
    print("Notes        :", record[6])
    print("-" * 50)

    confirm = input(
        "\nAre you sure you want to delete this medical record? (Y/N): "
    )

    if confirm.upper() == "Y":

        try:

            query = """
            DELETE FROM medical_records
            WHERE record_id = %s
            """

            cur.execute(query, (record_id,))
            con.commit()

            print("\nMedical record deleted successfully!")

        except mysql.connector.Error as err:

            print("\nError deleting medical record.")
            print("Error:", err)

    else:

        print("\nDeletion cancelled.")

    pause()


# ============================================================
# BILLING
# ============================================================

def billing_menu():

    while True:

        show_header("BILLING")

        print("1. Create New Bill")
        print("2. View All Bills")
        print("3. Search Bill")
        print("4. Update Bill")
        print("5. Delete Bill")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_bill()

        elif choice == "2":
            view_bills()

        elif choice == "3":
            search_bill()

        elif choice == "4":
            update_bill()

        elif choice == "5":
            delete_bill()

        elif choice == "6":
            break

        else:
            print("\nInvalid choice.")
            pause()


# ============================================================
# CREATE NEW BILL
# ============================================================

def add_bill():

    show_header("BILLING > CREATE BILL")

    print("Enter Billing Details")
    print("-" * 60)

    # Show patients
    print("\nAvailable Patients")
    print("-" * 40)

    cur.execute(
        "SELECT patient_id, name FROM patients ORDER BY patient_id"
    )

    records = cur.fetchall()

    if len(records) == 0:

        print("No patients found.")
        pause()
        return

    for record in records:
        print(record[0], "-", record[1])

    patient_id = input("\nEnter Patient ID: ")

    cur.execute(
        "SELECT * FROM patients WHERE patient_id = %s",
        (patient_id,)
    )

    patient = cur.fetchone()

    if patient is None:

        print("\nPatient not found.")
        pause()
        return

    # Show appointments
    print("\nAvailable Appointments")
    print("-" * 70)

    query = """
    SELECT
        appointments.appointment_id,
        patients.name,
        doctors.name,
        appointments.appointment_date,
        appointments.status
    FROM appointments
    JOIN patients
        ON appointments.patient_id = patients.patient_id
    JOIN doctors
        ON appointments.doctor_id = doctors.doctor_id
    WHERE appointments.patient_id = %s
    ORDER BY appointments.appointment_date DESC
    """

    cur.execute(query, (patient_id,))

    records = cur.fetchall()

    if len(records) == 0:

        print("No appointments found for this patient.")
        pause()
        return

    for record in records:

        print(
            record[0],
            "- Patient:",
            record[1],
            "| Doctor:",
            record[2],
            "| Date:",
            record[3],
            "| Status:",
            record[4]
        )

    appointment_id = input("\nEnter Appointment ID: ")

    # Check appointment
    cur.execute(
        """
        SELECT *
        FROM appointments
        WHERE appointment_id = %s
        AND patient_id = %s
        """,
        (appointment_id, patient_id)
    )

    appointment = cur.fetchone()

    if appointment is None:

        print("\nAppointment not found for this patient.")
        pause()
        return

    # Bill date
    while True:

        bill_date = input(
            "Bill Date (DD-MM-YYYY): "
        )

        try:

            bill_date = datetime.strptime(
                bill_date,
                "%d-%m-%Y"
            ).strftime("%Y-%m-%d")

            break

        except ValueError:

            print(
                "Invalid date."
                "\nPlease enter the date like 03-09-2026."
            )

    # Get charges
    while True:

        try:

            consultation_fee = float(
                input("Consultation Fee : ")
            )

            medicine_charge = float(
                input("Medicine Charge   : ")
            )

            test_charge = float(
                input("Test Charge       : ")
            )

            other_charge = float(
                input("Other Charge      : ")
            )

            break

        except ValueError:

            print("\nPlease enter valid numbers.")

    total_amount = (
        consultation_fee
        + medicine_charge
        + test_charge
        + other_charge
    )

    payment_status = "Pending"

    print("\nTotal Amount:", format(total_amount, ".2f"))

    query = """
    INSERT INTO billing
    (patient_id, appointment_id, bill_date,
     consultation_fee, medicine_charge, test_charge,
     other_charge, total_amount, payment_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        patient_id,
        appointment_id,
        bill_date,
        consultation_fee,
        medicine_charge,
        test_charge,
        other_charge,
        total_amount,
        payment_status
    )

    try:

        cur.execute(query, values)
        con.commit()

        bill_id = cur.lastrowid

        print("\nBill created successfully!")
        print("Bill ID:", bill_id)
        print("Total Amount:", format(total_amount, ".2f"))

    except mysql.connector.Error as err:

        print("\nError creating bill.")
        print("Error:", err)

    pause()


# ============================================================
# VIEW ALL BILLS
# ============================================================

def view_bills():

    show_header("BILLING > VIEW BILLS")

    query = """
    SELECT
        billing.bill_id,
        patients.name AS patient_name,
        billing.appointment_id,
        billing.bill_date,
        billing.total_amount,
        billing.payment_status
    FROM billing
    JOIN patients
        ON billing.patient_id = patients.patient_id
    ORDER BY billing.bill_date DESC
    """

    cur.execute(query)

    records = cur.fetchall()

    if len(records) == 0:

        print("No bills found.")

    else:

        print("BILL LIST")
        print("-" * 90)

        print(
            f"{'ID':<6}"
            f"{'PATIENT':<25}"
            f"{'APPOINTMENT':<15}"
            f"{'DATE':<15}"
            f"{'TOTAL':<12}"
            f"{'STATUS':<15}"
        )

        print("-" * 90)

        for record in records:

            print(
                f"{record[0]:<6}"
                f"{record[1]:<25}"
                f"{record[2]:<15}"
                f"{str(record[3]):<15}"
                f"{format(record[4], '.2f'):<12}"
                f"{record[5]:<15}"
            )

        print("-" * 90)

    pause()


# ============================================================
# SEARCH BILL
# ============================================================

def search_bill():

    show_header("BILLING > SEARCH BILL")

    print("1. Search by Bill ID")
    print("2. Search by Patient Name")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        bill_id = input("\nEnter Bill ID: ")

        query = """
        SELECT
            billing.bill_id,
            patients.name AS patient_name,
            doctors.name AS doctor_name,
            billing.appointment_id,
            billing.bill_date,
            billing.consultation_fee,
            billing.medicine_charge,
            billing.test_charge,
            billing.other_charge,
            billing.total_amount,
            billing.payment_status
        FROM billing
        JOIN patients
            ON billing.patient_id = patients.patient_id
        JOIN appointments
            ON billing.appointment_id = appointments.appointment_id
        JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
        WHERE billing.bill_id = %s
        """

        cur.execute(query, (bill_id,))

    elif choice == "2":

        name = input("\nEnter Patient Name: ")

        query = """
        SELECT
            billing.bill_id,
            patients.name AS patient_name,
            doctors.name AS doctor_name,
            billing.appointment_id,
            billing.bill_date,
            billing.consultation_fee,
            billing.medicine_charge,
            billing.test_charge,
            billing.other_charge,
            billing.total_amount,
            billing.payment_status
        FROM billing
        JOIN patients
            ON billing.patient_id = patients.patient_id
        JOIN appointments
            ON billing.appointment_id = appointments.appointment_id
        JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
        WHERE patients.name LIKE %s
        ORDER BY billing.bill_date DESC
        """

        cur.execute(query, ("%" + name + "%",))

    else:

        print("\nInvalid choice.")
        pause()
        return

    records = cur.fetchall()

    if len(records) == 0:

        print("\nNo bill found.")

    else:

        print("\nBILL DETAILS")
        print("-" * 60)

        for record in records:

            print("Bill ID            :", record[0])
            print("Patient            :", record[1])
            print("Doctor             :", record[2])
            print("Appointment ID     :", record[3])
            print("Bill Date          :", record[4])
            print("Consultation Fee   :", record[5])
            print("Medicine Charge    :", record[6])
            print("Test Charge        :", record[7])
            print("Other Charge       :", record[8])
            print("Total Amount       :", record[9])
            print("Payment Status     :", record[10])

            print("-" * 60)

    pause()


# ============================================================
# UPDATE BILL
# ============================================================

def update_bill():

    show_header("BILLING > UPDATE BILL")

    bill_id = input("Enter Bill ID: ")

    cur.execute(
        "SELECT * FROM billing WHERE bill_id = %s",
        (bill_id,)
    )

    record = cur.fetchone()

    if record is None:

        print("\nBill not found.")
        pause()
        return

    print("\nBill Found")
    print("-" * 60)
    print("Bill ID          :", record[0])
    print("Patient ID       :", record[1])
    print("Appointment ID   :", record[2])
    print("Bill Date        :", record[3])
    print("Consultation Fee :", record[4])
    print("Medicine Charge  :", record[5])
    print("Test Charge      :", record[6])
    print("Other Charge     :", record[7])
    print("Total Amount     :", record[8])
    print("Payment Status   :", record[9])
    print("-" * 60)

    print("\nWhat do you want to update?")
    print("1. Consultation Fee")
    print("2. Medicine Charge")
    print("3. Test Charge")
    print("4. Other Charge")
    print("5. Payment Status")
    print("6. Cancel")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        try:
            new_value = float(
                input("Enter new consultation fee: ")
            )
        except ValueError:
            print("\nInvalid amount.")
            pause()
            return

        query = """
        UPDATE billing
        SET consultation_fee = %s,
            total_amount =
                %s + medicine_charge + test_charge + other_charge
        WHERE bill_id = %s
        """

        values = (new_value, new_value, bill_id)

    elif choice == "2":

        try:
            new_value = float(
                input("Enter new medicine charge: ")
            )
        except ValueError:
            print("\nInvalid amount.")
            pause()
            return

        query = """
        UPDATE billing
        SET medicine_charge = %s,
            total_amount =
                consultation_fee + %s + test_charge + other_charge
        WHERE bill_id = %s
        """

        values = (new_value, new_value, bill_id)

    elif choice == "3":

        try:
            new_value = float(
                input("Enter new test charge: ")
            )
        except ValueError:
            print("\nInvalid amount.")
            pause()
            return

        query = """
        UPDATE billing
        SET test_charge = %s,
            total_amount =
                consultation_fee + medicine_charge + %s + other_charge
        WHERE bill_id = %s
        """

        values = (new_value, new_value, bill_id)

    elif choice == "4":

        try:
            new_value = float(
                input("Enter new other charge: ")
            )
        except ValueError:
            print("\nInvalid amount.")
            pause()
            return

        query = """
        UPDATE billing
        SET other_charge = %s,
            total_amount =
                consultation_fee + medicine_charge + test_charge + %s
        WHERE bill_id = %s
        """

        values = (new_value, new_value, bill_id)

    elif choice == "5":

        print("\nPayment Status")
        print("-" * 30)
        print("1. Pending")
        print("2. Paid")
        print("3. Partially Paid")

        status_choice = input("\nEnter status choice: ")

        if status_choice == "1":

            new_value = "Pending"

        elif status_choice == "2":

            new_value = "Paid"

        elif status_choice == "3":

            new_value = "Partially Paid"

        else:

            print("\nInvalid status.")
            pause()
            return

        query = """
        UPDATE billing
        SET payment_status = %s
        WHERE bill_id = %s
        """

        values = (new_value, bill_id)

    elif choice == "6":

        return

    else:

        print("\nInvalid choice.")
        pause()
        return

    try:

        cur.execute(query, values)
        con.commit()

        print("\nBill updated successfully!")

        # Show updated total
        cur.execute(
            "SELECT total_amount FROM billing WHERE bill_id = %s",
            (bill_id,)
        )

        updated_bill = cur.fetchone()

        if updated_bill is not None:

            print(
                "Updated Total Amount:",
                format(updated_bill[0], ".2f")
            )

    except mysql.connector.Error as err:

        print("\nError updating bill.")
        print("Error:", err)

    pause()


# ============================================================
# DELETE BILL
# ============================================================

def delete_bill():

    show_header("BILLING > DELETE BILL")

    bill_id = input("Enter Bill ID: ")

    cur.execute(
        "SELECT * FROM billing WHERE bill_id = %s",
        (bill_id,)
    )

    record = cur.fetchone()

    if record is None:

        print("\nBill not found.")
        pause()
        return

    print("\nBill Found")
    print("-" * 50)
    print("Bill ID          :", record[0])
    print("Patient ID       :", record[1])
    print("Appointment ID   :", record[2])
    print("Bill Date        :", record[3])
    print("Total Amount     :", record[8])
    print("Payment Status   :", record[9])
    print("-" * 50)

    confirm = input(
        "\nAre you sure you want to delete this bill? (Y/N): "
    )

    if confirm.upper() == "Y":

        try:

            query = "DELETE FROM billing WHERE bill_id = %s"

            cur.execute(query, (bill_id,))
            con.commit()

            print("\nBill deleted successfully!")

        except mysql.connector.Error as err:

            print("\nError deleting bill.")
            print("Error:", err)

    else:

        print("\nDeletion cancelled.")

    pause()


# ============================================================
# REPORTS
# ============================================================

def reports_menu():

    while True:

        show_header("REPORTS")

        print("1. Patient Report")
        print("2. Doctor Report")
        print("3. Appointment Report")
        print("4. Medical Records Report")
        print("5. Billing Report")
        print("6. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            patient_report()

        elif choice == "2":
            doctor_report()

        elif choice == "3":
            appointment_report()

        elif choice == "4":
            medical_record_report()

        elif choice == "5":
            billing_report()

        elif choice == "6":
            break

        else:
            print("\nInvalid choice.")
            pause()


# ============================================================
# PATIENT REPORT
# ============================================================

def patient_report():

    show_header("REPORTS > PATIENT REPORT")

    cur.execute(
        "SELECT COUNT(*) FROM patients"
    )

    result = cur.fetchone()

    total_patients = result[0]

    print("PATIENT REPORT")
    print("-" * 50)
    print("Total Number of Patients:", total_patients)

    print("\nPatients by Gender")
    print("-" * 50)

    query = """
    SELECT gender, COUNT(*)
    FROM patients
    GROUP BY gender
    ORDER BY gender
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            ":",
            record[1]
        )

    print("\nPatients by Blood Group")
    print("-" * 50)

    query = """
    SELECT blood_group, COUNT(*)
    FROM patients
    GROUP BY blood_group
    ORDER BY blood_group
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            ":",
            record[1]
        )

    pause()


# ============================================================
# DOCTOR REPORT
# ============================================================

def doctor_report():

    show_header("REPORTS > DOCTOR REPORT")

    cur.execute(
        "SELECT COUNT(*) FROM doctors"
    )

    result = cur.fetchone()

    total_doctors = result[0]

    print("DOCTOR REPORT")
    print("-" * 50)
    print("Total Number of Doctors:", total_doctors)

    print("\nDoctors by Department")
    print("-" * 60)

    query = """
    SELECT
        departments.department_name,
        COUNT(doctors.doctor_id)
    FROM doctors
    JOIN departments
        ON doctors.department_id = departments.department_id
    GROUP BY departments.department_name
    ORDER BY departments.department_name
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            ":",
            record[1]
        )

    print("\nAverage Consultation Fee")
    print("-" * 50)

    cur.execute(
        "SELECT AVG(consultation_fee) FROM doctors"
    )

    result = cur.fetchone()

    if result[0] is not None:

        print(
            "Average Fee:",
            format(result[0], ".2f")
        )

    pause()


# ============================================================
# APPOINTMENT REPORT
# ============================================================

def appointment_report():

    show_header("REPORTS > APPOINTMENT REPORT")

    cur.execute(
        "SELECT COUNT(*) FROM appointments"
    )

    result = cur.fetchone()

    total_appointments = result[0]

    print("APPOINTMENT REPORT")
    print("-" * 50)
    print(
        "Total Number of Appointments:",
        total_appointments
    )

    print("\nAppointments by Status")
    print("-" * 50)

    query = """
    SELECT status, COUNT(*)
    FROM appointments
    GROUP BY status
    ORDER BY status
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            ":",
            record[1]
        )

    print("\nAppointments by Doctor")
    print("-" * 60)

    query = """
    SELECT
        doctors.name,
        COUNT(appointments.appointment_id)
    FROM appointments
    JOIN doctors
        ON appointments.doctor_id = doctors.doctor_id
    GROUP BY doctors.name
    ORDER BY COUNT(appointments.appointment_id) DESC
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            ":",
            record[1]
        )

    pause()


# ============================================================
# MEDICAL RECORD REPORT
# ============================================================

def medical_record_report():

    show_header("REPORTS > MEDICAL RECORD REPORT")

    cur.execute(
        "SELECT COUNT(*) FROM medical_records"
    )

    result = cur.fetchone()

    total_records = result[0]

    print("MEDICAL RECORD REPORT")
    print("-" * 50)
    print(
        "Total Medical Records:",
        total_records
    )

    print("\nRecords by Doctor")
    print("-" * 60)

    query = """
    SELECT
        doctors.name,
        COUNT(medical_records.record_id)
    FROM medical_records
    JOIN doctors
        ON medical_records.doctor_id = doctors.doctor_id
    GROUP BY doctors.name
    ORDER BY COUNT(medical_records.record_id) DESC
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            ":",
            record[1]
        )

    print("\nRecords by Diagnosis")
    print("-" * 60)

    query = """
    SELECT
        diagnosis,
        COUNT(*)
    FROM medical_records
    GROUP BY diagnosis
    ORDER BY COUNT(*) DESC
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            ":",
            record[1]
        )

    pause()


# ============================================================
# BILLING REPORT
# ============================================================

def billing_report():

    show_header("REPORTS > BILLING REPORT")

    cur.execute(
        "SELECT COUNT(*) FROM billing"
    )

    result = cur.fetchone()

    total_bills = result[0]

    print("BILLING REPORT")
    print("-" * 50)
    print("Total Number of Bills:", total_bills)

    # Total revenue
    cur.execute(
        "SELECT SUM(total_amount) FROM billing"
    )

    result = cur.fetchone()

    print("\nTotal Billing Amount:")

    if result[0] is None:

        print("0.00")

    else:

        print(
            format(result[0], ".2f")
        )

    # Paid amount
    cur.execute(
        """
        SELECT SUM(total_amount)
        FROM billing
        WHERE payment_status = 'Paid'
        """
    )

    result = cur.fetchone()

    print("\nTotal Paid Amount:")

    if result[0] is None:

        print("0.00")

    else:

        print(
            format(result[0], ".2f")
        )

    # Pending amount
    cur.execute(
        """
        SELECT SUM(total_amount)
        FROM billing
        WHERE payment_status = 'Pending'
        """
    )

    result = cur.fetchone()

    print("\nTotal Pending Amount:")

    if result[0] is None:

        print("0.00")

    else:

        print(
            format(result[0], ".2f")
        )

    # Payment status
    print("\nBills by Payment Status")
    print("-" * 50)

    query = """
    SELECT
        payment_status,
        COUNT(*)
    FROM billing
    GROUP BY payment_status
    ORDER BY payment_status
    """

    cur.execute(query)

    records = cur.fetchall()

    for record in records:

        print(
            record[0],
            ":",
            record[1]
        )

    pause()


# --------------------------------------------------
# MAIN MENU
# --------------------------------------------------

def main_menu():

    while True:

        show_header("MAIN MENU")

        print("1. Patient Management")
        print("2. Doctor Management")
        print("3. Appointment Management")
        print("4. Medical Records")
        print("5. Billing")
        print("6. Reports")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            patient_menu()

        elif choice == "2":
            doctor_menu()

        elif choice == "3":
            appointment_menu()

        elif choice == "4":
            medical_record_menu()

        elif choice == "5":
            billing_menu()

        elif choice == "6":
            reports_menu()

        elif choice == "7":
            show_header("EXIT")

            print("Thank you for using the Healthcare Management System.")

            break

        else:
            print("\nInvalid choice.")
            pause()


# --------------------------------------------------
# START PROGRAM
# --------------------------------------------------

print("Connected to MySQL successfully!")

pause()

main_menu()

con.close()
