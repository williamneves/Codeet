from ..extensions import photos,db,bcrypt
from flask_app.models.models import User, Codeet
from flask_app.models.forms import RegisterForm, LoginForm, CodeetForm, updateProfileForm
from flask import redirect, render_template,request,url_for,request,flash,Blueprint
from datetime import datetime
import uuid
from flask_login import login_user, login_required, current_user, logout_user
import os

auth = Blueprint('auth', __name__)


#******************************************************
#Routes
#******************************************************

# LOGIN
@auth.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('views.index'))
    
    loginform = LoginForm()
    
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if not user:
            return render_template("index.html",loginform=loginform,message="User not found")
        if not bcrypt.check_password_hash(user.password, loginform.password.data):
            return render_template("index.html",loginform=loginform,message='Wrong password')
        
        print(loginform.remember.data)
        
        login_user(user, remember=loginform.remember.data)
        return redirect(url_for('views.index')) 
    
    return render_template("index.html",loginform=loginform)


#LOGOUT
@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))



#REGISTER
@auth.route('/register/', methods=[ 'POST','GET'])
def register():
    
    loginform = LoginForm()
    registerform = RegisterForm()
    print("route register")
    if registerform.validate_on_submit():
        print("route register validates")
        image_filename="profile_images/defaut_user.png"
        
        if registerform.image.data:
            datestr = uuid.uuid4()
            random_image_name = f"avatar_{datestr}"
            image_filename = photos.save(registerform.image.data, name=f"profile_images/{random_image_name}.")
        
        new_user = User(
                    username=registerform.username.data.lower(),
                    email=registerform.email.data,
                    image=image_filename,
                    created_at=datetime.utcnow(),
                    password=bcrypt.generate_password_hash(registerform.password.data))
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=registerform.username.data).first()
        login_user(user, remember=True)
        
        return redirect(url_for('views.profile'))
    
    print("not validates")
    return render_template("register.html", registerform = registerform,loginform = loginform)


#Update profile
@auth.route('/update-profile/', methods=[ 'POST'])
@login_required
def update_profile():
    
    print('update profile')
    update_profileForm = updateProfileForm()
    
    print(update_profileForm.validate_on_submit())

    if update_profileForm.validate_on_submit():
        
        print(update_profileForm.image.data )
        print(update_profileForm.image.data )
        
        if update_profileForm.image.data != None and current_user.image != "profile_images/defaut_user.png":
            
            print('old image replace',current_user.image)
            
            #remove old image
            old_image_path = url_for('static', filename=f"img/uploads/{current_user.image}")
            os.remove(old_image_path)
        
        if update_profileForm.image.data:
            #setting  random image name
            datestr = uuid.uuid4()
            random_image_name = f"avatar_{datestr}"
            image_filename = photos.save(update_profileForm.image.data, name=f"profile_images/{random_image_name}.")

            #query user to update
            user_to_update = User.query.filter_by(id=current_user.id).first()
            
            #Updating user
            user_to_update.username = update_profileForm.username.data.lower()
            user_to_update.email = update_profileForm.email.data
            user_to_update.image = image_filename
            user_to_update.name = update_profileForm.name.data
            user_to_update.location = update_profileForm.location.data
            user_to_update.bio = update_profileForm.bio.data
            user_to_update.birth_date = update_profileForm.birth_date.data
        
            db.session.add(user_to_update)
            db.session.commit()
            
        
        return redirect(url_for('views.profile'))
    
    return 'some tthing wrong'