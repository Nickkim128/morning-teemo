from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Article schemas
class ArticleBase(BaseModel):
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None
    category: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    sentiment: Optional[float] = None

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    content: str
    role: str  # 'user' or 'assistant'

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    conversation_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Conversation schemas
class ConversationBase(BaseModel):
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    created_at: datetime
    messages: List[Message] = []
    
    class Config:
        from_attributes = True

# User preference schemas
class UserPreferenceBase(BaseModel):
    user_id: str
    preferred_categories: Optional[List[str]] = []
    tone_preference: Optional[str] = "casual"
    briefing_time: Optional[str] = "08:00"

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreference(UserPreferenceBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chat request/response schemas
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: Optional[List[str]] = []

# News briefing schema
class NewsBriefing(BaseModel):
    summary: str
    articles: List[Article]
    generated_at: datetime
    categories: List[str] 