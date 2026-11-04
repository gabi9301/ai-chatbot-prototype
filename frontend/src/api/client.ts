const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_URL}${path}`, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
    })

    if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
    }

    return response.json()
}