
import { useNavigate } from 'react-router-dom'

function Overview() {
  const navigate = useNavigate()

  return (
    <div className="page-content">
      <section className="welcome-section">
        <div>
          <p className="date-label">ORGANISATION WORKSPACE</p>
          <h1>Good evening, Vidhi 👋</h1>
          <p className="subtitle">
            Here's what's happening with your AI assistant today.
          </p>
        </div>
        <button className="primary-button" onClick={() => navigate('/documents')}>
          ＋ Add Documents
        </button>
      </section>

      <section className="stats-grid">
        <div className="stat-card">
          <div className="stat-top">
            <span>Total Documents</span>
            <div className="stat-icon purple">▤</div>
          </div>
          <h2>24</h2>
          <p><span className="positive">↑ 12%</span> from last month</p>
        </div>

        <div className="stat-card">
          <div className="stat-top">
            <span>Total Conversations</span>
            <div className="stat-icon blue">☏</div>
          </div>
          <h2>1,284</h2>
          <p><span className="positive">↑ 18%</span> from last month</p>
        </div>

        <div className="stat-card">
          <div className="stat-top">
            <span>Questions Answered</span>
            <div className="stat-icon green">✧</div>
          </div>
          <h2>3,642</h2>
          <p><span className="positive">↑ 24%</span> from last month</p>
        </div>

        <div className="stat-card">
          <div className="stat-top">
            <span>Knowledge Base</span>
            <div className="stat-icon orange">◫</div>
          </div>
          <h2>86.4 <small>%</small></h2>
          <p>Document processing complete</p>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="panel documents-panel">
          <div className="panel-header">
            <div>
              <h3>Recent Documents</h3>
              <p>Manage your organisation's knowledge base.</p>
            </div>
            <button className="text-button" onClick={() => navigate('/documents')}>
              View all →
            </button>
          </div>

          <div className="document-list">
            <div className="document-row">
              <div className="file-icon pdf">PDF</div>
              <div className="document-info">
                <strong>Organisation Handbook.pdf</strong>
                <small>2.4 MB · 12 pages</small>
              </div>
              <span className="status">Processed</span>
            </div>

            <div className="document-row">
              <div className="file-icon pdf">PDF</div>
              <div className="document-info">
                <strong>Admission Guidelines.pdf</strong>
                <small>1.8 MB · 8 pages</small>
              </div>
              <span className="status">Processed</span>
            </div>

            <div className="document-row">
              <div className="file-icon pdf">PDF</div>
              <div className="document-info">
                <strong>Fee Structure 2026.pdf</strong>
                <small>980 KB · 5 pages</small>
              </div>
              <span className="status">Processed</span>
            </div>

            <div className="document-row">
              <div className="file-icon pdf">PDF</div>
              <div className="document-info">
                <strong>Scholarship Policy.pdf</strong>
                <small>1.2 MB · 7 pages</small>
              </div>
              <span className="status processing">Processing</span>
            </div>
          </div>
        </div>

        <div className="panel assistant-panel">
          <div className="panel-header">
            <div>
              <h3>Your AI Assistant</h3>
              <p>Configure your organisation's chatbot.</p>
            </div>
            <span className="online-dot"></span>
          </div>

          <div className="assistant-preview">
            <div className="bot-avatar">✧</div>
            <h3>Acme Assistant</h3>
            <span className="live-label">● Active</span>
            <p>Hello! How can I help you today?</p>
          </div>

          <div className="assistant-actions">
            <button className="secondary-button">⚙ Configure Assistant</button>
            <button className="primary-button">Preview Chatbot ↗</button>
          </div>
        </div>
      </section>

      <section className="bottom-grid">
        <div className="panel activity-panel">
          <div className="panel-header">
            <div>
              <h3>Recent Activity</h3>
              <p>Latest updates from your workspace.</p>
            </div>
          </div>

          <div className="activity-row">
            <div className="activity-icon green">✓</div>
            <div>
              <strong>Document processed successfully</strong>
              <small>Organisation Handbook.pdf</small>
            </div>
            <time>10 min ago</time>
          </div>

          <div className="activity-row">
            <div className="activity-icon blue">✧</div>
            <div>
              <strong>New conversation started</strong>
              <small>Public chatbot</small>
            </div>
            <time>35 min ago</time>
          </div>

          <div className="activity-row">
            <div className="activity-icon purple">↑</div>
            <div>
              <strong>Knowledge base updated</strong>
              <small>3 new documents added</small>
            </div>
            <time>2 hours ago</time>
          </div>
        </div>

        <div className="panel usage-panel">
          <div className="panel-header">
            <div>
              <h3>Usage Overview</h3>
              <p>Your monthly usage.</p>
            </div>
          </div>

          <div className="usage-item">
            <div><span>Documents</span><strong>24 / 50</strong></div>
            <div className="progress-track">
              <div className="progress-fill purple-fill" style={{ width: '48%' }}></div>
            </div>
          </div>

          <div className="usage-item">
            <div><span>AI Conversations</span><strong>1,284 / 2,000</strong></div>
            <div className="progress-track">
              <div className="progress-fill blue-fill" style={{ width: '64.2%' }}></div>
            </div>
          </div>

          <p className="usage-note">Usage figures are sample dashboard data.</p>
        </div>
      </section>

      <footer className="footer">
        <span>© 2026 OrgBot. All rights reserved.</span>
        <span>Built for smarter organisations ✦</span>
      </footer>
    </div>
  )
}

export default Overview
