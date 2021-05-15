from threading import current_thread
from flask import render_template, redirect, url_for, flash, request
from wtforms.widgets.core import Select
from .app import app
from .models import Item, User, db
from .forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', active_home="active")


# Market page


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():

    purchase_form = PurchaseForm()
    sell_form = SellForm()

    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        item_object = Item.query.filter_by(name=purchased_item).first()
        if item_object:
            if current_user.can_purchase(item_object):
                item_object.purchase_item(current_user)
                flash(
                    f'Purchased {item_object.name} item successfully', category="success")
            else:
                flash(
                    f'Your budget of {current_user.budget} is insuffecient to make this purchase!!', category='danger')

        owned_item = request.form.get('selling_item')
        owned_item_obj = Item.query.filter_by(name=owned_item).first()
        if owned_item_obj:
            if current_user.can_sell(owned_item_obj):
                owned_item_obj.sell_item(current_user)
                flash(
                    f'Successfully sold { owned_item_obj.name} back to market!!s', category="success")
            else:
                print(current_user)
                print(owned_item_obj)
                flash(f'This item could not be sold', category="danger")

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, owned_items=owned_items, active_market="active", sell_form=sell_form, purchase_form=purchase_form)

# Register page


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():  # validates the user input using the validators and then just returns true when the form is submitted
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

# Login page


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

# Logout


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Logged out successfully', category='info')
    return redirect(url_for('home_page'))
