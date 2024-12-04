from flask import Flask, render_template, session, request, url_for, redirect
from datetime import datetime
import pymysql

conn = pymysql.connect(host='localhost', 
                       user='root', 
                       password='', 
                       db='flying_schema',
                       charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

app.secret_key = 'isabelle'

# IZZY 
@app.route('/userHome')
def userHome():
    #JUST FOR TESTING
    session['email'] = 'alaska@mr.com'
    #end just for testing
    
    #gets name of user
    email = session['email']
    cursor=conn.cursor()
    cursor.execute('SELECT first_name FROM customer WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    name = user['first_name'] 

    #gets flights of user
    cursor2 = conn.cursor()
    cursor2.execute('SELECT flight.airline_name, flight.airport_code, flight.arrival, flight.departure, flight.arrival_airport_code FROM ticket INNER JOIN flight ON ticket.flight_num = flight.flight_num WHERE ticket.email = %s', (email,))
    userFlights = cursor2.fetchall()
    cursor2.close()
    flightInfoList= []
    for flight in userFlights:

        airline = flight['airline_name']
        departureLocation = flight['airport_code']
        arrivalDateTime = flight['arrival']
        departureDateTime = flight['departure']
        arrivalLocation = flight['arrival_airport_code']

        arrivalDate = arrivalDateTime.strftime("%B %d, %Y")
        arrivalTime = arrivalDateTime.strftime("%I:%M %p").lstrip("0").replace(":00", "")
        departureDate = departureDateTime.strftime("%B %d, %Y")
        departureTime = departureDateTime.strftime("%I:%M %p").lstrip("0").replace(":00", "")
        flightInfo = {
            "airline": airline,
            "departureLocation": departureLocation,
            "arrivalDate": arrivalDate,
            "arrivalTime": arrivalTime,
            "departureDate": departureDate,
            "departureTime": departureTime,
            "arrivalLocation": arrivalLocation
        }
        flightInfoList.append(flightInfo)

    return render_template('userHome.html', name=name, flightInfo=flightInfoList)
    

# IZZY
@app.route('/tripSearch', methods=['GET', 'POST'])
def tripSearch():
    if request.method == 'POST':
        #getting information from form
        startingPoint = request.form['startingPoint']
        destination = request.form['destination']
        tripType = request.form['tripType']
        
        deptMonth = request.form['deptMonth']
        deptYear = request.form['deptYear']
        deptDay = request.form['deptDay']

        deptDate = f"{deptYear}-{deptMonth}-{deptDay}"

        #need if statement incase of one-way
        return_date_str = None
        if request.form.get('retMonth') and request.form.get('retDay') and request.form.get('retYear'):
            retMonth = request.form['retMonth']
            retDay = request.form['retDay']
            retYear = request.form['retYear']
            retDate = f"{retYear}-{retMonth}-{retDay}"

        
        
    
        cursor =  conn.cursor()


        #round trip query
        if tripType == 'round-trip':
            query = """SELECT * 
                       FROM flight 
                       WHERE airport_code=%s AND arrival_airport_code=%s AND departure=%s AND arrival=%s"""
            cursor.execute(query, (startingPoint, destination, deptDate, retDate))

        #one way query
        else:
            query = """SELECT * 
                       FROM flight 
                       WHERE airport_code=%s AND arrival_airport_code=%s AND DATE(departure)=%s"""
            cursor.execute(query, (startingPoint, destination, deptDate))
        
        results = cursor.fetchall()
        return render_template('results.html', results=results)


            


    return render_template('tripSearch.html')

# function to determine if the user is a customer or staff - ISABELLE
def determine_user_type(email, password):
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM Customer WHERE email = %s', (email,))
    customer = cursor.fetchone()
    if customer and customer['password'] == password:

        return "customer"

    cursor.execute('SELECT password FROM Staff WHERE email = %s', (email,))
    staff = cursor.fetchone()
    if staff and customer['password' == password:

        return "staff"

    return None

# ISABELLE 
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user_type = determine_user_type(username, password)
        if user_type == "customer":
            session['user_id'] = username
            session['role'] = 'customer'
            return redirect(url_for('/userHome'))
        elif user_type == "staff":
            session['user'] = username
            session['role'] = 'staff'
            return redirect(url_for('/staffHome'))
        else:
            error_message = "User not found. Please check your login details."
            return render_template('login.html', error=error_message)
    return render_template('login.html')

# HOMEPAGE, the first page you see when you open the app ISABELLE
@app.route('/homepage')
def homepage():
    if request.method == 'POST':
        # getting information from form
        startingPoint = request.form['startingPoint']
        destination = request.form['destination']
        tripType = request.form['tripType']

        deptMonth = request.form['deptMonth']
        deptYear = request.form['deptYear']
        deptDay = request.form['deptDay']

        deptDate = f"{deptYear}-{deptMonth}-{deptDay}"

        # need if statement incase of one-way
        return_date_str = None
        if request.form.get('retMonth') and request.form.get('retDay') and request.form.get('retYear'):
            retMonth = request.form['retMonth']
            retDay = request.form['retDay']
            retYear = request.form['retYear']
            retDate = f"{retYear}-{retMonth}-{retDay}"

        cursor = conn.cursor()
        print("Starting Point:", startingPoint)
        print("Destination:", destination)
        print("Departure Date:", deptDate)

        # round trip query
        if tripType == 'round-trip':
            query = """SELECT * 
                           FROM flight 
                           WHERE airport_code=%s AND arrival_airport_code=%s AND departure=%s AND arrival=%s"""
            cursor.execute(query, (startingPoint, destination, deptDate, retDate))

        # one way query
        else:
            query = """SELECT * 
                           FROM flight 
                           WHERE airport_code=%s AND arrival_airport_code=%s AND DATE(departure)=%s"""
            cursor.execute(query, (startingPoint, destination, deptDate))

        results = cursor.fetchall()
        return render_template('results.html', results=results)

    return render_template('homepage.html')

# ISABELLE 
@app.route('/staffHome', methods=['GET'])
def staffHome():
    if 'role' in session and session['role'] == 'staff':
        username = session['user']
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE (departure > NOW() and departure < current_date + INTERVAL '1 MONTH'"
        cursor.execute(query)
        flights = cursor.fetchall()

        cursor.execute("SELECT first_name FROM staff WHERE username = %s", (username,))
        user = cursor.fetchone()
        name = user['first_name']
        return render_template('staffHome.html', flights=flights, name = name)
    else:
        return redirect(url_for('loginAuth'))




if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
