from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
photos = UploadSet('photos', IMAGES)