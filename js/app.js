/* ==========================================================================
   API MONITOR — PERFORMANCE ANALYTICS DASHBOARD
   Frontend Application Logic (Interactive Reference Layout)
   ========================================================================== */

// ========== MOCK DATA STORE ==========
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
    { id: 11, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 195, status: 'Healthy', checked_at: '2026-09-25 06:30:00' },
    { id: 12, api_id: 2, api_name: 'GitHub API Gateway', status_code: 200, response_time: 450, status: 'Healthy', checked_at: '2026-09-25 06:30:05' },
    { id: 13, api_id: 3, api_name: 'ReqRes Users & Auth', status_code: 200, response_time: 690, status: 'Slow', checked_at: '2026-09-25 06:30:10' },
    { id: 14, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 110, status: 'Healthy', checked_at: '2026-09-25 04:00:00' },
    { id: 15, api_id: 2, api_name: 'GitHub API Gateway', status_code: 200, response_time: 530, status: 'Slow', checked_at: '2026-09-25 04:00:05' },
];

let nextApiId = 6;
let nextHistoryId = 16;
let currentActivityTab = 'activity';
let currentSearchQuery = '';

// ========== DOM REFERENCES ==========
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');
const menuToggle = document.getElementById('menu-toggle');
const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
const pages = document.querySelectorAll('.page');
const toastContainer = document.getElementById('toast-container');
const dynamicPageTitle = document.getElementById('dynamic-page-title');

// ========== NAVIGATION ==========
function navigateTo(pageName) {
    if (!pageName) return;

    navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.page === pageName);
    });

    pages.forEach(page => {
        page.classList.toggle('active', page.id === `page-${pageName}`);
    });

    if (dynamicPageTitle) {
        const titles = {
            dashboard: 'Analytics',
            apis: 'API Endpoints',
            monitor: 'Live Monitoring',
            history: 'Health History',
            analytics: 'Performance Analytics'
        };
        dynamicPageTitle.textContent = titles[pageName] || 'Analytics';
    }

    sidebar.classList.remove('open');
    if (sidebarOverlay) sidebarOverlay.classList.remove('active');

    refreshPageData(pageName);
}

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        if (link.dataset.page) {
            e.preventDefault();
            navigateTo(link.dataset.page);
        }
    });
});

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        if (sidebarOverlay) sidebarOverlay.classList.toggle('active');
    });
}

if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        sidebarOverlay.classList.remove('active');
    });
}

// Quick action buttons
document.getElementById('mobile-check-all')?.addEventListener('click', checkAllAPIs);
document.getElementById('nav-btn-check-all')?.addEventListener('click', (e) => {
    e.preventDefault();
    checkAllAPIs();
});
document.getElementById('btn-quick-new-api')?.addEventListener('click', () => {
    navigateTo('apis');
    setTimeout(() => {
        document.getElementById('api-name')?.focus();
    }, 100);
});

// Fullscreen toggle
document.getElementById('btn-fullscreen-toggle')?.addEventListener('click', () => {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
    } else {
        document.exitFullscreen().catch(() => {});
    }
});

// Global Search Filter
const globalSearchInput = document.getElementById('global-search-input');
if (globalSearchInput) {
    globalSearchInput.addEventListener('input', (e) => {
        currentSearchQuery = e.target.value.toLowerCase().trim();
        renderActivityRows();
        renderAPITable();
    });
}

// Activity Tab Switcher
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentActivityTab = btn.dataset.tab;
        renderActivityRows();
    });
});

// ========== THEME TOGGLE ==========
function setTheme(isDark) {
    document.body.classList.toggle('dark-mode', isDark);

    const icon = isDark ? 'fa-sun' : 'fa-moon';
    const oldIcon = isDark ? 'fa-moon' : 'fa-sun';

    const themeIcon = document.getElementById('theme-icon');
    const mobileIcon = document.getElementById('mobile-theme-icon');
    if (themeIcon) { themeIcon.classList.remove(oldIcon); themeIcon.classList.add(icon); }
    if (mobileIcon) { mobileIcon.classList.remove(oldIcon); mobileIcon.classList.add(icon); }

    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Refresh charts
    renderDashboardWaveChart();
    renderHealthDonutChart();
    renderWeeklyBarsChart();

    const activePage = document.querySelector('.page.active')?.id?.replace('page-', '');
    if (activePage === 'analytics') renderAnalyticsCharts();
}

document.getElementById('theme-toggle')?.addEventListener('click', () => {
    setTheme(!document.body.classList.contains('dark-mode'));
});
document.getElementById('mobile-theme-toggle')?.addEventListener('click', () => {
    setTheme(!document.body.classList.contains('dark-mode'));
});

