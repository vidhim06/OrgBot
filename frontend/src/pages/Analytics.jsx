
import '../App.css'

function Analytics() {
  const dailyData = [
    { day: 'Mon', value: 45 },
    { day: 'Tue', value: 65 },
    { day: 'Wed', value: 52 },
    { day: 'Thu', value: 85 },
    { day: 'Fri', value: 70 },
    { day: 'Sat', value: 95 },
    { day: 'Sun', value: 60 },
  ]

  const questions = [
    { question: 'What are the admission requirements?', count: 248 },
    { question: 'What is the fee structure?', count: 192 },
    { question: 'How can I apply for scholarships?', count: 156 },
    { question: 'What are the office timings?', count: 124 },
    { question: 'How do I contact support?', count: 98 },
  ]

  const maxCount = Math.max(...questions.map(item => item.count))

  return (
    <div className="analytics-page">
      <div className="analytics-heading">
        <div>
          <p className="date-label">WORKSPACE INSIGHTS</p>
          <h1>Analytics</h1>
          <p className="subtitle">
            Understand how people interact with your organisation's AI assistant.
          </p>
        </div>

        <select className="analytics-filter" defaultValue="7">
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
        </select>
      </div>

      <section className="analytics-stats">
        <div className="panel analytics-stat-card">
          <span>Total Conversations</span>
          <h2>1,284</h2>
          <p className="positive">↑ 18% from last month</p>
        </div>

        <div className="panel analytics-stat-card">
          <span>Questions Answered</span>
          <h2>3,642</h2>
          <p className="positive">↑ 24% from last month</p>
        </div>

        <div className="panel analytics-stat-card">
          <span>Average Response Time</span>
          <h2>2.4s</h2>
          <p className="positive">↓ 12% from last month</p>
        </div>

        <div className="panel analytics-stat-card">
          <span>Resolution Rate</span>
          <h2>86.4%</h2>
          <p className="positive">↑ 6.2% from last month</p>
        </div>
      </section>

      <section className="panel analytics-chart-panel">
        <div className="analytics-panel-heading">
          <div>
            <h3>Conversation Activity</h3>
            <p>Daily conversations during the selected period.</p>
          </div>
          <span className="chart-legend">
            <span></span> Conversations
          </span>
        </div>

        <div className="bar-chart">
          {dailyData.map(item => (
            <div className="bar-column" key={item.day}>
              <strong>{item.value}</strong>
              <div className="bar-track">
                <div
                  className="bar-fill"
                  style={{ height: `${item.value}%` }}
                ></div>
              </div>
              <span>{item.day}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="analytics-bottom-grid">
        <div className="panel popular-questions">
          <div className="analytics-panel-heading">
            <div>
              <h3>Most Asked Questions</h3>
              <p>Questions visitors ask your chatbot most often.</p>
            </div>
          </div>

          {questions.map((item, index) => (
            <div className="question-item" key={item.question}>
              <div className="question-info">
                <span>{index + 1}. {item.question}</span>
                <strong>{item.count}</strong>
              </div>
              <div className="question-track">
                <div
                  className="question-fill"
                  style={{ width: `${(item.count / maxCount) * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>

        <div className="panel analytics-summary">
          <div className="analytics-panel-heading">
            <div>
              <h3>Knowledge Base Usage</h3>
              <p>Document engagement overview.</p>
            </div>
          </div>

          <div className="knowledge-summary">
            <div className="knowledge-circle">
              <div>
                <strong>86.4%</strong>
                <small>Coverage</small>
              </div>
            </div>
          </div>

          <div className="knowledge-detail">
            <span><i className="legend-dot purple-dot"></i> Documents available</span>
            <strong>24</strong>
          </div>

          <div className="knowledge-detail">
            <span><i className="legend-dot blue-dot"></i> Questions answered</span>
            <strong>3,642</strong>
          </div>

          <div className="knowledge-detail">
            <span><i className="legend-dot orange-dot"></i> Pending processing</span>
            <strong>1</strong>
          </div>
        </div>
      </section>

      <p className="analytics-disclaimer">
        These are sample analytics figures for demonstration. Live data will be connected later.
      </p>
    </div>
  )
}

export default Analytics
