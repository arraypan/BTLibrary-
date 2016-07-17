from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo

from models import User, Taco, Check


def email_exists(Form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')



class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[DataRequired(),
                    Email(),
                    email_exists
                    ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class SigninForm(Form):
    phoneNumber = StringField('Enter Your Phone Number', [DataRequired(), Length(min=10)])

class TacoForm(Form):
    phoneNumber = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    fullName = StringField('Full Name', validators=[DataRequired()])
    member = BooleanField('Temple Member')



