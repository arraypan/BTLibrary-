from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask_peewee.admin import Admin
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_admin import Admin, AdminIndexView, BaseView, expose

from flask.ext.admin.contrib.peewee import ModelView
import forms
import models

class MyHomeView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'joimnasdf*&@)JOINSf*@ih89f2n'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == int(userid))
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
@login_required
def index():
    tacos = models.Taco.select()
    checks = models.Check.select()
    return render_template('index.html', tacos=tacos)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.select().where(
                models.User.email ** form.email.data
            ).get()
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Email or password is invalid")
        except models.DoesNotExist:
            flash("Email or password is invalid")
    return render_template('login.html', form=form)

@app.route('/signin', methods=('GET','POST'))
def signIn():
    form = forms.SigninForm()
    if form.validate_on_submit():
        models.Check.create(phoneNumber=form.phoneNumber.data)

        try:
            user = models.Taco.select().where(


            models.Taco.phoneNumber ** form.phoneNumber.data).get()




            flash("Welcome to Temple Library", "Success")

            return redirect(url_for('signIn'))



        except models.DoesNotExist:
            flash("We cant find you on System")
            return redirect(url_for('new_taco'))
    return render_template('signin.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/signup', methods=('GET', 'POST'))
@login_required
def new_taco():
    form = forms.TacoForm()
    if form.validate_on_submit():
        models.Taco.create(user=g.user._get_current_object(),
                           phoneNumber=form.phoneNumber.data,
                           fullName=form.fullName.data,
                           member=form.member.data)
        flash("User Created", "success")
        return redirect(url_for('signIn'))
    return render_template('signup.html', form=form)




if __name__ == '__main__':
    models.initialize()
    admin = Admin(app, name="Temple")
    admin.add_view(MyModelView(models.User))
    admin.add_view(MyModelView(models.Taco, name="Member Info"))
    admin.add_view(MyModelView(models.Check))


    try:
        models.User.create_user(
            email='rughaniarpan@gmail.com',
            password='password',
            admin = True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)