<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Sales Dashboard 2024</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  :root {
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #21253a;
    --accent: #4f8ef7;
    --accent2: #34c98e;
    --accent3: #f7894f;
    --accent4: #e05c6f;
    --text: #e8eaf0;
    --text-muted: #8b90a7;
    --border: #2e3350;
    --radius: 14px;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; min-height:100vh; }
  
  /* HEADER */
  .header {
    background: linear-gradient(135deg, #1a1d27 0%, #21253a 100%);
    border-bottom: 1px solid var(--border);
    padding: 20px 32px;
    display: flex; align-items:center; justify-content:space-between;
  }
  .header h1 { font-size:1.5rem; font-weight:700; }
  .header h1 span { color:var(--accent); }
  .header-meta { color:var(--text-muted); font-size:0.85rem; text-align:right; }
  .ai-badge {
    background:linear-gradient(90deg,#4f8ef7,#34c98e);
    color:#fff; border-radius:20px; padding:4px 14px; font-size:0.78rem; font-weight:600;
    display:inline-block; margin-top:4px;
  }

  /* NAV TABS */
  .tabs {
    display:flex; gap:4px; padding:16px 32px 0;
    background:var(--surface); border-bottom:1px solid var(--border);
  }
  .tab {
    padding:10px 20px; border-radius:10px 10px 0 0; cursor:pointer;
    font-size:0.88rem; font-weight:500; color:var(--text-muted);
    border:1px solid transparent; border-bottom:none;
    transition: all 0.2s;
  }
  .tab:hover { color:var(--text); background:var(--surface2); }
  .tab.active { color:var(--accent); background:var(--bg); border-color:var(--border); }

  /* MAIN */
  .main { padding:28px 32px; max-width:1600px; margin:0 auto; }
  .page { display:none; }
  .page.active { display:block; }

  /* KPI GRID */
  .kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; margin-bottom:28px; }
  .kpi-card {
    background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
    padding:20px 22px; position:relative; overflow:hidden;
  }
  .kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
  }
  .kpi-card.blue::before { background:linear-gradient(90deg,#4f8ef7,#7eb8ff); }
  .kpi-card.green::before { background:linear-gradient(90deg,#34c98e,#5ee8b0); }
  .kpi-card.orange::before { background:linear-gradient(90deg,#f7894f,#ffb07a); }
  .kpi-card.red::before { background:linear-gradient(90deg,#e05c6f,#ff8a9a); }
  .kpi-label { font-size:0.78rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px; }
  .kpi-value { font-size:1.75rem; font-weight:700; line-height:1; }
  .kpi-sub { font-size:0.8rem; color:var(--text-muted); margin-top:6px; }

  /* CHART GRID */
  .chart-grid { display:grid; gap:20px; }
  .chart-grid.cols2 { grid-template-columns:1fr 1fr; }
  .chart-grid.cols3 { grid-template-columns:1fr 1fr 1fr; }
  .chart-grid.cols12 { grid-template-columns:1.5fr 1fr; }
  .chart-card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:var(--radius); padding:22px;
  }
  .chart-card h3 { font-size:0.92rem; font-weight:600; color:var(--text-muted); margin-bottom:16px; text-transform:uppercase; letter-spacing:0.05em; }
  .chart-wrap { position:relative; }
  
  /* ANOMALIES */
  .anomaly-grid { display:grid; gap:14px; }
  .anomaly-card {
    border-radius:var(--radius); padding:16px 20px;
    border-left:4px solid;
  }
  .anom-high { background:#2a1520; border-color:#e05c6f; }
  .anom-warn { background:#252010; border-color:#f7894f; }
  .anom-info { background:#102030; border-color:#4f8ef7; }
  .anom-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
  .anom-type { font-weight:600; font-size:0.9rem; }
  .anom-severity { font-size:0.75rem; font-weight:700; padding:2px 10px; border-radius:20px; }
  .anom-high .anom-severity { background:#e05c6f22; color:#e05c6f; }
  .anom-warn .anom-severity { background:#f7894f22; color:#f7894f; }
  .anom-info .anom-severity { background:#4f8ef722; color:#4f8ef7; }
  .anom-detail { font-size:0.85rem; color:var(--text-muted); line-height:1.5; }

  /* TABLE */
  .data-table { width:100%; border-collapse:collapse; font-size:0.87rem; }
  .data-table th { background:var(--surface2); color:var(--text-muted); padding:10px 14px; text-align:left; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.05em; }
  .data-table td { padding:10px 14px; border-top:1px solid var(--border); }
  .data-table tr:hover td { background:var(--surface2); }
  .rank-badge { display:inline-block; width:22px; height:22px; border-radius:50%; text-align:center; line-height:22px; font-size:0.75rem; font-weight:700; }
  .rank1 { background:#f7d547; color:#000; }
  .rank2 { background:#adb5bd; color:#000; }
  .rank3 { background:#c8894f; color:#fff; }
  .rankn { background:var(--surface2); color:var(--text-muted); }
  
  .section-title {
    font-size:1.1rem; font-weight:700; margin-bottom:20px;
    padding-bottom:10px; border-bottom:1px solid var(--border);
    color:var(--text);
  }
  .mb20 { margin-bottom:20px; }
  
  @media(max-width:900px) {
    .chart-grid.cols2, .chart-grid.cols3, .chart-grid.cols12 { grid-template-columns:1fr; }
    .main { padding:16px; }
    .tabs { padding:12px 16px 0; overflow-x:auto; }
  }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>🤖 <span>AI</span> Sales Intelligence Dashboard</h1>
    <div style="color:var(--text-muted);font-size:0.85rem;margin-top:4px;">Full Year 2024 · Multi-Region Analysis</div>
  </div>
  <div class="header-meta">
    <div>Powered by Claude AI</div>
    <div class="ai-badge">✦ AI-Powered Insights</div>
  </div>
</div>

<div class="tabs">
  <div class="tab active" onclick="showPage('overview')">📊 Overview</div>
  <div class="tab" onclick="showPage('trends')">📈 Trends</div>
  <div class="tab" onclick="showPage('regions')">🌍 Regions</div>
  <div class="tab" onclick="showPage('products')">📦 Products</div>
  <div class="tab" onclick="showPage('team')">👥 Sales Team</div>
  <div class="tab" onclick="showPage('anomalies')">⚠️ Anomalies</div>
</div>

<div class="main">

<!-- ══════ OVERVIEW ══════ -->
<div class="page active" id="page-overview">
  <div class="kpi-grid">
    <div class="kpi-card blue">
      <div class="kpi-label">Total Revenue</div>
      <div class="kpi-value">$21.80M</div>
      <div class="kpi-sub">Full Year 2024</div>
    </div>
    <div class="kpi-card green">
      <div class="kpi-label">Total Profit</div>
      <div class="kpi-value">$11.25M</div>
      <div class="kpi-sub">Avg Margin: 61.3%</div>
    </div>
    <div class="kpi-card orange">
      <div class="kpi-label">Total Orders</div>
      <div class="kpi-value">2,000</div>
      <div class="kpi-sub">Completion Rate: 87.1%</div>
    </div>
    <div class="kpi-card blue">
      <div class="kpi-label">Avg Order Value</div>
      <div class="kpi-value">$12,519</div>
      <div class="kpi-sub">Units Sold: 3,997</div>
    </div>
    <div class="kpi-card green">
      <div class="kpi-label">Top Region</div>
      <div class="kpi-value" style="font-size:1.2rem">MENA</div>
      <div class="kpi-sub">Highest Revenue</div>
    </div>
    <div class="kpi-card orange">
      <div class="kpi-label">Top Category</div>
      <div class="kpi-value" style="font-size:1.2rem">Services</div>
      <div class="kpi-sub">Best Performer</div>
    </div>
    <div class="kpi-card red">
      <div class="kpi-label">Total Discounts</div>
      <div class="kpi-value">$1,005,774</div>
      <div class="kpi-sub">Value Given Away</div>
    </div>
    <div class="kpi-card blue">
      <div class="kpi-label">Anomalies Flagged</div>
      <div class="kpi-value">4</div>
      <div class="kpi-sub">AI-Detected Issues</div>
    </div>
  </div>

  <div class="chart-grid cols2 mb20">
    <div class="chart-card">
      <h3>Revenue by Quarter</h3>
      <div class="chart-wrap"><canvas id="quarterChart" height="200"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Revenue by Channel</h3>
      <div class="chart-wrap"><canvas id="channelChart" height="200"></canvas></div>
    </div>
  </div>

  <div class="chart-grid cols12">
    <div class="chart-card">
      <h3>Monthly Revenue Overview</h3>
      <div class="chart-wrap"><canvas id="overviewMonthly" height="180"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Region Revenue Share</h3>
      <div class="chart-wrap"><canvas id="regionPieOverview" height="180"></canvas></div>
    </div>
  </div>
</div>

<!-- ══════ TRENDS ══════ -->
<div class="page" id="page-trends">
  <div class="section-title">📈 Monthly Revenue & Profit Trends</div>
  <div class="chart-grid mb20">
    <div class="chart-card">
      <h3>Revenue vs Profit — Monthly</h3>
      <div class="chart-wrap"><canvas id="monthlyRevProfit" height="160"></canvas></div>
    </div>
  </div>
  <div class="chart-grid cols2">
    <div class="chart-card">
      <h3>Month-over-Month Growth (%)</h3>
      <div class="chart-wrap"><canvas id="momChart" height="220"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Average Profit Margin by Month</h3>
      <div class="chart-wrap"><canvas id="marginChart" height="220"></canvas></div>
    </div>
  </div>
</div>

<!-- ══════ REGIONS ══════ -->
<div class="page" id="page-regions">
  <div class="section-title">🌍 Regional Performance Analysis</div>
  <div class="chart-grid cols2 mb20">
    <div class="chart-card">
      <h3>Revenue by Region</h3>
      <div class="chart-wrap"><canvas id="regionBarChart" height="260"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Revenue Share Distribution</h3>
      <div class="chart-wrap"><canvas id="regionDoughnut" height="260"></canvas></div>
    </div>
  </div>
  <div class="chart-card">
    <h3>Region Revenue vs Profit Comparison</h3>
    <div class="chart-wrap"><canvas id="regionCompare" height="140"></canvas></div>
  </div>
</div>

<!-- ══════ PRODUCTS ══════ -->
<div class="page" id="page-products">
  <div class="section-title">📦 Product & Category Analysis</div>
  <div class="chart-grid cols2 mb20">
    <div class="chart-card">
      <h3>Revenue by Category</h3>
      <div class="chart-wrap"><canvas id="catRevChart" height="260"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Average Profit Margin by Category (%)</h3>
      <div class="chart-wrap"><canvas id="catMarginChart" height="260"></canvas></div>
    </div>
  </div>
</div>

<!-- ══════ TEAM ══════ -->
<div class="page" id="page-team">
  <div class="section-title">👥 Sales Team Leaderboard</div>
  <div class="chart-grid cols12 mb20">
    <div class="chart-card">
      <h3>Revenue by Sales Rep</h3>
      <div class="chart-wrap"><canvas id="repChart" height="280"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Leaderboard</h3>
      <table class="data-table">
        <thead><tr><th>#</th><th>Rep</th><th>Revenue</th><th>Orders</th></tr></thead>
        <tbody>
          <tr>
            <td><span class="rank-badge rank1">1</span></td>
            <td>Sarah Johnson</td>
            <td>$2,627,784</td>
            <td>188</td>
          </tr><tr>
            <td><span class="rank-badge rank2">2</span></td>
            <td>Fatima Al-Zahrani</td>
            <td>$2,582,216</td>
            <td>173</td>
          </tr><tr>
            <td><span class="rank-badge rank3">3</span></td>
            <td>Ahmed Al-Rashidi</td>
            <td>$2,565,827</td>
            <td>189</td>
          </tr><tr>
            <td><span class="rank-badge rankn">4</span></td>
            <td>Carlos Mendez</td>
            <td>$2,349,372</td>
            <td>160</td>
          </tr><tr>
            <td><span class="rank-badge rankn">5</span></td>
            <td>Mohammed Al-Otaibi</td>
            <td>$2,224,661</td>
            <td>173</td>
          </tr><tr>
            <td><span class="rank-badge rankn">6</span></td>
            <td>Lucas Müller</td>
            <td>$2,196,877</td>
            <td>172</td>
          </tr><tr>
            <td><span class="rank-badge rankn">7</span></td>
            <td>Emma Thompson</td>
            <td>$1,848,821</td>
            <td>165</td>
          </tr><tr>
            <td><span class="rank-badge rankn">8</span></td>
            <td>Noor Al-Hamdan</td>
            <td>$1,820,059</td>
            <td>181</td>
          </tr><tr>
            <td><span class="rank-badge rankn">9</span></td>
            <td>Priya Sharma</td>
            <td>$1,793,875</td>
            <td>178</td>
          </tr><tr>
            <td><span class="rank-badge rankn">10</span></td>
            <td>Chen Wei</td>
            <td>$1,786,077</td>
            <td>162</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<!-- ══════ ANOMALIES ══════ -->
<div class="page" id="page-anomalies">
  <div class="section-title">⚠️ AI-Detected Anomalies & Flags</div>
  <div class="kpi-grid mb20">
    <div class="kpi-card red"><div class="kpi-label">High Severity</div>
      <div class="kpi-value">2</div></div>
    <div class="kpi-card orange"><div class="kpi-label">Warnings</div>
      <div class="kpi-value">1</div></div>
    <div class="kpi-card blue"><div class="kpi-label">Info</div>
      <div class="kpi-value">1</div></div>
    <div class="kpi-card green"><div class="kpi-label">Total Flags</div>
      <div class="kpi-value">4</div></div>
  </div>
  <div class="anomaly-grid">
    
        <div class="anomaly-card anom-warn">
            <div class="anom-header">
                <span class="anom-type">Revenue Drop</span>
                <span class="anom-severity">Warning</span>
            </div>
            <div class="anom-detail">February: Revenue dropped -33.8% MoM ($1,042,511)</div>
        </div>
        <div class="anomaly-card anom-high">
            <div class="anom-header">
                <span class="anom-type">Revenue Spike</span>
                <span class="anom-severity">High</span>
            </div>
            <div class="anom-detail">March: Revenue jumped +53.5% MoM ($1,600,548)</div>
        </div>
        <div class="anomaly-card anom-high">
            <div class="anom-header">
                <span class="anom-type">Revenue Spike</span>
                <span class="anom-severity">High</span>
            </div>
            <div class="anom-detail">December: Revenue jumped +31.5% MoM ($2,720,885)</div>
        </div>
        <div class="anomaly-card anom-info">
            <div class="anom-header">
                <span class="anom-type">High Discount Usage</span>
                <span class="anom-severity">Info</span>
            </div>
            <div class="anom-detail">174 orders had ≥15% discount ($408,481 total discount value)</div>
        </div>
  </div>
</div>

</div><!-- /main -->

<script>
// ── DATA ──────────────────────────────────────────
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const revData = [1574942.0, 1042511.0, 1600548.0, 1362207.0, 1534530.0, 1839599.0, 1818197.0, 2038905.0, 2078401.0, 2115076.0, 2069766.0, 2720885.0];
const profitData = [821521.0, 542881.0, 772054.0, 734029.0, 777986.0, 952538.0, 967065.0, 1029732.0, 1037485.0, 1063557.0, 1106875.0, 1443205.0];
const marginData = [52.2, 52.1, 48.2, 53.9, 50.7, 51.8, 53.2, 50.5, 49.9, 50.3, 53.5, 53.0];
const momData = [0, -33.8, 53.5, -14.9, 12.7, 19.9, -1.2, 12.1, 1.9, 1.8, -2.1, 31.5];
const regionLabels = ["MENA", "Americas", "Europe", "Asia"];
const regionRev = [5812361.0, 5524759.0, 5456320.0, 5002128.0];
const regionProfit = [3048828.0, 2832550.0, 2772238.0, 2595314.0];
const catLabels = ["Services", "Hardware", "Software", "Subscriptions"];
const catRev = [9231172.0, 8748590.0, 2773538.0, 1042268.0];
const catMargin = [55.2, 37.9, 72.1, 79.9];
const repNames = ["Sarah Johnson", "Fatima Al-Zahrani", "Ahmed Al-Rashidi", "Carlos Mendez", "Mohammed Al-Otaibi", "Lucas M\u00fcller", "Emma Thompson", "Noor Al-Hamdan", "Priya Sharma", "Chen Wei"];
const repRev = [2627784.0, 2582216.0, 2565827.0, 2349372.0, 2224661.0, 2196877.0, 1848821.0, 1820059.0, 1793875.0, 1786077.0];
const chLabels = ["Direct Sales", "Online Platform", "Cold Outreach", "Inbound Lead", "Partner Network"];
const chRev = [5277270.0, 4624138.0, 4075001.0, 3975124.0, 3844035.0];
const qLabels = ["Q1", "Q2", "Q3", "Q4"];
const qRev = [4218002.0, 4736335.0, 5935503.0, 6905728.0];
const qProfit = [2136456.0, 2464554.0, 3034282.0, 3613638.0];

const COLORS = ['#4f8ef7','#34c98e','#f7894f','#e05c6f','#a78bfa','#fbbf24','#22d3ee','#f472b6'];
const SURFACE = '#21253a';

Chart.defaults.color = '#8b90a7';
Chart.defaults.borderColor = '#2e3350';
Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";

function mkChart(id, config) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  return new Chart(ctx.getContext('2d'), config);
}

// Overview — Quarter
mkChart('quarterChart', {type:'bar', data:{
  labels: qLabels,
  datasets:[
    {label:'Revenue',data:qRev,backgroundColor:'#4f8ef7aa',borderColor:'#4f8ef7',borderWidth:2,borderRadius:6},
    {label:'Profit',data:qProfit,backgroundColor:'#34c98eaa',borderColor:'#34c98e',borderWidth:2,borderRadius:6}
  ]
}, options:{responsive:true, plugins:{legend:{position:'top'}}, scales:{y:{ticks:{callback:v=>'$'+v.toLocaleString()}}}}
});

// Overview — Channel donut
mkChart('channelChart', {type:'doughnut', data:{
  labels:chLabels, datasets:[{data:chRev,backgroundColor:COLORS,borderWidth:0}]
}, options:{responsive:true, plugins:{legend:{position:'right'},tooltip:{callbacks:{label:ctx=>ctx.label+': $'+ctx.raw.toLocaleString()}}}}
});

// Overview — Monthly bar
mkChart('overviewMonthly', {type:'bar', data:{
  labels:months,
  datasets:[{label:'Revenue',data:revData,backgroundColor:'#4f8ef7aa',borderColor:'#4f8ef7',borderWidth:2,borderRadius:4}]
}, options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>'$'+v.toLocaleString()}}}}
});

// Overview — Region pie
mkChart('regionPieOverview', {type:'pie', data:{
  labels:regionLabels, datasets:[{data:regionRev,backgroundColor:COLORS,borderWidth:0}]
}, options:{responsive:true,plugins:{legend:{position:'right'},tooltip:{callbacks:{label:ctx=>ctx.label+': $'+ctx.raw.toLocaleString()}}}}
});

// Trends — Monthly line
mkChart('monthlyRevProfit', {type:'line', data:{
  labels:months,
  datasets:[
    {label:'Revenue',data:revData,borderColor:'#4f8ef7',backgroundColor:'#4f8ef720',fill:true,tension:0.4,pointRadius:4},
    {label:'Profit',data:profitData,borderColor:'#34c98e',backgroundColor:'#34c98e20',fill:true,tension:0.4,pointRadius:4}
  ]
}, options:{responsive:true,plugins:{legend:{position:'top'}},scales:{y:{ticks:{callback:v=>'$'+v.toLocaleString()}}}}
});

// Trends — MoM
mkChart('momChart', {type:'bar', data:{
  labels:months,
  datasets:[{
    label:'MoM Growth %',data:momData,
    backgroundColor:momData.map(v=>v>=0?'#34c98eaa':'#e05c6faa'),
    borderColor:momData.map(v=>v>=0?'#34c98e':'#e05c6f'),
    borderWidth:2,borderRadius:4
  }]
}, options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>v+'%'}}}}
});

// Trends — Margin
mkChart('marginChart', {type:'line', data:{
  labels:months,
  datasets:[{label:'Margin %',data:marginData,borderColor:'#a78bfa',backgroundColor:'#a78bfa20',fill:true,tension:0.4,pointRadius:4}]
}, options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>v+'%'}}}}
});

// Regions
mkChart('regionBarChart', {type:'bar', data:{
  labels:regionLabels,
  datasets:[{label:'Revenue',data:regionRev,backgroundColor:COLORS.map(c=>c+'aa'),borderColor:COLORS,borderWidth:2,borderRadius:6}]
}, options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>'$'+v.toLocaleString()}}}}
});
mkChart('regionDoughnut', {type:'doughnut', data:{
  labels:regionLabels, datasets:[{data:regionRev,backgroundColor:COLORS,borderWidth:0}]
}, options:{responsive:true,plugins:{legend:{position:'bottom'},tooltip:{callbacks:{label:ctx=>ctx.label+': $'+ctx.raw.toLocaleString()}}}}
});
mkChart('regionCompare', {type:'bar', data:{
  labels:regionLabels,
  datasets:[
    {label:'Revenue',data:regionRev,backgroundColor:'#4f8ef7aa',borderColor:'#4f8ef7',borderWidth:2,borderRadius:4},
    {label:'Profit',data:regionProfit,backgroundColor:'#34c98eaa',borderColor:'#34c98e',borderWidth:2,borderRadius:4}
  ]
}, options:{responsive:true,plugins:{legend:{position:'top'}},scales:{y:{ticks:{callback:v=>'$'+v.toLocaleString()}}}}
});

