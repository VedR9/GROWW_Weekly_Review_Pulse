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

  const getCrashComparison = () => {
    if (!previous || typeof previous.crash_rate === 'undefined') return null;
    const diff = latest.crash_rate - previous.crash_rate;
    if (diff > 0) {
      return <span style={{ color: '#ef4444' }}>Up {diff.toFixed(1)}% from last week. Issues are NOT resolved.</span>;
    } else if (diff < 0) {
      return <span style={{ color: 'var(--accent-primary)' }}>Down {Math.abs(diff).toFixed(1)}% from last week. Bugs are being fixed! 🎉</span>;
    }
    return <span>Unchanged from last week.</span>;
  };

  return (
    <div className="dashboard-container">
      {/* Dynamic Crash/Health Banner */}
      <div className={`alert-banner ${latest.critical_alert ? 'critical' : 'healthy'}`} style={{
        background: latest.critical_alert ? 'rgba(239, 68, 68, 0.15)' : 'rgba(0, 208, 156, 0.1)',
        borderColor: latest.critical_alert ? 'rgba(239, 68, 68, 0.4)' : 'rgba(0, 208, 156, 0.3)',
        color: latest.critical_alert ? '#fca5a5' : 'var(--accent-primary)'
      }}>
        <AlertTriangle size={20} />
        <div>
          <strong>{latest.critical_alert ? 'CRITICAL ALERT:' : 'SYSTEM HEALTH:'}</strong> 
          {' '}Crash/Bug reports at {latest.crash_rate}%. 
          {' '}{getCrashComparison()}
        </div>
      </div>

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
        {/* Feature Radar */}
        <div className="glass-panel radar-section">
          <h2 className="section-title"><Lightbulb size={18} style={{ display: 'inline', marginRight: '8px' }}/>Feature Radar</h2>
          <p className="radar-subtitle">Most requested by users this week</p>
          <ul className="radar-list">
            {(latest.feature_requests || []).map((feature, i) => {
              const name = typeof feature === 'string' ? feature : feature.name;
              const pct = typeof feature === 'string' ? null : feature.percentage;
              
              return (
                <li key={i}>
                  <div className="radar-rank">{i + 1}</div>
                  <div style={{ flex: 1 }}>
                    <div className="radar-text">{name}</div>
                    {pct && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '6px' }}>
                        <div style={{ flex: 1, height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                          <div style={{ width: `${pct}%`, height: '100%', background: 'var(--accent-primary)' }} />
                        </div>
                        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{pct}%</span>
                      </div>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        </div>

        {/* Action Ideas */}
        <div className="glass-panel radar-section">
          <h2 className="section-title">🚀 Action Ideas</h2>
          <p className="radar-subtitle">Recommended by AI</p>
          <ul className="action-list" style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {(latest.action_ideas || []).map((idea, i) => {
              const parts = idea.replace(/\*\*/g, '').split(':');
              return (
                <li key={i} style={{ background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)' }}>
                  <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
                    <div style={{ width: '20px', height: '20px', borderRadius: '4px', border: '2px solid var(--accent-primary)', flexShrink: 0, marginTop: '2px' }}></div>
                    <div style={{ fontSize: '0.95rem', lineHeight: '1.5', color: 'var(--text-main)' }}>
                      {parts.length > 1 ? (
                        <>
                          <strong style={{ color: 'var(--accent-primary)' }}>{parts[0]}:</strong>
                          {parts.slice(1).join(':')}
                        </>
                      ) : (
                        idea.replace(/\*\*/g, '')
                      )}
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      </div>

      {/* Chart Section Full Width */}
      <div className="glass-panel chart-section" style={{ height: '400px', marginBottom: '1.5rem' }}>
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
    </div>
  );
}

export default App;
