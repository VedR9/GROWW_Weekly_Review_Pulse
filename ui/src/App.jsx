import React, { useEffect, useState } from 'react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts';
import { Sparkles, TrendingUp, TrendingDown, MessageSquare, Star } from 'lucide-react';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="label">{label}</p>
        <p style={{ color: 'var(--accent-primary)', fontWeight: 'bold' }}>
          Sentiment: {payload[0].value}%
        </p>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          Avg Rating: {payload[0].payload.avg_rating} ⭐
        </p>
      </div>
    );
  }
  return null;
};

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/history.json')
      .then(res => res.json())
      .then(json => {
        // Sort chronologically for the chart
        const sorted = json.sort((a, b) => new Date(a.date) - new Date(b.date));
        setData(sorted);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load history", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
  }

  if (data.length === 0) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>No data available</div>;
  }

  const latest = data[data.length - 1];
  const previous = data.length > 1 ? data[data.length - 2] : null;

  const renderTrend = (current, prev, isInverse = false) => {
    if (!prev) return null;
    const diff = current - prev;
    const isUp = diff > 0;
    // For sentiment/rating, up is good. For some metrics, it might be inverse.
    const isGood = isInverse ? !isUp : isUp;
    
    return (
      <span className={`metric-trend ${isGood ? 'trend-up' : 'trend-down'}`}>
        {isUp ? '↑' : '↓'} {Math.abs(diff).toFixed(1)}
      </span>
    );
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div>
          <h1>Weekly Review Pulse</h1>
          <p>AI-driven sentiment analysis of App Store & Play Store reviews</p>
        </div>
        <button className="btn-primary" onClick={() => alert("This triggers the GitHub Action pipeline!")}>
          <Sparkles size={18} />
          Generate Pulse
        </button>
      </header>

      {/* Metrics Grid */}
      <div className="metric-grid">
        <div className="glass-panel metric-card">
          <span className="metric-title"><Star size={16} /> Avg Rating</span>
          <div className="metric-value">
            {latest.avg_rating}
            {renderTrend(latest.avg_rating, previous?.avg_rating)}
          </div>
        </div>
        
        <div className="glass-panel metric-card">
          <span className="metric-title"><TrendingUp size={16} /> Sentiment Score</span>
          <div className="metric-value">
            {latest.sentiment_score}%
            {renderTrend(latest.sentiment_score, previous?.sentiment_score)}
          </div>
        </div>

        <div className="glass-panel metric-card">
          <span className="metric-title"><MessageSquare size={16} /> Reviews Processed</span>
          <div className="metric-value">
            {latest.total_reviews}
            {renderTrend(latest.total_reviews, previous?.total_reviews)}
          </div>
        </div>

        <div className="glass-panel metric-card">
          <span className="metric-title"><Sparkles size={16} /> Top Theme</span>
          <div style={{ fontSize: '1.25rem', fontWeight: 600, marginTop: '0.5rem', color: 'var(--text-main)' }}>
            "{latest.top_theme}"
          </div>
        </div>
      </div>

      {/* Chart Section */}
      <div className="glass-panel chart-section">
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.2rem', color: 'var(--text-muted)' }}>
          Sentiment Trend (Week over Week)
        </h2>
        <ResponsiveContainer width="100%" height="85%">
          <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorSentiment" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis 
              dataKey="date" 
              stroke="var(--text-muted)" 
              tick={{fill: 'var(--text-muted)', fontSize: 12}} 
              tickLine={false}
              axisLine={false}
              tickFormatter={(val) => new Date(val).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            />
            <YAxis 
              stroke="var(--text-muted)" 
              tick={{fill: 'var(--text-muted)', fontSize: 12}}
              tickLine={false}
              axisLine={false}
              domain={[0, 100]}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(255,255,255,0.1)', strokeWidth: 2 }} />
            <Area 
              type="monotone" 
              dataKey="sentiment_score" 
              stroke="var(--accent-primary)" 
              strokeWidth={3}
              fillOpacity={1} 
              fill="url(#colorSentiment)" 
              activeDot={{ r: 6, fill: "var(--accent-primary)", stroke: "var(--bg-dark)", strokeWidth: 2 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* History Table */}
      <div className="glass-panel history-section">
        <h2>Pulse History</h2>
        <table className="history-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Reviews</th>
              <th>Avg Rating</th>
              <th>Sentiment</th>
              <th>Top Theme</th>
            </tr>
          </thead>
          <tbody>
            {[...data].reverse().map((row, idx) => (
              <tr key={idx}>
                <td style={{ fontWeight: 500 }}>{row.date}</td>
                <td>{row.total_reviews}</td>
                <td>{row.avg_rating} ⭐</td>
                <td>
                  <span style={{
                    color: row.sentiment_score > 60 ? 'var(--accent-primary)' : 
                           row.sentiment_score > 40 ? '#fbbf24' : '#ef4444'
                  }}>
                    {row.sentiment_score}%
                  </span>
                </td>
                <td style={{ color: 'var(--text-muted)' }}>"{row.top_theme}"</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
