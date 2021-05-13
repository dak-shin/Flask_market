from flask import render_template, redirect, url_for
from .app import app
from .models import Item, User, db
from .forms import RegisterForm

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
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email_address=form.email_address.data,
                        password=form.password1.data)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        # Validation errors
        for err_msg in form.errors.values():
            print(f'Error : {err_msg}')
    return render_template('register.html', form=form, )








