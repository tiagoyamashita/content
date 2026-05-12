---
label: "memory-estimator"
group: "System Design"
order: 99
---
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>System Design Canvas</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Syne:wght@400;500;600;700;800&display=swap');

  :root {
    --bg: #0a0b0e;
    --surface: #111318;
    --surface2: #181c24;
    --surface3: #1e2330;
    --border: #2a3040;
    --border2: #3a4455;
    --text: #e8eaf0;
    --text-muted: #6b7590;
    --text-dim: #3d4560;
    --accent: #4f8ef7;
    --accent2: #7c3aed;
    --green: #22d37a;
    --amber: #f59e0b;
    --red: #f04255;
    --cyan: #22d4e8;
    --panel-w: 220px;
    --node-font: 'JetBrains Mono', monospace;
    --ui-font: 'Syne', sans-serif;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: var(--ui-font);
    background: var(--bg);
    color: var(--text);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    user-select: none;
  }

  /* ─── TOP BAR ─── */
  .topbar {
    height: 48px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 20px;
    flex-shrink: 0;
    z-index: 100;
  }
  .topbar-logo {
    font-family: var(--node-font);
    font-size: 13px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .topbar-logo::before {
    content: '';
    width: 8px; height: 8px;
    background: var(--accent);
    border-radius: 2px;
    display: inline-block;
  }
  .topbar-sep { width: 1px; height: 24px; background: var(--border); }
  .topbar-hint {
    font-size: 11px;
    color: var(--text-muted);
    font-family: var(--node-font);
  }
  .topbar-actions { margin-left: auto; display: flex; gap: 8px; }
  .btn {
    font-family: var(--node-font);
    font-size: 11px;
    padding: 5px 12px;
    border-radius: 5px;
    border: 1px solid var(--border2);
    background: var(--surface2);
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.15s;
  }
  .btn:hover { background: var(--surface3); color: var(--text); border-color: var(--accent); }
  .btn-danger:hover { border-color: var(--red); color: var(--red); }
  .btn-primary {
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
    font-weight: 600;
  }
  .btn-primary:hover { background: #3a7de8; }

  /* ─── LAYOUT ─── */
  .workspace {
    display: flex;
    flex: 1;
    overflow: hidden;
  }

  /* ─── SIDEBAR ─── */
  .sidebar {
    width: var(--panel-w);
    background: var(--surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    flex-shrink: 0;
  }
  .sidebar::-webkit-scrollbar { width: 4px; }
  .sidebar::-webkit-scrollbar-track { background: transparent; }
  .sidebar::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

  .sidebar-section { padding: 12px 10px 4px; }
  .sidebar-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim);
    padding: 0 4px 8px;
    font-family: var(--node-font);
  }
  .node-list { display: flex; flex-direction: column; gap: 4px; }

  .node-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 7px;
    border: 1px solid transparent;
    cursor: grab;
    transition: all 0.12s;
    font-size: 12px;
    font-family: var(--node-font);
    font-weight: 500;
  }
  .node-item:hover {
    background: var(--surface2);
    border-color: var(--border);
  }
  .node-item:active { cursor: grabbing; opacity: 0.7; }

  .node-icon {
    width: 32px; height: 32px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    border: 1px solid transparent;
  }
  .node-item-info { display: flex; flex-direction: column; }
  .node-item-name { font-size: 11px; font-weight: 600; color: var(--text); }
  .node-item-sub  { font-size: 9px; color: var(--text-muted); margin-top: 1px; }

  /* ─── CANVAS ─── */
  .canvas-wrap {
    flex: 1;
    position: relative;
    overflow: hidden;
    background-color: var(--bg);
    background-image:
      linear-gradient(var(--border) 1px, transparent 1px),
      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 32px 32px;
    background-position: -1px -1px;
  }

  #canvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
  }

  /* SVG connection layer */
  #svg-layer {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: visible;
  }
  #svg-layer path, #svg-layer line {
    pointer-events: stroke;
    cursor: pointer;
  }

  /* ─── NODES ─── */
  .node {
    position: absolute;
    min-width: 140px;
    border-radius: 10px;
    border: 1.5px solid var(--border2);
    background: var(--surface2);
    cursor: move;
    transition: box-shadow 0.15s, border-color 0.15s;
    font-family: var(--node-font);
  }
  .node:hover, .node.selected {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(79,142,247,0.15), 0 8px 32px rgba(0,0,0,0.5);
    z-index: 10;
  }
  .node.selected { box-shadow: 0 0 0 3px rgba(79,142,247,0.25), 0 12px 40px rgba(0,0,0,0.6); }

  .node-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 12px 8px;
    border-bottom: 1px solid var(--border);
  }
  .node-header-icon {
    width: 26px; height: 26px;
    border-radius: 5px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
  }
  .node-title {
    font-size: 11px;
    font-weight: 600;
    color: var(--text);
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .node-delete {
    width: 18px; height: 18px;
    border-radius: 4px;
    border: none;
    background: transparent;
    color: var(--text-dim);
    cursor: pointer;
    font-size: 12px;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.12s;
    opacity: 0;
  }
  .node:hover .node-delete { opacity: 1; }
  .node-delete:hover { background: var(--red); color: #fff; }

  .node-body {
    padding: 8px 12px 10px;
  }
  .node-tag {
    font-size: 9px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 4px;
  }
  .node-label {
    font-size: 10px;
    color: var(--text-muted);
    line-height: 1.4;
  }
  .node-port-row {
    display: flex;
    justify-content: space-between;
    padding: 0 0 6px;
    gap: 4px;
  }
  .node-stat {
    font-size: 9px;
    padding: 2px 6px;
    border-radius: 3px;
    background: var(--surface3);
    color: var(--text-muted);
    border: 1px solid var(--border);
    white-space: nowrap;
  }

  /* Connection ports (dots on edges) */
  .port {
    position: absolute;
    width: 12px; height: 12px;
    border-radius: 50%;
    background: var(--surface2);
    border: 2px solid var(--border2);
    cursor: crosshair;
    transition: all 0.15s;
    z-index: 20;
  }
  .port:hover, .port.active {
    background: var(--accent);
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(79,142,247,0.3);
    transform: scale(1.3);
  }
  .port-top    { top: -6px;    left: 50%; transform: translateX(-50%); }
  .port-bottom { bottom: -6px; left: 50%; transform: translateX(-50%); }
  .port-left   { left: -6px;  top: 50%; transform: translateY(-50%); }
  .port-right  { right: -6px; top: 50%; transform: translateY(-50%); }
  .port-top:hover    { transform: translateX(-50%) scale(1.3); }
  .port-bottom:hover { transform: translateX(-50%) scale(1.3); }
  .port-left:hover   { transform: translateY(-50%) scale(1.3); }
  .port-right:hover  { transform: translateY(-50%) scale(1.3); }

  /* ─── CONNECTIONS ─── */
  .conn-path {
    fill: none;
    stroke: var(--border2);
    stroke-width: 1.5;
    transition: stroke 0.15s;
  }
  .conn-path:hover { stroke: var(--accent); stroke-width: 2; }
  .conn-path.selected-conn { stroke: var(--accent); stroke-width: 2; }
  .conn-arrow { fill: var(--border2); }
  .conn-path:hover + .conn-arrow,
  .conn-path.selected-conn + .conn-arrow { fill: var(--accent); }

  /* temp line while dragging */
  #temp-line { stroke: var(--accent); stroke-width: 1.5; stroke-dasharray: 6 4; fill: none; }

  /* ─── STATUS BAR ─── */
  .statusbar {
    height: 24px;
    background: var(--surface);
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 16px;
    font-family: var(--node-font);
    font-size: 10px;
    color: var(--text-muted);
    flex-shrink: 0;
  }
  .status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--green);
    display: inline-block;
    margin-right: 4px;
  }
  .statusbar-right { margin-left: auto; }

  /* ─── EMPTY STATE ─── */
  .empty-hint {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    pointer-events: none;
    opacity: 0.35;
  }
  .empty-hint-icon { font-size: 40px; }
  .empty-hint-text {
    font-size: 13px;
    font-family: var(--node-font);
    color: var(--text-muted);
    text-align: center;
    line-height: 1.6;
  }

  /* Node color themes */
  .theme-blue   .node-header-icon, .theme-blue   .node-icon { background: rgba(79,142,247,0.15); border-color: rgba(79,142,247,0.3); }
  .theme-green  .node-header-icon, .theme-green  .node-icon { background: rgba(34,211,122,0.12); border-color: rgba(34,211,122,0.3); }
  .theme-red    .node-header-icon, .theme-red    .node-icon { background: rgba(240,66,85,0.12);  border-color: rgba(240,66,85,0.3); }
  .theme-amber  .node-header-icon, .theme-amber  .node-icon { background: rgba(245,158,11,0.12); border-color: rgba(245,158,11,0.3); }
  .theme-purple .node-header-icon, .theme-purple .node-icon { background: rgba(124,58,237,0.12); border-color: rgba(124,58,237,0.3); }
  .theme-cyan   .node-header-icon, .theme-cyan   .node-icon { background: rgba(34,212,232,0.12); border-color: rgba(34,212,232,0.3); }

  .theme-blue   .node.selected { border-color: var(--accent); }
  .theme-green  .node { border-color: rgba(34,211,122,0.25); }
  .theme-green  .node.selected { border-color: var(--green); box-shadow: 0 0 0 3px rgba(34,211,122,0.15), 0 12px 40px rgba(0,0,0,0.6); }
  .theme-red    .node { border-color: rgba(240,66,85,0.25); }
  .theme-red    .node.selected { border-color: var(--red); box-shadow: 0 0 0 3px rgba(240,66,85,0.15), 0 12px 40px rgba(0,0,0,0.6); }
  .theme-amber  .node { border-color: rgba(245,158,11,0.25); }
  .theme-amber  .node.selected { border-color: var(--amber); box-shadow: 0 0 0 3px rgba(245,158,11,0.15), 0 12px 40px rgba(0,0,0,0.6); }
  .theme-purple .node { border-color: rgba(124,58,237,0.25); }
  .theme-purple .node.selected { border-color: var(--accent2); box-shadow: 0 0 0 3px rgba(124,58,237,0.15), 0 12px 40px rgba(0,0,0,0.6); }
  .theme-cyan   .node { border-color: rgba(34,212,232,0.25); }
  .theme-cyan   .node.selected { border-color: var(--cyan); box-shadow: 0 0 0 3px rgba(34,212,232,0.15), 0 12px 40px rgba(0,0,0,0.6); }
