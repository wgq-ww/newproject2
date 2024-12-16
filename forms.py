from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from unwrap.user.models import User

class RegistrationForm(FlaskForm):
    firstname=StringField("First Name",
                          validators=[DataRequired(),Length(min=2,max=20)])
    lastname = StringField("Last Name",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email=StringField("Email",
                      validators=[DataRequired(),Email()])
    password=PasswordField("Password",
                           validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",
                                   validators=[DataRequired(),EqualTo("password")])
    submit= SubmitField('Sign Up')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email has been "
                                  "taken!!!!")





class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    password = PasswordField("Password",
                             validators=[DataRequired()])

    remember=BooleanField('Remember me')

    submit = SubmitField('Sign In')



class UpdateAccountForm(FlaskForm):
    firstname=StringField("First Name",validators=[DataRequired(),Length(min=2,max=20)])
    lastname=StringField("Last Name",validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",validators=[DataRequired(), Email()])
    submit =SubmitField('Update')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email has been "
                                  "taken!!!!")


