import gateway_client
import logging
from flask import Flask
from flask import request, session, render_template, redirect, url_for, flash

# https://towardsdatascience.com/using-python-flask-and-ajax-to-pass-information-between-the-client-and-server-90670c64d688

app = Flask(__name__)
app.config['SECRET_KEY'] = '52a645324b49268eb7335fe0d9fe5b675ab33b49053845b4' # For flash
app.secret_key = "BAD_SECRET_KEY"


# +-----------------+
# | Default routing |
# +-----------------+
@app.route('/')
def index():
    return redirect(url_for('homepage'))


# +------------------------------------------------------------------+
# | Routing verso homepage, se già loggato viene indirizzato in home |
# +------------------------------------------------------------------+
@app.route('/homepage', methods=['GET','POST'])
def homepage():
    if session.get('username', None) != None:
        return redirect(url_for('home'))
    return render_template('homepage.html')


# +-------------------------------------+
# | Routing verso home, login richiesto |
# +-------------------------------------+
@app.route('/home', methods=['GET','POST'])
def home():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    return render_template('home.html', agency=session.get('isAgency', None), hasAgency=session.get('hasAgency', None))


# +------------------------------------------------------------------+
# | Routing verso register, se già loggato viene indirizzato in home |
# +------------------------------------------------------------------+
@app.route('/register', methods=['GET','POST'])
def register():
    if session.get('username', None) != None:
        return redirect(url_for('home'))
    if request.method == 'POST':

        try:
            if request.form['submit'] == 'user_register':
                # se viene registrato un utente
                email = request.form['email']
                password = request.form['user_password']
                registered = gateway_client.registration(email, password, False)
            else:
                # se viene registrata un'agenzia
                agency = request.form['agency_name']
                password = request.form['agency_password']
                registered = gateway_client.registration(agency, password, True)

            if registered:
                flash('Successfully registered, log in to the site to enter the platform!')
                return redirect(url_for('login'))
            else:
                flash('Error, please try again using an other username/agency name.')
        except:
            flash('Sorry, something went wrong! Please try again.')

    return render_template('register.html')


# +---------------------------------------------------------------+
# | Routing verso login, se già loggato viene indirizzato in home |
# +---------------------------------------------------------------+
@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('username', None) != None:
        return redirect(url_for('home'))
    if request.method == 'POST':
        try:
            if request.form['submit'] == 'user_login':
                # se logga un utente
                username = request.form['email']
                password = request.form['user_password']
                isAgency = False
                isLogged = gateway_client.doLogin(username, password, isAgency)
            else:
                # se logga un'agenzia
                username = request.form['agency_name']
                password = request.form['agency_password']
                isAgency = True
                isLogged = gateway_client.doLogin(username, password, isAgency)

            if isLogged == 1:
                # Credenziali corrette (se logga un utente) + setup sessione
                session['username'] = username
                session['isAgency'] = str(isAgency)
                session['hasAgency'] = str(False)
                return redirect(url_for('home'))
            elif isLogged == 2:
                # Credenziali corrette (se logga un'agenzia) + setup sessione
                session['username'] = username
                session['isAgency'] = str(isAgency)
                session['hasAgency'] = str(True)
                return redirect(url_for('home'))
            elif isLogged == 0:
                # Credenziali errate
                flash('Invalid credentials.')
        except:
            flash('Sorry, something went wrong! Please try again.')
    return render_template('login.html')


# +-------------------------------------------------------------------------+
# | Routing verso homepage dopo aver cancellato la session, login richiesto |
# +-------------------------------------------------------------------------+
@app.route("/logout")
def logout():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    session.pop('username', None)
    session.pop('isAgency', None)
    session.pop('hasAgency', None)
    return redirect(url_for('homepage'))