</style>
</head>
<body>

<!-- TOP BAR -->
<div class="topbar">
  <div class="topbar-logo">sysdesign.canvas</div>
  <div class="topbar-sep"></div>
  <span class="topbar-hint">drag from panel · click ports to connect · del to remove selected</span>
  <div class="topbar-actions">
    <button class="btn btn-danger" onclick="clearAll()">Clear</button>
    <button class="btn" onclick="exportSVG()">Export SVG</button>
    <button class="btn btn-primary" onclick="autoLayout()">Auto Layout</button>
  </div>
</div>

<!-- WORKSPACE -->
<div class="workspace">

  <!-- SIDEBAR -->
  <div class="sidebar">

    <div class="sidebar-section">
      <div class="sidebar-label">Networking</div>
      <div class="node-list">
        <div class="node-item theme-amber" draggable="true" data-type="loadbalancer">
          <div class="node-icon">⚖️</div>
          <div class="node-item-info">
            <span class="node-item-name">Load Balancer</span>
            <span class="node-item-sub">L4 / L7 routing</span>
          </div>
        </div>
        <div class="node-item theme-blue" draggable="true" data-type="api-gateway">
          <div class="node-icon">🚦</div>
          <div class="node-item-info">
            <span class="node-item-name">API Gateway</span>
            <span class="node-item-sub">rate limit · auth</span>
          </div>
        </div>
        <div class="node-item theme-cyan" draggable="true" data-type="cdn">
          <div class="node-icon">🌐</div>
          <div class="node-item-info">
            <span class="node-item-name">CDN</span>
            <span class="node-item-sub">edge caching</span>
          </div>
        </div>
        <div class="node-item theme-blue" draggable="true" data-type="dns">
          <div class="node-icon">🗺️</div>
          <div class="node-item-info">
            <span class="node-item-name">DNS</span>
            <span class="node-item-sub">name resolution</span>
          </div>
        </div>
        <div class="node-item theme-blue" draggable="true" data-type="firewall">
          <div class="node-icon">🛡️</div>
          <div class="node-item-info">
            <span class="node-item-name">Firewall</span>
            <span class="node-item-sub">WAF · ACL</span>
          </div>
        </div>
      </div>
    </div>

    <div class="sidebar-section">
      <div class="sidebar-label">Compute</div>
      <div class="node-list">
        <div class="node-item theme-blue" draggable="true" data-type="app-server">
          <div class="node-icon">🖥️</div>
          <div class="node-item-info">
            <span class="node-item-name">App Server</span>
            <span class="node-item-sub">HTTP · REST</span>
          </div>
        </div>
        <div class="node-item theme-blue" draggable="true" data-type="microservice">
          <div class="node-icon">⚙️</div>
          <div class="node-item-info">
            <span class="node-item-name">Microservice</span>
            <span class="node-item-sub">gRPC · REST</span>
          </div>
        </div>
        <div class="node-item theme-purple" draggable="true" data-type="lambda">
          <div class="node-icon">λ</div>
          <div class="node-item-info">
            <span class="node-item-name">Lambda / FaaS</span>
            <span class="node-item-sub">serverless fn</span>
          </div>
        </div>
        <div class="node-item theme-blue" draggable="true" data-type="worker">
          <div class="node-icon">🔧</div>
          <div class="node-item-info">
            <span class="node-item-name">Worker</span>
            <span class="node-item-sub">background jobs</span>
          </div>
        </div>
        <div class="node-item theme-cyan" draggable="true" data-type="container">
          <div class="node-icon">📦</div>
          <div class="node-item-info">
            <span class="node-item-name">Container</span>
            <span class="node-item-sub">Docker · K8s pod</span>
          </div>
        </div>
      </div>
    </div>

    <div class="sidebar-section">
      <div class="sidebar-label">Data</div>
      <div class="node-list">
        <div class="node-item theme-green" draggable="true" data-type="database">
          <div class="node-icon">🗄️</div>
          <div class="node-item-info">
            <span class="node-item-name">SQL Database</span>
            <span class="node-item-sub">Postgres · MySQL</span>
          </div>
        </div>
        <div class="node-item theme-green" draggable="true" data-type="nosql">
          <div class="node-icon">🍃</div>
          <div class="node-item-info">
            <span class="node-item-name">NoSQL DB</span>
            <span class="node-item-sub">Mongo · DynamoDB</span>
          </div>
        </div>
        <div class="node-item theme-red" draggable="true" data-type="redis">
          <div class="node-icon">⚡</div>
          <div class="node-item-info">
            <span class="node-item-name">Redis</span>
            <span class="node-item-sub">cache · session</span>
          </div>
        </div>
        <div class="node-item theme-amber" draggable="true" data-type="queue">
          <div class="node-icon">📨</div>
          <div class="node-item-info">
            <span class="node-item-name">Message Queue</span>
            <span class="node-item-sub">Kafka · RabbitMQ</span>
          </div>
        </div>
        <div class="node-item theme-purple" draggable="true" data-type="search">
          <div class="node-icon">🔍</div>
          <div class="node-item-info">
            <span class="node-item-name">Search Engine</span>
            <span class="node-item-sub">Elasticsearch</span>
          </div>
        </div>
        <div class="node-item theme-green" draggable="true" data-type="blob">
          <div class="node-icon">🪣</div>
          <div class="node-item-info">
            <span class="node-item-name">Object Storage</span>
            <span class="node-item-sub">S3 · GCS · Blob</span>
          </div>
        </div>
      </div>
    </div>

    <div class="sidebar-section">
      <div class="sidebar-label">Infra / Observability</div>
      <div class="node-list">
        <div class="node-item theme-cyan" draggable="true" data-type="monitoring">
          <div class="node-icon">📊</div>
          <div class="node-item-info">
            <span class="node-item-name">Monitoring</span>
            <span class="node-item-sub">Prometheus · DD</span>
          </div>
        </div>
        <div class="node-item theme-amber" draggable="true" data-type="logging">
          <div class="node-icon">📋</div>
          <div class="node-item-info">
            <span class="node-item-name">Log Aggregator</span>
            <span class="node-item-sub">ELK · Loki</span>
          </div>
        </div>
        <div class="node-item theme-purple" draggable="true" data-type="auth">
          <div class="node-icon">🔐</div>
          <div class="node-item-info">
            <span class="node-item-name">Auth Service</span>
            <span class="node-item-sub">OAuth · JWT</span>
          </div>
        </div>
        <div class="node-item theme-blue" draggable="true" data-type="client">
          <div class="node-icon">💻</div>
          <div class="node-item-info">
            <span class="node-item-name">Client</span>
            <span class="node-item-sub">browser · mobile</span>
          </div>
        </div>
      </div>
    </div>

    <div style="height: 16px;"></div>
  </div>

  <!-- CANVAS -->
  <div class="canvas-wrap" id="canvas-wrap">
    <div class="empty-hint" id="empty-hint">
      <div class="empty-hint-icon">⬡</div>
      <div class="empty-hint-text">drag components from the left panel<br>click the ● ports to draw connections</div>
    </div>
    <svg id="svg-layer">
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="var(--border2)" />
        </marker>
        <marker id="arrow-selected" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="var(--accent)" />
        </marker>
      </defs>
      <path id="temp-line" style="display:none" />
    </svg>
    <div id="canvas"></div>
  </div>

