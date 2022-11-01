import gateway_client
from flask import Flask
from flask import request, session, render_template, redirect, url_for, flash, make_response

# https://towardsdatascience.com/using-python-flask-and-ajax-to-pass-information-between-the-client-and-server-90670c64d688

app = Flask(__name__)
app.config['SECRET_KEY'] = '52a645324b49268eb7335fe0d9fe5b675ab33b49053845b4' # For flash
app.secret_key = "BAD_SECRET_KEY"


@app.route('/')
def index():
    return redirect(url_for('homepage'))


@app.route('/homepage', methods=['GET','POST'])
def homepage():
    return render_template('homepage.html')


@app.route('/home', methods=['GET','POST'])
def home():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    return render_template('home.html', agency=session.get('isAgency', None))


@app.route('/register', methods=['GET','POST'])
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
            flash('Successfully registered, log in to the site to enter the platform')
            return redirect(url_for('login'))
        elif registered == None:
            flash('Error, please try again using an other username/agency name')
        else:
            flash('Error, please try again using an other username/agency name')
        
    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
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
            session['username'] = username
            session['isAgency'] = str(isAgency)
            if not isAgency:
                session['email'] = gateway_client.getEmail(username)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')

    return render_template('login.html')


@app.route("/logout")
def logout():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    session.pop('username', None)
    session.pop('isAgency', None)
    session.pop('email', None)
    return redirect(url_for('homepage'))


@app.route('/newpassword', methods=['GET','POST'])
def newpassword():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    isAgency = session['isAgency']
    type1 = None
    if request.method == 'POST':
        service  = request.form['service']
        save     = request.form.get('savePssw')
        if save == 'yes':
            save = True
        else:
            save = False
        username = session['username']
        len      = request.form['len']
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
                    npw = gateway_client.getNewAlphNumPw(username, int(len), service, symbol, save)
                elif type1 == 'uc':
                    npw = gateway_client.getNewUpperPw(username, int(len), service, symbol, save)
                else:
                    npw = gateway_client.getNewLowerPw(username, int(len), service, symbol, save)
            else:
                npw = gateway_client.getNewNumPw(username, int(len), service, symbol, save)

            message = "Your new password:"
            
            if save:
                message = "New password correctly saved:"
                if not service:
                    flash('Error: to save your password, you need to specify the liked Service!')
                    return render_template('newPassword.html', agency=isAgency)

                if not npw[1]:
                    flash('Error saving your password!')
                    return render_template('newPassword.html', agency=isAgency)

            return render_template('newPassword.html', agency=isAgency, newpasswd=npw[0], msg=message)

    return render_template('newPassword.html', agency=isAgency)


@app.route('/savepassword', methods=['GET','POST'])
def savepassword():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    isAgency = session['isAgency']
    if request.method == 'POST':
        password = request.form['password']
        service = request.form['service']
        if request.form['submit'] == 'save':
            username = session['username']
            ret = gateway_client.savePw(username, str(password), service)
            if ret:
                flash('Password for \''+service+'\' successfully stored!')
            else:
                flash('Error: the DB is not responding or this is already your password for \''+service+'\'!')
        else:
            # SAFETY_CHECK
            flash('Error!: SAFETY_CHECK still not implemented!')  # DA IMPLEMENTARE

    return render_template('savePassword.html', agency=isAgency)


@app.route('/newdoublecode', methods=['GET','POST'])
def newdoublecode():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    isAgency = session['isAgency']
    if request.method == 'POST':
        code = gateway_client.getNewNumPw(6, False)
        return render_template('newDoubleCode.html', agency=isAgency, newpasswd=code)
    return render_template('newDoubleCode.html', agency=isAgency)


@app.route('/listpasswords', methods=['GET','POST'])
def listpasswords():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    isAgency = session['isAgency']
    if request.method == 'POST':
        username = session['username']
        lista = gateway_client.doList(username)
        if lista:
            return render_template('listPasswords.html', agency=isAgency, lista=lista)
        else:
            flash('No passwords found!')
    return render_template('listPasswords.html', agency=isAgency)

@app.route('/grouplist', methods=('GET', 'POST'))
def grouplist():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    if session.get('isAgency', None) != 'True':
        # if request.method == 'POST':
        #   qualcosa
        return render_template('groupList.html', lista=["gruppo1","gruppo2","gruppo3"])
    return redirect(url_for('home'))

@app.route('/groupcreate', methods=('GET', 'POST'))
def groupcreate():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    isAgency = session['isAgency']
    if session.get('isAgency', None) == 'True':
        # if request.method == 'POST':
        #   qualcosa
        return render_template('groupCreate.html')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)