// Products
mkChart('catRevChart', {type:'bar', data:{
  labels:catLabels,
  datasets:[{label:'Revenue',data:catRev,backgroundColor:COLORS.map(c=>c+'bb'),borderColor:COLORS,borderWidth:2,borderRadius:6}]
}, options:{responsive:true,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{callback:v=>'$'+v.toLocaleString()}}}}
});
mkChart('catMarginChart', {type:'bar', data:{
  labels:catLabels,
  datasets:[{label:'Avg Margin %',data:catMargin,backgroundColor:'#a78bfaaa',borderColor:'#a78bfa',borderWidth:2,borderRadius:6}]
}, options:{responsive:true,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{callback:v=>v+'%'}}}}
});

// Team
mkChart('repChart', {type:'bar', data:{
  labels:repNames,
  datasets:[{label:'Revenue',data:repRev,backgroundColor:COLORS.map((c,i)=>i===0?'#f7d54799':c+'99'),borderColor:COLORS.map((c,i)=>i===0?'#f7d547':c),borderWidth:2,borderRadius:6}]
}, options:{responsive:true,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{callback:v=>'$'+v.toLocaleString()}}}}
});

// ── TABS ──────────────────────────────────────────
function showPage(name) {
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('page-'+name).classList.add('active');
  event.target.classList.add('active');
}
</script>
</body>
</html>