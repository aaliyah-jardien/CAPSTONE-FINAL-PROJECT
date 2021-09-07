# Aaliyah Jardien, Class 2
# Capstone Backend Project

# importing from python
import datetime

import sqlite3
import re

# importing from flask
import flask_mail
from flask import Flask, request
from flask_cors import CORS
from flask_mail import Message


# FUNCTION CREATES DICTIONARIES OF MYSQL IN JSON FORMAT
def dict_factory(cursor, row):
    duh = {}
    for idx, col in enumerate(cursor.description):
        duh[col[0]] = row[idx]
    return duh


# CREATING A CLASS FOR THE DENTIST DATABASE
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("dentist_appointment.db")
        self.cursor = self.conn.cursor()

        print("Slamat Opened Database successfully")

        self.conn.execute("CREATE TABLE IF NOT EXISTS dentist(dentist_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "dentist_name TEXT NOT NULL,"
                          "dentist_surname TEXT NOT NULL,"
                          "dentist_email TEXT NOT NULL,"
                          "dentist_username TEXT NOT NULL,"
                          "dentist_password TEXT NOT NULL)")
        print("Dentist table created successfully!")

        self.conn.execute("CREATE TABLE IF NOT EXISTS patient(patient_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "patient_name TEXT NOT NULL,"
                          "patient_surname TEXT NOT NULL,"
                          "patient_dob DATE,"
                          "patient_gender TEXT NOT NULL,"
                          "patient_email TEXT NOT NULL,"
                          "patient_cellphone INTEGER NOT NULL,"
                          "patient_password TEXT NOT NULL)")
        print("Patient table created successfully!")

        self.conn.execute("CREATE TABLE IF NOT EXISTS booking(booking_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "patient_name TEXT NOT NULL,"
                          "patient_surname TEXT NOT NULL,"
                          "patient_email TEXT NOT NULL,"
                          "patient_cellphone INTEGER NOT NULL,"
                          "patient_service TEXT NOT NULL,"
                          "todays_date CURRENT_DATE,"
                          "booking_date DATE,"
                          "patient_id INTEGER,"
                          "CONSTRAINT fk_patients FOREIGN KEY(patient_id) REFERENCES patient(patient_id))")
        print("Booking table was created successfully!")
        self.conn.close()


Database()

# CREATING THE APP
app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SUPER_KEY'] = 'super-secret'

# FLASK MAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'aaliyahjardien4@gmail.com'
app.config['MAIL_PASSWORD'] = 'icecream2002%'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = flask_mail.Mail(app)


# FIRST WELCOMING ROUTE
@app.route('/', methods=["GET"])
def welcome():
    response = {}
    if request.method == "GET":
        response["message"] = "Welcome to Aaliyah's Dentistry!"
    return response


# zxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxczxcvxcvzxcvzxcvzxcvzxcvzxcvzx
# ROUTE FOR REGISTERING DENTIST (post)
@app.route('/dentist-register/', methods=["POST"])
def register_admin():
    response = {}
    try:
        dentist_name = request.json["dentist_name"]
        dentist_surname = request.json["dentist_surname"]
        dentist_email = request.json["dentist_email"]
        dentist_username = request.json["dentist_username"]
        dentist_password = request.json["dentist_password"]
        # VALIDATING EMAIL
        ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

        if request.method == "POST":
            if re.search(ex, dentist_email):
                with sqlite3.connect("dentist_appointment.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO dentist("
                                   "dentist_name,"
                                   "dentist_surname,"
                                   "dentist_email,"
                                   "dentist_username,"
                                   "dentist_password) VALUES(?, ?, ?, ?, ?)",
                                   (dentist_name, dentist_surname, dentist_email, dentist_username, dentist_password))
                    conn.commit()

                    response['message'] = "Dentist registered successfully"
                    response['status_code'] = 201
                    response['data'] = {
                        "dentist_name": dentist_name,
                        "dentist_surname": dentist_surname,
                        "dentist_email": dentist_email,
                        "dentist_username": dentist_username,
                        "dentist_password": dentist_password
                    }
                return response

            else:
                response['message'] = "Invalid Email"
                response['status_code'] = 404
                return response

        else:
            response['message'] = "Incorrect method"
            response['status_code'] = 400
            return response

    except ValueError:
        response['message'] = "Incorrect Values"
        response['status_code'] = 400
        return response

    except ConnectionError:
        response['message'] = "Connection Failed"
        response['status_code'] = 500
        return response

    except TimeoutError:
        response['message'] = "Connection Timeout"
        response['status_code'] = 500
        return response

# ROUTE VIEWING DENTISTS (get)
@app.route('/view-dentist/', methods=["GET"])
def view_dentist():
    response = {}
    with sqlite3.connect("dentist_appointment.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dentist")

        response['status_code'] = 200
        response['message'] = "Fetched all dentists"
        response['date'] = cursor.fetchall()
    return response


