from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    summary = Column(Text)
    source = Column(String(100))
    category = Column(String(50))
    url = Column(String(1000))
    published_at = Column(DateTime)
    sentiment = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100))
    session_id = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship to messages
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    timestamp = Column(DateTime, server_default=func.now())
    
    # Relationship to conversation
    conversation = relationship("Conversation", back_populates="messages")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True)
    preferred_categories = Column(Text)  # JSON string of categories
    tone_preference = Column(String(50))  # 'casual', 'formal', 'humorous'
    briefing_time = Column(String(10))  # Time in HH:MM format
    created_at = Column(DateTime, server_default=func.now()) 