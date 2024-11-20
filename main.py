from flask import Flask, render_template, session, request, url_for, redirect
import pymysql

conn = pymysql.connect(host='localhost', 
                       user='root', 
                       password='root', 
                       db='flying_schema',
                       charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

#app.secret_key = 'isabelle'


@app.route('/userHome')
def userHome():
    #email = session['email']
    #cursor=conn.cursor()
    #cursor.execute('SELECT first_name FROM customer WHERE email = %s', (email,))
    #user = cursor.fetchone()
    #cursor.close()
    return render_template('userHome.html')
    #if user:
     #   name = user['first_name'] 
      #  return render_template('index.html', name=name)
    
@app.route('/userTrips')
def userTrips():
    return render_template('userTrips.html')

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
                       FROM flights 
                       WHERE startingPoint=%s AND destination=%s AND deptDate=%s AND retDate=%s"""
            cursor.execute(query, (startingPoint, destination, deptDate, retDate))

        #one way query
        else:
            query = """SELECT * 
                       FROM flights 
                       WHERE startingPoint=%s AND destination=%s AND deptDate=%s"""
            cursor.execute(query, (startingPoint, destination, deptDate))
        
        results = cursor.fetchall()

        if results:
            return render_template('results.html', results=results)
        else:
            return render_template('results.html', message='No flights found')


            


    return render_template('tripSearch.html')


        


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)