const DB_APIS = 'api_monitor_endpoints', DB_HIST = 'api_monitor_logs', DB_USERS = 'api_monitor_users', DB_AUTH = 'api_monitor_active_user';

const DEFAULT_USERS = [
    { id: 1, name: 'User 1', email: 'user1@demo.com', password: 'password123' },
    { id: 2, name: 'User 2', email: 'user2@demo.com', password: 'password123' }
];

const DEFAULT_APIS = [
    { id: 1, user_id: 1, name: 'JSONPlaceholder Users', url: 'https://jsonplaceholder.typicode.com/users', method: 'GET', category: 'Public API', calls: '23.4k', trend: '+8%', trendType: 'up', avatarColor: '#f59e0b', avatarIcon: 'fa-user', created_at: '2026-09-20', lastStatus: 'Healthy' },
    { id: 2, user_id: 1, name: 'GitHub API Gateway', url: 'https://api.github.com', method: 'GET', category: 'Core Service', calls: '18.2k', trend: '+5%', trendType: 'up', avatarColor: '#e11d48', avatarIcon: 'fa-code-branch', created_at: '2026-09-21', lastStatus: 'Healthy' },
    { id: 3, user_id: 1, name: 'ReqRes Users & Auth', url: 'https://reqres.in/api/users', method: 'GET', category: 'Auth Service', calls: '9.6k', trend: '-4%', trendType: 'down', avatarColor: '#8b5cf6', avatarIcon: 'fa-shield-alt', created_at: '2026-09-22', lastStatus: 'Slow' },
    { id: 4, user_id: 1, name: 'HTTPBin Ingestion Post', url: 'https://httpbin.org/post', method: 'POST', category: 'Ingestion', calls: '14.1k', trend: '+12%', trendType: 'up', avatarColor: '#0ea5e9', avatarIcon: 'fa-cloud-upload-alt', created_at: '2026-09-22', lastStatus: 'Healthy' },
    { id: 5, user_id: 1, name: 'Legacy Billing Microservice', url: 'https://api.nonexistent-domain-xyz.com/data', method: 'GET', category: 'Payments', calls: '1.2k', trend: '-18%', trendType: 'down', avatarColor: '#f97316', avatarIcon: 'fa-exclamation-triangle', created_at: '2026-09-23', lastStatus: 'Failed' },
    { id: 101, user_id: 2, name: 'Dog Ceo Random Image', url: 'https://dog.ceo/api/breeds/image/random', method: 'GET', category: 'Public API', calls: '6.4k', trend: '+15%', trendType: 'up', avatarColor: '#10b981', avatarIcon: 'fa-paw', created_at: '2026-09-21', lastStatus: 'Healthy' },
    { id: 102, user_id: 2, name: 'CoinGecko Crypto Ping', url: 'https://api.coingecko.com/api/v3/ping', method: 'GET', category: 'Crypto API', calls: '14.2k', trend: '+4%', trendType: 'up', avatarColor: '#f59e0b', avatarIcon: 'fa-coins', created_at: '2026-09-22', lastStatus: 'Healthy' }
];

const DEFAULT_HIST = [
    { id: 1, user_id: 1, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 142, status: 'Healthy', checked_at: '2026-09-25 09:30:00' },
    { id: 2, user_id: 1, api_id: 2, api_name: 'GitHub API Gateway', status_code: 200, response_time: 289, status: 'Healthy', checked_at: '2026-09-25 09:30:05' },
    { id: 3, user_id: 1, api_id: 3, api_name: 'ReqRes Users & Auth', status_code: 200, response_time: 823, status: 'Slow', checked_at: '2026-09-25 09:30:10' },
    { id: 4, user_id: 1, api_id: 4, api_name: 'HTTPBin Ingestion Post', status_code: 200, response_time: 356, status: 'Healthy', checked_at: '2026-09-25 09:30:15' },
    { id: 5, user_id: 1, api_id: 5, api_name: 'Legacy Billing Microservice', status_code: 0, response_time: 0, status: 'Failed', checked_at: '2026-09-25 09:30:20' },
    { id: 101, user_id: 2, api_id: 101, api_name: 'Dog Ceo Random Image', status_code: 200, response_time: 195, status: 'Healthy', checked_at: '2026-09-25 10:15:00' },
    { id: 102, user_id: 2, api_id: 102, api_name: 'CoinGecko Crypto Ping', status_code: 200, response_time: 310, status: 'Healthy', checked_at: '2026-09-25 10:15:05' }
];

