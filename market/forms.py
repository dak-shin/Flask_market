from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .models import User


class RegisterForm(FlaskForm):

    def validate_username(self, new_username):
        # validate_ is the prefix used by flaskforms to use this as a validator on the field whose field name is next to validator_
        # in this case it is username, Similarly for email address as well
        user = User.query.filter_by(username=new_username.data).first()
        if user:
            raise ValidationError("Username is already taken.")

    def validate_email_address(self, new_email):
        email = User.query.filter_by(email_address=new_email.data).first()
        if email:
            raise ValidationError(
                "There is already an account associated with this email.")

    username = StringField(label="Username", validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label="Email", validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):

    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Purchase")


class SellForm(FlaskForm):
    submit = SubmitField(label="Sell")
