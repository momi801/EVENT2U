from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Para SQLite
engine = create_engine("sqlite:///meubanco.db")

