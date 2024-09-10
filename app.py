from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Carregando as configurações do banco de dados
app.config.from_object(Config)

# Inicializando a extensão SQLAlchemy
db = SQLAlchemy(app)

# Testando a Conexão com o Banco de Dados
@app.route('/test-db')
def test_db():
    try:
        # Criando uma sessão para executar a consulta
        result = db.session.execute(text('SELECT 1')).first()
        return "Conexão com o banco de dados realizada com sucesso!"
    except Exception as e:
        return f"Erro na conexão: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
