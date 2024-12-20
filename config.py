import os

class Config:
    # Configuração da URI de conexão com o MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    #  para testes locais  'mysql+pymysql://lanchonete:123456@localhost/lanchonete_db'
    
    # Desativar a sinalização do SQLAlchemy sobre modificações de objetos
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Outros parâmetros de configuração, se necessário
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
