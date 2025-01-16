from flask import Blueprint, render_template

messageBP = Blueprint("messageBP",__name__,static_folder="static",template_folder="templates")

@messageBP.route("/")
def inbox():
    return render_template("messages.html")
