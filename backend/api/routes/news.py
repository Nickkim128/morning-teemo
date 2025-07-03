from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend.core.database import get_db
from backend.models.models import Article
from backend.schemas.schemas import Article as ArticleSchema, NewsBriefing
from backend.services.news_service import news_service
from backend.services.ai_service import ai_service

router = APIRouter()

@router.get("/briefing", response_model=NewsBriefing)
async def get_morning_briefing(db: Session = Depends(get_db)):
    """Get the morning news briefing"""
    try:
        # Get latest articles from database
        articles = db.query(Article).order_by(Article.created_at.desc()).limit(20).all()
        
        # If no articles in DB, fetch fresh ones
        if not articles:
            await refresh_news(db)
            articles = db.query(Article).order_by(Article.created_at.desc()).limit(20).all()
        
        # Convert to schema objects
        article_schemas = [ArticleSchema.from_orm(article) for article in articles]
        
        # Generate AI briefing
        briefing_text = ai_service.generate_morning_briefing(article_schemas)
        
        # Get categories
        categories = list(set([article.category for article in articles if article.category]))
        
        return NewsBriefing(
            summary=briefing_text,
            articles=article_schemas[:10],  # Top 10 articles
            generated_at=datetime.now(),
            categories=categories
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating briefing: {str(e)}")

@router.get("/articles", response_model=List[ArticleSchema])
async def get_articles(
    limit: int = 20,
    category: str = None,
    db: Session = Depends(get_db)
):
    """Get paginated articles"""
    try:
        query = db.query(Article).order_by(Article.created_at.desc())
        
        if category:
            query = query.filter(Article.category == category)
        
        articles = query.limit(limit).all()
        return [ArticleSchema.from_orm(article) for article in articles]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {str(e)}")

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get available news categories"""
    try:
        categories = db.query(Article.category).distinct().all()
        return [cat[0] for cat in categories if cat[0]]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@router.post("/refresh")
async def refresh_news(db: Session = Depends(get_db)):
    """Fetch fresh news from all sources"""
    try:
        # Fetch articles from news services
        articles = await news_service.fetch_all_news()
        
        # Save to database
        saved_count = 0
        for article_data in articles:
            # Check if article already exists
            existing = db.query(Article).filter(
                Article.title == article_data.title,
                Article.source == article_data.source
            ).first()
            
            if not existing:
                article = Article(**article_data.dict())
                db.add(article)
                saved_count += 1
        
        db.commit()
        
        return {
            "message": f"Successfully refreshed news",
            "fetched": len(articles),
            "saved": saved_count
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error refreshing news: {str(e)}")

@router.get("/trending")
async def get_trending_topics():
    """Get trending topics from current news"""
    try:
        topics = await news_service.get_trending_topics()
        return {"topics": topics}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending topics: {str(e)}")

@router.get("/article/{article_id}/summary")
async def get_article_summary(article_id: int, db: Session = Depends(get_db)):
    """Get AI-generated summary for a specific article"""
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        article_schema = ArticleSchema.from_orm(article)
        summary = ai_service.summarize_article(article_schema)
        
        return {"summary": summary}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}") 