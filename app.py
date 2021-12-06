from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random
import string
from form import *
from models import *

# test
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
# from werkzeug.utils import cached_property
#

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# from models import db  # <-- this needs to be placed after app is created
#
# migrate = Migrate(app, db)
# manager = migrate(app)
# manager.add_command('db', MigrateCommand)

db = SQLAlchemy(app)


# db.app = app
# db.init_app(app)

class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


@app.before_first_request
def create_tables():
    db.create_all()


# Create a test user(for 1st time running)
# new_user = Users("Hieu", "veronica.lodge@email.com", "123abc")
# db.session.add(new_user)
# db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        print(Urls.query.filter_by(long=url_received).first())
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


# @app.route('/signup', methods=['POST', 'GET'])
# def signup():


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        print(form.email.data)
        user = Users.query.filter_by(email=form.email.data, password=form.password.data).first()
        print(Users.query.filter_by(email=form.email.data, password=form.password.data).first())
        if user:
            session['user'] = user.email
            return redirect(url_for('home', _scheme='http', _external=True))
        else:
            print("Wrong Email or Password")
            return render_template("login.html", form=form, message="Wrong Email or Password. Please Try Again.")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'user' in session:
        session.clear()
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
    app.run()
