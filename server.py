from mysqlconnection import MySQLConnector
from flask import Flask, request, redirect, render_template, session, flash
import re
import md5
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app, 'registration')


@app.route('/') 
def index():
    users = mysql.query_db("SELECT * FROM users")
    return render_template('index.html', all_users=users)


@app.route('/newuser', methods=['POST']) 
def newuser():

    print "----"
    first = request.form['first_name']
    last = request.form['last_name']
    email = request.form['email']
    password = md5.new(request.form['password']).hexdigest()
    con_password = request.form['con_password']

    print first
    print last
    print email
    print password
    print con_password

    if len(first) and len(last) < 2 or first.isalpha() and last.isalpha():
        flash("At least 2 characters for first and last names")
        if not EMAIL_REGEX.match(request.form['email']):
            flash("Email is not valid")

        if len(password) < 8:
            flash("Password must be over 8 characters")
    else:
        query = "INSERT INTO users (first, last, email, password, con_password, created_at, updated_at) VALUES (:first, :last, :email, :password, :con_password, NOW(), NOW())"

        data = {
            'first': first,
            'last': last,
            'email': email,
            'password': password,
            'con_password': con_password
            }
        
        mysql.query_db(query, data)
        flash("Thank you for submitting the form as all entires are correct")

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['log_email']
    password = md5.new(request.form['log_password']).hexdigest()
    user_query = "SELECT * FROM users where users.email = :email AND users.password = :password"

    query_data = {
        'email': email,
        'password': password
        }

        

    user = mysql.query_db(user_query, query_data)
    print "Users ", user
    print "query_data ", query_data
    print "email ", email
    print "password ", password
    return redirect('/') 

app.run(debug=True)