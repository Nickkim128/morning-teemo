# 🌅 Morning News AI Assistant

A **Morning Brew-style** conversational news application that delivers personalized news briefings and enables interactive chat about current events. Built with FastAPI, Next.js, and OpenAI GPT-4.

![Status](https://img.shields.io/badge/Status-Working-brightgreen)
![Backend](https://img.shields.io/badge/Backend-FastAPI-blue)
![Frontend](https://img.shields.io/badge/Frontend-Next.js-black)
![AI](https://img.shields.io/badge/AI-OpenAI%20GPT--4-orange)

## ✨ Features

### 🤖 **AI-Powered Conversations**
- **Morning Brew Personality**: Witty, engaging, conversational tone
- **Context-Aware**: References current news in conversations
- **Follow-up Questions**: Keeps discussions flowing naturally
- **Smart Analogies**: Makes complex topics easy to understand

### 📰 **Intelligent News Aggregation**
- **Multiple Sources**: NewsAPI, Guardian API integration
- **Real-time Updates**: Fresh news fetching and storage
- **Smart Categorization**: Organized by topics and sources
- **AI Summaries**: Morning Brew-style article summaries

### 💬 **Interactive Chat Interface**
- **Session Management**: Persistent conversations
- **Typing Indicators**: Real-time chat experience
- **Quick Actions**: Pre-defined conversation starters
- **Source Citations**: News references in responses

### 🎯 **Daily Briefings**
- **Personalized Summaries**: AI-generated news roundups
- **Engaging Commentary**: Witty insights on current events
- **Story Connections**: Links between related news items
- **Modern UI**: Beautiful, responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key (with billing enabled)
- NewsAPI key
- Guardian API key

### 1. Clone & Setup Backend

```bash
git clone <your-repo-url>
cd Start\ Up\ Project

# Install Python dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=sk-proj-your-key-here
# NEWS_API_KEY=your-newsapi-key
# GUARDIAN_API_KEY=your-guardian-key
```

### 2. Start Backend Server

```bash
# From project root
python -m backend.main

# Backend runs on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### 3. Setup & Start Frontend

```bash
# In new terminal, from project root
cd frontend
npm install
npm run dev

# Frontend runs on http://localhost:3000
```

### 4. Initialize with News Data

```bash
# Fetch initial news articles
curl -X POST http://localhost:8000/api/news/refresh
```

## 📖 API Documentation

### 🔗 **News Endpoints**
- `GET /api/news/briefing` - Get AI-generated morning briefing
- `GET /api/news/articles` - Fetch paginated articles
- `POST /api/news/refresh` - Update news from sources
- `GET /api/news/categories` - Get available categories

### 💬 **Chat Endpoints**
- `POST /api/chat/message` - Send message to AI assistant
- `POST /api/chat/new-session` - Create new conversation
- `GET /api/chat/history/{session_id}` - Get conversation history
- `DELETE /api/chat/session/{session_id}` - Delete conversation

### 🔧 **Utility Endpoints**
- `GET /` - API status and information
- `GET /health` - Health check

## 🛠️ Technology Stack

### **Backend**
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with SQLite
- **OpenAI GPT-4**: AI conversation engine
- **Pydantic**: Data validation and settings
- **AsyncIO**: Concurrent news fetching

### **Frontend**
- **Next.js 14**: React framework with App Router
- **Tailwind CSS**: Utility-first styling
- **TypeScript**: Type-safe development
- **Lucide Icons**: Modern icon library

### **Integrations**
- **NewsAPI**: Comprehensive news aggregation
- **Guardian API**: Quality journalism source
- **OpenAI**: Advanced language model

## 📁 Project Structure

```
Start Up Project/
├── backend/
│   ├── main.py              # FastAPI application entry
│   │   ├── core/
│   │   │   ├── config.py        # Settings and configuration
│   │   │   └── database.py      # Database setup
│   │   ├── models/
│   │   │   └── models.py        # SQLAlchemy database models
│   │   ├── schemas/
│   │   │   └── schemas.py       # Pydantic data schemas
│   │   ├── services/
│   │   │   ├── news_service.py  # News aggregation logic
│   │   │   └── ai_service.py    # OpenAI integration
│   │   └── api/routes/
│   │       ├── news.py          # News API endpoints
│   │       └── chat.py          # Chat API endpoints
│   ├── requirements.txt         # Python dependencies
│   ├── morning_news.db         # SQLite database
│   └── README.md               # Project documentation
```

## 🔑 Environment Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-key
OPENAI_MODEL=gpt-4
MAX_TOKENS=1000
TEMPERATURE=0.7

# News API Keys
NEWS_API_KEY=your-newsapi-key
GUARDIAN_API_KEY=your-guardian-api-key

# Database
DATABASE_URL=sqlite:///./morning_news.db

# Development
DEBUG=true
```

## 🎨 Key Features Demonstrated

### **Morning Brew Personality**
The AI assistant embodies the signature Morning Brew style:
- Casual, conversational tone with light humor
- Smart analogies that make complex topics digestible
- Engaging follow-up questions
- Optimistic yet realistic perspective
- Coffee shop conversation vibe

### **Intelligent Fallback System**
- Graceful degradation when APIs are unavailable
- Mock responses maintain app functionality
- Automatic retry mechanisms
- Error logging and monitoring

### **Real-time News Integration**
- Live news fetching from multiple sources
- Duplicate detection and prevention
- Automatic categorization
- Source attribution and linking

## 🔄 Development Workflow

### **Adding New Features**
1. Backend changes in `backend/` directory
2. Frontend updates in `frontend/app/` directory
3. Database migrations via SQLAlchemy
4. API documentation auto-updates

### **Testing**
```bash
# Test backend endpoints
curl -X GET http://localhost:8000/health

# Test chat functionality
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "test"}'
```

## 🚀 Deployment Ready

The application is production-ready with:
- ✅ Environment-based configuration
- ✅ Error handling and logging
- ✅ Database persistence
- ✅ API rate limiting considerations
- ✅ Responsive frontend design
- ✅ Docker support ready

## 📝 API Keys Setup

### **OpenAI API Key**
1. Visit [OpenAI Platform](https://platform.openai.com)
2. Create account and add billing information
3. Generate API key in API Keys section
4. Add to `.env` file

### **NewsAPI Key**
1. Sign up at [NewsAPI.org](https://newsapi.org)
2. Get free API key (500 requests/day)
3. Add to `.env` file

### **Guardian API Key**
1. Register at [Guardian Open Platform](https://open-platform.theguardian.com)
2. Request API key
3. Add to `.env` file

## 🎯 Current Status: Fully Functional

- ✅ **Backend API**: All endpoints working
- ✅ **Frontend UI**: Complete interface
- ✅ **Database**: 95+ articles stored
- ✅ **AI Integration**: OpenAI GPT-4 responding
- ✅ **News Aggregation**: Multiple sources active
- ✅ **Chat System**: Real-time conversations
- ✅ **Morning Briefings**: AI-generated summaries

## 🤝 Contributing

This is a demonstration project showcasing modern web development practices with AI integration. Feel free to explore, learn, and build upon it!

## 📄 License

MIT License - feel free to use this project as inspiration for your own Morning Brew-style applications! 