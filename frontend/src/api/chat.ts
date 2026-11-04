import { apiFetch } from "./client"

interface ChatApiResponse {
    reply: string
}

export async function sendMessageToApi(message: string): Promise<string> {
    const data = await apiFetch<ChatApiResponse>('/chat', {
        method: 'POST',
        body: JSON.stringify({ message }),
    })

    return data.reply
}

export async function resetConversation(): Promise<void> {
    await apiFetch('/reset', { method: 'POST' })
}