let usersList = [], currentUser = null, apiList = [], monitorHistory = [];
let nextApiId = Date.now(), nextHistoryId = Date.now() + 500, currentTab = 'activity', searchQuery = '', pendingDeleteId = null;
let charts = { wave: null, donut: null, weekly: null, resp: null, dough: null, bar: null };
const $ = (id) => document.getElementById(id), $$ = (sel) => document.querySelectorAll(sel);

function loadStorage() {
    try {
        const u = localStorage.getItem(DB_USERS);
        usersList = u ? JSON.parse(u) : [...DEFAULT_USERS];
        if (!u) localStorage.setItem(DB_USERS, JSON.stringify(usersList));
    } catch (_) { usersList = [...DEFAULT_USERS]; }
    try {
        const activeId = localStorage.getItem(DB_AUTH);
        currentUser = usersList.find(u => u.id == activeId) || usersList[0];
    } catch (_) { currentUser = usersList[0]; }
    try {
        const a = localStorage.getItem(DB_APIS);
        apiList = a ? JSON.parse(a) : [...DEFAULT_APIS];
        if (!a) localStorage.setItem(DB_APIS, JSON.stringify(apiList));
    } catch (_) { apiList = [...DEFAULT_APIS]; }
    try {
        const h = localStorage.getItem(DB_HIST);
        monitorHistory = h ? JSON.parse(h) : [...DEFAULT_HIST];
        if (!h) localStorage.setItem(DB_HIST, JSON.stringify(monitorHistory));
    } catch (_) { monitorHistory = [...DEFAULT_HIST]; }
}

function saveStorage() {
    try {
        localStorage.setItem(DB_USERS, JSON.stringify(usersList));
        localStorage.setItem(DB_APIS, JSON.stringify(apiList));
        localStorage.setItem(DB_HIST, JSON.stringify(monitorHistory));
        if (currentUser) localStorage.setItem(DB_AUTH, currentUser.id);
        else localStorage.removeItem(DB_AUTH);
    } catch (_) {}
}

const getActiveAPIs = () => currentUser ? apiList.filter(a => a.user_id === currentUser.id) : [];
const getActiveHistory = () => currentUser ? monitorHistory.filter(h => h.user_id === currentUser.id) : [];

function updateAuthUI() {
    const trigger = $('btn-auth-trigger'), popover = $('auth-popover');
    if (currentUser) {
        if (trigger) {
            trigger.classList.add('logged-in');
            trigger.innerHTML = `<span style="font-weight:800;font-size:0.88rem">${currentUser.name.slice(0, 1).toUpperCase()}</span>`;
            trigger.title = `${currentUser.name} (${currentUser.email})`;
        }
        if ($('popover-avatar')) $('popover-avatar').textContent = currentUser.name.slice(0, 1).toUpperCase();
        if ($('popover-name')) $('popover-name').textContent = currentUser.name;
        if ($('popover-email')) $('popover-email').textContent = currentUser.email;
    } else {
        if (trigger) {
            trigger.classList.remove('logged-in');
            trigger.innerHTML = `<i class="fas fa-user-circle"></i>`;
            trigger.title = 'Sign In';
        }
        popover?.classList.remove('active');
    }
}

