import gateway_client
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify, url_for, flash, redirect
import tempfile
import random
import socket  # for the hostname

# https://towardsdatascience.com/using-python-flask-and-ajax-to-pass-information-between-the-client-and-server-90670c64d688

app = Flask(__name__)
app.config['SECRET_KEY'] = '52a645324b49268eb7335fe0d9fe5b675ab33b49053845b4'       # serve a flash



@app.route('/newpassword/', methods=('GET', 'POST'))
def newpassword():
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

                service = request.form['service']
                save = request.form['check']



                if type1 == 'ulc':
                    npw = gateway_client.getNewAlphNumPw(int(len), symbol)
                elif type1 == 'uc':
                    npw = gateway_client.getNewUpperPw(int(len), symbol)
                else:
                    npw = gateway_client.getNewLowerPw(int(len), symbol)

            else:

                npw = gateway_client.getNewNumPw(int(len), symbol)


            return render_template('newPassword.html', newpasswd=npw)
    return render_template('newPassword.html')

@app.route('/savepassword/', methods=('GET', 'POST'))
def savepassword():
    if request.method == 'POST':
        code = gateway_client.getNewNumPw(6)
        return render_template('savePassword.html', newpasswd=code)
    return render_template('savePassword.html')


@app.route('/newdoublecode/', methods=('GET', 'POST'))
def newdoublecode():
    if request.method == 'POST':
        code = gateway_client.getNewNumPw(6)
        return render_template('newDoubleCode.html', newpasswd=code)
    return render_template('newDoubleCode.html')


@app.route('/listpasswords/', methods=('GET', 'POST'))
def listpasswords():
    if request.method == 'POST':
        pwlist = {'p1': 'n', 'p2':'n','p3': 't', 'p4': 'n', 'p5': 't'}
        return render_template('listPasswords.html', pwlist=pwlist)
    return render_template('listPasswords.html')



@app.route('/')
def home():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


