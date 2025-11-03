from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Text, ForeignKey, PrimaryKey 
from sqlalchemy.orm import declarative_base

Base = declarative_base()