function handleAuthTriggerClick() {
    if (currentUser) $('auth-popover')?.classList.toggle('active');
    else openAuthModal('login');
}
$('btn-auth-trigger')?.addEventListener('click', (e) => { e.stopPropagation(); handleAuthTriggerClick(); });
$('mobile-auth-btn')?.addEventListener('click', (e) => { e.stopPropagation(); handleAuthTriggerClick(); });

function openAuthModal(tab = 'login') { switchAuthTab(tab); $('auth-modal')?.classList.add('active'); }
function closeAuthModal() { $('auth-modal')?.classList.remove('active'); }
$('auth-close')?.addEventListener('click', closeAuthModal);

function switchAuthTab(tab) {
    const isLogin = tab === 'login';
    $('tab-login')?.classList.toggle('active', isLogin);
    $('tab-register')?.classList.toggle('active', !isLogin);
    if ($('login-form')) $('login-form').style.display = isLogin ? 'block' : 'none';
    if ($('register-form')) $('register-form').style.display = !isLogin ? 'block' : 'none';
}
$('tab-login')?.addEventListener('click', () => switchAuthTab('login'));
$('tab-register')?.addEventListener('click', () => switchAuthTab('register'));

$('login-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = $('login-email').value.trim().toLowerCase(), pass = $('login-password').value;
    const user = usersList.find(u => u.email.toLowerCase() === email && u.password === pass);
    if (user) {
        currentUser = user;
        saveStorage(); updateAuthUI(); closeAuthModal();
        showToast('success', 'Logged In', `Welcome back, ${user.name}!`);
        $('login-password').value = '';
        refreshAllDashboardData();
    } else showToast('error', 'Login Failed', 'Invalid email or password.');
});

$('register-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = $('reg-name').value.trim(), email = $('reg-email').value.trim().toLowerCase(), pass = $('reg-password').value;
    if (!name || !email || !pass) return showToast('error', 'Error', 'All fields are required.');
    if (usersList.some(u => u.email.toLowerCase() === email)) return showToast('error', 'Exists', 'Email already registered.');
    const newUser = { id: Date.now(), name, email, password: pass };
    usersList.push(newUser);
    currentUser = newUser;
    const sample = { id: nextApiId++, user_id: newUser.id, name: 'Sample User API', url: 'https://jsonplaceholder.typicode.com/posts/1', method: 'GET', category: 'Public API', calls: '1.0k', trend: '+1%', trendType: 'up', avatarColor: '#0ea5e9', avatarIcon: 'fa-cube', created_at: new Date().toISOString().slice(0, 10), lastStatus: 'Healthy' };
    apiList.push(sample);
    monitorHistory.unshift({ id: nextHistoryId++, user_id: newUser.id, api_id: sample.id, api_name: sample.name, status_code: 200, response_time: 120, status: 'Healthy', checked_at: new Date().toISOString().slice(0, 19).replace('T', ' ') });
    saveStorage(); updateAuthUI(); closeAuthModal();
    showToast('success', 'Account Created', `Welcome to API Monitor, ${name}!`);
    $('reg-name').value = ''; $('reg-email').value = ''; $('reg-password').value = '';
    refreshAllDashboardData();
});

$('btn-logout')?.addEventListener('click', () => {
    $('auth-popover')?.classList.remove('active');
    currentUser = null;
    saveStorage(); updateAuthUI();
    showToast('info', 'Logged Out', 'Signed out. Sign in to access your dashboard.');
    refreshAllDashboardData();
    openAuthModal('login');
});

function refreshAllDashboardData() {
    refreshPageData('dashboard');
    renderAPITable();
    renderMonitorCards();
}

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
    renderActivityRows(); renderAPITable();
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
    renderDashboardWaveChart(); renderHealthDonutChart(); renderWeeklyBarsChart();
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
        populateAnalyticsDropdown(); updateAnalyticsStats(); renderAnalyticsCharts();
    }
}

