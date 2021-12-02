from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random
import string
from form import *
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.url'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

users = [
    {"id": 1, "full_name": "Pet Rescue Team", "email" : "veronica.lodge@email.com", "password" : "123abc"}
]

@app.before_first_request
def create_tables():
    db.create_all()
#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        found_url = Urls.query.filter_by(long=url_received).first()
        # check if url stored in db
        if found_url:
            # return
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            print(short_url)
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('url_page.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check if account is on users
        user = next(
            (user for user in users if user["email"] == form.email.data and user["password"] == form.password.data),
            None)
        if user is None:
            return render_template("login.html", form=form, message="Wrong Email or Password. Please Try Again.")
        else:
            session['user'] = user
            return redirect(url_for('home', _scheme='http', _external=True))
            # return render_template("login.html", message="Successfully Logged In!" )
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('index', _scheme='http', _external=True))

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    print(Urls.query.filter_by(short=short_url).first())
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesnt exist</h1>'

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)

@app.route('/all_urls')
def display_all():
    return render_template('all_urls.html', vals=Urls.query.all())


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
