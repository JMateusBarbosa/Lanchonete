from sqlalchemy import create_engine
from urllib.parse import quote


password = "@110810"
encoded_password = quote(password)
# Use a URI do banco no config.py
DATABASE_URI =  f"postgresql://postgres.nluifbshkudhwithwrtu:{encoded_password}@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URI)

try:
    with engine.connect() as conn:
        print("Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print("Erro na conexão com o banco de dados:")
    print(f"Tipo de erro: {type(e)}")
    print(f"Detalhes: {e}")
