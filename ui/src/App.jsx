import React, { useEffect, useState } from 'react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts';
import { Sparkles, TrendingUp, TrendingDown, MessageSquare, Star, AlertTriangle, Lightbulb, Smartphone } from 'lucide-react';

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
        const sorted = json.sort((a, b) => new Date(a.date) - new Date(b.date));
        setData(sorted);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load history", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="centered-msg">Loading...</div>;
  if (data.length === 0) return <div className="centered-msg">No data available</div>;

  const latest = data[data.length - 1];
  const previous = data.length > 1 ? data[data.length - 2] : null;

  const renderTrend = (current, prev, isInverse = false) => {
    if (prev === undefined || prev === null) return null;
    const diff = current - prev;
    const isUp = diff > 0;
    const isGood = isInverse ? !isUp : isUp;
    
    return (
      <span className={`metric-trend ${isGood ? 'trend-up' : 'trend-down'}`}>
        {isUp ? '↑' : '↓'} {Math.abs(diff).toFixed(1)}
      </span>
    );
  };

  return (
    <div className="dashboard-container">
      {/* Critical Bug Alert Banner */}
      {latest.critical_alert && (
        <div className="alert-banner">
          <AlertTriangle size={20} />
          <strong>CRITICAL ALERT:</strong> High volume of crash/bug reports detected this week ({latest.crash_rate}% of reviews).
        </div>
      )}

      <header className="dashboard-header">
        <div>
          <h1>Weekly Review Pulse</h1>
          <p>AI-driven sentiment analysis for week of <strong>{new Date(latest.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</strong></p>
        </div>
        <button className="btn-primary" onClick={() => alert("This triggers the GitHub Action pipeline!")}>
          <Sparkles size={18} />
          Generate Pulse
        </button>
      </header>

      {/* Metrics Grid */}
      <div className="metric-grid">
        {/* Rating & Split */}
        <div className="glass-panel metric-card">
          <span className="metric-title"><Star size={16} /> Avg Rating</span>
          <div className="metric-value">
            {latest.avg_rating}
            {renderTrend(latest.avg_rating, previous?.avg_rating)}
          </div>
          <div className="platform-split">
            <span title="App Store"><span className="icon-apple">🍏</span> {latest.app_store_rating || '-'}</span>
            <span title="Play Store"><span className="icon-android">🤖</span> {latest.play_store_rating || '-'}</span>
          </div>
        </div>
        
        {/* Sentiment */}
        <div className="glass-panel metric-card">
          <span className="metric-title"><TrendingUp size={16} /> Sentiment Score</span>
          <div className="metric-value">
            {latest.sentiment_score}%
            {renderTrend(latest.sentiment_score, previous?.sentiment_score)}
          </div>
        </div>

        {/* Top Theme */}
        <div className="glass-panel metric-card" style={{ gridColumn: 'span 2' }}>
          <span className="metric-title"><MessageSquare size={16} /> Top Theme</span>
          <div style={{ fontSize: '1.25rem', fontWeight: 600, marginTop: '0.5rem', color: 'var(--text-main)' }}>
            "{latest.top_theme}"
          </div>
        </div>
      </div>

      <div className="layout-split">
        {/* Chart Section */}
        <div className="glass-panel chart-section">
          <h2 className="section-title">Sentiment Trend (Week over Week)</h2>
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
                tickLine={false} axisLine={false}
                tickFormatter={(val) => new Date(val).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              />
              <YAxis stroke="var(--text-muted)" tick={{fill: 'var(--text-muted)', fontSize: 12}} tickLine={false} axisLine={false} domain={[0, 100]} />
              <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(255,255,255,0.1)', strokeWidth: 2 }} />
              <Area type="monotone" dataKey="sentiment_score" stroke="var(--accent-primary)" strokeWidth={3} fillOpacity={1} fill="url(#colorSentiment)" activeDot={{ r: 6, fill: "var(--accent-primary)", stroke: "var(--bg-dark)", strokeWidth: 2 }} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Feature Radar */}
        <div className="glass-panel radar-section">
          <h2 className="section-title"><Lightbulb size={18} style={{ display: 'inline', marginRight: '8px' }}/>Feature Radar</h2>
          <p className="radar-subtitle">Most requested by users this week</p>
          <ul className="radar-list">
            {(latest.feature_requests || []).map((feature, i) => (
              <li key={i}>
                <div className="radar-rank">{i + 1}</div>
                <div className="radar-text">{feature}</div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