# +--------------------------------------------+
# | Routing verso newpassword, login richiesto |
# +--------------------------------------------+
@app.route('/newpassword', methods=['GET','POST'])
def newpassword():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    if session.get('isAgency', None) != 'True':
        isAgency = session.get('isAgency', None)
        type1 = None
        if request.method == 'POST':
            service  = request.form['service']
            save     = request.form.get('savePssw')
            if save == 'yes':
                save = True
            else:
                save = False
            username = session.get('username', None)
            len      = request.form['len']
            if not len:
                flash('Len is required!')
            else:

                if not request.form.get('symb'):
                    symbol = False
                else:
                    symbol = True

                type = request.form['r1']
                try:
                    if type != 'num':
                        type1 = request.form['r2']
                        if type1 == 'ulc':
                            npw = gateway_client.getNewAlphaNumericPassword(username, int(len), service, symbol, save)
                        elif type1 == 'uc':
                            npw = gateway_client.getNewUpperPassword(username, int(len), service, symbol, save)
                        else:
                            npw = gateway_client.getNewLowerPassword(username, int(len), service, symbol, save)
                    else:
                        npw = gateway_client.getNewNumericPassword(username, int(len), service, symbol, save)

                    message = "Your new password:"

                    if save:
                        message = "New password correctly saved:"
                        if not service:
                            flash('Error: to save your password, you need to specify the liked Service!')
                            return render_template('newPassword.html', agency=isAgency, hasAgency=session.get('hasAgency', None))
                        if not npw[1]:
                            flash('Error saving your password!')
                            return render_template('newPassword.html', agency=isAgency, hasAgency=session.get('hasAgency', None))

                    return render_template('newPassword.html', agency=isAgency, hasAgency=session.get('hasAgency', None), newpasswd=npw[0], msg=message)
                except:
                    flash('Sorry, something went wrong! Please try again.')

        return render_template('newPassword.html', agency=isAgency, hasAgency=session.get('hasAgency', None))
    return redirect(url_for('home'))


# +---------------------------------------------+
# | Routing verso savepassword, login richiesto |
# +---------------------------------------------+
@app.route('/savepassword', methods=['GET','POST'])
def savepassword():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    if session.get('isAgency', None) != 'True':
        isAgency = session.get('isAgency', None)
        if request.method == 'POST':
            password = request.form['password']
            service = request.form['service']
            if request.form['submit'] == 'save':
                username = session.get('username', None)
                try:
                    ret = gateway_client.savePassword(username, str(password), service)
                    if ret:
                        flash('Password for \''+service+'\' successfully stored!')
                except:
                    flash('Sorry, something went wrong! Please try again.')

        return render_template('savePassword.html', agency=isAgency, hasAgency=session.get('hasAgency', None))
    return redirect(url_for('home'))


# +---------------------------------------------+
# | Routing verso listpassword, login richiesto |
# +---------------------------------------------+
@app.route('/listpasswords', methods=['GET','POST'])
def listpasswords():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    if session.get('isAgency', None) != 'True':
        isAgency = session.get('isAgency', None)
        if request.method == 'POST':
            username = session.get('username', None)
            try:
                lista = gateway_client.doList(username)
                if lista:
                    return render_template('listPasswords.html', agency=isAgency, hasAgency=session.get('hasAgency', None), lista=lista)
            except:
                flash('Sorry, something went wrong! Please try again.')

        return render_template('listPasswords.html', agency=isAgency, hasAgency=session.get('hasAgency', None))
    return redirect(url_for('home'))


# +------------------------------------------+
# | Routing verso grouplist, login richiesto |
# +------------------------------------------+
@app.route('/grouplist', methods=('GET', 'POST'))
def grouplist():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    if session.get('isAgency', None) != 'True':
        if request.method == 'POST':
            try:
                email = session['username']
                splitted = (request.form['submit']).split(',')
                group_name = splitted[0]
                service = splitted[1]
                response, message = gateway_client.passwordRequest(group_name, email, service)
                flash(message)
            except:
                flash('Sorry, an error occurred requiring the Shared Password! Please try again.')
        try:
            lista = gateway_client.groupList(session.get('username', None))
            return render_template('groupList.html', agency=session.get('isAgency', None), hasAgency=session.get('hasAgency', None), lista=lista)
        except:
            flash('Sorry, something went wrong! Please try again.')
            return render_template('groupList.html', agency=session.get('isAgency', None), hasAgency=session.get('hasAgency', None), lista={})

    return redirect(url_for('home'))


