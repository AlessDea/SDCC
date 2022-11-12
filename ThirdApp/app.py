import requests
from flask import Flask, redirect, url_for, render_template, request, session, flash
import sys
import json

app = Flask(__name__)
app.secret_key = "BAD_SECRET_KEY" # secret key for the session

ip = ''
url_prefix = 'http://'
url_suffix_doubleauth = ':30001/double_auth'
url_suffix_register_user = ':30001/register_user'
url_suffix_shared = ':30001/shared_pass'
url_register_user = ''
url_doubleauth = ''
url_shared = ''


@app.route("/", methods=["GET","POST"])
@app.route("/mylogin", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form['submit'] == 'login':
            email = request.form['email']
            service = 'MyService'
            msg = {'email': email, 'service': service}
            resp = requests.put(url_doubleauth, json=json.dumps(msg))
            if resp.json()['Answer'] == "OK":
                session['email'] = email
                session['service'] = service
                return redirect(url_for("doubleauth"))

            flash('Something went wrong, please retry.', category="login_error")
        else:
            email = request.form['email']
            service = 'MyService'
            msg = {'email': email, 'service': service}
            resp = requests.put(url_register_user, json=json.dumps(msg))
            if resp.json()['Answer'] == "REGISTERED":
                flash('Registered successfully!', category="register_success")
            else:
                flash('Something went wrong during the registration, please retry!', category="register_error")

    return render_template("mylogin.html")


@app.route('/doubleauth', methods=["GET","POST"])
def doubleauth(): 
    if session.get('email', None) == None:
        return redirect(url_for("login"))

    if request.method == "POST":
        email = session['email']
        service = session.get("service", None)
        code = str(request.form['code1']) + str(request.form['code2']) + str(request.form['code3']) + str(request.form['code4']) + str(request.form['code5'])
        msg = {'email': email, 'service':  service, 'code': code}
        resp = requests.post(url_doubleauth, json=json.dumps(msg))
        if resp.json()['Answer'] == "CORRECT":
            return redirect(url_for("protectedarea"))
        flash("Error! Try again!")

    return render_template("doubleauth.html")

@app.route("/protectedarea", methods=["GET","POST"])
def protectedarea():
    if session.get('email', None) == None:
        return redirect(url_for("login"))

    if request.method == "POST":
        email = session['email']
        service = session.get('service', None)
        password = request.form['password']
        group_name = request.form['group_name']
        msg = {'email': email, 'service': service, 'group_name': group_name, 'password': password}
        resp = requests.post(url_shared, json=json.dumps(msg))
        if resp.json()['Answer'] == "OK":
            return redirect(url_for("home"))
        flash("Error! Try again!")
    return render_template("protectedarea.html")
    

@app.route("/home", methods=["GET","POST"])
def home():
    if request.method == "POST":
        return redirect(url_for("logout"))
    return render_template("home.html")


@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('service', None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Usage: python3 app.py IP_MINIKUBE")
    else:
        ip = sys.argv[1]
        url_doubleauth = url_prefix + str(ip) + url_suffix_doubleauth
        url_register_user = url_prefix + str(ip) + url_suffix_register_user
        url_shared = url_prefix + str(ip) + url_suffix_shared
        app.run(host="0.0.0.0",debug=True)