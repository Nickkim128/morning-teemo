'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import ChatInterface from './components/ChatInterface'
import NewsBriefing from './components/NewsBriefing'
import Header from './components/Header'

export default function Home() {
  const [briefing, setBriefing] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchBriefing()
  }, [])

  const fetchBriefing = async () => {
    try {
      setLoading(true)
      const response = await axios.get('/api/news/briefing')
      setBriefing(response.data)
    } catch (err) {
      setError('Failed to load morning briefing')
      console.error('Error fetching briefing:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Morning Briefing Section */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">☀️</span>
                Morning Briefing
              </h2>
              
              {loading ? (
                <div className="animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                </div>
              ) : error ? (
                <div className="text-red-600 p-4 bg-red-50 rounded-lg">
                  {error}
                  <button 
                    onClick={fetchBriefing}
                    className="ml-4 text-sm underline hover:no-underline"
                  >
                    Try again
                  </button>
                </div>
              ) : briefing ? (
                <NewsBriefing briefing={briefing} />
              ) : null}
            </div>
          </div>

          {/* Chat Interface Section */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
                <span className="mr-2">💬</span>
                Chat with AI Assistant
              </h2>
              <ChatInterface />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
} 