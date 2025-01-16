from flask import Blueprint, render_template, session, redirect, request, url_for, flash, jsonify

import security, database

signupBP = Blueprint("signupBP",__name__,static_folder="static",template_folder="templates")

public_key, private_key = security.gen_key_pair()

@signupBP.route("/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        signup_data = request.get_json()

        username = signup_data.get("username")
        password = signup_data.get("password")

        password = security.decrypt(password, private_key)

        if database.existing_user(username):
            print(f"user {username} exists")
            flash("Username already exists")
            return jsonify({"redirect_url": url_for("signupBP.signup")})
        else:
            database.add_user(username, password)
            session["username"]=username
            return jsonify({"redirect_url": url_for("main")}), 200
    return render_template("signup.html")