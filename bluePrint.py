from flask import Blueprint , render_template

# repApp = Blueprint("auth" , __name__)

@repApp.route("/login")
def home():
	return render_template("login.html")