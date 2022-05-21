from flask import Flask, render_template, request, flash , redirect , url_for
from flask_login import LoginManager , login_required , login_user , logout_user , current_user , UserMixin

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcking123'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"

db.init_app(app)

# User model
class User(UserMixin , db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

login_manager = LoginManager()
login_manager.init_app(app)

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
        password = request.form.get("name")
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No email registered")
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
                new_user = User(email=email , password=password , name=name)
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
    return render_template("profile.html" , name=current_user.password)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