</div>

<!-- STATUS BAR -->
<div class="statusbar">
  <span><span class="status-dot"></span>canvas ready</span>
  <span id="status-nodes">0 nodes</span>
  <span id="status-conns">0 connections</span>
  <span class="statusbar-right" id="status-mode">select mode</span>
</div>

<script>
// ── NODE DEFINITIONS ──────────────────────────────────────────────
const NODE_DEFS = {
  'loadbalancer': { label: 'Load Balancer', icon: '⚖️', theme: 'amber', tag: 'networking', stats: ['Round Robin', 'L7'] },
  'api-gateway':  { label: 'API Gateway',   icon: '🚦', theme: 'blue',  tag: 'networking', stats: ['REST', 'Rate Limit'] },
  'cdn':          { label: 'CDN',           icon: '🌐', theme: 'cyan',  tag: 'networking', stats: ['Edge', 'Cache'] },
  'dns':          { label: 'DNS',           icon: '🗺️', theme: 'blue',  tag: 'networking', stats: ['A', 'CNAME'] },
  'firewall':     { label: 'Firewall',      icon: '🛡️', theme: 'blue',  tag: 'security',   stats: ['WAF', 'ACL'] },
  'app-server':   { label: 'App Server',    icon: '🖥️', theme: 'blue',  tag: 'compute',    stats: ['HTTP/2', ':8080'] },
  'microservice': { label: 'Microservice',  icon: '⚙️', theme: 'blue',  tag: 'compute',    stats: ['gRPC', 'REST'] },
  'lambda':       { label: 'Lambda',        icon: 'λ',  theme: 'purple',tag: 'compute',    stats: ['FaaS', 'Event'] },
  'worker':       { label: 'Worker',        icon: '🔧', theme: 'blue',  tag: 'compute',    stats: ['Queue', 'Async'] },
  'container':    { label: 'Container',     icon: '📦', theme: 'cyan',  tag: 'compute',    stats: ['Docker', 'K8s'] },
  'database':     { label: 'SQL Database',  icon: '🗄️', theme: 'green', tag: 'data',       stats: ['ACID', ':5432'] },
  'nosql':        { label: 'NoSQL DB',      icon: '🍃', theme: 'green', tag: 'data',       stats: ['Document', 'CAP'] },
  'redis':        { label: 'Redis',         icon: '⚡', theme: 'red',   tag: 'cache',      stats: ['In-mem', ':6379'] },
  'queue':        { label: 'Message Queue', icon: '📨', theme: 'amber', tag: 'messaging',  stats: ['Async', 'FIFO'] },
  'search':       { label: 'Elasticsearch', icon: '🔍', theme: 'purple',tag: 'data',       stats: ['Full-text', ':9200'] },
  'blob':         { label: 'Object Storage',icon: '🪣', theme: 'green', tag: 'storage',    stats: ['S3', 'Immutable'] },
  'monitoring':   { label: 'Monitoring',    icon: '📊', theme: 'cyan',  tag: 'observability', stats: ['Metrics', 'Alerts'] },
  'logging':      { label: 'Log Aggregator',icon: '📋', theme: 'amber', tag: 'observability', stats: ['ELK', 'Loki'] },
  'auth':         { label: 'Auth Service',  icon: '🔐', theme: 'purple',tag: 'security',   stats: ['OAuth2', 'JWT'] },
  'client':       { label: 'Client',        icon: '💻', theme: 'blue',  tag: 'client',     stats: ['Browser', 'Mobile'] },
};

