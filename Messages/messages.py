from flask import Blueprint, render_template, session, flash, url_for, redirect

messageBP = Blueprint("messageBP",__name__,static_folder="static",template_folder="templates")

@messageBP.route("/")
def inbox():
    if "username" not in session:
        flash("Must be logged in")
        return redirect(url_for("loginBP.login"))
    return render_template("messages.html")
