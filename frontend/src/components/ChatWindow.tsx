import Message from "./Message"
import type { ChatMessage } from "../types"

interface ChatWindowProps {
    messages: ChatMessage[]
    isLoading: boolean
}

function ChatWindow({ messages, isLoading }: ChatWindowProps) {
    return (
        <div className="messages">
            {messages.map((message, index) => (
                <Message key={index} role={message.role} content={message.content} />
            ))}
            {isLoading && <Message role="assistant" content="..." />}
        </div>
    )
}

export default ChatWindow