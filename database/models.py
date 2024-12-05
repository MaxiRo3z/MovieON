from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)  # Agregado
    full_name = Column(String, nullable=False)  # Agregado


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, nullable=False)  # Aquí usamos el movie_id de la API
    content = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    
