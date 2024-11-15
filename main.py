from flask import Flask, render_template, session, request, url_for, redirect
#import pymysql

#conn = pymysql.connect(host='localhost', 
#                       user='root', 
 #                      password='root', 
  #                     db='flying_schema',
   #                    charset="utf8mb4",
    #                   cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

#app.secret_key = 'isabelle'


@app.route('/userHome')
def userHome():
    #email = session['email']
    #cursor=conn.cursor()
    #cursor.execute('SELECT first_name FROM customer WHERE email = %s', (email,))
    #user = cursor.fetchone()
    #cursor.close()
    return render_template('index.html')
    #if user:
     #   name = user['first_name'] 
      #  return render_template('index.html', name=name)
    
@app.route('/userTrips')
def userTrips():
    return render_template('userTrips.html')

@app.route('/tripSearch')
def tripSearch():
    return render_template('tripSearch.html')


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)