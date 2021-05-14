from flask import render_template, redirect, url_for, flash
from .app import app
from .models import Item, User, db
from .forms import RegisterForm, LoginForm
from flask_login import login_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():  # validates the user input using the validators and also returns true when the form is submitted
        new_user = User(username=form.username.data,
                        email_address=form.email_address.data,
                        pw=form.password1.data)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        # Validation errors
        for err_msg in form.errors.values():
            flash(f'Error : {err_msg}', category="danger")
    return render_template('register.html', form=form, )


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password_entered=form.password.data):
            login_user(user)
            flash(
                f"Logged in Successfully!! Welcome {user.username}", category="success")
            return redirect(url_for('market_page'))
        else:
            flash('Invalid credentials, Please try again', category="danger")

    return render_template('login.html', form=form)
