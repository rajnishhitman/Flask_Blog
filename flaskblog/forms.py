from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from validate_email import validate_email as v_m


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        is_valid = v_m(email_address=email.data,
                       check_regex=True, check_mx=True,
                       from_address='my@from.addr.ess', helo_host='my.host.name',
                       smtp_timeout=10, dns_timeout=10, use_blacklist=True)

        if user:
            raise ValidationError('That email is taken, Please choose a different one.')
        if not is_valid:
            raise ValidationError('That email is not valid. Please choose a valid email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            is_valid = v_m(email_address=email.data,
                           check_regex=True, check_mx=True,
                           from_address='my@from.addr.ess', helo_host='my.host.name',
                           smtp_timeout=10, dns_timeout=10, use_blacklist=True)

            if user:
                raise ValidationError('That email is taken, Please choose a different one.')
            if not is_valid:
                raise ValidationError('That email is not valid. Please choose a valid email.')