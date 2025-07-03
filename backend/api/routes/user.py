from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from backend.core.database import get_db
from backend.models.models import UserPreference
from backend.schemas.schemas import UserPreference as UserPreferenceSchema, UserPreferenceCreate

router = APIRouter()

@router.get("/preferences/{user_id}", response_model=UserPreferenceSchema)
async def get_user_preferences(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    try:
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if not preferences:
            # Create default preferences
            default_categories = ["general", "business", "technology"]
            preferences = UserPreference(
                user_id=user_id,
                preferred_categories=json.dumps(default_categories),
                tone_preference="casual",
                briefing_time="08:00"
            )
            db.add(preferences)
            db.commit()
            db.refresh(preferences)
        
        # Convert JSON string back to list for response
        categories = json.loads(preferences.preferred_categories) if preferences.preferred_categories else []
        
        return UserPreferenceSchema(
            id=preferences.id,
            user_id=preferences.user_id,
            preferred_categories=categories,
            tone_preference=preferences.tone_preference,
            briefing_time=preferences.briefing_time,
            created_at=preferences.created_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching preferences: {str(e)}")

@router.post("/preferences", response_model=UserPreferenceSchema)
async def create_or_update_preferences(
    preferences: UserPreferenceCreate,
    db: Session = Depends(get_db)
):
    """Create or update user preferences"""
    try:
        # Check if preferences already exist
        existing = db.query(UserPreference).filter(
            UserPreference.user_id == preferences.user_id
        ).first()
        
        if existing:
            # Update existing preferences
            existing.preferred_categories = json.dumps(preferences.preferred_categories)
            existing.tone_preference = preferences.tone_preference
            existing.briefing_time = preferences.briefing_time
            db.commit()
            db.refresh(existing)
            
            return UserPreferenceSchema(
                id=existing.id,
                user_id=existing.user_id,
                preferred_categories=preferences.preferred_categories,
                tone_preference=existing.tone_preference,
                briefing_time=existing.briefing_time,
                created_at=existing.created_at
            )
        else:
            # Create new preferences
            new_preferences = UserPreference(
                user_id=preferences.user_id,
                preferred_categories=json.dumps(preferences.preferred_categories),
                tone_preference=preferences.tone_preference,
                briefing_time=preferences.briefing_time
            )
            db.add(new_preferences)
            db.commit()
            db.refresh(new_preferences)
            
            return UserPreferenceSchema(
                id=new_preferences.id,
                user_id=new_preferences.user_id,
                preferred_categories=preferences.preferred_categories,
                tone_preference=new_preferences.tone_preference,
                briefing_time=new_preferences.briefing_time,
                created_at=new_preferences.created_at
            )
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating preferences: {str(e)}")

@router.get("/preferences/{user_id}/categories")
async def get_user_categories(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user's preferred categories"""
    try:
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if not preferences:
            return {"categories": ["general", "business", "technology"]}
        
        categories = json.loads(preferences.preferred_categories) if preferences.preferred_categories else []
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@router.post("/preferences/{user_id}/categories")
async def update_user_categories(
    user_id: str,
    categories: List[str],
    db: Session = Depends(get_db)
):
    """Update user's preferred categories"""
    try:
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if not preferences:
            # Create new preferences
            preferences = UserPreference(
                user_id=user_id,
                preferred_categories=json.dumps(categories),
                tone_preference="casual",
                briefing_time="08:00"
            )
            db.add(preferences)
        else:
            # Update existing
            preferences.preferred_categories = json.dumps(categories)
        
        db.commit()
        db.refresh(preferences)
        
        return {"message": "Categories updated successfully", "categories": categories}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating categories: {str(e)}")

@router.get("/available-categories")
async def get_available_categories():
    """Get all available news categories"""
    categories = [
        "general",
        "business",
        "technology",
        "sports",
        "entertainment",
        "health",
        "science",
        "politics",
        "world"
    ]
    return {"categories": categories}

@router.get("/tone-options")
async def get_tone_options():
    """Get available tone preferences"""
    tones = [
        {"value": "casual", "label": "Casual & Friendly"},
        {"value": "professional", "label": "Professional"},
        {"value": "humorous", "label": "Light & Humorous"},
        {"value": "serious", "label": "Serious & Formal"}
    ]
    return {"tones": tones} 