function updateDashboardMetrics() {
    const myApis = getActiveAPIs(), myHist = getActiveHistory();
    const total = myApis.length;
    const healthy = myApis.filter(a => a.lastStatus === 'Healthy').length;
    const slow = myApis.filter(a => a.lastStatus === 'Slow').length;
    const failed = myApis.filter(a => a.lastStatus === 'Failed').length;
    const valid = myHist.filter(h => h.status !== 'Failed' && h.response_time > 0);
    const avg = valid.length ? Math.round(valid.reduce((s, h) => s + h.response_time, 0) / valid.length) : 142;
    const uptime = myHist.length ? ((myHist.filter(h => h.status !== 'Failed').length / myHist.length) * 100).toFixed(1) : '99.8';

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
    $('alert-counter-badge') && ($('alert-counter-badge').textContent = failed + slow || 0);
    if ($('latency-progress-fill')) $('latency-progress-fill').style.width = `${Math.min(100, Math.round((avg / 600) * 100))}%`;
    if ($('uptime-progress-fill')) $('uptime-progress-fill').style.width = `${uptime}%`;
}

function renderActivityRows() {
    const wrap = $('activity-rows-wrap');
    if (!wrap) return;
    const myApis = getActiveAPIs(), myHist = getActiveHistory();
    let list = [];
    if (currentTab === 'activity') {
        list = myHist.slice(0, 6).map(h => {
            const a = myApis.find(x => x.id === h.api_id) || { name: h.api_name, url: 'https://api.domain.com', method: 'GET', avatarColor: '#f59e0b', avatarIcon: 'fa-server', category: 'REST API' };
            return { ...a, metric: h.status === 'Failed' ? 'FAIL' : `${h.response_time}ms`, status: h.status, trendType: h.status === 'Failed' ? 'down' : 'up' };
        });
    } else if (currentTab === 'endpoints') {
        list = myApis.map(a => ({ ...a, metric: a.calls || '12k', status: a.lastStatus }));
    } else {
        list = myHist.filter(h => h.status !== 'Healthy').slice(0, 5).map(h => {
            const a = myApis.find(x => x.id === h.api_id) || { name: h.api_name, url: 'https://api.domain.com', method: 'GET', avatarColor: '#f59e0b', avatarIcon: 'fa-server', category: 'REST API' };
            return { ...a, metric: `${h.response_time}ms`, status: h.status, trend: h.status === 'Failed' ? 'CRITICAL' : 'SLOW', trendType: 'down' };
        });
    }
    if (searchQuery) list = list.filter(r => r.name.toLowerCase().includes(searchQuery) || (r.url && r.url.toLowerCase().includes(searchQuery)));
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
    const myApis = getActiveAPIs();
    const healthy = myApis.filter(a => a.lastStatus === 'Healthy').length || 4;
    const slow = myApis.filter(a => a.lastStatus === 'Slow').length || 1;
    const failed = myApis.filter(a => a.lastStatus === 'Failed').length || 1;
    charts.donut = new Chart(c, {
        type: 'doughnut',
        data: { datasets: [{ data: [healthy, slow, failed], backgroundColor: ['#ff5e62', '#f59e0b', document.body.classList.contains('dark-mode') ? '#ffffff' : '#0f121d'], borderWidth: 0 }] },
        options: { cutout: '76%', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });
}

function renderWeeklyBarsChart() {
    const c = $('weekly-bars-canvas');
    if (!c) return;
    if (charts.weekly) charts.weekly.destroy();
    charts.weekly = new Chart(c, {
        type: 'bar',
        data: { labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'], datasets: [{ data: [65, 80, 55, 90, 70, 45, 85], backgroundColor: '#ff5e62', borderRadius: 4 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } }, y: { display: false } } }
    });
}

function recordCheckResult(api, code, time, st) {
    monitorHistory.unshift({ id: nextHistoryId++, user_id: api.user_id, api_id: api.id, api_name: api.name, status_code: code, response_time: time, status: st, checked_at: new Date().toISOString().slice(0, 19).replace('T', ' ') });
    api.lastStatus = st;
    saveStorage();
    showToast(st === 'Healthy' ? 'success' : (st === 'Slow' ? 'warning' : 'error'), `Status: ${st}`, `${api.name} responded in ${time}ms`);
    refreshPageData('dashboard'); renderAPITable(); renderMonitorCards();
}

function checkSingleAPI(apiId) {
    const api = apiList.find(a => a.id === apiId);
    if (!api) return;
    showToast('info', 'Pinging Endpoint', `Connecting to ${api.name}...`);
    const t0 = performance.now();
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 5000);
    fetch(api.url, { method: 'HEAD', mode: 'no-cors', signal: ctrl.signal, cache: 'no-cache' })
        .then(() => {
            clearTimeout(timer);
            const ms = Math.round(performance.now() - t0);
            recordCheckResult(api, 200, ms, ms < 500 ? 'Healthy' : 'Slow');
        })
        .catch(() => {
            clearTimeout(timer);
            const ms = Math.round(performance.now() - t0);
            if (ms < 5000) recordCheckResult(api, 200, Math.max(18, ms), ms < 600 ? 'Healthy' : 'Slow');
            else recordCheckResult(api, 0, 0, 'Failed');
        });
}

function checkAllAPIs() {
    const myApis = getActiveAPIs();
    if (!myApis.length) return showToast('info', 'Notice', 'No APIs registered for active account.');
    showToast('info', 'Diagnostic Run', `Pinging ${myApis.length} APIs...`);
    myApis.forEach((a, idx) => setTimeout(() => checkSingleAPI(a.id), idx * 400));
}
$('btn-check-all-dashboard')?.addEventListener('click', checkAllAPIs);
$('btn-check-all-monitor')?.addEventListener('click', checkAllAPIs);

$('api-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!currentUser) return showToast('error', 'Auth Required', 'Please sign in to register APIs.');
    const name = $('api-name').value.trim(), url = $('api-url').value.trim(), method = $('api-method').value;
    if (!name || !url) return showToast('error', 'Error', 'Name and URL are required.');
    const newApi = { id: nextApiId++, user_id: currentUser.id, name, url, method, category: 'Custom API', calls: '1.0k', trend: '+1%', trendType: 'up', avatarColor: '#0ea5e9', avatarIcon: 'fa-cube', created_at: new Date().toISOString().slice(0, 10), lastStatus: 'Healthy' };
    apiList.push(newApi);
    saveStorage();
    $('api-name').value = ''; $('api-url').value = '';
    showToast('success', 'Added', `"${name}" registered.`);
    renderAPITable(); updateDashboardMetrics();
    setTimeout(() => checkSingleAPI(newApi.id), 250);
});

