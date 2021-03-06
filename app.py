from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
import random
import string
from form import *


# from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from models import *



@app.before_first_request
def create_tables():
    db.create_all()


# Create a test user(for 1st time running)
# new_user = Users("HieuAnh","veronica.lodge@email.com", "123")
# db.session.add(new_user)
# db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        userid = session['user']
        print(userid)
        # print(Urls.query.filter_by(long=url_received).first())
        found_url = Urls.query.filter_by(long=url_received).first()
        # check if url stored in db
        if found_url:
            # return
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            print(short_url)
            new_url = Urls(url_received, short_url, userid)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('url_page.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_user = Users(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        # print(form.email.data)
        user = Users.query.filter_by(email=form.email.data, password=form.password.data).first()
        # print(Users.query.filter_by(email=form.email.data, password=form.password.data).first())
        if user:
            session['user'] = user.id_user
            #set cookies
            # # ss = {}
            # res = make_response(session)
            # print(user.id_user)
            # res.set_cookie("cookies", user.id_user)
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
    # print(Urls.query.filter_by(short=short_url).first())
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesnt exist</h1>'


@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)


@app.route('/all_urls')
def display_all():
    userid = session['user']
    # print(userid)
    return render_template('all_urls.html', vals=Urls.query.filter_by(user_id=userid))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
