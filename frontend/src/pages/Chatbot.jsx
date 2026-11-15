
import { useState } from 'react'
import '../App.css'

function Chatbot() {
  const [botName, setBotName] = useState('Acme Assistant')
  const [welcomeMessage, setWelcomeMessage] = useState(
    'Hello! How can I help you today?'
  )
  const [language, setLanguage] = useState('English')
  const [themeColor, setThemeColor] = useState('#7564e8')
  const [saved, setSaved] = useState(false)

  // Actual chatbot conversation
  const [messages, setMessages] = useState([])
  const [question, setQuestion] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [chatError, setChatError] = useState('')

  // Save chatbot settings (currently demo-only)
  const handleSave = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 2500)
  }

  // Send question to FastAPI backend
  const handleSend = async () => {
    const trimmedQuestion = question.trim()

    if (!trimmedQuestion || chatLoading) return

    const token = localStorage.getItem('access_token')

    if (!token) {
      setChatError('Please log in again.')
      return
    }

    setChatError('')
    setChatLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          question: trimmedQuestion
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Unable to get an answer.')
      }

      setMessages(previous => [
        ...previous,
        {
          role: 'user',
          content: trimmedQuestion
        },
        {
          role: 'bot',
          content: data.answer || 'No answer received.',
          sources: data.sources || []
        }
      ])

      setQuestion('')
    } catch (error) {
      setChatError(error.message)
    } finally {
      setChatLoading(false)
    }
  }

  return (
    <div className="chatbot-page">

      {/* Page Heading */}
      <div className="chatbot-heading">
        <div>
          <p className="date-label">AI ASSISTANT</p>
          <h1>Chatbot Configuration</h1>
          <p className="subtitle">
            Personalise how your organisation's AI assistant looks and responds.
          </p>
        </div>

        <button className="primary-button" onClick={handleSave}>
          Save Changes
        </button>
      </div>

      {saved && (
        <div className="document-message">
          Settings saved in this demo session.
        </div>
      )}

      {/* Configuration and Live Preview */}
      <div className="chatbot-layout">

        {/* Assistant Settings */}
        <section className="panel chatbot-settings">
          <h3>Assistant Identity</h3>
          <p className="settings-description">
            Set the basic information for your AI assistant.
          </p>

          <label>Assistant Name</label>
          <input
            className="settings-input"
            value={botName}
            onChange={e => setBotName(e.target.value)}
            placeholder="Enter assistant name"
          />

          <label>Welcome Message</label>
          <textarea
            className="settings-textarea"
            value={welcomeMessage}
            onChange={e => setWelcomeMessage(e.target.value)}
            placeholder="Enter welcome message"
            rows={3}
          />

          <label>Response Language</label>
          <select
            className="settings-input"
            value={language}
            onChange={e => setLanguage(e.target.value)}
          >
            <option>English</option>
            <option>Hinglish</option>
            <option>Hindi</option>
          </select>

          <div className="settings-divider"></div>

          <h3>Appearance</h3>
          <p className="settings-description">
            Choose the primary colour of your chatbot.
          </p>

          <label>Theme Colour</label>
          <div className="color-picker-row">
            <input
              type="color"
              value={themeColor}
              onChange={e => setThemeColor(e.target.value)}
            />
            <span>{themeColor.toUpperCase()}</span>
          </div>

          <div className="settings-divider"></div>

          <h3>Public Access</h3>
          <p className="settings-description">
            Your public chatbot link will be available after backend integration.
          </p>

          <div className="public-link-placeholder">
            <span>🔗</span>
            <span>Public chatbot link not generated yet</span>
          </div>
        </section>

        {/* Live Preview */}
        <section className="panel chatbot-preview-panel">
          <div className="preview-heading">
            <div>
              <h3>Live Preview</h3>
              <p>See how your assistant will appear to visitors.</p>
            </div>
            <span className="preview-status">● Preview</span>
          </div>

          <div className="chat-preview-window">
            <div
              className="chat-preview-header"
              style={{ backgroundColor: themeColor }}
            >
              <div className="preview-bot-avatar">✧</div>
              <div>
                <strong>{botName || 'Your Assistant'}</strong>
                <small>● Online</small>
              </div>
            </div>

            <div className="chat-preview-body">
              <div className="bot-message">
                {welcomeMessage || 'Your welcome message will appear here.'}
              </div>

              <div className="user-message">
                What can you help me with?
              </div>

              <div className="bot-message">
                I'm here to answer your questions using the organisation's documents!
              </div>
            </div>

            <div className="chat-preview-input">
              <span>Type your message...</span>
              <button style={{ backgroundColor: themeColor }}>
                ➤
              </button>
            </div>
          </div>

          <div className="preview-note">
            Selected language: <strong>{language}</strong>
          </div>
        </section>
      </div>

      {/* Actual Working Chatbot */}
      <section
        className="panel"
        style={{ marginTop: '24px', padding: '24px' }}
      >
        <div className="preview-heading">
          <div>
            <h3>{botName || 'OrgBot Assistant'}</h3>
            <p>
              Ask questions based on your organisation's uploaded PDFs.
            </p>
          </div>
          <span className="preview-status">● Connected</span>
        </div>

        {/* Chat Messages */}
        <div
          style={{
            minHeight: '280px',
            maxHeight: '420px',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '14px',
            padding: '18px',
            background: '#f8f8fc',
            borderRadius: '12px',
            marginTop: '18px'
          }}
        >
          {messages.length === 0 ? (
            <div className="bot-message">
              {welcomeMessage}
              <br />
              <small>
                Try asking a question about your uploaded documents.
              </small>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                style={{
                  alignSelf:
                    message.role === 'user' ? 'flex-end' : 'flex-start',
                  maxWidth: '80%'
                }}
              >
                <div
                  className={
                    message.role === 'user'
                      ? 'user-message'
                      : 'bot-message'
                  }
                >
                  {message.content}
                </div>

                {message.sources?.length > 0 && (
                  <div
                    style={{
                      fontSize: '12px',
                      marginTop: '6px'
                    }}
                  >
                    <strong>Sources:</strong>

                    {message.sources.map((source, sourceIndex) => {
                      const sourceName =
                        typeof source === 'string'
                          ? source
                          : source.source || source.filename || 'Document'

                      const page =
                        typeof source === 'object' ? source.page : null

                      return (
                        <div key={sourceIndex}>
                          {sourceName}
                          {page ? ` (Page ${page})` : ''}
                        </div>
                      )
                    })}
                  </div>
                )}
              </div>
            ))
          )}

          {chatLoading && (
            <div className="bot-message">
              Thinking...
            </div>
          )}
        </div>

        {/* Error Message */}
        {chatError && (
          <p style={{ color: 'red', marginTop: '12px' }}>
            {chatError}
          </p>
        )}

        {/* Chat Input */}
        <form
          onSubmit={e => {
            e.preventDefault()
            handleSend()
          }}
          style={{
            display: 'flex',
            gap: '12px',
            marginTop: '16px'
          }}
        >
          <input
            className="settings-input"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="Ask something about your organisation..."
            disabled={chatLoading}
          />

          <button
            className="primary-button"
            type="submit"
            disabled={chatLoading || !question.trim()}
          >
            {chatLoading ? 'Thinking...' : 'Send'}
          </button>
        </form>
      </section>
    </div>
  )
}

export default Chatbot
