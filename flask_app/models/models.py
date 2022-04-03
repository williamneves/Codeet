from flask_app import db
from flask_login import UserMixin
import uuid
from sqlalchemy.sql import func
import re



#******************************************************
#Classes
#******************************************************

#Followers relationship table
followers = db.Table('follower',
                    db.Column('id', db.Integer, primary_key=True,autoincrement=True),
                    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('followee_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('created_at', db.DateTime(timezone=True), default=func.now())
                    )   

#Likes
likes = db.Table('likes',
    db.Column('id', db.Integer, primary_key=True,autoincrement=True),
    db.Column('codeet_id', db.Integer,db.ForeignKey('codeet.id'),primary_key=True),
    db.Column('user_id', db.Integer,db.ForeignKey('user.id'),primary_key=True),
    db.Column('created_at', db.DateTime(timezone=True), default=func.now())
                    )

#Tags
codeet_tags = db.Table('codeet_tags',
    db.Column('id', db.Integer, primary_key=True,autoincrement=True),
    db.Column('codeet_id', db.Integer,db.ForeignKey('codeet.id'),primary_key=True),
    db.Column('tag_id', db.Integer,db.ForeignKey('tags.id'),primary_key=True),
    db.Column('created_at', db.DateTime(timezone=True), default=func.now())
                    )





#User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True,nullable=False)
    email = db.Column(db.String(255),unique=True, nullable=False)
    image = db.Column(db.String(255),default='profile_images/defaut_user.png')
    password = db.Column(db.String(255),nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    name = db.Column(db.String(255))
    birth_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    location = db.Column(db.String(255))
    bio = db.Column(db.String(600))
    #Add codeets at User
    codeets = db.relationship('Codeet',backref='user',lazy='dynamic')
    #Add Follow relationship
    following = db.relationship('User', secondary=followers,
                                primaryjoin=(followers.c.follower_id==id),
                                secondaryjoin=(followers.c.followee_id==id),
                                backref=db.backref('followers', lazy='dynamic',overlaps="followers,following"), lazy='dynamic')
    
    followed_by = db.relationship('User', secondary=followers,
                                primaryjoin=(followers.c.followee_id==id),
                                secondaryjoin=(followers.c.follower_id==id),
                                backref=db.backref('followees', lazy='dynamic',overlaps="followers,following"), lazy='dynamic',overlaps="followers,following")

    
    
    #Codeet.user.
class Codeet(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(255),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    # Likes
    likes = db.relationship('User', secondary=likes,lazy='subquery',backref=db.backref('codeet',lazy=True))
    
    codeet_tags = db.relationship('Tags', secondary=codeet_tags,lazy='dynamic',backref=db.backref('codeet',lazy=True))
    
    #Tags
class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255),unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())


def create_tags_from_codeet(codeet):
    # the regular expression
    regex = "#(\w+)"

    # extracting the hashtags
    hashtag_list = re.findall(regex, codeet)
    
    tags_obj = []
    
    for tag in hashtag_list:
        
        print(tag)
        
        unique_tag = Tags.query.filter_by(tag=tag).all()
        
        print(unique_tag)
        
        if len(unique_tag) == 0:
            
            
            tag_class = Tags(tag=tag.lower())
            db.session.add(tag_class)
            db.session.commit()
            tags_obj.append(tag_class)
        else:
            tags_obj.append(unique_tag[0])
            
        
    
    return tags_obj