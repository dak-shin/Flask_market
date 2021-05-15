from flask import render_template, redirect, url_for, flash
from wtforms.widgets.core import Select
from .app import app
from .models import Item, User, db
from .forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', active_home="active")


@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    purchase_form = PurchaseForm()
    sell_form = SellForm()

    return render_template('market.html', items=items, active_market="active", purchase_form=purchase_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():  # validates the user input using the validators and also returns true when the form is submitted
        new_user = User(username=form.username.data,
                        email_address=form.email_address.data,
                        pw=form.password1.data)

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Account created and logged in succeffully", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        # Validation errors
        for err_msg in form.errors.values():
            flash(f'Error : {err_msg}', category="danger")
    return render_template('register.html', form=form, active_register="active")


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

    return render_template('login.html', form=form, active_login="active")


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Logged out successfully', category='info')
    return redirect(url_for('home_page'))