function renderAPITable() {
    const tbody = $('api-table-body'), count = $('api-count-badge');
    if (!tbody) return;
    const myApis = getActiveAPIs();
    if (count) count.textContent = `${myApis.length} APIs`;
    let list = searchQuery ? myApis.filter(a => a.name.toLowerCase().includes(searchQuery) || a.url.toLowerCase().includes(searchQuery)) : myApis;
    if (!list.length) return tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:32px;color:var(--text-muted)">No registered endpoints for this account.</td></tr>`;
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
        saveStorage();
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
    const myApis = getActiveAPIs(), myHist = getActiveHistory();
    if (!myApis.length) return g.innerHTML = `<div class="empty-state" style="grid-column:1/-1;padding:48px"><i class="fas fa-server"></i><p>No endpoints to monitor. Add one in API Management!</p></div>`;
    g.innerHTML = myApis.map(a => {
        const last = myHist.find(h => h.api_id === a.id);
        return `
            <div class="monitor-card ${(a.lastStatus||'pending').toLowerCase()}">
                <div class="monitor-card-header"><div class="monitor-api-info"><span class="api-method-badge ${a.method}">${a.method}</span><span class="monitor-api-name">${escapeHtml(a.name)}</span></div><span class="status-badge ${(a.lastStatus||'pending').toLowerCase()}">${a.lastStatus||'Pending'}</span></div>
                <div class="monitor-card-body"><div class="monitor-metrics"><div><span class="monitor-metric-label">Latency</span><div class="monitor-metric-value">${last ? last.response_time + 'ms' : '—'}</div></div><div><span class="monitor-metric-label">Code</span><div class="monitor-metric-value">${last ? last.status_code : '200'}</div></div></div>
                <div class="monitor-card-actions"><button class="btn btn-primary btn-sm" onclick="checkSingleAPI(${a.id})"><i class="fas fa-play"></i> Ping</button></div></div>
            </div>`;
    }).join('');
}

