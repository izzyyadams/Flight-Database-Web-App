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

#function to organize data from query to use for display IZZY
def organizeData(results):
    flightInfoList= []
    for flight in results:


        arrivalDateTime = flight['arrival']
        departureDateTime = flight['departure']
        arrivalDate = arrivalDateTime.strftime("%B %d, %Y")
        arrivalTime = arrivalDateTime.strftime("%I:%M %p").lstrip("0").replace(":00", "")
        departureDate = departureDateTime.strftime("%B %d, %Y")
        departureTime = departureDateTime.strftime("%I:%M %p").lstrip("0").replace(":00", "")
        flightInfo = {
            "airline": flight['airline_name'],
            "departureLocation": flight['airport_code'],
            "arrivalDate": arrivalDate,
            "arrivalTime": arrivalTime,
            "departureDate": departureDate,
            "departureTime": departureTime,
            "arrivalLocation": flight['arrival_airport_code'],
            "basePrice": flight['base_price'],
            "status": flight['Status'],
            "flightNum": flight['flight_num']
        }
        flightInfoList.append(flightInfo)


    return flightInfoList


# IZZY 
@app.route('/userHome')
def userHome():
    
    #gets name of user
    email = session['user_id']
    cursor=conn.cursor()
    cursor.execute('SELECT first_name FROM customer WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    name = user['first_name'] 

    #gets flights of user
    cursor2 = conn.cursor()
    query = """SELECT flight.airline_name, flight.airport_code, flight.arrival, flight.departure, flight.arrival_airport_code, flight.base_price, flight.Status, flight.flight_num 
            FROM ticket INNER JOIN flight ON ticket.flight_num = flight.flight_num 
            WHERE ticket.email = %s and flight.departure > NOW()
            """
    cursor2.execute(query, (email,))
    userFlights = cursor2.fetchall()
    cursor2.close()
    flightInfoList = organizeData(userFlights)

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
        if request.form.get('retMonth') and request.form.get('retDay') and request.form.get('retYear'):
            retMonth = request.form['retMonth']
            retDay = request.form['retDay']
            retYear = request.form['retYear']
            retDate = f"{retYear}-{retMonth}-{retDay}"    
    
        cursor =  conn.cursor()


        #one-way
        query = """SELECT * 
                FROM flight 
                WHERE airport_code=%s AND arrival_airport_code=%s AND DATE(departure)=%s"""
        cursor.execute(query, (startingPoint, destination, deptDate))
        leaving = cursor.fetchall()
        organizedLeavingData = organizeData(leaving)
        cursor.close()



        #only happens if round-trip
        cursor =  conn.cursor()
        if tripType == 'round-trip':
            query2 = """SELECT * 
                       FROM flight 
                       WHERE airport_code=%s AND arrival_airport_code=%s AND DATE(departure)=%s"""
            cursor.execute(query2, (destination, startingPoint, retDate))
            returning = cursor.fetchall()
            organizedReturningData = organizeData(returning)
            cursor.close()
            combinedData =  zip(organizedLeavingData, organizedReturningData)
        else:
            combinedData=[]
            organizedReturningData = []

        return render_template('results.html', flightInfoLeaving=organizedLeavingData, flightInfoReturning=organizedReturningData, combinedData=combinedData, tripType=tripType)
            


    return render_template('tripSearch.html')

#function to cancel ticket, sends user back to home IZZY

@app.route('/cancelTicket', methods=['POST'])
def cancelTicket():
    email = session['user_id']
    flightNum = request.form['cancelTicket']
    cursor = conn.cursor()
    query = """DELETE 
                FROM Ticket
                WHERE flight_num=%s and email=%s
            """
    cursor.execute(query, (flightNum, email))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('userHome'))

