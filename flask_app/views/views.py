from crypt import methods
from ..extensions import db
from flask_app.models.models import User, Codeet, followers, likes, Tags,codeet_tags,create_tags_from_codeet, Reply
from flask_app.models.forms import RegisterForm, LoginForm, CodeetForm, updateProfileForm
from flask import jsonify, redirect, render_template,request,url_for,request,flash,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import login_user, login_required, current_user, logout_user

views = Blueprint('views', __name__)


#******************************************************
#Routes
#******************************************************
    
@views.route('/')
def index():
    
    is_logged = current_user.is_authenticated
    
    today = datetime.utcnow()
    loginform = LoginForm()
    codeetform = CodeetForm()
    
    # Query for just the codeets from followed users
    # if current_user.is_authenticated:
    #     codeets = Codeet.query.join(followers, (followers.c.followee_id == Codeet.user_id)).filter(followers.c.follower_id == current_user.id).order_by(Codeet.created_at.desc()).all()
    
    codeets = Codeet.query.order_by(Codeet.created_at.desc()).all()
    
    
    return render_template("index.html",loginform=loginform,codeets=codeets,today=today,is_logged=is_logged,current_user=current_user,codeetform=codeetform)

#******************************************************
# Tags View
#******************************************************

@views.route('/tags/<tagname>/')
def tag(tagname):
    
    is_logged = current_user.is_authenticated
    
    today = datetime.utcnow()
    loginform = LoginForm()
    codeetform = CodeetForm()
    
    
    query_tag = Tags.query.filter_by(tag=tagname).first()
    
    print(query_tag.tag)
    
    
    codeets = db.session.query(Codeet).join(codeet_tags,(codeet_tags.c.codeet_id == Codeet.id)).filter(codeet_tags.c.tag_id == query_tag.id).all()
    
    print(codeets)
    
    
    return render_template("index.html",loginform=loginform,codeets=codeets,today=today,is_logged=is_logged,current_user=current_user,codeetform=codeetform)

#******************************************************
# Profile View
#******************************************************

@views.route('/profile/')
@login_required
def profile():
    
    update_profileForm = updateProfileForm()
    registerform = RegisterForm()
    
    today = datetime.utcnow()
    loginform = LoginForm()
    codeetform = CodeetForm()
    
    codeets = Codeet.query.filter_by(user_id=current_user.id).order_by(Codeet.created_at.desc()).all()
    total_codeets = len(codeets)
    
    return render_template('profile.html',loginform=loginform, current_user=current_user,codeetform=codeetform,codeets=codeets,total_codeets=total_codeets,today=today,user=current_user,registerform=registerform,update_profileForm=update_profileForm)


#******************************************************
# Add codeet View
#******************************************************

@views.route('/add-codeet/', methods=['POST'])
@login_required
def add_codeet():
    # Creating the new codeet
    new_codeet = Codeet(text=request.json['text'],user_id=current_user.id)
    db.session.add(new_codeet)
    print('new codeet')
    
    # Creatring the tags
    tags_list = create_tags_from_codeet(new_codeet.text)
    # Input tags in Codeet relationship
    
    for tag in tags_list:
    
        new_codeet.codeet_tags.append(tag)

    
    db.session.commit()
    
    codeet = Codeet.query.filter_by(user_id=current_user.id).order_by(Codeet.created_at.desc()).first()
    today = datetime.utcnow()
    
    # headers = {'Content-Type': 'text/html'}
    
    return render_template('includes/codeet.html',codeet=codeet,today=today)

@views.route('/<username>/')
def user_timeline(username):
    
    today = datetime.utcnow()
    loginform = LoginForm()
    codeetform = CodeetForm()
    
    user_found = User.query.filter_by(username=username.lower()).first()
    
    if user_found == None:
        flash(f'This user not exist',category='user_not_exist')
        return redirect(url_for('views.index'))
        
    user = User.query.filter_by(username=username.lower()).first()
    followed_by = user.followed_by.all()
    following = user.following.all()
    
    own_profile = False
    is_following = False
    is_logged = current_user.is_authenticated
    
    if is_logged:
        if current_user.username == username:
            own_profile = True
    
        if current_user in followed_by:
            is_following = True
    
    codeets = Codeet.query.filter_by(user_id=user.id).order_by(Codeet.created_at.desc()).all()
    total_codeets = len(codeets)
    
    return render_template('timeline.html',
        loginform=loginform,user=user,
        codeetform=codeetform,codeets=codeets,
        today=today,current_user=current_user,
        total_codeets=total_codeets,followed_by=followed_by,
        is_following=is_following,own_profile=own_profile,
        is_logged=is_logged,following=following)
    
    
@views.route('/codeet/<codeet_id>/')
def codeet(codeet_id):
    
    today = datetime.utcnow()
    loginform = LoginForm()
    codeetform = CodeetForm()
    
    codeet = Codeet.query.filter_by(id=codeet_id).first()
    
    if codeet == None:
        flash(f'This codeet not exist',category='codeet_not_exist')
        return redirect(url_for('views.index'))
    
    user = User.query.filter_by(id=codeet.user_id).first()
    
    return render_template('codeetpage.html',
        loginform=loginform,user=user,
        codeetform=codeetform,codeet=codeet,
        today=today,current_user=current_user)


@views.route('/new-reply/', methods=['POST'])
def new_reply():
    
    new_reply = Reply(reply_text = request.form["reply_text"],user_id=current_user.id,codeet_id=request.form["codeet_id"])
    
    codeet = Codeet.query.filter_by(id=request.form["codeet_id"]).first()
    codeet.replies.append(new_reply)
    db.session.commit()
    
    return redirect(url_for('views.codeet',codeet_id=request.form["codeet_id"]))
    
    

        
@views.route('/follow/<username>')
@login_required
def follow(username):
    
    user_to_follow = User.query.filter_by(username=username).first()

    if not current_user in user_to_follow.following:
        current_user.following.append(user_to_follow)
        db.session.commit()
        return redirect(url_for('views.user_timeline',username=username))
    
    flash(f'User is already followed by you!')
    return redirect(url_for('views.user_timeline',username=username))


@views.route('/add-like/', methods=['POST'])
@login_required
def add_like():
    
    codeet_to_like = Codeet.query.filter_by(id=request.json['codeet_id']).first()
    
    if codeet_to_like.user.id != current_user.id:
    
        if not current_user in codeet_to_like.likes:
            codeet_to_like.likes.append(current_user)
            db.session.commit()
            print(codeet_to_like.likes,"LIKED!")
            
            response = {'response': ": Liked!"}
            
            return jsonify(response)
            
        if  current_user in codeet_to_like.likes:
            codeet_to_like.likes.remove(current_user)
            db.session.commit()
            print(codeet_to_like.likes,"Unliked!")
            
            response = {'response': "Unliked!"}
            
            return jsonify(response)
    
    else:
        
        response = {'response': "This is your post"}
    
        return jsonify(response)