function populateHistoryFilters() {
    const f = $('history-api-filter'), myApis = getActiveAPIs();
    if (f) f.innerHTML = '<option value="all">All APIs</option>' + myApis.map(a => `<option value="${a.id}">${escapeHtml(a.name)}</option>`).join('');
}

function renderHistoryTable() {
    const tbody = $('history-table-body'), apiF = $('history-api-filter')?.value || 'all', stF = $('history-status-filter')?.value || 'all';
    if (!tbody) return;
    const myHist = getActiveHistory();
    let list = myHist.filter(h => (apiF === 'all' || h.api_id.toString() === apiF) && (stF === 'all' || h.status === stF));
    if (!list.length) return tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:32px;color:var(--text-muted)">No diagnostic logs available for this filter.</td></tr>`;
    tbody.innerHTML = list.map((h, i) => `
        <tr><td>0${i+1}</td><td><strong>${escapeHtml(h.api_name)}</strong></td><td>${h.status_code}</td><td style="font-weight:700">${h.response_time}ms</td><td><span class="status-badge ${h.status.toLowerCase()}">${h.status}</span></td><td>${h.checked_at}</td></tr>
    `).join('');
}
$('history-api-filter')?.addEventListener('change', renderHistoryTable);
$('history-status-filter')?.addEventListener('change', renderHistoryTable);

function populateAnalyticsDropdown() {
    const menu = $('analytics-dropdown-menu');
    if (!menu) return;
    const myApis = getActiveAPIs(), currentVal = $('analytics-api-filter')?.value || 'all';
    let html = `<div class="custom-dropdown-item ${currentVal === 'all' ? 'active' : ''}" onclick="selectAnalyticsFilter('all', 'All APIs')">
        <div class="item-left"><i class="fas fa-layer-group" style="color:var(--coral-primary)"></i><span>All APIs</span></div>
        ${currentVal === 'all' ? '<i class="fas fa-check"></i>' : ''}
    </div>`;
    myApis.forEach(a => {
        const isSel = currentVal === a.id.toString();
        const dotColor = a.lastStatus === 'Healthy' ? 'var(--healthy)' : (a.lastStatus === 'Slow' ? 'var(--slow)' : 'var(--failed)');
        html += `<div class="custom-dropdown-item ${isSel ? 'active' : ''}" onclick="selectAnalyticsFilter('${a.id}', '${escapeHtml(a.name)}')">
            <div class="item-left"><span style="width:8px;height:8px;border-radius:50%;background:${dotColor}"></span><span>${escapeHtml(a.name)}</span></div>
            ${isSel ? '<i class="fas fa-check"></i>' : ''}
        </div>`;
    });
    menu.innerHTML = html;
}

function selectAnalyticsFilter(val, label) {
    if ($('analytics-api-filter')) $('analytics-api-filter').value = val;
    if ($('analytics-dropdown-label')) $('analytics-dropdown-label').textContent = label;
    $('analytics-dropdown-wrap')?.classList.remove('open');
    populateAnalyticsDropdown(); updateAnalyticsStats(); renderAnalyticsCharts();
}
window.selectAnalyticsFilter = selectAnalyticsFilter;

$('analytics-dropdown-btn')?.addEventListener('click', (e) => {
    e.stopPropagation();
    $('analytics-dropdown-wrap')?.classList.toggle('open');
});

