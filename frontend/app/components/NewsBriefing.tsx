'use client'

import { useState } from 'react'
import { formatDistanceToNow } from 'date-fns'

interface Article {
  id: number
  title: string
  summary: string
  source: string
  category: string
  url: string
  published_at: string
  created_at: string
}

interface Briefing {
  summary: string
  articles: Article[]
  generated_at: string
  categories: string[]
}

interface NewsBriefingProps {
  briefing: Briefing
}

export default function NewsBriefing({ briefing }: NewsBriefingProps) {
  const [showAllArticles, setShowAllArticles] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string>('all')

  const filteredArticles = selectedCategory === 'all' 
    ? briefing.articles 
    : briefing.articles.filter(article => article.category === selectedCategory)

  const displayedArticles = showAllArticles 
    ? filteredArticles 
    : filteredArticles.slice(0, 5)

  return (
    <div className="space-y-6">
      {/* AI Summary */}
      <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <span className="text-2xl">🤖</span>
          </div>
          <div className="ml-3">
            <h3 className="text-lg font-medium text-blue-800 mb-2">
              Your Morning Briefing
            </h3>
            <div className="text-blue-700 whitespace-pre-wrap leading-relaxed">
              {briefing.summary}
            </div>
            <div className="text-sm text-blue-600 mt-3">
              Generated {formatDistanceToNow(new Date(briefing.generated_at))} ago
            </div>
          </div>
        </div>
      </div>

      {/* Category Filter */}
      {briefing.categories.length > 1 && (
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedCategory('all')}
            className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
              selectedCategory === 'all'
                ? 'bg-blue-100 text-blue-800 border border-blue-300'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All ({briefing.articles.length})
          </button>
          {briefing.categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition-colors capitalize ${
                selectedCategory === category
                  ? 'bg-blue-100 text-blue-800 border border-blue-300'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {category} ({briefing.articles.filter(a => a.category === category).length})
            </button>
          ))}
        </div>
      )}

      {/* Articles List */}
      <div className="space-y-4">
        <h4 className="text-lg font-semibold text-gray-800 flex items-center">
          <span className="mr-2">📰</span>
          Latest Articles
        </h4>
        
        {displayedArticles.map((article, index) => (
          <div key={article.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-medium text-white bg-blue-500 px-2 py-1 rounded-full">
                    #{index + 1}
                  </span>
                  <span className="text-xs font-medium text-gray-500 capitalize">
                    {article.category}
                  </span>
                  <span className="text-xs text-gray-400">•</span>
                  <span className="text-xs text-gray-500">
                    {article.source}
                  </span>
                </div>
                
                <h5 className="font-semibold text-gray-800 mb-2 leading-tight">
                  {article.title}
                </h5>
                
                <p className="text-gray-600 text-sm mb-3 leading-relaxed">
                  {article.summary}
                </p>
                
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-400">
                    {formatDistanceToNow(new Date(article.published_at))} ago
                  </span>
                  
                  {article.url && (
                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium hover:underline"
                    >
                      Read more →
                    </a>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Show More/Less Button */}
      {filteredArticles.length > 5 && (
        <div className="text-center">
          <button
            onClick={() => setShowAllArticles(!showAllArticles)}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors"
          >
            {showAllArticles 
              ? `Show Less` 
              : `Show ${filteredArticles.length - 5} More Articles`
            }
          </button>
        </div>
      )}

      {/* Refresh Button */}
      <div className="text-center pt-4 border-t border-gray-200">
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center mx-auto"
        >
          <span className="mr-2">🔄</span>
          Refresh News
        </button>
      </div>
    </div>
  )
} 