from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    team = Column(String, nullable=False)
    no = Column(String, nullable=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    matches = Column(Integer, default=0)
    photo_path = Column(String, nullable=True)

class PlayerMedia(Base):
    __tablename__ = "player_media"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    type = Column(String, nullable=False)
    src_path = Column(String, nullable=True)
    description = Column(String, nullable=True)

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String, nullable=False)
    sender_id = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    sent_at = Column(String, nullable=True)

class Tactic(Base):
    __tablename__ = "tactics"

    id = Column(Integer, primary_key=True, index=True)
    team = Column(String, nullable=False)
    formation = Column(String, nullable=True)
    slots = Column(JSON, nullable=True)

class SiteData(Base):
    __tablename__ = "site_data"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(JSON, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