// ── STATE ─────────────────────────────────────────────────────────
let nodes = [];
let connections = [];
let nodeIdCounter = 0;
let connIdCounter = 0;
let selectedNode = null;
let selectedConn = null;
let draggingNode = null;
let dragOffX = 0, dragOffY = 0;
let connectingFrom = null; // { nodeId, port }
let tempLineActive = false;

const canvas = document.getElementById('canvas');
const canvasWrap = document.getElementById('canvas-wrap');
const svgLayer = document.getElementById('svg-layer');
const tempLine = document.getElementById('temp-line');
const emptyHint = document.getElementById('empty-hint');

// ── STATUS ────────────────────────────────────────────────────────
function updateStatus() {
  document.getElementById('status-nodes').textContent = `${nodes.length} node${nodes.length !== 1 ? 's' : ''}`;
  document.getElementById('status-conns').textContent = `${connections.length} connection${connections.length !== 1 ? 's' : ''}`;
  emptyHint.style.display = nodes.length === 0 ? 'flex' : 'none';
}

// ── NODE CREATION ─────────────────────────────────────────────────
function createNode(type, x, y) {
  const def = NODE_DEFS[type];
  if (!def) return;
  const id = `node-${++nodeIdCounter}`;
  const nodeData = { id, type, x, y, label: def.label };
  nodes.push(nodeData);

  const el = document.createElement('div');
  el.className = `node theme-${def.theme}`;
  el.id = id;
  el.style.left = x + 'px';
  el.style.top  = y + 'px';
  el.innerHTML = `
    <div class="node-header">
      <div class="node-header-icon">${def.icon}</div>
      <span class="node-title" contenteditable="true" spellcheck="false">${def.label}</span>
      <button class="node-delete" title="Delete" onclick="deleteNode('${id}')">✕</button>
    </div>
    <div class="node-body">
      <div class="node-tag">${def.tag}</div>
      <div class="node-port-row">
        ${def.stats.map(s => `<span class="node-stat">${s}</span>`).join('')}
      </div>
    </div>
    <div class="port port-top"    data-node="${id}" data-side="top"></div>
    <div class="port port-bottom" data-node="${id}" data-side="bottom"></div>
    <div class="port port-left"   data-node="${id}" data-side="left"></div>
    <div class="port port-right"  data-node="${id}" data-side="right"></div>
  `;

  // node drag
  el.addEventListener('mousedown', onNodeMouseDown);
  // stop contenteditable from triggering drag
  el.querySelector('.node-title').addEventListener('mousedown', e => e.stopPropagation());

  // port interactions
  el.querySelectorAll('.port').forEach(p => {
    p.addEventListener('mousedown', onPortMouseDown);
  });

  canvas.appendChild(el);
  updateStatus();
  selectNode(id);
  redrawConnections();
  return nodeData;
}

