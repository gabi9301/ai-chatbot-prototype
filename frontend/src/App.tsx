import { useState } from 'react'
import { sendMessageToApi, resetConversation } from './api/chat'
import ChatWindow from './components/ChatWindow'
import MessageInput from './components/MessageInput'
import type { ChatMessage } from './types'
import './App.css'

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (message: string) => {
    const userMessage: ChatMessage = { role: 'user', content: message }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const reply = await sendMessageToApi(message)
      const assistantMessage: ChatMessage = { role: 'assistant', content: reply }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error(error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = async () => {
    try {
      await resetConversation()
      setMessages([])
    } catch (error) {
      console.error(error)
    }
  }
  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>AI Chatbot</h1>
        <button onClick={handleReset}>Reset</button>
      </header>
      <ChatWindow messages={messages} isLoading={isLoading} />
      <MessageInput onSend={sendMessage} />
    </div>
  )
}

export default App