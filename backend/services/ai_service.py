from openai import OpenAI
from typing import List, Dict, Optional
from backend.core.config import settings
from backend.schemas.schemas import Article, Message
import logging
import random

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        self.use_mock = False  # Set to True for testing without OpenAI
        
        # Morning Brew personality prompt
        self.system_prompt = """You are a witty, engaging morning news assistant inspired by Morning Brew. Your personality traits:

- Use a casual, conversational tone with light humor where appropriate
- Break down complex topics into digestible, easy-to-understand insights
- Ask engaging follow-up questions to keep the conversation flowing
- Reference current events contextually and make connections between stories
- Be informative but never boring - think of yourself as a smart friend over coffee
- Use analogies and relatable examples to explain complex concepts
- Maintain optimism while being realistic about serious topics
- Always cite your sources when discussing specific news stories
- Keep responses concise but thorough - aim for the sweet spot between brief and detailed

Remember: You're helping someone start their day with the news, so be energetic, insightful, and genuinely helpful. Think Morning Brew newsletter meets friendly conversation."""

    def _get_mock_response(self, message_type: str, user_message: str = "", articles: List[Article] = None) -> str:
        """Generate mock responses for testing when OpenAI API is unavailable"""
        
        if message_type == "briefing":
            return """☀️ Good morning! Welcome to your daily dose of what's happening around the world!

🏛️ **Politics & Policy**: There's quite a bit of political movement today with various policy discussions heating up across different regions. Leaders are making moves that could shape the coming months.

💼 **Business Buzz**: The markets are showing some interesting patterns, with tech stocks getting attention and traditional sectors adapting to new realities. Always fascinating to watch how these trends develop!

🌍 **Global Affairs**: International relations continue to evolve, with diplomatic discussions and strategic partnerships making headlines. It's like watching a very complex chess game unfold.

What catches your eye from today's news? I'm here to dive deeper into any of these stories or chat about whatever's on your mind! ☕"""

        elif message_type == "chat":
            responses = [
                f"That's a great question about {user_message[:30]}... Based on what I'm seeing in today's news, there are definitely some interesting angles to explore. What specific aspect would you like to dive into?",
                f"Interesting point! The news today actually touches on similar themes. From what I can tell, there are a few key developments that might be relevant to what you're asking about.",
                f"I love that you're thinking about this! 📰 Today's headlines have some fascinating connections to your question. Let me share what I'm seeing...",
                f"Great timing asking about this! There's actually quite a bit happening in the news right now that relates to your question. Want to explore the latest developments?",
                f"You've hit on something that's definitely making waves today! ☕ The current news cycle has some really compelling stories around this topic."
            ]
            
            base_response = random.choice(responses)
            
            if articles and len(articles) > 0:
                article = random.choice(articles[:3])
                base_response += f"\n\nFor example, there's this story from {article.source}: '{article.title[:100]}...' which really highlights some of the key issues at play."
            
            base_response += "\n\nWhat's your take on this? Any particular angle you'd like to explore further?"
            
            return base_response
        
        return "I'm here to chat about today's news! What would you like to know? ☕"

    def generate_morning_briefing(self, articles: List[Article]) -> str:
        """Generate a Morning Brew-style briefing from articles"""
        if not articles:
            return "Good morning! I don't have any fresh news to share right now, but I'm here to chat about whatever's on your mind! ☕"
        
        # First try OpenAI
        try:
            # Prepare article summaries for the prompt
            article_summaries = []
            for i, article in enumerate(articles[:10], 1):  # Limit to top 10 articles
                summary = f"{i}. **{article.title}** ({article.source})\n   {article.summary[:200]}..."
                article_summaries.append(summary)
            
            articles_text = "\n\n".join(article_summaries)
            
            briefing_prompt = f"""Create a Morning Brew-style news briefing from these articles. Make it engaging, conversational, and informative. Include:

1. A warm, energetic greeting
2. 3-5 key stories with witty commentary
3. Connections between stories when relevant
4. A closing that invites follow-up questions

Articles:
{articles_text}

Write this as if you're chatting with a friend over coffee. Be engaging, insightful, and don't be afraid to add personality!"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": briefing_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating briefing with OpenAI: {e}")
            # Fall back to mock response
            return self._get_mock_response("briefing", articles=articles)

    def chat_response(self, message: str, conversation_history: List[Message] = None, articles: List[Article] = None) -> str:
        """Generate a conversational response to user message"""
        
        # First try OpenAI
        try:
            # Build conversation context
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add recent conversation history
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages for context
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Add current news context if available
            if articles:
                news_context = "Current news context:\n"
                for article in articles[:5]:  # Top 5 articles for context
                    news_context += f"- {article.title} ({article.source}): {article.summary[:100]}...\n"
                
                context_message = f"Here's some current news context to help inform your responses:\n\n{news_context}\n\nNow respond to the user's message."
                messages.append({"role": "system", "content": context_message})
            
            # Add user message
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating chat response with OpenAI: {e}")
            # Fall back to mock response
            return self._get_mock_response("chat", message, articles)

    def summarize_article(self, article: Article) -> str:
        """Generate a concise, engaging summary of an article"""
        
        try:
            prompt = f"""Summarize this news article in 2-3 sentences with a Morning Brew style - conversational, engaging, and informative:

Title: {article.title}
Content: {article.content[:1000]}...
Source: {article.source}

Make it sound like you're explaining it to a friend over coffee."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error summarizing article with OpenAI: {e}")
            return article.summary or "This story is developing, and there's definitely more to unpack here. The key details are still emerging, but it's worth keeping an eye on how this unfolds!"

    def extract_key_topics(self, articles: List[Article]) -> List[str]:
        """Extract key topics from a list of articles"""
        if not articles:
            return []
        
        try:
            articles_text = "\n".join([f"{article.title}: {article.summary}" for article in articles[:20]])
            
            prompt = f"""Extract 5-10 key topics/themes from these news articles. Return them as a simple list:

{articles_text}

Topics:"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts key topics from news articles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            topics_text = response.choices[0].message.content
            # Parse the response to extract topics
            topics = [topic.strip().lstrip('- ').lstrip('• ') for topic in topics_text.split('\n') if topic.strip()]
            return topics[:10]  # Return max 10 topics
            
        except Exception as e:
            logger.error(f"Error extracting topics with OpenAI: {e}")
            # Return categories from articles as fallback
            return list(set([article.category for article in articles[:10] if article.category]))

# Global instance
ai_service = AIService() 