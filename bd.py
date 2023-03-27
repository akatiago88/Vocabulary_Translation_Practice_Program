from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    english = Column(String, nullable=False)
    translation = Column(String, nullable=False)


class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    word_count = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)


def create_database():
    engine = create_engine('sqlite:///vocab_quiz.db')
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return session_factory


def get_database_session():
    session_factory = create_database()
    return session_factory
