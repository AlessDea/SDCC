import gateway_client
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify, url_for, flash, redirect
from flask import make_response
import tempfile
import random
import socket  # for the hostname

# https://towardsdatascience.com/using-python-flask-and-ajax-to-pass-information-between-the-client-and-server-90670c64d688

app = Flask(__name__)
app.config['SECRET_KEY'] = '52a645324b49268eb7335fe0d9fe5b675ab33b49053845b4'       # serve a flash


@app.route('/home/', methods=('GET', 'POST'))
def home():
    # name = request.cookies.get('userID')
    return render_template('home.html')

@app.route('/newpassword/', methods=('GET', 'POST'))
def newpassword():
    isAgency = request.cookies.get('isAgency')
    type1 = None
    if request.method == 'POST':
        len = request.form['len']
        if not len:
            flash('Len is required!')
        else:

            if not request.form.get('symb'):
                symbol = False
            else:
                symbol = True

            type = request.form['r1']
            if type != 'num':
                type1 = request.form['r2']
                if type1 == 'ulc':
                    npw = gateway_client.getNewAlphNumPw(int(len), symbol)
                elif type1 == 'uc':
                    npw = gateway_client.getNewUpperPw(int(len), symbol)
                else:
                    npw = gateway_client.getNewLowerPw(int(len), symbol)
            else:
                npw = gateway_client.getNewNumPw(int(len), symbol)

            service = request.form['service']
            save = request.form.get('savePssw')

            if save:
                if not service:
                    flash('Error: to save your password, you need to specify the liked Service!')
                    return render_template('newPassword.html', agency=isAgency)
                username = request.cookies.get('userID')
                gateway_client.savePw(username, str(npw), service)          # BISOGNA METTERCI IL FLASH SE E' ANDATO BENE O NO

            return render_template('newPassword.html', agency=isAgency, newpasswd=npw)
    return render_template('newPassword.html', agency=isAgency)

@app.route('/savepassword/', methods=('GET', 'POST'))
def savepassword():
    isAgency = request.cookies.get('isAgency')
    if request.method == 'POST':
        password = request.form['password']
        service = request.form['service']
        if request.form['submit'] == 'save':
            username = request.cookies.get('userID')
            ret = gateway_client.savePw(username, str(password), service)
            if ret:
                flash('Password for \''+service+'\' successfully stored!')
            else:
                flash('Error: the DB is not responding or this is already your password for \''+service+'\'!')
        else:
            # SAFETY_CHECK
            flash('Error!: SAFETY_CHECK still not implemented!')            # DA IMPLEMENTARE

    return render_template('savePassword.html', agency=isAgency)

@app.route('/newdoublecode/', methods=('GET', 'POST'))
def newdoublecode():
    isAgency = request.cookies.get('isAgency')
    if request.method == 'POST':
        code = gateway_client.getNewNumPw(6, False)
        return render_template('newDoubleCode.html', agency=isAgency, newpasswd=code)
    return render_template('newDoubleCode.html', agency=isAgency)

@app.route('/listpasswords/', methods=('GET', 'POST'))
def listpasswords():
    isAgency = request.cookies.get('isAgency')
    if request.method == 'POST':
        username = request.cookies.get('userID')
        lista = gateway_client.doList(username)
        if lista:
            return render_template('listPasswords.html', agency=isAgency, lista=lista)
        else:
            flash('No password found!')
    return render_template('listPasswords.html', agency=isAgency)

@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    email = request.cookies.get('email')
    return '<h1>UserID = '+name+', Email = '+email+'</h1>'

@app.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if request.form['submit'] == 'user_login':
            username = request.form['username']
            password = request.form['user_password']
            isAgency = False
            isLogged = gateway_client.doLogin(username, password, isAgency)
        else:
            username = request.form['agency_name']
            password = request.form['agency_password']
            isAgency = True
            isLogged = gateway_client.doLogin(username, password, isAgency)

        if isLogged:
            resp = make_response(render_template('home.html', agency=str(isAgency)))
            resp.set_cookie('userID', username)
            resp.set_cookie('isAgency', str(isAgency))
            
            if not isAgency:
                resp.set_cookie('email', gateway_client.getEmail(username))

            return resp
            
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route("/logout")
def logout():
    resp = make_response(render_template('homepage.html'))
    resp.set_cookie('userID', '')
    resp.set_cookie('isAgency', '')
    resp.set_cookie('email', '')
    return resp

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        if request.form['submit'] == 'user_register':
            username = request.form['username']
            password = request.form['user_password']
            email = request.form['email']
            registered = gateway_client.registration(username, password, email)
        else:
            username = request.form['agency_name']
            password = request.form['agency_password']
            registered = gateway_client.registration(username, password, "")

        if registered:
            flash('Successfully registered!')
            return render_template('register.html')
        elif registered == None:
            flash('Error, please try again using an other username/agency name')
        else:
            flash('Error, please try again using an other username/agency name')
    return render_template('register.html')

@app.route('/homepage/', methods=('GET', 'POST'))
def homepage():
    if request.method == 'POST':
        return render_template('homepage.html')
    return render_template('homepage.html')

@app.route('/')
def index():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


