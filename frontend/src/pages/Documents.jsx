
import { useEffect, useRef, useState } from 'react'
import '../App.css'

function Documents() {
  const fileInputRef = useRef(null)

  const [documents, setDocuments] = useState([])
  const [search, setSearch] = useState('')
  const [message, setMessage] = useState('')
  const [isDragging, setIsDragging] = useState(false)

  // Fetch previously uploaded documents from backend
  useEffect(() => {
    const fetchDocuments = async () => {
      const token = localStorage.getItem('access_token')

      if (!token) {
        setMessage('Please log in to view your documents.')
        return
      }

      try {
        const response = await fetch(
          'http://127.0.0.1:8000/documents',
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Could not load documents.')
        }

        setDocuments(
          data.documents.map(document => ({
            id: document.id,
            name: document.filename,
            size: '—',
            pages: document.pages_processed,
            chunks: document.chunks_created,
            status: document.status
          }))
        )
      } catch (error) {
        setMessage(error.message)
      }
    }

    fetchDocuments()
  }, [])

  // Format file size
  const formatSize = bytes => {
    if (bytes >= 1024 * 1024) {
      return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
    }

    return `${(bytes / 1024).toFixed(2)} KB`
  }

  // Upload and process PDF files
  const processFiles = async files => {
    if (!files || files.length === 0) return

    const selectedFiles = Array.from(files)

    const pdfFiles = selectedFiles.filter(
      file =>
        file.type === 'application/pdf' ||
        file.name.toLowerCase().endsWith('.pdf')
    )

    if (pdfFiles.length !== selectedFiles.length) {
      setMessage(
        'Only PDF files are supported. Non-PDF files were skipped.'
      )
    } else {
      setMessage('')
    }

    if (pdfFiles.length === 0) return

    const token = localStorage.getItem('access_token')

    if (!token) {
      setMessage('Your session has expired. Please log in again.')
      return
    }

    for (const file of pdfFiles) {
      const documentId = `${Date.now()}-${Math.random()}`

      const newDocument = {
        id: documentId,
        name: file.name,
        size: formatSize(file.size),
        pages: '—',
        chunks: '—',
        status: 'Processing'
      }

      setDocuments(previous => [newDocument, ...previous])
      setMessage(`Uploading ${file.name}...`)

      try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch(
          'http://127.0.0.1:8000/upload',
          {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${token}`
            },
            body: formData
          }
        )

        const data = await response.json()

        if (!response.ok) {
          throw new Error(
            typeof data.detail === 'string'
              ? data.detail
              : JSON.stringify(data.detail || 'Upload failed.')
          )
        }

        setDocuments(previous =>
          previous.map(document =>
            document.id === documentId
              ? {
                  ...document,
                  pages: data.pages_processed,
                  chunks: data.chunks_created,
                  status: 'Processed',
                  serverId: data.document_id
                }
              : document
          )
        )

        setMessage(
          `${file.name} uploaded and processed successfully!`
        )
      } catch (error) {
        setDocuments(previous =>
          previous.map(document =>
            document.id === documentId
              ? { ...document, status: 'Failed' }
              : document
          )
        )

        setMessage(`${file.name}: ${error.message}`)
      }
    }
  }

  // Handle file selection
  const handleUpload = event => {
    processFiles(event.target.files)
    event.target.value = ''
  }

  // Drag and drop handlers
  const handleDragOver = event => {
    event.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = event => {
    event.preventDefault()

    if (!event.currentTarget.contains(event.relatedTarget)) {
      setIsDragging(false)
    }
  }

  const handleDrop = event => {
    event.preventDefault()
    setIsDragging(false)
    processFiles(event.dataTransfer.files)
  }

  // Remove document from current page only
  const handleDelete = id => {
    setDocuments(previous =>
      previous.filter(document => document.id !== id)
    )

    setMessage(
      'Document removed from this page. The server file is not deleted.'
    )
  }

  // Search documents
  const filteredDocuments = documents.filter(document =>
    document.name.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="documents-page">

      {/* Page Heading */}
      <div className="documents-heading">
        <div>
          <p className="date-label">KNOWLEDGE BASE</p>
          <h1>Documents</h1>
          <p className="subtitle">
            Upload and manage the documents your AI assistant uses to answer questions.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={() => fileInputRef.current?.click()}
        >
          ＋ Upload Documents
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          multiple
          hidden
          onChange={handleUpload}
        />
      </div>

      {/* Upload Dropzone */}
      <div
        className={`upload-dropzone ${isDragging ? 'drag-active' : ''}`}
        onClick={() => fileInputRef.current?.click()}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onKeyDown={event => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault()
            fileInputRef.current?.click()
          }
        }}
        role="button"
        tabIndex={0}
        aria-label="Upload PDF documents"
      >
        <div className="dropzone-icon">↑</div>

        <h3>Drag and drop your PDF files here</h3>
        <p>Or browse files from your computer</p>

        <button
          className="secondary-button"
          onClick={event => {
            event.stopPropagation()
            fileInputRef.current?.click()
          }}
        >
          Browse Files
        </button>

        <small>
          Supported format: PDF | Maximum size: 20 MB per file
        </small>
      </div>

      {/* Status Message */}
      {message && (
        <div className="document-message">
          {message}
          <button onClick={() => setMessage('')}>×</button>
        </div>
      )}

      {/* Document Statistics */}
      <section className="document-stats">
        <div className="panel document-stat">
          <span>Total Documents</span>
          <strong>{documents.length}</strong>
        </div>

        <div className="panel document-stat">
          <span>Processed</span>
          <strong>
            {documents.filter(d => d.status === 'Processed').length}
          </strong>
        </div>

        <div className="panel document-stat">
          <span>Processing / Failed</span>
          <strong>
            {documents.filter(d => d.status !== 'Processed').length}
          </strong>
        </div>
      </section>

      {/* Document Manager */}
      <section className="panel document-manager">
        <div className="document-manager-header">
          <div>
            <h3>Your Knowledge Base</h3>
            <p>Documents uploaded to this organisation.</p>
          </div>

          <input
            className="document-search"
            type="search"
            placeholder="Search documents..."
            value={search}
            onChange={event => setSearch(event.target.value)}
          />
        </div>

        <div className="document-table">
          <div className="document-table-head">
            <span>DOCUMENT NAME</span>
            <span>SIZE</span>
            <span>PAGES</span>
            <span>STATUS</span>
            <span>ACTION</span>
          </div>

          {filteredDocuments.length === 0 ? (
            <div className="empty-documents">
              No documents uploaded yet.
            </div>
          ) : (
            filteredDocuments.map(document => (
              <div
                className="document-table-row"
                key={document.id}
              >
                <div className="table-document-name">
                  <div className="file-icon pdf">PDF</div>
                  <strong>{document.name}</strong>
                </div>

                <span>{document.size}</span>
                <span>{document.pages}</span>

                <span>
                  <span
                    className={`status ${
                      document.status === 'Processed'
                        ? ''
                        : 'processing'
                    }`}
                  >
                    {document.status}
                  </span>
                </span>

                <button
                  className="delete-button"
                  title="Remove from this page only"
                  onClick={() => handleDelete(document.id)}
                >
                  Remove
                </button>
              </div>
            ))
          )}
        </div>

        <div className="document-table-footer">
          Showing {filteredDocuments.length} of {documents.length} documents
        </div>
      </section>

      {/* Upload Information */}
      <section className="upload-information">
        <div className="upload-info-icon">ⓘ</div>

        <div>
          <strong>About document processing</strong>
          <p>
            Uploaded PDFs are extracted, divided into text chunks,
            converted into embeddings and stored in your organisation's
            separate knowledge base.
          </p>
        </div>
      </section>

    </div>
  )
}

export default Documents
