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
    
    name = StringField('Name', validators=[Regexp('^[A-Za-z- ]+$',message='Just letters are accepted.'),Length(min=3, max=60)])
    
    email = EmailField('Email', validators=[InputRequired('An email is required.'),Email(message='This email is not valid.')])
    
    password = PasswordField("Password", validators=[InputRequired('A password is required.')])
    
    confirm_password = PasswordField("Password", validators=[InputRequired('Need to confirm your password.')])
    
    image = FileField('Avatar', validators=[FileAllowed(IMAGES, message='Only images are allowed.')])
    
    birth_date = DateField('Birth date', format='%Y-%m-%d')
    
    location = StringField('Location')
    
    bio = TextAreaField('Bio', validators=[Length(max=600)])
    



#LoginForm
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('An username is required.'),Regexp('^[A-Za-z0-9-.]+$',message='Just letters, numbers and "." (dots) are accepted.'),Length(min=3, max=30, message='Username needs to have 3-30 chars.')])
    
    password = PasswordField("Password", validators=[InputRequired('A password is required.')])
    
    remember = BooleanField("Remember me",default=True)
    
    
#CodeetForm
class CodeetForm(FlaskForm):
    text = TextAreaField('Codeet',validators=[InputRequired('Need to say something'),Length(max=255, message='A codeet can only contains 255 chars max.')])
    

#ChangePasswordForm
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[InputRequired('A password is required.')])
    
    new_password = PasswordField("New password", validators=[InputRequired('A password is required.')])
    
    confirm_password = PasswordField("Confirm password", validators=[InputRequired('Need to confirm your password.')])
