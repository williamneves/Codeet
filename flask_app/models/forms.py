from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Regexp, Email
from flask_wtf.file import FileAllowed, FileField
from flask_uploads import IMAGES

#******************************************************
#Forms
#******************************************************

#RegisterForm
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('An username is required.'),Regexp('^[A-Za-z0-9-.]+$',message='Just letters, numbers and "." (dots) are accepted.'),Length(min=3, max=30, message='Username needs to have 3-30 chars.')])
    email = EmailField('Email', validators=[InputRequired('An email is required.'),Email(message='This email is not valid.')])
    password = PasswordField("Password", validators=[InputRequired('A password is required.')])
    image = FileField('Avatar', validators=[FileAllowed(IMAGES, message='Only images are allowed.')])

#LoginForm
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('An username is required.'),Regexp('^[A-Za-z0-9-.]+$',message='Just letters, numbers and "." (dots) are accepted.'),Length(min=3, max=30, message='Username needs to have 3-30 chars.')])
    password = PasswordField("Password", validators=[InputRequired('A password is required.')])
    remember = BooleanField("Remember me",default=True)
    
    
#CodeetForm
class CodeetForm(FlaskForm):
    text = TextAreaField('Codeet',validators=[InputRequired('Need to say something'),Length(max=255, message='A codeet can only contains 255 chars max.')])
    
