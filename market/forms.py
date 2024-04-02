#similar to models
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    #To avoid having same usernames
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try another username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists! Please try a different one')

    #Creating fields for the information
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])#To create validations during the input of data
    email_address = StringField(label='Email Address:',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6),DataRequired()]) #Datarequired makes sure that the field is not empty
    password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])#To make sure that password1 matches password2
    #To be able to submit the info entered,
    submit = SubmitField(label='Create Account')
    

#To login users
class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

#To allow users to purchase item and sell items
class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
