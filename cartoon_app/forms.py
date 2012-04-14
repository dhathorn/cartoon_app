from flask.ext.wtf import Form, IntegerField, TextField, PasswordField, validators, ValidationError, RecaptchaField, RadioField, DateField, BooleanField
from models import *
import datetime

#this only works with our user class
class CheckPassword(object):
    def __init__(self, message = 'That password does not match the one we have on record'):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter(User.email == form.email.data).first()
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError(self.message)

class LoginForm(Form):
    email = TextField('email', [validators.Required()])
    password = PasswordField('password', [validators.Required(), CheckPassword()])

class ExperimentForm(Form):
    choice = RadioField('choice', [validators.Required()], choices=[('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5')])

class StartForm(Form):
    recaptcha = RecaptchaField(label="Prove you're a human")
