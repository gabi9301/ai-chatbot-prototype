import { useState, useRef, type ChangeEvent } from 'react'
import { ingestDocument } from '../api/rag'

function IngestPanel() {
    const [content, setContent] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const [ingestDocId, setIngestDocId] = useState<number | null>(null)

    const fileRef = useRef<HTMLInputElement>(null);

    const ALLOWED_EXTENSIONS = ['txt']

    const handleFileChange = async (e: ChangeEvent<HTMLInputElement>) => {
        const selected = e.target.files?.[0]
        if (!selected) return

        const extension = selected.name.split('.').pop()?.toLowerCase()
        if (!extension || !ALLOWED_EXTENSIONS.includes(extension)) {
            e.target.value = ''
            return
        }

        try {
            const text = await selected.text()
            if (text.trim() === '') return
            setContent(text)
        } catch (err) {
            console.error("An error occured while extracting texts from file")
        }
    }

    const handleSubmit = async () => {
        if (content.trim() === '') return
        setIsLoading(true)

        try {
            const data = await ingestDocument({ content: content })
            setIngestDocId(data.id)
        } catch (err) {
            console.error("An error occured while ingesting document")
        } finally {
            setIsLoading(false)
        }
        setContent('')

        if (fileRef.current) {
            fileRef.current.value = '';
        }
    }

    return (
        <div className="ingest-panel">
            <input
                type="file"
                ref={fileRef}
                accept={ALLOWED_EXTENSIONS.map((ext) => `.${ext}`).join(',')}
                onChange={handleFileChange}
                disabled={isLoading}
            />
            <textarea
                id="ingestTextarea"
                readOnly={true}
                value={content}
            />
            {isLoading
                ? (<div>Ingesting in process...</div>)
                : (ingestDocId
                    ? (<div>Ingested as document #{ingestDocId}</div>)
                    : (<div></div>))}
            <button
                onClick={handleSubmit}
                disabled={isLoading || !content}
            >Submit
            </button>
        </div>
    )
}

export default IngestPanel