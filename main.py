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

# class for dentist database
class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect('dentist.db')
        self.cursor = self.conn.cursor()

    def sending_to_database(self, query, values):
        self.cursor.execute(query, values)
        self.conn.commit()

    def single_select(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def fetch(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

# fetching users from the database
def fetch_users():
    with sqlite3.connect('dentist.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users_data = cursor.fetchall()

        new_data = []

        for data in users_data:
            new_data.append(User(data[0], data[5], data[6]))

        return new_data

# creating table for admin
def init_user_table():
    conn = sqlite3.connect('dentist.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS admin (admin_id INTEGER PRIMARY KEY,"
                 "admin_email TEXT NOT NULL,"
                 "admin_password TEXT NOT NULL,"
                 "admin_name TEXT NOT NULL,"
                 "admin_cellphone TEXT NOT NULL)")

    print("Admin table successfully")
    conn.close()


init_user_table()
users = fetch_users()

# creating table for dentist
def init_user_table():
    conn = sqlite3.connect('dentist.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS admin (dentist_id INTEGER PRIMARY KEY,"
                 "dentist_email TEXT NOT NULL,"
                 "dentist_password TEXT NOT NULL,"
                 "dentist_name TEXT NOT NULL,"
                 "dentist_cellphone TEXT NOT NULL)")

    print("dentist table successfully")
    conn.close()


init_user_table()
users = fetch_users()

# creating table for patient
def init_user_table():
    conn = sqlite3.connect('patient.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS patient (patient_id INTEGER PRIMARY KEY,"
                 "patient_email TEXT NOT NULL,"
                 "patient_password TEXT NOT NULL,"
                 "patient_name TEXT NOT NULL,"
                 "patient_surname TEXT NOT NULL,"
                 "patient_dob TEXT NOT NULL,"
                 "patient_gender TEXT NOT NULL"
                 "patient_cellphone TEXT NOT NULL)")

    print("Admin table successfully")
    conn.close()


init_user_table()
users = fetch_users()

# route for .....
@app.route('/')
def hello_world():
    return 'Hello, World!'

# route for user to login
@app.route('/user/login/')
def user_login():
    login_tries = 4
    if login_tries > 4:
        return 'Your account has been locked. Contact the administrator'
    return 'Please login with username and password!'


@app.route('/user/logout/')
def user_logout():
    return 'Successfully, logout!'


if __name__ == '__main__':
    app.run()