// ── NODE SELECTION ────────────────────────────────────────────────
function selectNode(id) {
  if (selectedNode) {
    const prev = document.getElementById(selectedNode);
    if (prev) prev.classList.remove('selected');
  }
  selectedNode = id;
  if (id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('selected');
  }
  clearConnSelection();
}

function clearConnSelection() {
  if (selectedConn !== null) {
    const path = document.getElementById(`conn-path-${selectedConn}`);
    if (path) path.classList.remove('selected-conn');
    selectedConn = null;
  }
}

// ── NODE DRAG ─────────────────────────────────────────────────────
function onNodeMouseDown(e) {
  if (e.target.classList.contains('port') || e.target.classList.contains('node-delete')) return;
  e.preventDefault();
  const el = e.currentTarget;
  selectNode(el.id);
  draggingNode = el.id;
  const rect = el.getBoundingClientRect();
  const wrapRect = canvasWrap.getBoundingClientRect();
  dragOffX = e.clientX - rect.left;
  dragOffY = e.clientY - rect.top;
  el.style.zIndex = 50;
}

document.addEventListener('mousemove', e => {
  if (draggingNode) {
    const wrapRect = canvasWrap.getBoundingClientRect();
    const el = document.getElementById(draggingNode);
    const x = e.clientX - wrapRect.left - dragOffX;
    const y = e.clientY - wrapRect.top  - dragOffY;
    el.style.left = Math.max(0, x) + 'px';
    el.style.top  = Math.max(0, y) + 'px';
    const nd = nodes.find(n => n.id === draggingNode);
    if (nd) { nd.x = Math.max(0, x); nd.y = Math.max(0, y); }
    redrawConnections();
  }
  if (tempLineActive) {
    const wrapRect = canvasWrap.getBoundingClientRect();
    const mx = e.clientX - wrapRect.left;
    const my = e.clientY - wrapRect.top;
    const [sx, sy] = getTempStart();
    const d = bezierPath(sx, sy, mx, my);
    tempLine.setAttribute('d', d);
  }
});

