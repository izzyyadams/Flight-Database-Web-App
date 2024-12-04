from flask import Flask, render_template, session, request, url_for, redirect
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
    email = session['email']
    cursor=conn.cursor()
    cursor.execute('SELECT first_name FROM customer WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        name = user['first_name'] 
        return render_template('userHome.html', name=name)
    else:
        error_message = "User not found. Please check your login details."
        return render_template('userHome.html', error=error_message)
    


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
        print("Starting Point:", startingPoint)
        print("Destination:", destination)
        print("Departure Date:", deptDate)

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