# +--------------------------------------------+
# | Routing verso groupcreate, login richiesto |
# +--------------------------------------------+
@app.route('/groupcreate', methods=('GET', 'POST'))
def groupcreate():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    isAgency = session.get('isAgency', None)
    if isAgency == 'True':
        if request.method == 'POST':
            counter = int(request.form['counter']) + 1
            if counter > 2:
                group_list = []
                for i in range(1,counter):
                    user = request.form['username'+str(i)]
                    if user in group_list:
                        flash('Error, duplicated user!')
                        return render_template('groupCreate.html', agency=isAgency, hasAgency=session.get('hasAgency', None))
                    group_list.append(user)
                group_name = request.form['group_name']

                try:
                    response = gateway_client.groupCreate(group_name, group_list, session.get('username', None))

                    if response == 0:
                        flash('Group \''+group_name+'\' created succesfully!')
                    elif response == -1:
                        flash('Error, something went wrong, try to use another Group Name!')
                    elif response == 1:
                        flash('Error, all the users has to be your employee!')
                except:
                    flash('Sorry, something went wrong! Please try again.')
            else:
                flash('Error, insert at least 2 different members!')
        return render_template('groupCreate.html', agency=isAgency, hasAgency=session.get('hasAgency', None))
    return redirect(url_for('home'))


# +--------------------------------------------+
# | Routing verso addemployee, login richiesto |
# +--------------------------------------------+
@app.route('/addemployee', methods=('GET', 'POST'))
def addemployee():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    if session.get('isAgency', None) == 'True':
        if request.method == 'POST':
            try:
                response = gateway_client.addEmployee(request.form['myInput'], session.get('username', None))
                if response:
                    flash('Employee correctly added!')
                else:
                    flash('Error, user not found or unable to add the employee!')
            except:
                flash('Sorry, something went wrong! Please try again.')

        return render_template('addEmployee.html', agency=session.get('isAgency', None), hasAgency=session.get('hasAgency', None))
    return redirect(url_for('home'))


# +---------------------------------------------+
# | Routing verso notification, login richiesto |
# +---------------------------------------------+
@app.route('/notification', methods=['GET','POST'])
def notification():
    if session.get('username', None) == None:
        return redirect(url_for('login'))
    if session.get('isAgency', None) != 'True':
        try:
            lista = gateway_client.getRequestList(session.get('username', None))
            logging.warning('Lista: ' + str(lista))
        except:
            flash('An error occurred, try again!')
            return render_template('notification.html', agency=session.get('isAgency', None), hasAgency=session.get('hasAgency', None), lista=[])

        if request.method == 'POST':

            values = (request.form['submit']).split(',')

            accept_decline = int(values[0])
            agency     = values[1]
            group_name = values[2]
            applicant  = values[3]
            token      = request.form['token']

            if accept_decline:
                accept_decline = True
            else:
                accept_decline = False

            try:
                response = False
                response = gateway_client.acceptDecline(group_name,agency,applicant,session.get('username', None), token, accept_decline)

                if response:
                    flash('Response correctly sent!')
                else:
                    flash('Sorry, something went wrong! Please try again.')

                lista = gateway_client.getRequestList(session.get('username', None))
                logging.warning('Lista: ' + str(lista) + ' | ' + str(type(lista)))

            except:
                if response:
                    flash('Response correctly sent but can\'t reload correctly the page.')
                else:
                    flash('Sorry, something went wrong! Please try again.')
                return render_template('notification.html', agency=session.get('isAgency', None), hasAgency=session.get('hasAgency', None), lista=[])

        return render_template('notification.html', agency=session.get('isAgency', None), hasAgency=session.get('hasAgency', None), lista=lista)
    
    return redirect(url_for('home'))


if __name__ == '__main__':
    logging.basicConfig()
    app.run(host='0.0.0.0', port=5000, debug=True)