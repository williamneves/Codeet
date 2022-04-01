from flask_app import photos,db,bcrypt
from flask_app.models.models import User, Codeet
from flask_app.models.forms import RegisterForm, LoginForm, CodeetForm
from flask import redirect, render_template,request,url_for,request,flash,make_response,Blueprint
from datetime import datetime
import uuid
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)


#******************************************************
#Routes
#******************************************************

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

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@auth.route('/profile/')
@login_required
def profile():
    
    today = datetime.utcnow()
    loginform = LoginForm()
    codeetform = CodeetForm()
    
    codeets = Codeet.query.filter_by(user_id=current_user.id).order_by(Codeet.created_at.desc()).all()
    total_codeets = len(codeets)
    
    return render_template('profile.html',loginform=loginform, user=current_user,codeetform=codeetform,codeets=codeets,total_codeets=total_codeets,today=today)



@auth.route('/register/', methods=[ 'POST','GET'])
def register():
    loginform = LoginForm()
    registerform = RegisterForm()

    if registerform.validate_on_submit():
        image_filename=""
        
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
        login_user(user)
        
        return redirect(url_for('views.profile'))
    
    return render_template("register.html", registerform = registerform,loginform = loginform)

