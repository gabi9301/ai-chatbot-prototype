import type { Role } from '../types'

interface MessageProps {
    role: Role
    content: string
}

function Message({ role, content }: MessageProps) {
    return (
        <div className={`message ${role}`}>
            {content}
        </div>
    )
}

export default Message