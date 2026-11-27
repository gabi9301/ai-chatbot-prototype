import { apiFetch } from "./client"

export interface DocumentIngest {
    content: string
    source?: string
    language?: "en" | "ja" | "ko"
}

export interface DocumentRead {
    id: number
    source: string | null
    content: string
    created_at: string
}

export async function ingestDocument(document: DocumentIngest): Promise<DocumentRead> {
    const data = await apiFetch<DocumentRead>('/ingest', {
        method: 'POST',
        body: JSON.stringify(document),
    })
    return data
}