(function loadSavedTheme() {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') {
        setTheme(true);
    }
})();

// ========== REFRESH PAGE DATA ==========
function refreshPageData(pageName) {
    switch (pageName) {
        case 'dashboard':
            updateDashboardMetrics();
            renderActivityRows();
            renderDashboardWaveChart();
            renderHealthDonutChart();
            renderWeeklyBarsChart();
            break;
        case 'apis':
            renderAPITable();
            break;
        case 'monitor':
            renderMonitorCards();
            break;
        case 'history':
            populateHistoryFilters();
            renderHistoryTable();
            break;
        case 'analytics':
            populateAnalyticsFilters();
            updateAnalyticsStats();
            renderAnalyticsCharts();
            break;
    }
}

// ========== DASHBOARD METRICS ==========
function updateDashboardMetrics() {
    const total = apiList.length;
    const healthy = apiList.filter(a => a.lastStatus === 'Healthy').length;
    const slow = apiList.filter(a => a.lastStatus === 'Slow').length;
    const failed = apiList.filter(a => a.lastStatus === 'Failed').length;

    const validChecks = monitorHistory.filter(h => h.status !== 'Failed' && h.response_time > 0);
    const avgResponse = validChecks.length > 0
        ? Math.round(validChecks.reduce((sum, h) => sum + h.response_time, 0) / validChecks.length)
        : 142;

    const totalChecks = monitorHistory.length;
    const successChecks = monitorHistory.filter(h => h.status !== 'Failed').length;
    const uptime = totalChecks > 0 ? ((successChecks / totalChecks) * 100).toFixed(1) : '99.8';

    // Hero Card metrics
    const heroTotalNumber = document.getElementById('hero-total-number');
    if (heroTotalNumber) heroTotalNumber.textContent = `${(total * 4.6).toFixed(4)}K`;

    const healthyPct = total > 0 ? Math.round((healthy / total) * 100) : 80;
    const slowPct = total > 0 ? Math.round((slow / total) * 100) : 15;
    const failedPct = total > 0 ? Math.round((failed / total) * 100) : 5;

    document.getElementById('hero-healthy-pct') && (document.getElementById('hero-healthy-pct').textContent = `%${healthyPct}`);
    document.getElementById('hero-slow-pct') && (document.getElementById('hero-slow-pct').textContent = `%${slowPct}`);
    document.getElementById('hero-failed-pct') && (document.getElementById('hero-failed-pct').textContent = `%${failedPct}`);

    // Donut card metrics
    document.getElementById('donut-uptime-number') && (document.getElementById('donut-uptime-number').innerHTML = `${uptime}<small>%</small>`);
    document.getElementById('legend-healthy-val') && (document.getElementById('legend-healthy-val').textContent = `%${healthyPct}`);
    document.getElementById('legend-slow-val') && (document.getElementById('legend-slow-val').textContent = `%${slowPct}`);
    document.getElementById('legend-failed-val') && (document.getElementById('legend-failed-val').textContent = `%${failedPct}`);

    // Right column metrics
    document.getElementById('side-avg-latency') && (document.getElementById('side-avg-latency').innerHTML = `${avgResponse} <small>ms</small>`);
    document.getElementById('side-uptime-pct') && (document.getElementById('side-uptime-pct').innerHTML = `${uptime}<small>%</small>`);
    document.getElementById('side-completed-count') && (document.getElementById('side-completed-count').textContent = successChecks * 68 || 874);

    // Progress fills
    const latencyProgress = Math.min(100, Math.max(10, Math.round((avgResponse / 800) * 100)));
    const latFill = document.getElementById('latency-progress-fill');
    if (latFill) latFill.style.width = `${latencyProgress}%`;

    const uptFill = document.getElementById('uptime-progress-fill');
    if (uptFill) uptFill.style.width = `${uptime}%`;

    // Tab counts
    const endpointCountEl = document.getElementById('tab-endpoint-count');
    if (endpointCountEl) endpointCountEl.textContent = total;

    const alertBadge = document.getElementById('alert-counter-badge');
    if (alertBadge) alertBadge.textContent = failed + slow || 6;
}

