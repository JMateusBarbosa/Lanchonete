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
    
    # Inicialize extensões sem SQLAlchemy
    Bootstrap(app)
    csrf.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI']:  # Ignora o banco se URI estiver vazia
        db.init_app(app)
        migrate.init_app(app, db)
    # Registre as rotas
    from app.blueprints import routes
    app.register_blueprint(routes.bp)

    return app
