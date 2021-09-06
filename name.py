# ROUTE TO REGISTER A PATIENT
@app.route('/patient', methods=['POST'])
def patient_registration():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    address = request.json['address']
    email = request.json['email']
    birth_date = request.json['birth_date']
    gender = request.json['gender']
    phone_num = request.json['phone_num']
    id_num = request.json['id_num']
    response = {}
    # to check if email is valid
    ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    x = "Welcome to the Dentist registration"
    try:
        if request.method == "POST":
            if re.search(ex, email):
                with sqlite3.connect("dentists.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO patients("
                                   "first_name,"
                                   "last_name,"
                                   "address,"
                                   "email,"
                                   "birth_date,"
                                   "gender,"
                                   "phone_num,"
                                   "id_num) VALUES(?,?,?,?,?,?,?,?)",
                                   (first_name, last_name, address, email, birth_date,
                                    gender, int(phone_num), int(id_num)))
                    conn.commit()
                    # Sending an email to the patient
                    msg = Message("Registered Successfully", sender="lifechoiceslotto147@gmail.com", recipients=[email])
                    msg.body = x
                    mail.send(msg)
                    response['message'] = "Registered patient successfully"
                    response['data'] = {
                        "first name": first_name,
                        "last_name": last_name,
                        "address": address,
                        "email": email,
                        "birth date": birth_date,
                        "gender": gender,
                        "phone number": phone_num,
                        "id number": id_num
                    }
                    response['status_code'] = 201
                return response
            else:
                response['error_message'] = "Invalid Email"
                response['status_code'] = 404
                return response
        else:
            if request.method != "POST":
                response['error'] = "Wrong method, it must be a POST"
                return response

    except ValueError:
        if phone_num != int or id_num != int:
            response['error_message'] = "Values or not in a number"
            response['status_code'] = 400
        return response
    except ConnectionError:
        response['message'] = "No Connection"
        return response


# ROUTE TO VIEW ONE PATIENT
@app.route('/view-patient/<int:patient_id>', methods=["GET"])
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


# ROUTE TO VIEW ALL THE PATIENTS
@app.route('/view-patient/', methods=['GET'])
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


# ROUTE FOR EDITING PATIENT
@app.route('/edit-patient/<int:patient_id>', methods=['PUT'])
def edit_patient(patient_id):
    # a route that can edit information of the patient
    response = {}
    email = request.json['email']
    phone_num = request.json['phone_num']
    address = request.json['address']
    # To check if the email is in correct format
    ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if request.method == "PUT":
        try:
            with sqlite3.connect("dentists.db") as conn:
                if re.search(ex, email):
                    cursor = conn.cursor()
                    cursor.execute("UPDATE patients SET email=?, phone_num=?, address=?"
                                   "WHERE patient_id=?", (email, phone_num, address, patient_id))
                    conn.commit()
                    response['message'] = "Update was successful"
                    response['status_code'] = 200
                    return response
                else:
                    response['error_message'] = "Invalid Email"
                    response['status_code'] = 404
                    return response
        except ValueError:
            response['error'] = "Failed"
            response['status_code'] = 404
            return response
    else:
        if request.method != "PUT":
            response['message'] = "Wrong method"
            response['status_code'] = 404


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


# ROUTE TO MAKE AN APPOINTMENT
@app.route('/appointment/<int:patient_id>', methods=["POST"])
def appointment(patient_id):
    response = {}
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone_num = request.json['phone_num']
    a_type = request.json['type']
    booking_date = request.json['booking_date']
    date_made = request.json['date_made']
    patient_id = patient_id
    # to check if email is valid
    ex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if request.method == "POST":
        if re.search(ex, email):
            with sqlite3.connect("dentists.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO appointments ("
                               "first_name,"
                               "last_name,"
                               "email,"
                               "phone_num,"
                               "type,"
                               "booking_date,"
                               "date_made,"
                               "patient_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                               (first_name, last_name, email, phone_num, a_type, booking_date, date_made, patient_id))
                conn.commit()
                msg = Message("Appointment", sender="lifechoiceslotto147@gmail.com", recipients=[email])
                msg.body = "Appointment was made for:" + str(first_name) + "for the date of " + str(booking_date)
                mail.send(msg)
                response['message'] = "appointment made successfully"
                response['status_code'] = 200
                response['data'] = {
                    "first name": first_name,
                    "last_name": last_name,
                    "phone_num": phone_num,
                    "email": email,
                    "type": a_type,
                    "booking_date": booking_date,
                    "date_made": date_made,
                    "patient_id": patient_id
                }
            return response