document.addEventListener('mouseup', e => {
  if (draggingNode) {
    const el = document.getElementById(draggingNode);
    if (el) el.style.zIndex = '';
    draggingNode = null;
  }
  if (tempLineActive) {
    tempLine.style.display = 'none';
    tempLineActive = false;
    connectingFrom = null;
    document.getElementById('status-mode').textContent = 'select mode';
  }
});

// ── PORT / CONNECTION ─────────────────────────────────────────────
let tempStartX = 0, tempStartY = 0;
function getTempStart() { return [tempStartX, tempStartY]; }

function getPortCenter(nodeId, side) {
  const el = document.getElementById(nodeId);
  const port = el.querySelector(`.port-${side}`);
  const wrapRect = canvasWrap.getBoundingClientRect();
  const r = port.getBoundingClientRect();
  return [r.left - wrapRect.left + r.width/2, r.top - wrapRect.top + r.height/2];
}

function onPortMouseDown(e) {
  e.preventDefault();
  e.stopPropagation();
  const nodeId = e.currentTarget.dataset.node;
  const side   = e.currentTarget.dataset.side;
  connectingFrom = { nodeId, side };
  const [sx, sy] = getPortCenter(nodeId, side);
  tempStartX = sx; tempStartY = sy;
  tempLine.style.display = 'block';
  tempLine.setAttribute('d', `M${sx},${sy} C${sx},${sy} ${sx},${sy} ${sx},${sy}`);
  tempLineActive = true;
  document.getElementById('status-mode').textContent = '🔗 connecting — click another port';
}

