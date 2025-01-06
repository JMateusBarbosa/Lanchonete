import os
from urllib.parse import quote


class Config:
    # Usando variáveis de ambiente para a conexão
    password = os.getenv('DB_PASSWORD')  # Variável de ambiente para a senha do banco de dados
    encoded_password = quote(password)

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{encoded_password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    # para teste do sistema local como banco ja hospedado f"postgresql://postgres.nluifbshkudhwithwrtu:{encoded_password}@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"
    #  para testes locais  'mysql+pymysql://lanchonete:123456@localhost/lanchonete_db'
    
    # Desativar a sinalização do SQLAlchemy sobre modificações de objetos
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Outros parâmetros de configuração, se necessário
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    #SECRET_KEY = 'CHAVE_SECRETA'