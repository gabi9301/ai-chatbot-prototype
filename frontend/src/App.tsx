import { useState } from 'react'
import RagPanel from './components/RagPanel'
import ChatPanel from './components/ChatPanel'

import './App.css'

function App() {
  const [mode, setMode] = useState<'rag' | 'chat'>('rag')

  return (
    <div className="app-shell">
      <nav className="nav-rail">
        <button className={mode === 'rag' ? 'is-active' : ''} onClick={() => setMode('rag')}>RAG</button>
        <button className={mode === 'chat' ? 'is-active' : ''} onClick={() => setMode('chat')}>Chat</button>
      </nav>
      <main className="main-area">
        {mode === 'rag' ? <RagPanel /> : <ChatPanel />}
      </main>
    </div>

  )
}

export default App