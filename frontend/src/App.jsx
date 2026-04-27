import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LayoutDashboard, Car, AlertCircle, Activity, Settings, LogOut, 
  Bell, Search, Clock, Zap, MoreHorizontal, ShieldAlert, CheckCircle2, 
  XCircle, TrendingUp, Video, ChevronRight, BarChart2, Info, History, Monitor 
} from 'lucide-react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts';

const API_BASE = "http://127.0.0.1:5000";

function App() {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState({ 
    total: 0, active: 0, alerts: 0, unknown: 0, 
    chart_data: [
      { name: '00:00', activity: 0 }, { name: '04:00', activity: 0 },
      { name: '08:00', activity: 0 }, { name: '12:00', activity: 0 },
      { name: '16:00', activity: 0 }, { name: '20:00', activity: 0 },
      { name: '24:00', activity: 0 },
    ]
  });
  const [camIndex, setCamIndex] = useState(0);

  const [lastAnnouncedPlate, setLastAnnouncedPlate] = useState("");

  const announcePlate = (log) => {
    if (log.plate_number === lastAnnouncedPlate) return;
    setLastAnnouncedPlate(log.plate_number);

    const last4 = log.plate_number.slice(-4).split('').join(' ');
    const msg = new SpeechSynthesisUtterance();
    msg.text = `Vehicle ${last4}. ${log.status}`;
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
  };

  const fetchData = async () => {
    try {
      const [logsRes, statsRes] = await Promise.all([
        axios.get(`${API_BASE}/logs`),
        axios.get(`${API_BASE}/stats`)
      ]);
      setLogs(logsRes.data);
      setStats(statsRes.data);
      
      // Announce the latest detection if it's new
      if (logsRes.data.length > 0) {
        announcePlate(logsRes.data[0]);
      }
    } catch (err) { console.error("API Error:", err); }
  };

  useEffect(() => {
    fetchData();
    const pollInterval = setInterval(fetchData, 5000); // Slower polling for stats

    // Real-time Event Listener for instant Audio
    const eventSource = new EventSource(`${API_BASE}/events`);
    eventSource.onmessage = (event) => {
      const newLog = JSON.parse(event.data);
      setLogs(prev => [newLog, ...prev.slice(0, 49)]);
      announcePlate(newLog); // Speak INSTANTLY
    };

    return () => {
      clearInterval(pollInterval);
      eventSource.close();
    };
  }, [lastAnnouncedPlate]);

  return (
    <div className="layout-wrapper">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <Zap size={24} className="text-red" fill="currentColor" />
          <span className="logo-text">SURVEIL<span className="logo-accent">AI</span></span>
        </div>
        
        <nav className="nav-section">
          <NavItem icon={<LayoutDashboard size={20}/>} label="Dashboard" active />
          <NavItem icon={<Car size={20}/>} label="Vehicles" />
          <NavItem icon={<AlertCircle size={20}/>} label="Alerts" />
          <NavItem icon={<Activity size={20}/>} label="Analytics" />
          <NavItem icon={<Settings size={20}/>} label="Settings" />
        </nav>

        <div className="sidebar-footer">
          <NavItem icon={<LogOut size={20}/>} label="Logout" />
          <div className="status-mini-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
              <ShieldAlert className="text-green" size={18} />
              <span style={{ fontSize: '12px', fontWeight: 800 }}>System Status</span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--accent-green)', fontWeight: 800 }}>All Systems Operational</p>
            <p style={{ fontSize: '9px', color: 'var(--text-dim)', textTransform: 'uppercase', marginTop: '4px' }}>Updated: 10:30:45 AM</p>
          </div>
        </div>
      </aside>

      {/* Main Container */}
      <div style={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden' }}>
        <header className="navbar">
          <div className="search-container">
            <Search size={18} style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-dim)' }} />
            <input type="text" placeholder="Search license plates, vehicles..." className="search-input" />
          </div>
          
          <div className="nav-actions">
            <div style={{ position: 'relative', cursor: 'pointer' }}>
              <Bell size={22} style={{ color: 'var(--text-muted)' }} />
              <span style={{ position: 'absolute', top: '-6px', right: '-6px', background: 'var(--accent-red)', color: 'white', fontSize: '10px', fontWeight: 900, width: '18px', height: '18px', display: 'flex', alignItems: 'center', justifyCenter: 'center', borderRadius: '50%', border: '2px solid var(--bg-page)' }}>2</span>
            </div>
            <div className="badge-live">
               <div className="dot-pulse" /> LIVE STREAM ACTIVE
            </div>
          </div>
        </header>

        <main className="main-content custom-scroll">
          <div className="page-header">
            <h1 className="page-title">Vehicle Monitoring Dashboard</h1>
            <p className="page-subtitle">Real-time Indian Number Plate Recognition System</p>
          </div>

          {/* Stats Grid */}
          <div className="stats-grid">
            <StatCard label="TOTAL VEHICLES" value={stats.total} icon={<Car size={22} />} colorClass="text-red" bgClass="bg-red-soft" />
            <StatCard label="ACTIVE (1H)" value={stats.active} icon={<Activity size={22} />} colorClass="text-green" bgClass="bg-green-soft" />
            <StatCard label="CRITICAL ALERTS" value={stats.alerts} icon={<AlertCircle size={22} />} colorClass="text-orange" bgClass="bg-orange-soft" />
            <StatCard label="UNKNOWN PLATES" value={stats.unknown} icon={<Info size={22} />} colorClass="text-blue" bgClass="bg-blue-soft" />
          </div>

          <div className="dashboard-grid">
            <div className="grid-left">
              {/* History Panel */}
              <div className="panel">
                <div className="panel-header">
                  <h2 className="panel-title"><History size={18} style={{ color: 'var(--text-dim)' }} /> Live Detection History</h2>
                  <button style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: '12px', padding: '8px 16px', fontSize: '10px', fontWeight: 900, color: 'white', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    View All <ChevronRight size={14} />
                  </button>
                </div>
                <div style={{ minHeight: '340px' }}>
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>PLATE NUMBER</th>
                        <th>STATUS</th>
                        <th>TYPE</th>
                        <th>TIMESTAMP</th>
                        <th>CONFIDENCE</th>
                      </tr>
                    </thead>
                    <tbody>
                      {logs.length > 0 ? logs.map((log, i) => (
                        <tr key={`${log.plate_number}-${log.timestamp}-${i}`}>
                          <td className="plate-cell">
                            {log.plate_number}
                            {log.found && (
                              <div style={{ fontSize: '9px', color: 'var(--accent-blue)', fontWeight: 800, marginTop: '4px', opacity: 0.8 }}>
                                OWNER: {log.owner_name}
                              </div>
                            )}
                          </td>
                          <td>
                            <span className={`status-badge ${
                              log.status_text === 'Allowed' ? 'bg-green-soft text-green' : 
                              log.status_text === 'Blacklisted' ? 'bg-red-soft text-red' : 
                              log.status_text === 'Unknown' ? 'bg-orange-soft text-orange' : 
                              'bg-dim-soft text-dim'
                            }`}>
                              {(log.status_text || 'Unknown').toUpperCase()}
                            </span>
                          </td>
                          <td style={{ color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>{log.type}</td>
                          <td style={{ color: 'var(--text-dim)', fontMono: 'true', fontWeight: 700 }}>{log.time_only}</td>
                          <td>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                               <div style={{ width: '80px', height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px', overflow: 'hidden' }}>
                                  <div style={{ width: `${log.confidence}%`, height: '100%', background: 'var(--accent-blue)' }} />
                               </div>
                               <span style={{ fontSize: '10px', fontWeight: 800, color: 'var(--text-dim)' }}>{log.confidence}%</span>
                            </div>
                          </td>
                        </tr>
                      )) : (
                        <tr>
                          <td colSpan="5" style={{ padding: '100px 0', textAlign: 'center', opacity: 0.4 }}>
                            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
                              <ShieldAlert size={48} className="text-dim" />
                              <div>
                                <p style={{ fontWeight: 900, fontSize: '16px', color: 'var(--text-primary)' }}>No Valid Detections Yet</p>
                                <p style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', marginTop: '4px', color: 'var(--text-dim)' }}>
                                  System is active and monitoring for valid Indian plates
                                </p>
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Chart Panel */}
              <div className="panel" style={{ padding: '32px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '32px' }}>
                  <h3 className="panel-title"><BarChart2 size={18} style={{ color: 'var(--text-dim)' }} /> Traffic Flow Analytics</h3>
                  <select style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: '10px', color: 'white', fontSize: '10px', fontWeight: 900, padding: '8px 16px' }}>
                    <option>Last 24 Hours</option>
                  </select>
                </div>
                <div style={{ height: '240px', position: 'relative' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={stats.chart_data}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.02)" vertical={false} />
                      <XAxis dataKey="name" stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
                      <YAxis stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
                      <Area type="monotone" dataKey="activity" stroke="var(--accent-blue)" fill="rgba(59, 130, 246, 0.05)" strokeWidth={3} />
                    </AreaChart>
                  </ResponsiveContainer>
                  {(!stats.chart_data || stats.chart_data.every(d => d.activity === 0)) && (
                     <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: 0.2 }}>
                        <BarChart2 size={40} style={{ marginBottom: '12px' }} />
                        <p style={{ fontSize: '14px', fontWeight: 900 }}>No traffic data available</p>
                     </div>
                  )}
                </div>
              </div>
            </div>

            <div className="grid-right">
              {/* System Status Panel */}
              <div className="panel" style={{ padding: '32px' }}>
                <h3 className="panel-title" style={{ marginBottom: '32px' }}><Monitor size={18} style={{ color: 'var(--text-dim)' }} /> System Status</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '2fr 3fr', gap: '24px', alignItems: 'center' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '10px', fontWeight: 800, color: 'var(--text-muted)' }}>CCTV Feed</span>
                      <button 
                        onClick={() => setCamIndex((prev) => (prev + 1) % 4)}
                        style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: '8px', padding: '4px 10px', fontSize: '9px', fontWeight: 900, color: 'white', cursor: 'pointer' }}
                      >
                        Switch (CAM {camIndex})
                      </button>
                    </div>
                    <div style={{ aspectRatio: '1/1', background: '#0c0c0e', borderRadius: '24px', border: '1px solid var(--border)', overflow: 'hidden', position: 'relative' }}>
                      <img 
                        src={`${API_BASE}/video_feed?index=${camIndex}`} 
                        alt="Stream" 
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
                        onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
                      />
                      <div style={{ display: 'none', position: 'absolute', inset: 0, flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'rgba(255,255,255,0.02)' }}>
                        <Video size={32} style={{ color: 'var(--text-dim)', marginBottom: '12px' }} />
                        <p style={{ fontSize: '9px', fontWeight: 900, color: 'var(--text-dim)', letterSpacing: '0.1em' }}>STREAM OFFLINE</p>
                      </div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    <StatusLine label="Camera Feed" />
                    <StatusLine label="AI Detection" />
                    <StatusLine label="Database" />
                    <StatusLine label="Notifications" />
                  </div>
                </div>
              </div>

              {/* Threat Level Panel */}
              <div className="panel" style={{ padding: '32px' }}>
                <h3 className="panel-title" style={{ marginBottom: '40px' }}><ShieldAlert size={18} style={{ color: 'var(--text-dim)' }} /> Threat Level</h3>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div className="gauge-container">
                    <svg viewBox="0 0 176 176" className="gauge-svg">
                      <circle cx="88" cy="88" r="75" className="gauge-bg" />
                      <circle cx="88" cy="88" r="75" className="gauge-fill" style={{ strokeDasharray: '470', strokeDashoffset: '350' }} />
                    </svg>
                    <div className="gauge-content">
                      <p style={{ fontSize: '24px', fontWeight: 900, color: 'var(--accent-green)', letterSpacing: '-0.05em' }}>LOW</p>
                      <p style={{ fontSize: '10px', fontWeight: 800, color: 'var(--text-dim)', textTransform: 'uppercase', marginTop: '2px' }}>Current Level</p>
                    </div>
                  </div>
                  <div style={{ width: '100%', marginTop: '48px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    <ThreatItem color="var(--accent-green)" label="LOW" desc="Normal traffic conditions" active />
                    <ThreatItem color="var(--accent-orange)" label="MEDIUM" desc="Increased monitoring" />
                    <ThreatItem color="var(--accent-red)" label="HIGH" desc="Critical attention required" />
                  </div>
                  <button style={{ width: '100%', marginTop: '32px', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border)', borderRadius: '16px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <ShieldAlert size={16} style={{ color: 'var(--text-dim)' }} />
                      <span style={{ fontSize: '10px', fontWeight: 900, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>View All Alerts</span>
                    </div>
                    <ChevronRight size={16} style={{ color: 'var(--text-dim)' }} />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

function StatCard({ label, value, icon, colorClass, bgClass }) {
  return (
    <div className="stat-card">
      <div className={`stat-icon-wrapper ${bgClass} ${colorClass}`}>
        {icon}
      </div>
      <p className="stat-label">{label}</p>
      <p className="stat-value">{value}</p>
      <div className="stat-trend">
        <TrendingUp size={12} /> 0% from last hour
      </div>
    </div>
  );
}

function StatusLine({ label }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--accent-green)' }} />
        <span style={{ fontSize: '10px', fontWeight: 800, color: 'var(--text-muted)' }}>{label}</span>
      </div>
      <span style={{ fontSize: '10px', fontWeight: 900, color: 'var(--accent-green)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Online</span>
    </div>
  );
}

function ThreatItem({ color, label, desc, active }) {
  return (
    <div style={{ display: 'flex', alignItems: 'start', gap: '20px', opacity: active ? 1 : 0.25, transition: 'opacity 0.3s' }}>
      <div style={{ width: '10px', height: '10px', borderRadius: '50%', marginTop: '6px', background: color }} />
      <div>
        <p style={{ fontSize: '11px', fontWeight: 900, letterSpacing: '-0.02em' }}>{label}</p>
        <p style={{ fontSize: '10px', fontWeight: 700, color: 'var(--text-dim)', marginTop: '2px' }}>{desc}</p>
      </div>
    </div>
  );
}

function NavItem({ icon, label, active }) {
  return (
    <div className={`nav-item ${active ? 'active' : ''}`}>
      <div className={active ? 'text-red' : ''}>{icon}</div>
      <span>{label}</span>
    </div>
  );
}

export default App;
