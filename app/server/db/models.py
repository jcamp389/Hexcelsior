from sqlalchemy import Column
from app.server.db import Base, db


class User(Base):
    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.String(255))
    password = Column(db.String(255))
    email = Column(db.String(255))
    last_login = Column(db.String(255))
    created_at = Column(db.String(255))
    currently_active = Column(db.Boolean, default=False)
    total_games_played = Column(db.Integer, default=0)
    total_games_won = Column(db.Integer, default=0)
    total_games_lost = Column(db.Integer, default=0)
    total_games_tied = Column(db.Integer, default=0)

class Player(Base):
    __tablename__ = 'players'

    id = Column(db.Integer, primary_key=True)
    score = Column(db.String(255))
    number = Column(db.Integer)
    base_tile = Column(db.String(255))
    cost = Column(db.Integer)
    color = Column(db.String(255))
    units = Column(db.String(255))

class Game(Base):
    __tablename__ = 'games'

    id = Column(db.Integer, primary_key=True)
    players = Column(db.String(255))
    created_at = Column(db.String(255))
    ended_at = Column(db.String(255))
    winner = Column(db.String(255))
    stats = Column(db.String(255))
    number_of_turns = Column(db.Integer)
    current_phase = Column(db.String(255))