#function to actually purchase the ticket IZZY
@app.route('/actualTicketPurchase', methods=['POST'])
def actualTicketCancel():
    purchaseDOBMonth = request.form['purchaseDOBMonth']
    purchaseDOBDay = request.form['purchaseDOBDay']
    purchaseDOBYear = request.form['purchaseDOBYear']
    purchaseDOBDate = f"{purchaseDOBYear}-{purchaseDOBMonth}-{purchaseDOBDay}"  
    
    flight_num1 = request.form['purchaseInfoNum1']
    calc_price1 = request.form['purchaseInfoPrice1']
    purchaseEmail =request.form['purchaseEmail']
    purchaseFirstName = request.form['purchaseFirstName']
    purchaseLastName = request.form['purchaseLastName']
    rating = None
    comments = None
    purchaseCardNum = request.form['purchaseCardNum']



    

    cursor = conn.cursor()
    query = """SELECT MAX(ticket_id), MAX(purchase_id), NOW() FROM purchase"""

    cursor.execute(query)
    queryInfo = cursor.fetchall()
    cursor.close()

    ticket_id = queryInfo[0]['MAX(ticket_id)'] + 1
    purchase_id = queryInfo[0]['MAX(purchase_id)'] + 1
    now = queryInfo[0]['NOW()']
    cursor = conn.cursor()
    query = """INSERT INTO `Ticket` (`ticket_id`, `email`, `flight_num`, `rating`, `comments`, `calc_price`, `first_name`, `last_name`, `dob`) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    query2 = """INSERT INTO `Purchase` (`purchase_id`, `ticket_id`, `purchase_date_time`, `card_info`) 
            VALUES(%s, %s, %s, %s)
            """
    cursor.execute(query, (ticket_id, purchaseEmail, flight_num1, rating, comments, calc_price1, purchaseFirstName, purchaseLastName, purchaseDOBDate))
    cursor.execute(query2, (purchase_id, ticket_id, now, purchaseCardNum))
    conn.commit()
    flight_num2 = request.form['purchaseInfoNum2']
    calc_price2 = request.form['purchaseInfoPrice2']
    if flight_num2:

        query = """INSERT INTO `Ticket` (`ticket_id`, `email`, `flight_num`, `rating`, `comments`, `calc_price`, `first_name`, `last_name`, `dob`) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(query, (ticket_id, purchaseEmail, flight_num2, rating, comments, calc_price2, purchaseFirstName, purchaseLastName, purchaseDOBDate))
    
    cursor.close()


    return redirect(url_for('userHome'))
    

           
#function to get to purchase page IZZY
@app.route('/purchaseTicket', methods=['GET', 'POST'])
def purchaseTicketRound():
    purchaseTicketFlightID1 = request.form['purchaseTicketNum1']
    purchaseTicketPricee1 = request.form['purchaseTicketPrice1']
    purchaseTicketFlightID2 = request.form['purchaseTicketNum2']
    purchaseTicketPricee2 = request.form['purchaseTicketPrice2']
    print(purchaseTicketFlightID2)

    return render_template('purchaseTicket.html', purchaseInfoNum1=purchaseTicketFlightID1, purchaseInfoPrice1=purchaseTicketPricee1, purchaseInfoNum2=purchaseTicketFlightID2, purchaseInfoPrice2=purchaseTicketPricee2)

#function to get to past flights page IZZY
@app.route('/userPastFlights', methods=['GET', 'POST'])
def userPastFlights():
    email = session['user_id']
    cursor = conn.cursor()
    query = """SELECT flight.airline_name, flight.airport_code, flight.arrival, flight.departure, flight.arrival_airport_code, flight.base_price, flight.Status, flight.flight_num, ticket.ticket_id 
            FROM ticket INNER JOIN flight ON ticket.flight_num = flight.flight_num 
            WHERE ticket.email = %s and flight.departure < NOW()"""
    cursor.execute(query, (email,))
    userFlights = cursor.fetchall()
    cursor.close()
    flightInfoList= []
    #cant sent this to function because it will miss ticket_id
    for flight in userFlights:
        arrivalDateTime = flight['arrival']
        departureDateTime = flight['departure']
        arrivalDate = arrivalDateTime.strftime("%B %d, %Y")
        arrivalTime = arrivalDateTime.strftime("%I:%M %p").lstrip("0").replace(":00", "")
        departureDate = departureDateTime.strftime("%B %d, %Y")
        departureTime = departureDateTime.strftime("%I:%M %p").lstrip("0").replace(":00", "")
        flightInfo = {
            "airline": flight['airline_name'],
            "departureLocation": flight['airport_code'],
            "arrivalDate": arrivalDate,
            "arrivalTime": arrivalTime,
            "departureDate": departureDate,
            "departureTime": departureTime,
            "arrivalLocation": flight['arrival_airport_code'],
            "basePrice": flight['base_price'],
            "status": flight['Status'],
            "flightNum": flight['flight_num'],
            "ticketID": flight['ticket_id']
        }
        flightInfoList.append(flightInfo)



    return render_template('userPastFlights.html', flightInfo=flightInfoList )