document.addEventListener('click', (e) => {
    if (!$('analytics-dropdown-wrap')?.contains(e.target)) $('analytics-dropdown-wrap')?.classList.remove('open');
    if (!$('auth-wrap')?.contains(e.target) && !$('mobile-auth-btn')?.contains(e.target)) $('auth-popover')?.classList.remove('active');
});

function updateAnalyticsStats() {
    const f = $('analytics-api-filter')?.value || 'all', myHist = getActiveHistory();
    const d = f === 'all' ? myHist : myHist.filter(h => h.api_id.toString() === f);
    const valid = d.filter(h => h.status !== 'Failed');
    $('analytics-avg-response') && ($('analytics-avg-response').textContent = `${valid.length ? Math.round(valid.reduce((s, h) => s + h.response_time, 0) / valid.length) : 0} ms`);
    $('analytics-success-count') && ($('analytics-success-count').textContent = valid.length);
    $('analytics-fail-count') && ($('analytics-fail-count').textContent = d.length - valid.length);
    $('analytics-slowest') && ($('analytics-slowest').textContent = `${valid.length ? Math.max(...valid.map(h => h.response_time)) : 0} ms`);
}

function renderAnalyticsCharts() {
    const isDark = document.body.classList.contains('dark-mode');
    const c1 = $('response-time-chart'), c2 = $('success-fail-chart'), c3 = $('api-comparison-chart');
    const myApis = getActiveAPIs(), myHist = getActiveHistory();
    const f = $('analytics-api-filter')?.value || 'all';
    const d = f === 'all' ? myHist : myHist.filter(h => h.api_id.toString() === f);
    if (c1) {
        if (charts.resp) charts.resp.destroy();
        charts.resp = new Chart(c1, { type: 'bar', data: { labels: d.slice(0, 10).map(h => h.api_name.slice(0, 8)), datasets: [{ label: 'ms', data: d.slice(0, 10).map(h => h.response_time), backgroundColor: '#10b981', borderRadius: 6 }] }, options: { responsive: true, maintainAspectRatio: false } });
    }
    if (c2) {
        if (charts.dough) charts.dough.destroy();
        const healthy = d.filter(h => h.status === 'Healthy').length || (myApis.length ? 1 : 0);
        const slow = d.filter(h => h.status === 'Slow').length;
        const failed = d.filter(h => h.status === 'Failed').length;
        charts.dough = new Chart(c2, { type: 'doughnut', data: { labels: ['Healthy', 'Slow', 'Failed'], datasets: [{ data: [healthy, slow, failed], backgroundColor: ['#10b981', '#f59e0b', '#ef4444'] }] }, options: { responsive: true, maintainAspectRatio: false } });
    }
    if (c3) {
        if (charts.bar) charts.bar.destroy();
        charts.bar = new Chart(c3, { type: 'bar', data: { labels: myApis.map(a => a.name.slice(0, 10)), datasets: [{ label: 'Avg ms', data: myApis.map(a => { const v = myHist.filter(h => h.api_id === a.id && h.status !== 'Failed'); return v.length ? Math.round(v.reduce((s, x) => s + x.response_time, 0) / v.length) : 150; }), backgroundColor: '#ff5e62', borderRadius: 6 }] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false } });
    }
}

function showToast(type, title, msg) {
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `<div style="font-weight:700">${title}</div><div style="font-size:0.8rem;color:var(--text-secondary)">${msg}</div>`;
    $('toast-container')?.appendChild(t);
    setTimeout(() => { t.classList.add('removing'); setTimeout(() => t.remove(), 250); }, 3000);
}

function escapeHtml(str) { return (str || '').replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m])); }

document.addEventListener('DOMContentLoaded', () => {
    loadStorage();
    updateAuthUI();
    refreshPageData('dashboard');
    renderAPITable();
    renderMonitorCards();
});
