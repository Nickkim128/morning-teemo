from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from backend.core.database import get_db
from backend.models.models import Conversation, Message, Article
from backend.schemas.schemas import (
    ChatMessage, 
    ChatResponse, 
    Conversation as ConversationSchema,
    Message as MessageSchema,
    Article as ArticleSchema
)
from backend.services.ai_service import ai_service

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_message: ChatMessage,
    db: Session = Depends(get_db)
):
    """Send a message to the AI assistant"""
    try:
        # Get or create conversation
        conversation = None
        if chat_message.session_id:
            conversation = db.query(Conversation).filter(
                Conversation.session_id == chat_message.session_id
            ).first()
        
        if not conversation:
            # Create new conversation
            session_id = str(uuid.uuid4())
            conversation = Conversation(
                session_id=session_id,
                user_id=chat_message.user_id
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        else:
            session_id = conversation.session_id
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            content=chat_message.message,
            role="user"
        )
        db.add(user_message)
        
        # Get conversation history
        history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.timestamp.desc()).limit(20).all()
        
        # Get recent articles for context
        articles = db.query(Article).order_by(Article.created_at.desc()).limit(10).all()
        article_schemas = [ArticleSchema.from_orm(article) for article in articles]
        
        # Generate AI response
        ai_response = ai_service.chat_response(
            message=chat_message.message,
            conversation_history=[MessageSchema.from_orm(msg) for msg in history],
            articles=article_schemas
        )
        
        # Save AI response
        assistant_message = Message(
            conversation_id=conversation.id,
            content=ai_response,
            role="assistant"
        )
        db.add(assistant_message)
        db.commit()
        
        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            sources=[article.url for article in articles[:3] if article.url]
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/history/{session_id}", response_model=ConversationSchema)
async def get_conversation_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get conversation history for a session"""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return ConversationSchema.from_orm(conversation)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

@router.post("/new-session")
async def create_new_session(
    user_id: str = None,
    db: Session = Depends(get_db)
):
    """Create a new conversation session"""
    try:
        session_id = str(uuid.uuid4())
        conversation = Conversation(
            session_id=session_id,
            user_id=user_id
        )
        db.add(conversation)
        db.commit()
        
        return {"session_id": session_id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@router.get("/sessions")
async def get_user_sessions(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all conversation sessions for a user"""
    try:
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.created_at.desc()).all()
        
        return [
            {
                "session_id": conv.session_id,
                "created_at": conv.created_at,
                "message_count": len(conv.messages)
            }
            for conv in conversations
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sessions: {str(e)}")

@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Delete a conversation session"""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Delete all messages first
        db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).delete()
        
        # Delete conversation
        db.delete(conversation)
        db.commit()
        
        return {"message": "Session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}") 