function onPortMouseUp(e) {
  if (!connectingFrom) return;
  e.preventDefault();
  e.stopPropagation();
  const toNodeId = e.currentTarget.dataset.node;
  const toSide   = e.currentTarget.dataset.side;
  if (toNodeId === connectingFrom.nodeId) return; // same node
  // check duplicate
  const dup = connections.find(c =>
    (c.fromNode === connectingFrom.nodeId && c.fromSide === connectingFrom.side && c.toNode === toNodeId && c.toSide === toSide) ||
    (c.fromNode === toNodeId && c.fromSide === toSide && c.toNode === connectingFrom.nodeId && c.toSide === connectingFrom.side)
  );
  if (!dup) {
    connections.push({ id: ++connIdCounter, fromNode: connectingFrom.nodeId, fromSide: connectingFrom.side, toNode: toNodeId, toSide });
    redrawConnections();
    updateStatus();
  }
  tempLine.style.display = 'none';
  tempLineActive = false;
  connectingFrom = null;
  document.getElementById('status-mode').textContent = 'select mode';
}

// Attach port mouseup after canvas is built (event delegation)
svgLayer.addEventListener('mouseup', () => {
  if (tempLineActive) {
    tempLine.style.display = 'none';
    tempLineActive = false;
    connectingFrom = null;
    document.getElementById('status-mode').textContent = 'select mode';
  }
});

// ── BEZIER HELPER ─────────────────────────────────────────────────
function bezierPath(x1, y1, x2, y2) {
  const dx = Math.abs(x2 - x1) * 0.55 + 30;
  const dy = Math.abs(y2 - y1) * 0.55 + 30;
  return `M${x1},${y1} C${x1 + (x2>x1?dx:-dx)},${y1} ${x2 - (x2>x1?dx:-dx)},${y2} ${x2},${y2}`;
}

// ── DRAW CONNECTIONS ──────────────────────────────────────────────
function redrawConnections() {
  // Remove old paths
  svgLayer.querySelectorAll('.conn-g').forEach(g => g.remove());

  connections.forEach(conn => {
    const fromEl = document.getElementById(conn.fromNode);
    const toEl   = document.getElementById(conn.toNode);
    if (!fromEl || !toEl) return;
    const [x1, y1] = getPortCenter(conn.fromNode, conn.fromSide);
    const [x2, y2] = getPortCenter(conn.toNode,   conn.toSide);
    const d = bezierPath(x1, y1, x2, y2);

    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.classList.add('conn-g');
    g.setAttribute('data-conn', conn.id);

    // Invisible wider hit area
    const hit = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    hit.setAttribute('d', d);
    hit.setAttribute('fill', 'none');
    hit.setAttribute('stroke', 'transparent');
    hit.setAttribute('stroke-width', '12');
    hit.style.cursor = 'pointer';
    hit.addEventListener('click', () => selectConn(conn.id));

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', d);
    path.classList.add('conn-path');
    path.id = `conn-path-${conn.id}`;
    path.setAttribute('marker-end', conn.id === selectedConn ? 'url(#arrow-selected)' : 'url(#arrow)');
    if (conn.id === selectedConn) path.classList.add('selected-conn');
    path.addEventListener('click', () => selectConn(conn.id));

    g.appendChild(hit);
    g.appendChild(path);
    svgLayer.insertBefore(g, tempLine);
  });
}

function selectConn(id) {
  clearConnSelection();
  selectedNode && selectNode(null);
  selectedConn = id;
  const path = document.getElementById(`conn-path-${id}`);
  if (path) {
    path.classList.add('selected-conn');
    path.setAttribute('marker-end', 'url(#arrow-selected)');
  }
}

// ── DRAG FROM SIDEBAR ─────────────────────────────────────────────
document.querySelectorAll('.node-item[draggable]').forEach(item => {
  item.addEventListener('dragstart', e => {
    e.dataTransfer.setData('text/plain', item.dataset.type);
    e.dataTransfer.effectAllowed = 'copy';
  });
});

canvasWrap.addEventListener('dragover', e => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'copy';
});

canvasWrap.addEventListener('drop', e => {
  e.preventDefault();
  const type = e.dataTransfer.getData('text/plain');
  if (!type) return;
  const wrapRect = canvasWrap.getBoundingClientRect();
  const x = e.clientX - wrapRect.left - 70;
  const y = e.clientY - wrapRect.top  - 40;
  createNode(type, Math.max(8, x), Math.max(8, y));
});