#post rate and comment (will replace preexisting ones) IZZY
@app.route('/rateAndComment', methods=['GET', 'POST'])
def rateAndComment():
    email = session['user_id']
    ticket_id = request.form['ticket_ID']
    rating = request.form['rating']
    comment = request.form['comment']
    print(email, ticket_id, rating, comment)
    cursor = conn.cursor()
    query = """UPDATE Ticket 
                SET rating=%s, comments=%s
                WHERE email=%s and ticket_id=%s
            """
    cursor.execute(query, (rating, comment, email, ticket_id))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('userPastFlights'))

#spending function IZZY
@app.route('/spending', methods=['GET', 'POST'])
def spending():

    email = session['user_id']
    today = datetime.today()
    oneYearAgo = today.replace(year=today.year - 1)
    cursor = conn.cursor()
    query = """SELECT SUM(ticket.calc_price) as amount
            FROM Purchase JOIN Ticket ON Purchase.ticket_id = Ticket.ticket_id
            WHERE email=%s and purchase.purchase_date_time > %s
            GROUP BY Ticket.email"""
    cursor.execute(query, (email, oneYearAgo))
    result = cursor.fetchall()
    lastYear = result[0]['amount']
    query2 = """SELECT DATE_FORMAT(Purchase.purchase_date_time, '%%Y-%%m') AS month, SUM(ticket.calc_price) AS totalSpent
                FROM Purchase JOIN Ticket ON Purchase.ticket_id = Ticket.ticket_id
                WHERE Ticket.email = %s
                GROUP BY month
                ORDER BY month ASC
            """
    cursor.execute(query2, (email,))
    result2 = cursor.fetchall()


    cursor.close()

    return render_template("spending.html", totalSpentYear=lastYear, data=result2)

#logout page IZZY
@app.route('/userLogout', methods=['GET', 'POST'])
def userLogout():
    if request.method == 'POST':
        yesNo = request.form['yesNo']
        if yesNo == 'logout':
            session.clear()
            return redirect(url_for('loginAuth'))
        else:
            return redirect(url_for('userHome'))

    return render_template('userLogout.html')







# function to determine if the user is a customer or staff - ISABELLE
def determine_user_type(email, password):
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM Customer WHERE email = %s', (email,))
    customer = cursor.fetchone()
    if customer and customer['password'] == password:

        return "customer"

    cursor.execute('SELECT password FROM Staff WHERE email = %s', (email,))
    staff = cursor.fetchone()
    if staff and customer['password' == password]:

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
            return redirect(url_for('userHome'))
        elif user_type == "staff":
            session['user'] = username
            session['role'] = 'staff'
            return redirect(url_for('staffHome'))
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
        results['ticket_id'] = []
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

        cursor2 = conn.cursor()
        cursor2.execute("SELECT first_name FROM staff WHERE username = %s", (username,))
        user = cursor.fetchone()
        name = user['first_name']
        return render_template('staffHome.html', flights=flights, name = name)
    else:
        return redirect(url_for('loginAuth'))

# Function to register a customer - ISABELLE 
@app.route('/customerRegister', methods=['GET', 'POST'])
def customerRegister():
    username = request.form['email']
    passport_country = request.form['passport_country']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    dob = request.form['dob']
    address = request.form['address']
    passport_number = request.form['passport_number']
    passport_exp_date = request.form['passport_exp_date']

    cursor = conn.cursor()
    query = 'Select * FROM Customer WHERE username = %'
    cursor.execute(query, (username,))
    data = cursor.fetchone()

    if data:
        error = "This customer already exists."
        cursor.close()
        return render_template("customerRegister.html", error=error)

    else:
        ins = 'INSERT INTO Customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username,passport_country, first_name, last_name,password, address, passport_number, dob, address, passport_exp_date))

        conn.commit()
        cursor.close()
        return render_template("loginAuth.html")


#FUNCTION to register a staff -ISABELLE 
@app.route('/staffRegister', methods=['GET', 'POST'])
def staffRegister():
    username = request.form['username']
    airline_name = request.form['airline_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    password = request.form['password']
    phone_number = request.form['phone_number']
    email = request.form['email']

    cursor = conn.cursor()
    query = 'SELECT * FROM Staff WHERE username = %'
    cursor.execute(query, (username,))
    data = cursor.fetchone()

    if data:
        error = "This staff already exists."
        cursor.close()
        return render_template("staffRegister.html", error=error)

    else:
        ins = "INSERT INTO Staff VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(ins, (username, airline_name, first_name, last_name, dob, password, phone_number, email))
        conn.commit()
        cursor.close()
        return render_template("loginAuth.html")





if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
