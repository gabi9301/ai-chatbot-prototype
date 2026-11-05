import { useEffect, useRef } from "react"
import Message from "./Message"
import type { ChatMessage } from "../types"

interface ChatWindowProps {
    messages: ChatMessage[]
    isLoading: boolean
}

function ChatWindow({ messages, isLoading }: ChatWindowProps) {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages, isLoading])
    return (
        <div className="messages">
            {messages.map((message, index) => (
                <Message key={index} role={message.role} content={message.content} />
            ))}
            {isLoading && (
                <div className="message assistant typing">
                    <span /><span /><span /><span /><span />
                </div>)}
            <div ref={bottomRef} />
        </div>
    )
}

export default ChatWindow