from sqlmodel import create_engine, Session
from dotenv import load_dotenv, find_dotenv
import os

APP_ENV = os.getenv("APP_ENV", "dev")

if APP_ENV == "test":
    load_dotenv(find_dotenv(".env.test"), override=True)
else:
    load_dotenv(find_dotenv(".env"), override=True)

# Connexion sécurisée avec des variables d’environnement
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
mysql_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(mysql_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session