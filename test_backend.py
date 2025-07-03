#!/usr/bin/env python3
"""
Simple test script to verify the Morning News AI Assistant backend.
Run this after setting up the backend to ensure everything works.
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test basic health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_news_refresh():
    """Test news refresh endpoint"""
    print("\n📰 Testing news refresh...")
    try:
        response = requests.post(f"{BASE_URL}/api/news/refresh")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ News refresh successful: {data}")
            return True
        else:
            print(f"❌ News refresh failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ News refresh error: {e}")
        return False

def test_morning_briefing():
    """Test morning briefing endpoint"""
    print("\n☀️ Testing morning briefing...")
    try:
        response = requests.get(f"{BASE_URL}/api/news/briefing")
        if response.status_code == 200:
            data = response.json()
            print("✅ Morning briefing generated successfully")
            print(f"Summary preview: {data.get('summary', '')[:200]}...")
            print(f"Articles count: {len(data.get('articles', []))}")
            return True
        else:
            print(f"❌ Morning briefing failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Morning briefing error: {e}")
        return False

def test_chat_message():
    """Test chat message endpoint"""
    print("\n💬 Testing chat message...")
    try:
        # First create a new session
        session_response = requests.post(f"{BASE_URL}/api/chat/new-session")
        if session_response.status_code != 200:
            print(f"❌ Failed to create session: {session_response.status_code}")
            return False
        
        session_id = session_response.json()["session_id"]
        
        # Send a test message
        message_data = {
            "message": "Tell me about the latest news in technology",
            "session_id": session_id
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json=message_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat message successful")
            print(f"AI Response preview: {data.get('response', '')[:200]}...")
            return True
        else:
            print(f"❌ Chat message failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat message error: {e}")
        return False

def test_user_preferences():
    """Test user preferences endpoint"""
    print("\n👤 Testing user preferences...")
    try:
        user_id = "test_user_123"
        
        # Get preferences (should create default if not exists)
        response = requests.get(f"{BASE_URL}/api/user/preferences/{user_id}")
        if response.status_code == 200:
            data = response.json()
            print("✅ User preferences retrieved successfully")
            print(f"Preferences: {data}")
            return True
        else:
            print(f"❌ User preferences failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ User preferences error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Morning News AI Assistant Backend Tests")
    print("=" * 60)
    
    # Check if backend is running
    if not test_health_check():
        print("\n❌ Backend is not running. Please start it first:")
        print("   cd backend && python main.py")
        return
    
    # Run tests
    tests = [
        test_news_refresh,
        test_morning_briefing,
        test_chat_message,
        test_user_preferences
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your backend is working correctly.")
        print("\nNext steps:")
        print("1. Set up the frontend: cd frontend && npm install && npm run dev")
        print("2. Visit http://localhost:3000 to see the full application")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("\nTroubleshooting:")
        print("1. Make sure you have set up your .env file with API keys")
        print("2. Check that your database is running and accessible")
        print("3. Verify all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 