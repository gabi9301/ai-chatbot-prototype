import { useState } from 'react'
import { askQuestion } from '../api/rag'

function AskPanel() {
    const [query, setQuery] = useState('')
    const [answer, setAnswer] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState('')

    const handleAsk = async () => {
        if (query.trim() === '') return
        setError('')
        setIsLoading(true)

        try {
            const data = await askQuestion({ query: query })
            setAnswer(data.answer)
        } catch (err) {
            setError("An error occured while generating RAG answer")
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="ask-panel">
            <textarea
                id="queryTextarea"
                onChange={(e) => { setQuery(e.target.value) }}
                value={query}
            />
            {isLoading
                ? (<div className="status">Generating RAG answer....</div>)
                : (<div></div>)
            }
            <button
                onClick={handleAsk}
                disabled={isLoading || !query}
            >Ask
            </button>
            {error && <div className="error">{error}</div>}
            <textarea readOnly value={answer} placeholder="No answer yet." />
        </div>
    )
}

export default AskPanel