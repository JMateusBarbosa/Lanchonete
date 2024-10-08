from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
# Inicialize o SQLAlchemy e CSRFProtect
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()  

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Inicialize as extensões
    Bootstrap(app)
    db.init_app(app)  # Inicializa o banco de dados
    csrf.init_app(app)  # Inicializa a proteção CSRF
    migrate.init_app(app, db)  # Inicialize o Flask-Migrate com o app e db

    # Registre as rotas
    from app.blueprints import routes
    app.register_blueprint(routes.bp)

    return app
