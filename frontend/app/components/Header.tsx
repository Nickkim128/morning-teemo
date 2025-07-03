'use client'

export default function Header() {
  return (
    <header className="morning-gradient text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="text-3xl">☕</div>
            <div>
              <h1 className="text-2xl font-bold">Morning News AI</h1>
              <p className="text-blue-100">Your witty news companion</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-colors">
              Settings
            </button>
            <button className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-colors">
              Refresh News
            </button>
          </div>
        </div>
      </div>
    </header>
  )
} 