// Port mouseup delegation on canvas
canvas.addEventListener('mouseup', e => {
  if (!connectingFrom) return;
  const port = e.target.closest('.port');
  if (port) onPortMouseUp({ ...e, currentTarget: port, preventDefault: () => {}, stopPropagation: () => {} });
});

// Actually wire the proper event
canvas.addEventListener('mouseup', e => {
  if (!connectingFrom) return;
  const port = e.target;
  if (port.classList.contains('port')) {
    const fakeE = { currentTarget: port, preventDefault: ()=>{}, stopPropagation: ()=>{} };
    onPortMouseUp(fakeE);
  }
}, true);

// ── DELETE KEY ────────────────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.target.contentEditable === 'true') return;
  if (e.key === 'Delete' || e.key === 'Backspace') {
    if (selectedConn !== null) {
      connections = connections.filter(c => c.id !== selectedConn);
      selectedConn = null;
      redrawConnections();
      updateStatus();
    } else if (selectedNode) {
      deleteNode(selectedNode);
    }
  }
  if (e.key === 'Escape') { selectNode(null); clearConnSelection(); }
});

// ── CANVAS CLICK (deselect) ────────────────────────────────────────
canvasWrap.addEventListener('mousedown', e => {
  if (e.target === canvasWrap || e.target === canvas || e.target === svgLayer) {
    selectNode(null);
    clearConnSelection();
  }
});

// ── DELETE NODE ────────────────────────────────────────────────────
function deleteNode(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
  nodes = nodes.filter(n => n.id !== id);
  connections = connections.filter(c => c.fromNode !== id && c.toNode !== id);
  if (selectedNode === id) selectedNode = null;
  redrawConnections();
  updateStatus();
}

// ── CLEAR ALL ─────────────────────────────────────────────────────
function clearAll() {
  if (nodes.length === 0) return;
  if (!confirm('Clear the entire canvas?')) return;
  canvas.innerHTML = '';
  nodes = []; connections = [];
  selectedNode = null; selectedConn = null;
  svgLayer.querySelectorAll('.conn-g').forEach(g => g.remove());
  updateStatus();
}

// ── AUTO LAYOUT ───────────────────────────────────────────────────
function autoLayout() {
  if (nodes.length === 0) return;
  const cols = Math.ceil(Math.sqrt(nodes.length));
  const padX = 60, padY = 60, spacX = 200, spacY = 140;
  nodes.forEach((nd, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    nd.x = padX + col * spacX;
    nd.y = padY + row * spacY;
    const el = document.getElementById(nd.id);
    if (el) { el.style.left = nd.x + 'px'; el.style.top = nd.y + 'px'; }
  });
  redrawConnections();
}

// ── EXPORT SVG ────────────────────────────────────────────────────
function exportSVG() {
  if (nodes.length === 0) { alert('Add some nodes first!'); return; }
  const wrapRect = canvasWrap.getBoundingClientRect();
  const svgClone = svgLayer.cloneNode(true);
  svgClone.querySelector('#temp-line')?.remove();

  // Embed node labels as text
  let nodeTexts = '';
  nodes.forEach(nd => {
    const el = document.getElementById(nd.id);
    const def = NODE_DEFS[nd.type];
    const title = el.querySelector('.node-title').textContent;
    nodeTexts += `
    <rect x="${nd.x}" y="${nd.y}" width="150" height="70" rx="10" fill="#181c24" stroke="#3a4455" stroke-width="1.5"/>
    <text x="${nd.x+18}" y="${nd.y+26}" font-family="monospace" font-size="14">${def.icon}</text>
    <text x="${nd.x+38}" y="${nd.y+26}" font-family="monospace" font-size="11" font-weight="600" fill="#e8eaf0">${title}</text>
    <text x="${nd.x+12}" y="${nd.y+46}" font-family="monospace" font-size="9" fill="#6b7590">${def.tag} · ${def.stats.join(' · ')}</text>`;
  });

  const fullSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="${wrapRect.width}" height="${wrapRect.height}" style="background:#0a0b0e">
  <defs>${svgClone.querySelector('defs').innerHTML}</defs>
  ${svgClone.innerHTML}
  ${nodeTexts}
</svg>`;
  const blob = new Blob([fullSVG], { type: 'image/svg+xml' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'system-design.svg';
  a.click();
}

// ── INIT ──────────────────────────────────────────────────────────
updateStatus();
</script>
</body>
</html>