from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = "../database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .home import home
    from .auth import auth
    from .faire_reco import faire_reco
    from .tableau_bord import tableau_bord
    from .monitoring  import monitoring

    from .about import about

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(faire_reco,url_prefix='/')
    app.register_blueprint(tableau_bord,url_prefix='/')
    
    app.register_blueprint(monitoring, url_prefix='/')

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(about, url_prefix='/')
    


    from .models import User, Note, lesBD

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

