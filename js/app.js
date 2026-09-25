let apiList = [
    { id: 1, name: 'JSONPlaceholder Users', url: 'https://jsonplaceholder.typicode.com/users', method: 'GET', category: 'Public API', calls: '23.4k', trend: '+8%', trendType: 'up', avatarColor: '#f59e0b', avatarIcon: 'fa-user', created_at: '2026-09-20 10:30:00', lastStatus: 'Healthy' },
    { id: 2, name: 'GitHub API Gateway', url: 'https://api.github.com', method: 'GET', category: 'Core Service', calls: '18.2k', trend: '+5%', trendType: 'up', avatarColor: '#e11d48', avatarIcon: 'fa-code-branch', created_at: '2026-09-21 14:15:00', lastStatus: 'Healthy' },
    { id: 3, name: 'ReqRes Users & Auth', url: 'https://reqres.in/api/users', method: 'GET', category: 'Auth Service', calls: '9.6k', trend: '-4%', trendType: 'down', avatarColor: '#8b5cf6', avatarIcon: 'fa-shield-alt', created_at: '2026-09-22 09:00:00', lastStatus: 'Slow' },
    { id: 4, name: 'HTTPBin Ingestion Post', url: 'https://httpbin.org/post', method: 'POST', category: 'Ingestion', calls: '14.1k', trend: '+12%', trendType: 'up', avatarColor: '#0ea5e9', avatarIcon: 'fa-cloud-upload-alt', created_at: '2026-09-22 11:45:00', lastStatus: 'Healthy' },
    { id: 5, name: 'Legacy Billing Microservice', url: 'https://api.nonexistent-domain-xyz.com/data', method: 'GET', category: 'Payments', calls: '1.2k', trend: '-18%', trendType: 'down', avatarColor: '#f97316', avatarIcon: 'fa-exclamation-triangle', created_at: '2026-09-23 08:20:00', lastStatus: 'Failed' },
];
let monitorHistory = [
    { id: 1, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 142, status: 'Healthy', checked_at: '2026-09-25 09:30:00' },
    { id: 2, api_id: 2, api_name: 'GitHub API Gateway', status_code: 200, response_time: 289, status: 'Healthy', checked_at: '2026-09-25 09:30:05' },
    { id: 3, api_id: 3, api_name: 'ReqRes Users & Auth', status_code: 200, response_time: 823, status: 'Slow', checked_at: '2026-09-25 09:30:10' },
    { id: 4, api_id: 4, api_name: 'HTTPBin Ingestion Post', status_code: 200, response_time: 356, status: 'Healthy', checked_at: '2026-09-25 09:30:15' },
    { id: 5, api_id: 5, api_name: 'Legacy Billing Microservice', status_code: 0, response_time: 0, status: 'Failed', checked_at: '2026-09-25 09:30:20' },
    { id: 6, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 178, status: 'Healthy', checked_at: '2026-09-25 08:00:00' },
    { id: 7, api_id: 2, api_name: 'GitHub API Gateway', status_code: 200, response_time: 312, status: 'Healthy', checked_at: '2026-09-25 08:00:05' },
    { id: 8, api_id: 3, api_name: 'ReqRes Users & Auth', status_code: 200, response_time: 1540, status: 'Slow', checked_at: '2026-09-25 08:00:10' },
    { id: 9, api_id: 4, api_name: 'HTTPBin Ingestion Post', status_code: 200, response_time: 410, status: 'Healthy', checked_at: '2026-09-25 08:00:15' },
    { id: 10, api_id: 5, api_name: 'Legacy Billing Microservice', status_code: 0, response_time: 0, status: 'Failed', checked_at: '2026-09-25 08:00:20' },
];
let nextApiId = 6, nextHistoryId = 11, currentTab = 'activity', searchQuery = '', pendingDeleteId = null;
let charts = { wave: null, donut: null, weekly: null, resp: null, dough: null, bar: null };
const $ = (id) => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);
function navigateTo(page) {
    if (!page) return;
    $$('.sidebar-nav .nav-link').forEach(l => l.classList.toggle('active', l.dataset.page === page));
    $$('.page').forEach(p => p.classList.toggle('active', p.id === `page-${page}`));
    const titles = { dashboard: 'Analytics', apis: 'API Endpoints', monitor: 'Live Monitoring', history: 'Health History', analytics: 'Performance Analytics' };
    if ($('dynamic-page-title')) $('dynamic-page-title').textContent = titles[page] || 'Analytics';
    $('sidebar')?.classList.remove('open');
    $('sidebar-overlay')?.classList.remove('active');
    refreshPageData(page);
}
$$('.sidebar-nav .nav-link').forEach(link => {
    link.addEventListener('click', (e) => { if (link.dataset.page) { e.preventDefault(); navigateTo(link.dataset.page); } });
});
$('menu-toggle')?.addEventListener('click', () => { $('sidebar')?.classList.toggle('open'); $('sidebar-overlay')?.classList.toggle('active'); });
$('sidebar-overlay')?.addEventListener('click', () => { $('sidebar')?.classList.remove('open'); $('sidebar-overlay')?.classList.remove('active'); });
$('btn-quick-new-api')?.addEventListener('click', () => { navigateTo('apis'); setTimeout(() => $('api-name')?.focus(), 80); });
$('mobile-check-all')?.addEventListener('click', checkAllAPIs);
$('nav-btn-check-all')?.addEventListener('click', (e) => { e.preventDefault(); checkAllAPIs(); });
$('btn-fullscreen-toggle')?.addEventListener('click', () => { !document.fullscreenElement ? document.documentElement.requestFullscreen().catch(()=>{}) : document.exitFullscreen().catch(()=>{}); });
$('global-search-input')?.addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderActivityRows();
    renderAPITable();
});
$$('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        $$('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentTab = btn.dataset.tab;
        renderActivityRows();
    });
});
function setTheme(isDark) {
    document.body.classList.toggle('dark-mode', isDark);
    const icon = isDark ? 'fa-sun' : 'fa-moon', oldIcon = isDark ? 'fa-moon' : 'fa-sun';
    [$('theme-icon'), $('mobile-theme-icon')].forEach(el => el && (el.classList.remove(oldIcon), el.classList.add(icon)));
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    renderDashboardWaveChart();
    renderHealthDonutChart();
    renderWeeklyBarsChart();
    if (document.querySelector('.page.active')?.id === 'page-analytics') renderAnalyticsCharts();
}
$('theme-toggle')?.addEventListener('click', () => setTheme(!document.body.classList.contains('dark-mode')));
$('mobile-theme-toggle')?.addEventListener('click', () => setTheme(!document.body.classList.contains('dark-mode')));
if (localStorage.getItem('theme') === 'dark') setTheme(true);
function refreshPageData(page) {
    if (page === 'dashboard') {
        updateDashboardMetrics(); renderActivityRows();
        renderDashboardWaveChart(); renderHealthDonutChart(); renderWeeklyBarsChart();
    } else if (page === 'apis') {
        renderAPITable();
    } else if (page === 'monitor') {
        renderMonitorCards();
    } else if (page === 'history') {
        populateHistoryFilters(); renderHistoryTable();
    } else if (page === 'analytics') {
        populateAnalyticsFilters(); updateAnalyticsStats(); renderAnalyticsCharts();
    }
}
function updateDashboardMetrics() {
    const total = apiList.length;
    const healthy = apiList.filter(a => a.lastStatus === 'Healthy').length;
    const slow = apiList.filter(a => a.lastStatus === 'Slow').length;
    const failed = apiList.filter(a => a.lastStatus === 'Failed').length;
    const valid = monitorHistory.filter(h => h.status !== 'Failed' && h.response_time > 0);
    const avg = valid.length ? Math.round(valid.reduce((s, h) => s + h.response_time, 0) / valid.length) : 142;
    const uptime = monitorHistory.length ? ((monitorHistory.filter(h => h.status !== 'Failed').length / monitorHistory.length) * 100).toFixed(1) : '99.8';
    if ($('hero-total-number')) $('hero-total-number').textContent = `${(total * 4.6).toFixed(4)}K`;
    const hPct = total ? Math.round((healthy / total) * 100) : 80;
    const sPct = total ? Math.round((slow / total) * 100) : 15;
    const fPct = total ? Math.round((failed / total) * 100) : 5;
    $('hero-healthy-pct') && ($('hero-healthy-pct').textContent = `%${hPct}`);
    $('hero-slow-pct') && ($('hero-slow-pct').textContent = `%${sPct}`);
    $('hero-failed-pct') && ($('hero-failed-pct').textContent = `%${fPct}`);
    $('donut-uptime-number') && ($('donut-uptime-number').innerHTML = `${uptime}<small>%</small>`);
    $('legend-healthy-val') && ($('legend-healthy-val').textContent = `%${hPct}`);
    $('legend-slow-val') && ($('legend-slow-val').textContent = `%${sPct}`);
    $('legend-failed-val') && ($('legend-failed-val').textContent = `%${fPct}`);
    $('side-avg-latency') && ($('side-avg-latency').innerHTML = `${avg} <small>ms</small>`);
    $('side-uptime-pct') && ($('side-uptime-pct').innerHTML = `${uptime}<small>%</small>`);
    $('side-completed-count') && ($('side-completed-count').textContent = valid.length * 68 || 874);
    $('tab-endpoint-count') && ($('tab-endpoint-count').textContent = total);
    $('alert-counter-badge') && ($('alert-counter-badge').textContent = failed + slow || 6);
    if ($('latency-progress-fill')) $('latency-progress-fill').style.width = `${Math.min(100, Math.round((avg / 600) * 100))}%`;
    if ($('uptime-progress-fill')) $('uptime-progress-fill').style.width = `${uptime}%`;
}
function renderActivityRows() {
    const wrap = $('activity-rows-wrap');
    if (!wrap) return;
    let list = [];
    if (currentTab === 'activity') {
        list = monitorHistory.slice(0, 6).map(h => {
            const a = apiList.find(x => x.id === h.api_id) || apiList[0];
            return { ...a, metric: h.status === 'Failed' ? 'FAIL' : `${h.response_time}ms`, status: h.status, trendType: h.status === 'Failed' ? 'down' : 'up' };
        });
    } else if (currentTab === 'endpoints') {
        list = apiList.map(a => ({ ...a, metric: a.calls || '12k', status: a.lastStatus }));
    } else {
        list = monitorHistory.filter(h => h.status !== 'Healthy').slice(0, 5).map(h => {
            const a = apiList.find(x => x.id === h.api_id) || apiList[0];
            return { ...a, metric: `${h.response_time}ms`, status: h.status, trend: h.status === 'Failed' ? 'CRITICAL' : 'SLOW', trendType: 'down' };
        });
    }
    if (searchQuery) list = list.filter(r => r.name.toLowerCase().includes(searchQuery) || r.url.toLowerCase().includes(searchQuery));
    if (!list.length) return wrap.innerHTML = `<div class="empty-state" style="padding:24px"><i class="fas fa-search"></i><p>No records found</p></div>`;
    wrap.innerHTML = list.map(item => `
        <div class="activity-row-item">
            <div class="row-left">
                <div class="row-avatar" style="background:${item.avatarColor || '#f59e0b'}"><i class="fas ${item.avatarIcon || 'fa-server'}"></i></div>
                <div class="row-info">
                    <div class="row-title-wrap"><span class="row-title">${escapeHtml(item.name)}</span><a href="${escapeHtml(item.url)}" target="_blank" class="row-external-icon"><i class="fas fa-external-link-alt"></i></a></div>
                    <span class="row-subtitle">${item.method} · ${escapeHtml(item.url)}</span>
                </div>
            </div>
            <div class="row-category">${escapeHtml(item.category || 'REST API')}</div>
            <div class="row-metric-wrap"><div class="row-metric-icon"><i class="fas fa-tachometer-alt"></i></div><span class="row-metric-text">${item.metric}</span></div>
            <div class="row-trend-badge ${item.trendType === 'up' ? 'trend-up' : 'trend-down'}"><i class="fas fa-arrow-${item.trendType === 'up' ? 'up' : 'down'}"></i><span>${item.trend || '+5%'}</span></div>
            <button class="card-dots-btn" onclick="checkSingleAPI(${item.id})" title="Ping Now"><i class="fas fa-play" style="font-size:0.8rem;color:var(--healthy)"></i></button>
        </div>
    `).join('');
}
function renderDashboardWaveChart() {
    const c = $('hero-wave-canvas');
    if (!c) return;
    if (charts.wave) charts.wave.destroy();
    charts.wave = new Chart(c, {
        type: 'line',
        data: {
            labels: Array(13).fill(''),
            datasets: [
                { data: [15, 28, 22, 38, 26, 42, 30, 48, 36, 52, 40, 58, 48], borderColor: '#67e8f9', borderWidth: 2.2, tension: 0.45, pointRadius: 0 },
                { data: [35, 20, 38, 22, 44, 28, 50, 32, 44, 30, 48, 35, 52], borderColor: '#c084fc', borderWidth: 2.2, tension: 0.45, pointRadius: 0 },
                { data: [25, 42, 30, 48, 32, 54, 38, 42, 56, 44, 60, 48, 62], borderColor: '#ffffff', borderWidth: 2.4, tension: 0.45, pointRadius: 0 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { display: false } } }
    });
}
function renderHealthDonutChart() {
    const c = $('health-donut-canvas');
    if (!c) return;
    if (charts.donut) charts.donut.destroy();
    const h = apiList.filter(a => a.lastStatus === 'Healthy').length || 4;
    const s = apiList.filter(a => a.lastStatus === 'Slow').length || 1;
    const f = apiList.filter(a => a.lastStatus === 'Failed').length || 1;
    charts.donut = new Chart(c, {
        type: 'doughnut',
        data: { labels: ['Healthy', 'Slow', 'Failed'], datasets: [{ data: [h, s, f], backgroundColor: ['#ff5e62', '#f59e0b', document.body.classList.contains('dark-mode') ? '#fff' : '#0f121d'], borderWidth: 0, borderRadius: 8 }] },
        options: { responsive: true, maintainAspectRatio: false, cutout: '72%', plugins: { legend: { display: false } } }
    });
}
function renderWeeklyBarsChart() {
    const c = $('weekly-bars-canvas');
    if (!c) return;
    if (charts.weekly) charts.weekly.destroy();
    const isDark = document.body.classList.contains('dark-mode');
    const bColor = isDark ? 'rgba(255,255,255,0.12)' : '#e5dfd5';
    charts.weekly = new Chart(c, {
        data: {
            labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
            datasets: [
                { type: 'line', data: [120, 160, 130, 240, 150, 180, 210], borderColor: isDark ? '#fff' : '#0f121d', borderWidth: 2, tension: 0.45, pointRadius: [0, 0, 0, 5, 0, 0, 0], pointBackgroundColor: '#ff5e62', order: 1 },
                { type: 'bar', data: [140, 180, 150, 280, 170, 200, 230], backgroundColor: [bColor, bColor, bColor, '#ff5e62', bColor, bColor, bColor], borderRadius: 16, barThickness: 16, order: 2 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false }, ticks: { color: isDark ? '#7d849b' : '#9599b0' } }, y: { display: false } } }
    });
}
function checkSingleAPI(apiId) {
    const api = apiList.find(a => a.id === apiId);
    if (!api) return;
    showToast('info', 'Pinging Endpoint', `Checking ${api.name}...`);
    setTimeout(() => {
        let code = 200, time = Math.round(Math.random() * 550 + 50), st = 'Healthy';
        if (api.url.includes('nonexistent')) { code = 0; time = 0; st = 'Failed'; }
        else if (time >= 500) st = 'Slow';
        monitorHistory.unshift({ id: nextHistoryId++, api_id: api.id, api_name: api.name, status_code: code, response_time: time, status: st, checked_at: new Date().toISOString().slice(0, 19).replace('T', ' ') });
        api.lastStatus = st;
        showToast(st === 'Healthy' ? 'success' : (st === 'Slow' ? 'warning' : 'error'), `Status: ${st}`, `${api.name} responded in ${time}ms`);
        refreshPageData('dashboard'); renderAPITable(); renderMonitorCards();
    }, 450);
}
function checkAllAPIs() {
    if (!apiList.length) return showToast('info', 'Notice', 'No APIs registered.');
    showToast('info', 'Diagnostic Run', `Pinging ${apiList.length} APIs...`);
    apiList.forEach((api, idx) => setTimeout(() => checkSingleAPI(api.id), idx * 300));
}
$('btn-check-all-dashboard')?.addEventListener('click', checkAllAPIs);
$('btn-check-all-monitor')?.addEventListener('click', checkAllAPIs);
$('api-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = $('api-name').value.trim(), url = $('api-url').value.trim(), method = $('api-method').value;
    if (!name || !url) return showToast('error', 'Error', 'Name and URL are required.');
    const newApi = { id: nextApiId++, name, url, method, category: 'Custom API', calls: '1.0k', trend: '+1%', trendType: 'up', avatarColor: '#0ea5e9', avatarIcon: 'fa-cube', created_at: new Date().toISOString().slice(0, 10), lastStatus: 'Healthy' };
    apiList.push(newApi);
    $('api-name').value = ''; $('api-url').value = '';
    showToast('success', 'Added', `"${name}" registered.`);
    renderAPITable(); updateDashboardMetrics();
    setTimeout(() => checkSingleAPI(newApi.id), 250);
});
function renderAPITable() {
    const tbody = $('api-table-body'), count = $('api-count-badge');
    if (!tbody) return;
    if (count) count.textContent = `${apiList.length} APIs`;
    let list = searchQuery ? apiList.filter(a => a.name.toLowerCase().includes(searchQuery) || a.url.toLowerCase().includes(searchQuery)) : apiList;
    tbody.innerHTML = list.map((a, i) => `
        <tr><td><strong>0${i+1}</strong></td><td><strong>${escapeHtml(a.name)}</strong></td><td class="url-cell">${escapeHtml(a.url)}</td><td><span class="api-method-badge ${a.method}">${a.method}</span></td><td><span class="status-badge ${(a.lastStatus||'pending').toLowerCase()}">${a.lastStatus||'Pending'}</span></td><td>${a.created_at}</td>
        <td><div class="action-btns"><button class="action-btn check" onclick="checkSingleAPI(${a.id})"><i class="fas fa-play"></i></button><button class="action-btn delete" onclick="confirmDeleteAPI(${a.id})"><i class="fas fa-trash-alt"></i></button></div></td></tr>
    `).join('');
}
function confirmDeleteAPI(id) {
    pendingDeleteId = id;
    $('modal-message').textContent = `Remove "${apiList.find(a=>a.id===id)?.name}"?`;
    $('confirm-modal')?.classList.add('active');
}
$('modal-confirm')?.addEventListener('click', () => {
    if (pendingDeleteId !== null) {
        apiList = apiList.filter(a => a.id !== pendingDeleteId);
        monitorHistory = monitorHistory.filter(h => h.api_id !== pendingDeleteId);
        pendingDeleteId = null;
        renderAPITable(); updateDashboardMetrics(); renderActivityRows();
        showToast('success', 'Deleted', 'API removed.');
    }
    $('confirm-modal')?.classList.remove('active');
});
$('modal-cancel')?.addEventListener('click', () => $('confirm-modal')?.classList.remove('active'));
$('modal-close')?.addEventListener('click', () => $('confirm-modal')?.classList.remove('active'));
function renderMonitorCards() {
    const g = $('monitor-grid');
    if (!g) return;
    g.innerHTML = apiList.map(a => {
        const last = monitorHistory.find(h => h.api_id === a.id);
        return `
            <div class="monitor-card ${(a.lastStatus||'pending').toLowerCase()}">
                <div class="monitor-card-header"><div class="monitor-api-info"><span class="api-method-badge ${a.method}">${a.method}</span><span class="monitor-api-name">${escapeHtml(a.name)}</span></div><span class="status-badge ${(a.lastStatus||'pending').toLowerCase()}">${a.lastStatus||'Pending'}</span></div>
                <div class="monitor-card-body"><div class="monitor-metrics"><div><span class="monitor-metric-label">Latency</span><div class="monitor-metric-value">${last ? last.response_time + 'ms' : '—'}</div></div><div><span class="monitor-metric-label">Code</span><div class="monitor-metric-value">${last ? last.status_code : '200'}</div></div></div>
                <div class="monitor-card-actions"><button class="btn btn-primary btn-sm" onclick="checkSingleAPI(${a.id})"><i class="fas fa-play"></i> Ping</button></div></div>
            </div>`;
    }).join('');
}
function populateHistoryFilters() {
    const f = $('history-api-filter');
    if (f) f.innerHTML = '<option value="all">All APIs</option>' + apiList.map(a => `<option value="${a.id}">${escapeHtml(a.name)}</option>`).join('');
}
function renderHistoryTable() {
    const tbody = $('history-table-body'), apiF = $('history-api-filter')?.value || 'all', stF = $('history-status-filter')?.value || 'all';
    if (!tbody) return;
    let list = monitorHistory.filter(h => (apiF === 'all' || h.api_id.toString() === apiF) && (stF === 'all' || h.status === stF));
    tbody.innerHTML = list.map((h, i) => `
        <tr><td>0${i+1}</td><td><strong>${escapeHtml(h.api_name)}</strong></td><td>${h.status_code}</td><td style="font-weight:700">${h.response_time}ms</td><td><span class="status-badge ${h.status.toLowerCase()}">${h.status}</span></td><td>${h.checked_at}</td></tr>
    `).join('');
}
$('history-api-filter')?.addEventListener('change', renderHistoryTable);
$('history-status-filter')?.addEventListener('change', renderHistoryTable);
function populateAnalyticsFilters() {
    const f = $('analytics-api-filter');
    if (f) f.innerHTML = '<option value="all">All APIs</option>' + apiList.map(a => `<option value="${a.id}">${escapeHtml(a.name)}</option>`).join('');
}
function updateAnalyticsStats() {
    const f = $('analytics-api-filter')?.value || 'all';
    const d = f === 'all' ? monitorHistory : monitorHistory.filter(h => h.api_id.toString() === f);
    const valid = d.filter(h => h.status !== 'Failed');
    $('analytics-avg-response') && ($('analytics-avg-response').textContent = `${valid.length ? Math.round(valid.reduce((s, h) => s + h.response_time, 0) / valid.length) : 0} ms`);
    $('analytics-success-count') && ($('analytics-success-count').textContent = valid.length);
    $('analytics-fail-count') && ($('analytics-fail-count').textContent = d.length - valid.length);
    $('analytics-slowest') && ($('analytics-slowest').textContent = `${valid.length ? Math.max(...valid.map(h => h.response_time)) : 0} ms`);
}
function renderAnalyticsCharts() {
    const isDark = document.body.classList.contains('dark-mode'), textColor = isDark ? '#9da4be' : '#575c75';
    const c1 = $('response-time-chart'), c2 = $('success-fail-chart'), c3 = $('api-comparison-chart');
    if (c1) {
        if (charts.resp) charts.resp.destroy();
        charts.resp = new Chart(c1, { type: 'bar', data: { labels: monitorHistory.slice(0, 10).map(h => h.api_name.slice(0, 8)), datasets: [{ label: 'ms', data: monitorHistory.slice(0, 10).map(h => h.response_time), backgroundColor: '#10b981', borderRadius: 6 }] }, options: { responsive: true, maintainAspectRatio: false } });
    }
    if (c2) {
        if (charts.dough) charts.dough.destroy();
        charts.dough = new Chart(c2, { type: 'doughnut', data: { labels: ['Healthy', 'Slow', 'Failed'], datasets: [{ data: [8, 3, 1], backgroundColor: ['#10b981', '#f59e0b', '#ef4444'] }] }, options: { responsive: true, maintainAspectRatio: false } });
    }
    if (c3) {
        if (charts.bar) charts.bar.destroy();
        charts.bar = new Chart(c3, { type: 'bar', data: { labels: apiList.map(a => a.name.slice(0, 10)), datasets: [{ label: 'Avg ms', data: [142, 289, 823, 356, 0], backgroundColor: '#ff5e62', borderRadius: 6 }] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false } });
    }
}
$('analytics-api-filter')?.addEventListener('change', () => { updateAnalyticsStats(); renderAnalyticsCharts(); });
function showToast(type, title, msg) {
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `<div style="font-weight:700">${title}</div><div style="font-size:0.8rem;color:var(--text-secondary)">${msg}</div>`;
    $('toast-container')?.appendChild(t);
    setTimeout(() => { t.classList.add('removing'); setTimeout(() => t.remove(), 250); }, 3000);
}
function escapeHtml(str) { return (str || '').replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m])); }
document.addEventListener('DOMContentLoaded', () => {
    refreshPageData('dashboard');
    renderAPITable();
    renderMonitorCards();
});
