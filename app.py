from flask import Flask, render_template, request, flash , redirect , url_for
from flask_login import  login_required , login_user , logout_user , current_user 
from werkzeug.security import generate_password_hash , check_password_hash

from extensions import db , login_manager , SECRET_KEY , DB_URI
from models import User


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

db.init_app(app)

login_manager.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect("user")

    return render_template("index.html" , current_user=current_user)


@app.route("/login" , methods=["GET" , "POST"]) 
def login():
    if request.method == "POST":
        email = request.form.get("email") 
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash("No email registered")
 
        elif not check_password_hash(user.password, password):
            flash("Password mismatched")
        
        else:
            login_user(user)
            return redirect(url_for('profile'))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email") 
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email is already registered")
        else:
            try:
                hashed_password = generate_password_hash(password)
                new_user = User(email=email , password=hashed_password , name=name)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('profile'))
            except Exception:
                flash("Error occured during creating user")

    return render_template("signup.html")


@app.route("/user")
@login_required
def profile():
    return render_template("profile.html" , name=current_user.name)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
