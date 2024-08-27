from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Inicialize as extensões
    Bootstrap(app)
    
    # Registre as rotas
    from app.views import routes
    app.register_blueprint(routes.bp)
    
    return app
