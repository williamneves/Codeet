from flask import Flask
from .extensions import photos,db,migrate,bcrypt
from flask_migrate import MigrateCommand
from flask_script import Manager, Server
from flask_uploads import configure_uploads
from flask_login import LoginManager



def create_app():
    app = Flask(__name__)

    #Server Configurations
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'Z\xe9\x98\xc1\x1f\x00E\x80`\xf2\xf2\xce'
    
    #Upload configurations
    app.config["UPLOADED_PHOTOS_DEST"] = "flask_app/static/img/uploads"
    configure_uploads(app,photos)
    
    #SQLAlchemy configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:00000000@localhost/db_twitter_clone'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db) #migrate setup

    
    #IMPORT VIEWS
    from .views.views import views
    from .views.auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    @app.template_filter('time_since')
    def time_since(delta):
    
        seconds = delta.total_seconds()

        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        if days > 0:
            return '%dd' % (days)
        elif hours > 0:
            return '%dh' % (hours)
        elif minutes > 0:
            return '%dm' % (minutes)
        else:
            return 'Just now'
    
    
    #IMPORT MODELS
    from .models.models import User,Codeet,likes,followers

    #LoginManager Configs
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.add_command("runserver", Server(port=5588,use_debugger=True))
    
    return app

    #******************************************************
    #Run Server
    #******************************************************

    # if __name__ == '__main__':
    #     manager.run()
    #     # app.run(debug=True,port=5027)