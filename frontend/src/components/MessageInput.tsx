import { useState } from 'react'

interface MessageInputProps {
    onSend: (message: string) => void
}

function MessageInput({ onSend }: MessageInputProps) {
    const [input, setInput] = useState('')

    const handleSend = () => {
        if (input.trim() === '') return
        onSend(input)
        setInput('')
    }

    return (
        <div className="message-input">
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type a message..."
            />
            <button onClick={handleSend}>Send</button>
        </div>
    )
}

export default MessageInput