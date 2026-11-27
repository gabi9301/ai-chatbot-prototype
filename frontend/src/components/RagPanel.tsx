import AskPanel from './AskPanel'
import IngestPanel from './IngestPanel'

function RagPanel() {
    return (
        <div className="rag-workspace">
            <IngestPanel />
            <AskPanel />

        </div>
    )
}

export default RagPanel