# ROUTE FOR DENTIST LOGIN USING PATCH METHOD
@app.route('/dentist-login/', methods=["PATCH"])
def dentist_login():
    response = {}

    if request.method == "PATCH":
        dentist_username = request.form["dentist_username"]
        dentist_password = request.form["dentist_password"]

        try:
            with sqlite3.connect("dentist_appointment.db") as conn:
                conn.row_factory = dict_factory
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM dentist WHERE dentist_username=? AND dentist_password=?",
                               (dentist_username, dentist_password))
                dentist = cursor.fetchone()

            response['status_code'] = 200
            response['data'] = dentist
            return response

        except ValueError:
            response['error'] = "Invalid"
            response['status_code'] = 404
            return response
    else:
        if request.method != "PATCH":
            response['message'] = "Incorrect Method"
            response['status_code'] = 400
            return response


# ROUTE FOR EDITING DENTIST (put)
# ROUTE FOR DELETING DENTIST (delete)


# zxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxczxcvxcvzxcvzxcvzxcvzxcvzxcvzxc
# ROUTE FOR REGISTERING & DISPLAYING PATIENTS
@app.route('/register-patient/', methods=["POST", "GET"])
def register_patient():
    response = {}

    try:
        if request.method == "POST":
            patient_email = request.json["patient_email"]
            patient_password = request.json["patient_password"]
            patient_name = request.json["patient_name"]
            patient_surname = request.json["patient_surname"]
            patient_dob = request.json["patient_dob"]
            patient_gender = request.json["patient_gender"]
            patient_cellphone = request.json["patient_cellphone"]

            # to check if email is valid
            ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
            x = "Welcome to the Dentist registration"
            if re.search(ex, patient_email):
                with sqlite3.connect('dentist_appointment.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO patient("
                                   "patient_email,"
                                   "patient_password,"
                                   "patient_name,"
                                   "patient_surname,"
                                   "patient_dob,"
                                   "patient_gender,"
                                   "patient_cellphone) VALUES(?, ?, ?, ?, ?, ?, ?)",
                                   (patient_email, patient_password, patient_name, patient_surname,
                                    patient_dob, patient_gender, patient_cellphone))

                    conn.commit()
                    response['message'] = "Patient successfully registered"
                    response['status_code'] = 201

            else:
                response['error_message'] = "Invalid Email"
                response['status_code'] = 404
                return response

        else:
            response['message'] = "Incorrect method"
            response['status_code'] = 400
            return response

    except ValueError:
        response['message'] = "Incorrect Values"
        response['status_code'] = 400
        return response

    except ConnectionError:
        response['message'] = "Connection Failed"
        response['status_code'] = 500
        return response

    except TimeoutError:
        response['message'] = "Connection Timeout"
        response['status_code'] = 500
        return response


# ROUTE FOR PATIENTS LOGGING IN


# ROUTE TO VIEW ONE PATIENT
@app.route('/view-one-patient/<int:patient_id>', methods=["GET"])
def view_patient(patient_id):
    response = {}
    with sqlite3.connect("dentists.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id=" + str(patient_id))
        patient = cursor.fetchone()
        response['data'] = patient
        response['message'] = "Fetched the patient successfully"
        response['status_code'] = 200
    return response


# # ROUTE TO VIEW ALL THE PATIENTS
@app.route('/view-all-patients/', methods=['GET'])
def fetch_patients():
    response = {}
    with sqlite3.connect("dentists.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")

        response['status_code'] = 200
        response['message'] = "Fetched all patients"
        response['data'] = cursor.fetchall()
    return response


# ROUTE FOR EDITING REGISTERED PATIENTS
@app.route('/edit-patient/', methods=["PUT"])
def edit_patient():
    response = {}

    if request.method == "PUT":
        try:
            patient_email = request.json["patient_email"]
            patient_password = request.json["patient_password"]
            patient_name = request.json["patient_name"]
            patient_surname = request.json["patient_surname"]
            patient_dob = request.json["patient_dob"]
            patient_gender = request.json["patient_gender"]
            patient_cellphone = request.json["patient_cellphone"]

            with sqlite3.connect('dentist_appointment.db') as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE patient SET patient_email=?,"
                               "patient_password=?,"
                               "patient_name=?,"
                               "patient_surname=?,"
                               "patient_dob=?,"
                               "patient_gender=?,"
                               "patient_cellphone=? WHERE patient_id=?",
                               (patient_email, patient_password, patient_name, patient_surname,
                                patient_dob, patient_gender, patient_cellphone))

                conn.commit()
                response['message'] = "Patient successfully registered"
                response['status_code'] = 201

        except ValueError:
            response['message'] = "Incorrect Values"
            response['status_code'] = 400
            return response

        except ConnectionError:
            response['message'] = "Connection Failed"
            response['status_code'] = 500
            return response

        except TimeoutError:
            response['message'] = "Connection Timeout"
            response['status_code'] = 500
            return response

    else:
        response['message'] = "Incorrect method"
        response['status_code'] = 400
        return response


