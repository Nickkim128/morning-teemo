import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from backend.core.config import settings
from backend.models.models import Article
from backend.schemas.schemas import ArticleCreate
import logging

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self):
        self.news_api_key = settings.NEWS_API_KEY
        self.guardian_api_key = settings.GUARDIAN_API_KEY
        self.news_api_base = settings.NEWS_API_BASE_URL
        self.guardian_api_base = settings.GUARDIAN_API_BASE_URL
        
    async def fetch_top_headlines(self, category: str = None, country: str = "us") -> List[Dict]:
        """Fetch top headlines from NewsAPI"""
        if not self.news_api_key:
            logger.warning("NewsAPI key not configured")
            return []
            
        url = f"{self.news_api_base}/top-headlines"
        params = {
            "apiKey": self.news_api_key,
            "country": country,
            "pageSize": 20
        }
        
        if category:
            params["category"] = category
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "ok":
                    return data.get("articles", [])
                else:
                    logger.error(f"NewsAPI error: {data.get('message')}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching news from NewsAPI: {e}")
            return []
    
    async def fetch_guardian_articles(self, section: str = None) -> List[Dict]:
        """Fetch articles from Guardian API"""
        if not self.guardian_api_key:
            logger.warning("Guardian API key not configured")
            return []
            
        url = f"{self.guardian_api_base}/search"
        params = {
            "api-key": self.guardian_api_key,
            "show-fields": "headline,trailText,body,thumbnail",
            "page-size": 20,
            "order-by": "newest"
        }
        
        if section:
            params["section"] = section
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("response", {}).get("status") == "ok":
                    return data.get("response", {}).get("results", [])
                else:
                    logger.error("Guardian API error")
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching news from Guardian: {e}")
            return []
    
    def process_newsapi_article(self, article: Dict) -> ArticleCreate:
        """Process NewsAPI article into our schema"""
        return ArticleCreate(
            title=article.get("title", ""),
            content=article.get("content", ""),
            summary=article.get("description", ""),
            source=article.get("source", {}).get("name", ""),
            url=article.get("url", ""),
            published_at=datetime.fromisoformat(
                article.get("publishedAt", "").replace("Z", "+00:00")
            ) if article.get("publishedAt") else None,
            category="general"
        )
    
    def process_guardian_article(self, article: Dict) -> ArticleCreate:
        """Process Guardian article into our schema"""
        fields = article.get("fields", {})
        return ArticleCreate(
            title=fields.get("headline", article.get("webTitle", "")),
            content=fields.get("body", ""),
            summary=fields.get("trailText", ""),
            source="The Guardian",
            url=article.get("webUrl", ""),
            published_at=datetime.fromisoformat(
                article.get("webPublicationDate", "").replace("Z", "+00:00")
            ) if article.get("webPublicationDate") else None,
            category=article.get("sectionName", "general")
        )
    
    async def fetch_all_news(self) -> List[ArticleCreate]:
        """Fetch news from all sources"""
        tasks = [
            self.fetch_top_headlines(),
            self.fetch_top_headlines("business"),
            self.fetch_top_headlines("technology"),
            self.fetch_guardian_articles("world"),
            self.fetch_guardian_articles("business"),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_articles = []
        
        # Process NewsAPI results
        for i, result in enumerate(results[:3]):
            if isinstance(result, list):
                for article in result:
                    try:
                        processed = self.process_newsapi_article(article)
                        all_articles.append(processed)
                    except Exception as e:
                        logger.error(f"Error processing NewsAPI article: {e}")
        
        # Process Guardian results
        for i, result in enumerate(results[3:]):
            if isinstance(result, list):
                for article in result:
                    try:
                        processed = self.process_guardian_article(article)
                        all_articles.append(processed)
                    except Exception as e:
                        logger.error(f"Error processing Guardian article: {e}")
        
        return all_articles
    
    async def get_trending_topics(self) -> List[str]:
        """Get trending topics from news"""
        # This is a simplified implementation
        # In production, you'd use NLP to extract topics
        articles = await self.fetch_all_news()
        topics = set()
        
        for article in articles:
            if article.category:
                topics.add(article.category)
        
        return list(topics)

# Global instance
news_service = NewsService() 