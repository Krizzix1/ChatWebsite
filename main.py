from flask import Flask, render_template, url_for, redirect, jsonify, request, session, flash
from Messages.messages import messageBP
from Login.login import loginBP
from Signup.signup import signupBP

import database, security

app = Flask(__name__)
app.register_blueprint(messageBP, url_prefix="/messages")
app.register_blueprint(loginBP, url_prefix="/login")
app.register_blueprint(signupBP, url_prefix="/signup")

#figure out this more later however its needed to stop users going straight to home page without logging in
app.secret_key = security.gen_secret_key()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        if action == "login":
            return redirect(url_for("loginBP.login"))
        elif action == "signup":
            return redirect(url_for("signupBP.signup"))
    return render_template("home.html")


@app.route("/main", methods=["GET","POST"])
def main():
    if "username" not in session:
        print("You must login first")
        flash("You must login first")
        return redirect(url_for("loginBP.login"))
    return render_template("main.html", username=session["username"])

@app.route("/logout", methods=["GET","POST"])
def logout():
    session.pop("username", None)
    flash("You have been logged out")
    return redirect(url_for("index"))


app.run(host="localhost",port=5001, debug=True)
