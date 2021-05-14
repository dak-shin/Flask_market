from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .models import User


class RegisterForm(FlaskForm):

    def validate_username(self, new_username):
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
