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
    
    # Inicialize extensões 
    Bootstrap(app)
    csrf.init_app(app)

    if app.config['SQLALCHEMY_DATABASE_URI']:  # Se URI for válida
        db.init_app(app)
        migrate.init_app(app, db)
        print("Banco de dados conectado com sucesso.")
    else:
        print("Aviso: Nenhum banco de dados configurado. O sistema continuará sem persistência.")

    # Registre as rotas
    from app.blueprints import routes
    app.register_blueprint(routes.bp)

    return app
