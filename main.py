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



if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)