# importing from flask
import sqlite3
from flask import Flask

app = Flask(__name__)


# class for admin
class Admin(object):
    def __init__(self, admin_id, admin_username, admin_password):
        self.admin_id = admin_id
        self.admin_username = admin_username
        self.admin_password = admin_password


# class for dentist
class Dentist(object):
    def __init__(self, dentist_id, dentist_username, dentist_password):
        self.dentist_id = dentist_id
        self.dentist_username = dentist_username
        self.dentist_password = dentist_password


# class for patient
class Patient(object):
    def __init__(self, patient_id, patient_username, patient_password):
        self.patient_id = patient_id
        self.patient_username = patient_username
        self.patient_password = patient_password


# fetching patients from the database
def fetch_users():
    with sqlite3.connect('dentist_appointment.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient")
        users_data = cursor.fetchall()

        new_data = []

        for data in users_data:
            new_data.append(Patient(data[0], data[5], data[6]))

        return new_data


# creating table for admin
def init_admin_table():
    conn = sqlite3.connect('dentist_appointment.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS admin (admin_id INTEGER PRIMARY KEY,"
                 "admin_email TEXT NOT NULL,"
                 "admin_password TEXT NOT NULL,"
                 "admin_name TEXT NOT NULL,"
                 "admin_cellphone INTEGER NOT NULL)")

    print("Admin table successfully")
    conn.close()


# creating table for dentist
def init_dentist_table():
    conn = sqlite3.connect('dentist_appointment.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS dentist (dentist_id INTEGER PRIMARY KEY,"
                 "dentist_email TEXT NOT NULL,"
                 "dentist_password TEXT NOT NULL,"
                 "dentist_name TEXT NOT NULL,"
                 "dentist_cellphone INTEGER NOT NULL)")

    print("Dentist table successfully")
    conn.close()


# creating table for patient
def init_patient_table():
    conn = sqlite3.connect('dentist_appointment.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS patient (patient_id INTEGER PRIMARY KEY,'
                 'patient_email TEXT NOT NULL,'
                 'patient_password TEXT NOT NULL,'
                 'patient_name TEXT NOT NULL,'
                 'patient_surname TEXT NOT NULL,'
                 'patient_dob TEXT NOT NULL,'
                 'patient_gender TEXT NOT NULL,'
                 'patient_cellphone INTEGER NOT NULL)')

    print("Patient table successfully")
    conn.close()


init_admin_table()
init_dentist_table()
init_patient_table()
users = fetch_users()

# route for .....
main = Flask(__name__)
main.debug = True


@main.route('/')
def hello_world():
    return 'Hello, World!'


# route for user to login
@main.route('/user/login/')
def user_login():
    login_tries = 3
    if login_tries > 3:
        return 'Your account has been locked. Contact the administrator'
    return 'Please login with username and password!'


@main.route('/user/logout/')
def user_logout():
    return 'Successfully, logout!'


if __name__ == '__main__':
    main.run()