# ROUTE FOR DELETING PATIENT
@app.route('/delete-patient/<int:patient_id>', methods=["DELETE"])
def delete_patient(patient_id):
    response = {}
    if request.method == "DELETE":
        with sqlite3.connect("dentists.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE patient_id=" + str(patient_id))
            conn.commit()

            response['status_code'] = 200
            response['message'] = "Patient deleted successfully"
        return response
    else:
        if request.method != "DELETE":
            response['status_code'] = 400
            response['message'] = "Wrong Method"
            return response


# ROUTE FOR USER TO LOGIN
# @app.route('/user/login/')
# def user_login():

# login_tries = 3:
#     if login_tries > 3:
#
#     return 'Your account has been locked. Contact the administrator'
#     return 'Please login with username and password!'


# zxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxczxcvxcvzxcvzxcvzxcvzxcvzxcvzxc
# ROUTE FOR ADDING BOOKING (post)
@app.route('/add-booking/<int:patient_id>', methods=["POST"])
def appointment(patient_id):
    response = {}

    try:
        patient_name = request.json["patient_name"]
        patient_surname = request.json["patient_surname"]
        patient_email = request.json["patient_email"]
        patient_cellphone = request.json["patient_cellphone"]
        patient_service = request.json["patient_service"]
        current_date = request.json["current_date"]
        booking_date = request.json["booking_date"]
        patient_id = patient_id

        # to check if email is valid
        ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if request.method == "POST":
            if re.search(ex, patient_email):
                with sqlite3.connect("dentist_appointment.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO booking ("
                                   "patient_name,"
                                   "patient_surname,"
                                   "patient_email,"
                                   "patient_cellphone,"
                                   "patient_service,"
                                   "current_date,"
                                   "booking_date,"
                                   "patient_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                                   (patient_name, patient_surname, patient_email, patient_cellphone,
                                    patient_service, current_date, booking_date, patient_id))
                    conn.commit()

                    msg = Message("Dentist Booking", sender="aaliyahjardien04@gmail.com", recipients=[patient_email])
                    msg.body = "Booking made for:" + str(patient_name) + "for the date of " + str(booking_date)
                    mail.send(msg)

                    response['message'] = "Booking made successfully"
                    response['status_code'] = 200
                    # response['data'] = {
                    #     patient_name: patient_name,
                    #     patient_surname: patient_surname,
                    #     patient_email: patient_email,
                    #     patient_cellphone: patient_cellphone,
                    #     patient_service: patient_service,
                    #     current_date: current_date,
                    #     booking_date: booking_date,
                    #     patient_id: patient_id
                    #     }
                    return response

            else:
                response['error_message'] = "Invalid Email"
                response['status_code'] = 404
                return response

        else:
            response['message'] = "Incorrect method"
            response['status_code'] = 400
            return response

    except ValueError:
        response['error'] = "Invalid"
        response['status_code'] = 404
        return response


# ROUTE TO DISPLAY ONE BOOKING
@app.route('/view-booking/<int:patient_id>', methods=['GET'])
def fetch_appointment(patient_id):
    response = {}
    with sqlite3.connect("dentist_appointment.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE patient_id=" + str(patient_id))
        date_check = cursor.fetchone()

        response['status_code'] = 200
        response['message'] = "Fetch one appointment"
        response['data'] = date_check
    return response


# ROUTE FOR DISPLAYING BOOKING (get)
@app.route('/display-booking/', methods=['GET'])
def view_appointments():
    response = {}
    with sqlite3.connect("dentist_appointment.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM booking")

        response['status_code'] = 200
        response['message'] = "Displaying all appointments."
        response['data'] = cursor.fetchall()
    return response


# # ROUTE FOR EDITING BOOKING (put)
# @app.route('/edit-booking/nt:patient_id>', methods=["PUT"])


# ROUTE FOR CANCELING BOOKING (delete)
@app.route('/delete-booking/<int:patient_id>', methods=["DELETE"])
def delete_appointment(patient_id):
    response = {}
    if request.method == "DELETE":
        with sqlite3.connect("dentist_appointment.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM appointments WHERE patient_id=" + str(patient_id))
            conn.commit()

            response['status_code'] = 200
            response['message'] = "Appointment deleted successfully"
        return response
    else:
        response['status_code'] = 400
        response['message'] = "Wrong Method"
        return response


# showing date & time of when the patient scheduled an appointment
x = datetime.datetime.now()
print(x)


@app.route('/user/logout/')
def user_logout():
    return 'Successfully, logout!'


# ERROR HANDLING
# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     # this handles all the errors is non-specific
#     response = e.get_response()
#     response.data = json.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
#     return response


@app.errorhandler(404)
def handle_exception(e):
    # this specifically handles 404 errors
    response = {'status_code': e.code, 'error_message': e.description}
    return response


@app.errorhandler(500)
def internal_server_error(e):
    # this specifically handles 500 errors
    response = {'status_code': e.code, 'error_message': e.description}
    return response


# RUNNING APP
if __name__ == '__main__':
    app.run()