// ========== RENDER ACTIVITY ROWS (Exact Screenshot Look) ==========
function renderActivityRows() {
    const wrap = document.getElementById('activity-rows-wrap');
    if (!wrap) return;

    let itemsToRender = [];

    if (currentActivityTab === 'activity') {
        // Show recent check events
        itemsToRender = monitorHistory.slice(0, 6).map((item, idx) => {
            const api = apiList.find(a => a.id === item.api_id) || apiList[0];
            return {
                id: item.id,
                api_id: item.api_id,
                name: item.api_name,
                url: api.url,
                method: api.method,
                category: api.category || 'REST API',
                metric: item.status === 'Failed' ? 'FAIL' : `${item.response_time}ms`,
                trend: api.trend || '+5%',
                trendType: item.status === 'Failed' ? 'down' : (item.response_time < 300 ? 'up' : 'down'),
                avatarColor: api.avatarColor || '#f59e0b',
                avatarIcon: api.avatarIcon || 'fa-server',
                checked_at: item.checked_at,
                status: item.status
            };
        });
    } else if (currentActivityTab === 'endpoints') {
        itemsToRender = apiList.map(api => ({
            id: api.id,
            api_id: api.id,
            name: api.name,
            url: api.url,
            method: api.method,
            category: api.category || 'Endpoint',
            metric: api.calls || '12.4k',
            trend: api.trend || '+6%',
            trendType: api.trendType || 'up',
            avatarColor: api.avatarColor || '#3b82f6',
            avatarIcon: api.avatarIcon || 'fa-plug',
            status: api.lastStatus
        }));
    } else if (currentActivityTab === 'alerts') {
        itemsToRender = monitorHistory.filter(h => h.status === 'Failed' || h.status === 'Slow').slice(0, 5).map(item => {
            const api = apiList.find(a => a.id === item.api_id) || apiList[0];
            return {
                id: item.id,
                api_id: item.api_id,
                name: item.api_name,
                url: api.url,
                method: api.method,
                category: item.status === 'Failed' ? 'Outage Incident' : 'Latency Degradation',
                metric: item.status === 'Failed' ? 'HTTP 500' : `${item.response_time}ms`,
                trend: item.status === 'Failed' ? 'CRITICAL' : 'WARNING',
                trendType: 'down',
                avatarColor: item.status === 'Failed' ? '#ef4444' : '#f59e0b',
                avatarIcon: item.status === 'Failed' ? 'fa-times-circle' : 'fa-exclamation-triangle',
                status: item.status
            };
        });
    }

    // Apply global search filter
    if (currentSearchQuery) {
        itemsToRender = itemsToRender.filter(row =>
            row.name.toLowerCase().includes(currentSearchQuery) ||
            row.url.toLowerCase().includes(currentSearchQuery) ||
            row.category.toLowerCase().includes(currentSearchQuery)
        );
    }

    if (itemsToRender.length === 0) {
        wrap.innerHTML = `
            <div class="empty-state" style="padding: 30px 10px;">
                <i class="fas fa-search"></i>
                <p>No records found</p>
                <span>Try a different filter or search term</span>
            </div>
        `;
        return;
    }

    wrap.innerHTML = itemsToRender.map(item => `
        <div class="activity-row-item">
            <div class="row-left">
                <div class="row-avatar" style="background: ${item.avatarColor};">
                    <i class="fas ${item.avatarIcon}"></i>
                </div>
                <div class="row-info">
                    <div class="row-title-wrap">
                        <span class="row-title">${escapeHtml(item.name)}</span>
                        <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener" class="row-external-icon" title="Open API URL">
                            <i class="fas fa-external-link-alt"></i>
                        </a>
                    </div>
                    <span class="row-subtitle">${item.method} · ${escapeHtml(item.url)}</span>
                </div>
            </div>

            <div class="row-category">${escapeHtml(item.category)}</div>

            <div class="row-metric-wrap">
                <div class="row-metric-icon">
                    <i class="fas ${item.status === 'Failed' ? 'fa-bolt' : 'fa-tachometer-alt'}"></i>
                </div>
                <span class="row-metric-text">${item.metric}</span>
            </div>

            <div class="row-trend-badge ${item.trendType === 'up' ? 'trend-up' : 'trend-down'}">
                <i class="fas ${item.trendType === 'up' ? 'fa-arrow-up' : 'fa-arrow-down'}"></i>
                <span>${item.trend}</span>
            </div>

            <div class="row-actions-wrap">
                <button class="card-dots-btn" onclick="checkSingleAPI(${item.api_id})" title="Check Now">
                    <i class="fas fa-play" style="font-size: 0.8rem; color: var(--healthy);"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// ========== HERO WAVE CHART (Embedded in Gradient Card) ==========
let heroWaveCanvasInstance = null;

function renderDashboardWaveChart() {
    const canvas = document.getElementById('hero-wave-canvas');
    if (!canvas) return;

    if (heroWaveCanvasInstance) heroWaveCanvasInstance.destroy();

    const ctx = canvas.getContext('2d');

    // 3 smooth oscillating wave lines intersecting each other (matches reference screenshot)
    heroWaveCanvasInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['', '', '', '', '', '', '', '', '', '', '', '', ''],
            datasets: [
                {
                    data: [15, 28, 22, 38, 26, 42, 30, 48, 36, 52, 40, 58, 48],
                    borderColor: '#67e8f9', // Cyan/Sky
                    borderWidth: 2.2,
                    tension: 0.45,
                    pointRadius: 0,
                    fill: false,
                },
                {
                    data: [35, 20, 38, 22, 44, 28, 50, 32, 44, 30, 48, 35, 52],
                    borderColor: '#c084fc', // Light Violet
                    borderWidth: 2.2,
                    tension: 0.45,
                    pointRadius: 0,
                    fill: false,
                },
                {
                    data: [25, 42, 30, 48, 32, 54, 38, 42, 56, 44, 60, 48, 62],
                    borderColor: '#ffffff', // White glow line
                    borderWidth: 2.4,
                    tension: 0.45,
                    pointRadius: 0,
                    fill: false,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                x: { display: false },
                y: { display: false, min: 10, max: 70 }
            }
        }
    });
}

// ========== HEALTH BREAKDOWN DONUT CHART ==========
let healthDonutInstance = null;

function renderHealthDonutChart() {
    const canvas = document.getElementById('health-donut-canvas');
    if (!canvas) return;

    if (healthDonutInstance) healthDonutInstance.destroy();

    const healthyCount = apiList.filter(a => a.lastStatus === 'Healthy').length || 4;
    const slowCount = apiList.filter(a => a.lastStatus === 'Slow').length || 1;
    const failedCount = apiList.filter(a => a.lastStatus === 'Failed').length || 1;

    const isDark = document.body.classList.contains('dark-mode');

    healthDonutInstance = new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Healthy', 'Slow', 'Failed'],
            datasets: [{
                data: [healthyCount, slowCount, failedCount],
                backgroundColor: [
                    '#ff5e62', // Coral/Pink
                    '#f59e0b', // Amber/Yellow
                    isDark ? '#ffffff' : '#0f121d' // Deep Obsidian
                ],
                borderWidth: 0,
                hoverOffset: 4,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '72%',
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0f121d',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e5f0',
                    cornerRadius: 8,
                    padding: 10,
                }
            }
        }
    });
}

// ========== WEEKLY BARS CHART (Matches Reference "Post Stats") ==========
let weeklyBarsInstance = null;

function renderWeeklyBarsChart() {
    const canvas = document.getElementById('weekly-bars-canvas');
    if (!canvas) return;

    if (weeklyBarsInstance) weeklyBarsInstance.destroy();

    const isDark = document.body.classList.contains('dark-mode');
    const barDefaultColor = isDark ? 'rgba(255, 255, 255, 0.12)' : '#e5dfd5';
    const highlightedBarColor = '#ff5e62'; // Highlighted Thursday bar!

    weeklyBarsInstance = new Chart(canvas, {
        data: {
            labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
            datasets: [
                {
                    type: 'line',
                    data: [120, 160, 130, 240, 150, 180, 210],
                    borderColor: isDark ? '#ffffff' : '#0f121d',
                    borderWidth: 2,
                    tension: 0.45,
                    pointRadius: [0, 0, 0, 5, 0, 0, 0],
                    pointBackgroundColor: '#ff5e62',
                    fill: false,
                    order: 1
                },
                {
                    type: 'bar',
                    data: [140, 180, 150, 280, 170, 200, 230],
                    backgroundColor: [
                        barDefaultColor,
                        barDefaultColor,
                        barDefaultColor,
                        highlightedBarColor, // Peak day
                        barDefaultColor,
                        barDefaultColor,
                        barDefaultColor
                    ],
                    borderRadius: 16,
                    borderSkipped: false,
                    barThickness: 16,
                    order: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0f121d',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e5f0',
                    cornerRadius: 8,
                    callbacks: {
                        label: ctx => `Latency: ${ctx.parsed.y} ms`
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        color: isDark ? '#7d849b' : '#9599b0',
                        font: { family: 'Plus Jakarta Sans', size: 11, weight: 600 }
                    }
                },
                y: {
                    display: false,
                    beginAtZero: true
                }
            }
        }
    });
}

// ========== CHECK APIS (INTERACTIVE FUNCTIONALITY) ==========
function checkSingleAPI(apiId) {
    const api = apiList.find(a => a.id === apiId);
    if (!api) return;

    showToast('info', 'Pinging Endpoint', `Checking response for ${api.name}...`);

    const simulatedDelay = Math.random() * 900 + 150;

    setTimeout(() => {
        let statusCode, responseTime, status;

        if (api.url.includes('nonexistent') || api.url.includes('invalid')) {
            statusCode = 0;
            responseTime = 0;
            status = 'Failed';
        } else {
            responseTime = Math.round(Math.random() * 600 + 45);
            statusCode = 200;
            status = responseTime < 500 ? 'Healthy' : 'Slow';
        }

        const historyEntry = {
            id: nextHistoryId++,
            api_id: api.id,
            api_name: api.name,
            status_code: statusCode,
            response_time: responseTime,
            status: status,
            checked_at: new Date().toISOString().slice(0, 19).replace('T', ' ')
        };

        monitorHistory.unshift(historyEntry);
        api.lastStatus = status;

        if (status === 'Healthy') {
            showToast('success', 'API Operational', `${api.name} responded in ${responseTime}ms`);
        } else if (status === 'Slow') {
            showToast('warning', 'Elevated Latency', `${api.name} took ${responseTime}ms`);
        } else {
            showToast('error', 'API Failure', `${api.name} failed to respond`);
        }

        refreshPageData('dashboard');
        renderAPITable();
        renderMonitorCards();
    }, simulatedDelay);
}

function checkAllAPIs() {
    if (apiList.length === 0) {
        showToast('info', 'No APIs Registered', 'Please register an API endpoint first.');
        return;
    }

    showToast('info', 'Executing Full Diagnostic', `Pinging ${apiList.length} APIs across regions...`);

    apiList.forEach((api, index) => {
        setTimeout(() => {
            checkSingleAPI(api.id);
        }, index * 450);
    });
}

document.getElementById('btn-check-all-dashboard')?.addEventListener('click', checkAllAPIs);
document.getElementById('btn-check-all-monitor')?.addEventListener('click', checkAllAPIs);

// ========== API FORM SUBMISSION ==========
const apiForm = document.getElementById('api-form');
if (apiForm) {
    apiForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const nameInput = document.getElementById('api-name');
        const urlInput = document.getElementById('api-url');
        const methodInput = document.getElementById('api-method');

        const name = nameInput.value.trim();
        const url = urlInput.value.trim();
        const method = methodInput.value;

        if (!name || !url) {
            showToast('error', 'Validation Notice', 'Name and URL are required.');
            return;
        }

        const avatarColors = ['#f59e0b', '#e11d48', '#8b5cf6', '#0ea5e9', '#10b981'];
        const avatarIcons = ['fa-server', 'fa-database', 'fa-cloud', 'fa-shield-alt', 'fa-cube'];
        const randomIdx = Math.floor(Math.random() * avatarColors.length);

        const newApi = {
            id: nextApiId++,
            name: name,
            url: url,
            method: method,
            category: 'Custom API',
            calls: '1.0k',
            trend: '+2%',
            trendType: 'up',
            avatarColor: avatarColors[randomIdx],
            avatarIcon: avatarIcons[randomIdx],
            created_at: new Date().toISOString().slice(0, 19).replace('T', ' '),
            lastStatus: 'Pending'
        };

        apiList.push(newApi);

        nameInput.value = '';
        urlInput.value = '';
        methodInput.value = 'GET';

        showToast('success', 'API Registered', `"${name}" added to surveillance matrix.`);
        renderAPITable();
        updateDashboardMetrics();

        // Immediate check
        setTimeout(() => checkSingleAPI(newApi.id), 400);
    });
}

// ========== RENDER APIS TABLE ==========
function renderAPITable() {
    const tbody = document.getElementById('api-table-body');
    const emptyState = document.getElementById('api-list-empty');
    const countBadge = document.getElementById('api-count-badge');

    if (!tbody) return;

    if (countBadge) countBadge.textContent = `${apiList.length} API${apiList.length !== 1 ? 's' : ''}`;

    let list = [...apiList];
    if (currentSearchQuery) {
        list = list.filter(a => a.name.toLowerCase().includes(currentSearchQuery) || a.url.toLowerCase().includes(currentSearchQuery));
    }

    if (list.length === 0) {
        if (tbody.parentElement && tbody.parentElement.parentElement) {
            tbody.parentElement.parentElement.style.display = 'none';
        }
        if (emptyState) emptyState.style.display = 'block';
        return;
    }

    if (tbody.parentElement && tbody.parentElement.parentElement) {
        tbody.parentElement.parentElement.style.display = 'block';
    }
    if (emptyState) emptyState.style.display = 'none';

    tbody.innerHTML = list.map((api, index) => `
        <tr>
            <td><strong>0${index + 1}</strong></td>
            <td>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="row-avatar" style="width: 32px; height: 32px; border-radius: 8px; background: ${api.avatarColor || '#3b82f6'}; font-size: 0.85rem;">
                        <i class="fas ${api.avatarIcon || 'fa-plug'}"></i>
                    </div>
                    <strong>${escapeHtml(api.name)}</strong>
                </div>
            </td>
            <td class="url-cell" title="${escapeHtml(api.url)}">${escapeHtml(api.url)}</td>
            <td><span class="api-method-badge ${api.method}">${api.method}</span></td>
            <td><span class="status-badge ${(api.lastStatus || 'pending').toLowerCase()}">${api.lastStatus || 'Pending'}</span></td>
            <td>${formatDate(api.created_at)}</td>
            <td>
                <div class="action-btns">
                    <button class="action-btn check" onclick="checkSingleAPI(${api.id})" title="Check Endpoint">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="action-btn history" onclick="viewAPIHistory(${api.id})" title="View Log">
                        <i class="fas fa-history"></i>
                    </button>
                    <button class="action-btn delete" onclick="confirmDeleteAPI(${api.id})" title="Remove">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// ========== DELETE API MODAL ==========
let pendingDeleteId = null;

function confirmDeleteAPI(apiId) {
    const api = apiList.find(a => a.id === apiId);
    if (!api) return;

    pendingDeleteId = apiId;
    document.getElementById('modal-title').textContent = 'Confirm API Removal';
    document.getElementById('modal-message').textContent = `Are you sure you want to delete "${api.name}"? All associated performance logs will be removed.`;
    document.getElementById('confirm-modal')?.classList.add('active');
}

function deleteAPI(apiId) {
    const api = apiList.find(a => a.id === apiId);
    if (!api) return;

    const name = api.name;
    apiList = apiList.filter(a => a.id !== apiId);
    monitorHistory = monitorHistory.filter(h => h.api_id !== apiId);

    showToast('success', 'Endpoint Removed', `"${name}" was deleted.`);
    renderAPITable();
    updateDashboardMetrics();
    renderActivityRows();
}

document.getElementById('modal-confirm')?.addEventListener('click', () => {
    if (pendingDeleteId !== null) {
        deleteAPI(pendingDeleteId);
        pendingDeleteId = null;
    }
    document.getElementById('confirm-modal')?.classList.remove('active');
});

document.getElementById('modal-cancel')?.addEventListener('click', () => {
    pendingDeleteId = null;
    document.getElementById('confirm-modal')?.classList.remove('active');
});

document.getElementById('modal-close')?.addEventListener('click', () => {
    pendingDeleteId = null;
    document.getElementById('confirm-modal')?.classList.remove('active');
});

// ========== LIVE MONITOR CARDS ==========
function renderMonitorCards() {
    const container = document.getElementById('monitor-grid');
    const emptyState = document.getElementById('monitor-empty');
    if (!container) return;

    if (apiList.length === 0) {
        container.style.display = 'none';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }

    container.style.display = 'grid';
    if (emptyState) emptyState.style.display = 'none';

    container.innerHTML = apiList.map(api => {
        const latestCheck = monitorHistory
            .filter(h => h.api_id === api.id)
            .sort((a, b) => new Date(b.checked_at) - new Date(a.checked_at))[0];

        const statusClass = (api.lastStatus || 'pending').toLowerCase();
        const responseTime = latestCheck ? latestCheck.response_time : '—';
        const statusCode = latestCheck ? (latestCheck.status_code === 0 ? 'ERR' : latestCheck.status_code) : '—';
        const lastChecked = latestCheck ? formatDate(latestCheck.checked_at) : 'Never';

        return `
            <div class="monitor-card ${statusClass}" id="monitor-card-${api.id}">
                <div class="monitor-card-header">
                    <div class="monitor-api-info">
                        <span class="api-method-badge ${api.method}">${api.method}</span>
                        <span class="monitor-api-name">${escapeHtml(api.name)}</span>
                    </div>
                    <span class="status-badge ${statusClass}">${api.lastStatus || 'Pending'}</span>
                </div>
                <div class="monitor-card-body">
                    <div class="monitor-metrics">
                        <div>
                            <span class="monitor-metric-label">Latency</span>
                            <div class="monitor-metric-value" style="color: var(--coral-primary);">
                                ${responseTime === '—' ? '—' : responseTime + ' ms'}
                            </div>
                        </div>
                        <div>
                            <span class="monitor-metric-label">HTTP Code</span>
                            <div class="monitor-metric-value">${statusCode}</div>
                        </div>
                        <div>
                            <span class="monitor-metric-label">Last Checked</span>
                            <div class="monitor-metric-value" style="font-size: 0.88rem;">${lastChecked}</div>
                        </div>
                        <div>
                            <span class="monitor-metric-label">Category</span>
                            <div class="monitor-metric-value" style="font-size: 0.88rem;">${escapeHtml(api.category || 'REST')}</div>
                        </div>
                    </div>
                    <div class="monitor-card-actions">
                        <button class="btn btn-primary btn-sm" onclick="checkSingleAPI(${api.id})">
                            <i class="fas fa-play"></i> Ping Now
                        </button>
                        <button class="btn btn-outline btn-sm" onclick="viewAPIHistory(${api.id})">
                            <i class="fas fa-history"></i> History
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// ========== HISTORY TABLE ==========
function viewAPIHistory(apiId) {
    navigateTo('history');
    const filterSelect = document.getElementById('history-api-filter');
    if (filterSelect) {
        filterSelect.value = apiId.toString();
        renderHistoryTable();
    }
}

function populateHistoryFilters() {
    const apiFilter = document.getElementById('history-api-filter');
    if (!apiFilter) return;

    const currentValue = apiFilter.value;
    apiFilter.innerHTML = '<option value="all">All APIs</option>';
    apiList.forEach(api => {
        apiFilter.innerHTML += `<option value="${api.id}">${escapeHtml(api.name)}</option>`;
    });

    if (currentValue !== 'all' && apiList.some(a => a.id.toString() === currentValue)) {
        apiFilter.value = currentValue;
    }
}

function renderHistoryTable() {
    const tbody = document.getElementById('history-table-body');
    const emptyState = document.getElementById('history-empty');
    if (!tbody) return;

    const apiFilter = document.getElementById('history-api-filter')?.value || 'all';
    const statusFilter = document.getElementById('history-status-filter')?.value || 'all';

    let filtered = [...monitorHistory].sort((a, b) => new Date(b.checked_at) - new Date(a.checked_at));

    if (apiFilter !== 'all') filtered = filtered.filter(h => h.api_id.toString() === apiFilter);
    if (statusFilter !== 'all') filtered = filtered.filter(h => h.status === statusFilter);

    if (filtered.length === 0) {
        if (tbody.parentElement && tbody.parentElement.parentElement) tbody.parentElement.parentElement.style.display = 'none';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }

    if (tbody.parentElement && tbody.parentElement.parentElement) tbody.parentElement.parentElement.style.display = 'block';
    if (emptyState) emptyState.style.display = 'none';

    tbody.innerHTML = filtered.map((entry, index) => `
        <tr>
            <td><strong>0${index + 1}</strong></td>
            <td><strong>${escapeHtml(entry.api_name)}</strong></td>
            <td>
                <span class="api-method-badge ${entry.status_code === 200 ? 'GET' : 'DELETE'}">
                    ${entry.status_code === 0 ? 'ERR' : entry.status_code}
                </span>
            </td>
            <td style="font-weight: 800; color: ${entry.status === 'Healthy' ? 'var(--healthy)' : (entry.status === 'Slow' ? 'var(--slow)' : 'var(--failed)')}">
                ${entry.status === 'Failed' ? '—' : entry.response_time + ' ms'}
            </td>
            <td><span class="status-badge ${entry.status.toLowerCase()}">${entry.status}</span></td>
            <td>${formatDate(entry.checked_at)}</td>
        </tr>
    `).join('');
}

document.getElementById('history-api-filter')?.addEventListener('change', renderHistoryTable);
document.getElementById('history-status-filter')?.addEventListener('change', renderHistoryTable);

// ========== ANALYTICS PAGE CHARTS ==========
let analyticsRespInstance = null;
let analyticsDoughnutInstance = null;
let analyticsBarInstance = null;

function populateAnalyticsFilters() {
    const apiFilter = document.getElementById('analytics-api-filter');
    if (!apiFilter) return;

    const currentValue = apiFilter.value;
    apiFilter.innerHTML = '<option value="all">All APIs</option>';
    apiList.forEach(api => {
        apiFilter.innerHTML += `<option value="${api.id}">${escapeHtml(api.name)}</option>`;
    });

    if (currentValue !== 'all' && apiList.some(a => a.id.toString() === currentValue)) {
        apiFilter.value = currentValue;
    }
}

function updateAnalyticsStats() {
    const filter = document.getElementById('analytics-api-filter')?.value || 'all';
    let data = filter === 'all' ? monitorHistory : monitorHistory.filter(h => h.api_id.toString() === filter);

    const validChecks = data.filter(h => h.status !== 'Failed' && h.response_time > 0);
    const avgResponse = validChecks.length > 0
        ? Math.round(validChecks.reduce((sum, h) => sum + h.response_time, 0) / validChecks.length)
        : 0;

    const successCount = data.filter(h => h.status !== 'Failed').length;
    const failCount = data.filter(h => h.status === 'Failed').length;
    const slowest = validChecks.length > 0 ? Math.max(...validChecks.map(h => h.response_time)) : 0;

    document.getElementById('analytics-avg-response') && (document.getElementById('analytics-avg-response').textContent = `${avgResponse} ms`);
    document.getElementById('analytics-success-count') && (document.getElementById('analytics-success-count').textContent = successCount);
    document.getElementById('analytics-fail-count') && (document.getElementById('analytics-fail-count').textContent = failCount);
    document.getElementById('analytics-slowest') && (document.getElementById('analytics-slowest').textContent = `${slowest} ms`);
}

function renderAnalyticsCharts() {
    const isDark = document.body.classList.contains('dark-mode');
    const textColor = isDark ? '#9da4be' : '#575c75';
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.05)';

    // Bar Latency Chart
    const canvas1 = document.getElementById('response-time-chart');
    if (canvas1) {
        if (analyticsRespInstance) analyticsRespInstance.destroy();
        const recentHistory = [...monitorHistory].reverse().slice(-12);

        analyticsRespInstance = new Chart(canvas1, {
            type: 'bar',
            data: {
                labels: recentHistory.map(h => formatTimeShort(h.checked_at)),
                datasets: [{
                    label: 'Response Time (ms)',
                    data: recentHistory.map(h => h.response_time),
                    backgroundColor: recentHistory.map(h => h.status === 'Healthy' ? '#10b981' : (h.status === 'Slow' ? '#f59e0b' : '#ef4444')),
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { display: false }, ticks: { color: textColor } },
                    y: { grid: { color: gridColor }, ticks: { color: textColor } }
                }
            }
        });
        canvas1.parentElement.style.height = '280px';
    }

    // Doughnut Health Chart
    const canvas2 = document.getElementById('success-fail-chart');
    if (canvas2) {
        if (analyticsDoughnutInstance) analyticsDoughnutInstance.destroy();
        const healthy = monitorHistory.filter(h => h.status === 'Healthy').length;
        const slow = monitorHistory.filter(h => h.status === 'Slow').length;
        const failed = monitorHistory.filter(h => h.status === 'Failed').length;

        analyticsDoughnutInstance = new Chart(canvas2, {
            type: 'doughnut',
            data: {
                labels: ['Healthy', 'Slow', 'Failed'],
                datasets: [{
                    data: [healthy, slow, failed],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%'
            }
        });
    }

    // Comparison Chart
    const canvas3 = document.getElementById('api-comparison-chart');
    if (canvas3) {
        if (analyticsBarInstance) analyticsBarInstance.destroy();

        const stats = apiList.map(api => {
            const checks = monitorHistory.filter(h => h.api_id === api.id && h.status !== 'Failed');
            const avg = checks.length > 0 ? Math.round(checks.reduce((s, h) => s + h.response_time, 0) / checks.length) : 0;
            return { name: api.name, avg: avg };
        });

        analyticsBarInstance = new Chart(canvas3, {
            type: 'bar',
            data: {
                labels: stats.map(s => s.name),
                datasets: [{
                    label: 'Avg Response Time',
                    data: stats.map(s => s.avg),
                    backgroundColor: '#ff5e62',
                    borderRadius: 8
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { color: gridColor }, ticks: { color: textColor } },
                    y: { grid: { display: false }, ticks: { color: textColor } }
                }
            }
        });
        canvas3.parentElement.style.height = '240px';
    }
}

document.getElementById('analytics-api-filter')?.addEventListener('change', () => {
    updateAnalyticsStats();
    renderAnalyticsCharts();
});

// ========== TOAST NOTIFICATION ==========
function showToast(type, title, message) {
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-bolt'
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="toast-icon ${icons[type] || 'fas fa-info-circle'}"></i>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 250);
    }, 3800);
}

// ========== UTILITY FUNCTIONS ==========
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;

    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;

    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    });
}

function formatTimeShort(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
}

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', () => {
    refreshPageData('dashboard');
    renderAPITable();
    renderMonitorCards();
});
