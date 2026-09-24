/* ==========================================
   API MONITOR — PERFORMANCE DASHBOARD
   Frontend JavaScript (Mock Data Version)
   ========================================== */

// ========== MOCK DATA STORE ==========
// This simulates a database. Will be replaced with PHP/MySQL calls later.

let apiList = [
    { id: 1, name: 'JSONPlaceholder Users', url: 'https://jsonplaceholder.typicode.com/users', method: 'GET', created_at: '2026-09-20 10:30:00', lastStatus: 'Healthy' },
    { id: 2, name: 'GitHub API', url: 'https://api.github.com', method: 'GET', created_at: '2026-09-21 14:15:00', lastStatus: 'Healthy' },
    { id: 3, name: 'ReqRes API', url: 'https://reqres.in/api/users', method: 'GET', created_at: '2026-09-22 09:00:00', lastStatus: 'Slow' },
    { id: 4, name: 'HTTPBin Post', url: 'https://httpbin.org/post', method: 'POST', created_at: '2026-09-22 11:45:00', lastStatus: 'Healthy' },
    { id: 5, name: 'Fake Broken API', url: 'https://api.nonexistent-domain-xyz.com/data', method: 'GET', created_at: '2026-09-23 08:20:00', lastStatus: 'Failed' },
];

let monitorHistory = [
    { id: 1, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 142, status: 'Healthy', checked_at: '2026-09-24 15:30:00' },
    { id: 2, api_id: 2, api_name: 'GitHub API', status_code: 200, response_time: 289, status: 'Healthy', checked_at: '2026-09-24 15:30:05' },
    { id: 3, api_id: 3, api_name: 'ReqRes API', status_code: 200, response_time: 823, status: 'Slow', checked_at: '2026-09-24 15:30:10' },
    { id: 4, api_id: 4, api_name: 'HTTPBin Post', status_code: 200, response_time: 356, status: 'Healthy', checked_at: '2026-09-24 15:30:15' },
    { id: 5, api_id: 5, api_name: 'Fake Broken API', status_code: 0, response_time: 0, status: 'Failed', checked_at: '2026-09-24 15:30:20' },
    { id: 6, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 178, status: 'Healthy', checked_at: '2026-09-24 14:00:00' },
    { id: 7, api_id: 2, api_name: 'GitHub API', status_code: 200, response_time: 312, status: 'Healthy', checked_at: '2026-09-24 14:00:05' },
    { id: 8, api_id: 3, api_name: 'ReqRes API', status_code: 200, response_time: 1540, status: 'Slow', checked_at: '2026-09-24 14:00:10' },
    { id: 9, api_id: 4, api_name: 'HTTPBin Post', status_code: 200, response_time: 410, status: 'Healthy', checked_at: '2026-09-24 14:00:15' },
    { id: 10, api_id: 5, api_name: 'Fake Broken API', status_code: 0, response_time: 0, status: 'Failed', checked_at: '2026-09-24 14:00:20' },
    { id: 11, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 195, status: 'Healthy', checked_at: '2026-09-24 12:30:00' },
    { id: 12, api_id: 2, api_name: 'GitHub API', status_code: 200, response_time: 450, status: 'Healthy', checked_at: '2026-09-24 12:30:05' },
    { id: 13, api_id: 3, api_name: 'ReqRes API', status_code: 200, response_time: 690, status: 'Slow', checked_at: '2026-09-24 12:30:10' },
    { id: 14, api_id: 1, api_name: 'JSONPlaceholder Users', status_code: 200, response_time: 110, status: 'Healthy', checked_at: '2026-09-24 10:00:00' },
    { id: 15, api_id: 2, api_name: 'GitHub API', status_code: 200, response_time: 530, status: 'Slow', checked_at: '2026-09-24 10:00:05' },
];

let nextApiId = 6;
let nextHistoryId = 16;

// ========== DOM REFERENCES ==========
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');
const menuToggle = document.getElementById('menu-toggle');
const navLinks = document.querySelectorAll('.nav-link');
const pages = document.querySelectorAll('.page');
const toastContainer = document.getElementById('toast-container');

// ========== NAVIGATION ==========

/**
 * Navigate to a specific page
 * @param {string} pageName - The page to navigate to
 */
function navigateTo(pageName) {
    // Update nav links
    navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.page === pageName);
    });

    // Update pages
    pages.forEach(page => {
        page.classList.toggle('active', page.id === `page-${pageName}`);
    });

    // Close mobile sidebar
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');

    // Refresh page data
    refreshPageData(pageName);
}

// Navigation link clicks
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo(link.dataset.page);
    });
});

// "View All" links
document.querySelectorAll('.view-all-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo(link.dataset.page);
    });
});

// Mobile menu toggle
menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    sidebarOverlay.classList.toggle('active');
});

sidebarOverlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
});

// Mobile check all
document.getElementById('mobile-check-all').addEventListener('click', () => {
    checkAllAPIs();
});

// ========== DARK MODE TOGGLE ==========

function setTheme(isDark) {
    document.body.classList.toggle('dark-mode', isDark);

    // Update icons
    const icon = isDark ? 'fa-sun' : 'fa-moon';
    const oldIcon = isDark ? 'fa-moon' : 'fa-sun';

    const themeIcon = document.getElementById('theme-icon');
    const mobileIcon = document.getElementById('mobile-theme-icon');

    if (themeIcon) { themeIcon.classList.remove(oldIcon); themeIcon.classList.add(icon); }
    if (mobileIcon) { mobileIcon.classList.remove(oldIcon); mobileIcon.classList.add(icon); }

    // Save preference
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Re-render charts with new colors
    const activePage = document.querySelector('.page.active')?.id?.replace('page-', '');
    if (activePage === 'dashboard') renderDashboardChart();
    if (activePage === 'analytics') renderAnalyticsCharts();
}

// Toggle handlers
document.getElementById('theme-toggle').addEventListener('click', () => {
    setTheme(!document.body.classList.contains('dark-mode'));
});

document.getElementById('mobile-theme-toggle').addEventListener('click', () => {
    setTheme(!document.body.classList.contains('dark-mode'));
});

// Load saved theme on startup
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
            updateDashboardStats();
            renderRecentChecks();
            renderAPIStatusList();
            renderDashboardChart();
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

// ========== DASHBOARD ==========

function updateDashboardStats() {
    const total = apiList.length;
    const healthy = apiList.filter(a => a.lastStatus === 'Healthy').length;
    const slow = apiList.filter(a => a.lastStatus === 'Slow').length;
    const failed = apiList.filter(a => a.lastStatus === 'Failed').length;

    // Calculate average response time from recent checks (non-failed)
    const validChecks = monitorHistory.filter(h => h.status !== 'Failed' && h.response_time > 0);
    const avgResponse = validChecks.length > 0
        ? Math.round(validChecks.reduce((sum, h) => sum + h.response_time, 0) / validChecks.length)
        : 0;

    // Uptime percentage
    const totalChecks = monitorHistory.length;
    const successChecks = monitorHistory.filter(h => h.status !== 'Failed').length;
    const uptime = totalChecks > 0 ? Math.round((successChecks / totalChecks) * 100) : 0;

    // Animate stat values
    animateValue('stat-total-value', total);
    animateValue('stat-healthy-value', healthy);
    animateValue('stat-slow-value', slow);
    animateValue('stat-failed-value', failed);

    document.getElementById('stat-avg-value').innerHTML = `${avgResponse} <small>ms</small>`;
    document.getElementById('stat-uptime-value').innerHTML = `${uptime}<small>%</small>`;
}

/**
 * Animate a numeric value change
 */
function animateValue(elementId, endValue) {
    const el = document.getElementById(elementId);
    const startValue = parseInt(el.textContent) || 0;
    if (startValue === endValue) return;

    const duration = 500;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(startValue + (endValue - startValue) * eased);

        el.textContent = current;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function renderRecentChecks() {
    const container = document.getElementById('recent-checks-list');
    const emptyState = document.getElementById('recent-empty');

    // Get latest 8 checks
    const recent = [...monitorHistory]
        .sort((a, b) => new Date(b.checked_at) - new Date(a.checked_at))
        .slice(0, 8);

    if (recent.length === 0) {
        container.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    container.style.display = 'flex';
    emptyState.style.display = 'none';

    container.innerHTML = recent.map(check => `
        <div class="check-item">
            <div class="check-status-dot ${check.status.toLowerCase()}"></div>
            <div class="check-info">
                <div class="check-name">${escapeHtml(check.api_name)}</div>
                <div class="check-meta">${formatStatusCode(check.status_code)} · ${formatDate(check.checked_at)}</div>
            </div>
            <div class="check-time ${check.status.toLowerCase()}">
                ${check.status === 'Failed' ? 'FAIL' : check.response_time + ' ms'}
            </div>
        </div>
    `).join('');
}

function renderAPIStatusList() {
    const container = document.getElementById('api-status-list');
    const emptyState = document.getElementById('status-empty');

    if (apiList.length === 0) {
        container.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    container.style.display = 'flex';
    emptyState.style.display = 'none';

    container.innerHTML = apiList.map(api => `
        <div class="api-status-item">
            <span class="api-method-badge ${api.method}">${api.method}</span>
            <span class="api-status-name">${escapeHtml(api.name)}</span>
            <span class="status-badge ${api.lastStatus.toLowerCase()}">${api.lastStatus}</span>
        </div>
    `).join('');
}

// ========== DASHBOARD CHART ==========

// Helper: get colors based on current theme
function getChartColors() {
    const isDark = document.body.classList.contains('dark-mode');
    return {
        gridColor: isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
        tickColor: isDark ? '#94a3b8' : '#64748b',
        tooltipBg: isDark ? '#1e293b' : '#ffffff',
        tooltipTitle: isDark ? '#f1f5f9' : '#1e293b',
        tooltipBody: isDark ? '#94a3b8' : '#64748b',
        tooltipBorder: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
        legendColor: isDark ? '#94a3b8' : '#64748b',
    };
}

let dashboardChartInstance = null;

function renderDashboardChart() {
    const canvas = document.getElementById('dashboard-response-chart');
    if (!canvas) return;

    if (dashboardChartInstance) {
        dashboardChartInstance.destroy();
    }

    // Group history by check time (latest 6 rounds)
    const sortedHistory = [...monitorHistory].sort((a, b) => new Date(a.checked_at) - new Date(b.checked_at));

    // Get unique API names
    const apiNames = [...new Set(sortedHistory.map(h => h.api_name))];

    // Get unique check times (rounded to nearest batch)
    const checkTimes = [...new Set(sortedHistory.map(h => h.checked_at))].sort().slice(-8);

    const colors = ['#818cf8', '#34d399', '#fbbf24', '#f87171', '#c084fc', '#38bdf8', '#fb923c'];

    const datasets = apiNames.map((name, idx) => {
        const data = checkTimes.map(time => {
            const entry = sortedHistory.find(h => h.api_name === name && h.checked_at === time);
            return entry ? entry.response_time : null;
        });

        return {
            label: name,
            data: data,
            borderColor: colors[idx % colors.length],
            backgroundColor: colors[idx % colors.length] + '15',
            borderWidth: 2,
            tension: 0.4,
            fill: true,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: colors[idx % colors.length],
        };
    });

    const tc = getChartColors();

    dashboardChartInstance = new Chart(canvas, {
        type: 'line',
        data: {
            labels: checkTimes.map(t => formatTimeShort(t)),
            datasets: datasets,
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    labels: {
                        color: tc.legendColor,
                        font: { family: 'Inter', size: 11, weight: 500 },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        padding: 20,
                    },
                },
                tooltip: {
                    backgroundColor: tc.tooltipBg,
                    titleColor: tc.tooltipTitle,
                    bodyColor: tc.tooltipBody,
                    borderColor: tc.tooltipBorder,
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 10,
                    titleFont: { family: 'Inter', weight: 600 },
                    bodyFont: { family: 'Inter' },
                    callbacks: {
                        label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y} ms`
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: tc.gridColor, drawBorder: false },
                    ticks: { color: tc.tickColor, font: { family: 'Inter', size: 11 } },
                },
                y: {
                    grid: { color: tc.gridColor, drawBorder: false },
                    ticks: {
                        color: tc.tickColor,
                        font: { family: 'Inter', size: 11 },
                        callback: val => val + ' ms',
                    },
                    beginAtZero: true,
                },
            },
        },
    });

    // Set canvas parent height
    canvas.parentElement.style.height = '280px';
}

// ========== API MANAGEMENT ==========

// Form submit
document.getElementById('api-form').addEventListener('submit', (e) => {
    e.preventDefault();

    const nameInput = document.getElementById('api-name');
    const urlInput = document.getElementById('api-url');
    const methodInput = document.getElementById('api-method');

    const name = nameInput.value.trim();
    const url = urlInput.value.trim();
    const method = methodInput.value;

    // Validate
    if (!name || !url) {
        showToast('error', 'Validation Error', 'Please fill in all fields.');
        return;
    }

    // Check duplicate URL
    if (apiList.some(a => a.url.toLowerCase() === url.toLowerCase())) {
        showToast('warning', 'Duplicate API', 'An API with this URL already exists.');
        return;
    }

    // Add API
    const newApi = {
        id: nextApiId++,
        name: name,
        url: url,
        method: method,
        created_at: new Date().toISOString().slice(0, 19).replace('T', ' '),
        lastStatus: 'Pending',
    };

    apiList.push(newApi);

    // Clear form
    nameInput.value = '';
    urlInput.value = '';
    methodInput.value = 'GET';

    showToast('success', 'API Added', `"${name}" has been registered successfully.`);
    renderAPITable();
});

function renderAPITable() {
    const tbody = document.getElementById('api-table-body');
    const emptyState = document.getElementById('api-list-empty');
    const countBadge = document.getElementById('api-count-badge');

    countBadge.textContent = `${apiList.length} API${apiList.length !== 1 ? 's' : ''}`;

    if (apiList.length === 0) {
        tbody.parentElement.parentElement.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    tbody.parentElement.parentElement.style.display = 'block';
    emptyState.style.display = 'none';

    tbody.innerHTML = apiList.map((api, index) => `
        <tr>
            <td>${index + 1}</td>
            <td><strong>${escapeHtml(api.name)}</strong></td>
            <td class="url-cell" title="${escapeHtml(api.url)}">${escapeHtml(api.url)}</td>
            <td><span class="api-method-badge ${api.method}">${api.method}</span></td>
            <td><span class="status-badge ${(api.lastStatus || 'pending').toLowerCase()}">${api.lastStatus || 'Pending'}</span></td>
            <td>${formatDate(api.created_at)}</td>
            <td>
                <div class="action-btns">
                    <button class="action-btn check" onclick="checkSingleAPI(${api.id})" title="Check API">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="action-btn history" onclick="viewAPIHistory(${api.id})" title="View History">
                        <i class="fas fa-clock-rotate-left"></i>
                    </button>
                    <button class="action-btn delete" onclick="confirmDeleteAPI(${api.id})" title="Delete API">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// ========== DELETE API ==========

let pendingDeleteId = null;

function confirmDeleteAPI(apiId) {
    const api = apiList.find(a => a.id === apiId);
    if (!api) return;

    pendingDeleteId = apiId;

    document.getElementById('modal-title').textContent = 'Delete API';
    document.getElementById('modal-message').textContent = `Are you sure you want to delete "${api.name}"? This will also remove all monitoring history for this API.`;

    const modal = document.getElementById('confirm-modal');
    modal.classList.add('active');
}

function deleteAPI(apiId) {
    const api = apiList.find(a => a.id === apiId);
    if (!api) return;

    const name = api.name;

    // Remove API
    apiList = apiList.filter(a => a.id !== apiId);

    // Remove related history
    monitorHistory = monitorHistory.filter(h => h.api_id !== apiId);

    showToast('success', 'API Deleted', `"${name}" has been removed.`);
    renderAPITable();
}

// Modal buttons
document.getElementById('modal-confirm').addEventListener('click', () => {
    if (pendingDeleteId !== null) {
        deleteAPI(pendingDeleteId);
        pendingDeleteId = null;
    }
    document.getElementById('confirm-modal').classList.remove('active');
});

document.getElementById('modal-cancel').addEventListener('click', () => {
    pendingDeleteId = null;
    document.getElementById('confirm-modal').classList.remove('active');
});

document.getElementById('modal-close').addEventListener('click', () => {
    pendingDeleteId = null;
    document.getElementById('confirm-modal').classList.remove('active');
});

// Close modal on overlay click
document.getElementById('confirm-modal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
        pendingDeleteId = null;
        e.currentTarget.classList.remove('active');
    }
});

// ========== MONITOR ==========

function renderMonitorCards() {
    const container = document.getElementById('monitor-grid');
    const emptyState = document.getElementById('monitor-empty');

    if (apiList.length === 0) {
        container.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    container.style.display = 'grid';
    emptyState.style.display = 'none';

    container.innerHTML = apiList.map(api => {
        // Get latest check for this API
        const latestCheck = monitorHistory
            .filter(h => h.api_id === api.id)
            .sort((a, b) => new Date(b.checked_at) - new Date(a.checked_at))[0];

        const statusClass = (api.lastStatus || 'pending').toLowerCase();
        const responseTime = latestCheck ? latestCheck.response_time : '—';
        const statusCode = latestCheck ? formatStatusCode(latestCheck.status_code) : '—';
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
                        <div class="monitor-metric">
                            <span class="monitor-metric-label">Response Time</span>
                            <span class="monitor-metric-value" id="metric-time-${api.id}">
                                ${responseTime === '—' ? '—' : responseTime + ' ms'}
                            </span>
                        </div>
                        <div class="monitor-metric">
                            <span class="monitor-metric-label">Status Code</span>
                            <span class="monitor-metric-value" id="metric-code-${api.id}">${statusCode}</span>
                        </div>
                        <div class="monitor-metric">
                            <span class="monitor-metric-label">Last Checked</span>
                            <span class="monitor-metric-value" style="font-size: 0.82rem;" id="metric-last-${api.id}">${lastChecked}</span>
                        </div>
                        <div class="monitor-metric">
                            <span class="monitor-metric-label">URL</span>
                            <span class="monitor-metric-value" style="font-size: 0.72rem; color: var(--text-secondary); word-break: break-all;">${escapeHtml(api.url)}</span>
                        </div>
                    </div>
                    <div class="monitor-card-actions">
                        <button class="btn btn-success btn-sm" onclick="checkSingleAPI(${api.id})">
                            <i class="fas fa-play"></i> Check
                        </button>
                        <button class="btn btn-outline btn-sm" onclick="viewAPIHistory(${api.id})">
                            <i class="fas fa-chart-line"></i> History
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Simulate checking a single API
 * In the real version, this will call the PHP backend
 */
function checkSingleAPI(apiId) {
    const api = apiList.find(a => a.id === apiId);
    if (!api) return;

    // Show loading state on monitor card
    const card = document.getElementById(`monitor-card-${apiId}`);
    if (card) {
        const checkBtn = card.querySelector('.btn-success');
        if (checkBtn) {
            checkBtn.disabled = true;
            checkBtn.innerHTML = '<span class="spinner"></span> Checking...';
        }
    }

    // Simulate API check with random delay
    const simulatedDelay = Math.random() * 1500 + 200; // 200-1700ms

    setTimeout(() => {
        let statusCode, responseTime, status;

        // Simulate different outcomes
        if (api.url.includes('nonexistent') || api.url.includes('invalid')) {
            // Failed API
            statusCode = 0;
            responseTime = 0;
            status = 'Failed';
        } else {
            // Simulate response time
            responseTime = Math.round(Math.random() * 800 + 50); // 50-850ms
            statusCode = 200;

            // Classify health
            if (responseTime < 500) {
                status = 'Healthy';
            } else if (responseTime <= 2000) {
                status = 'Slow';
            } else {
                status = 'Failed';
            }
        }

        // Create history entry
        const historyEntry = {
            id: nextHistoryId++,
            api_id: api.id,
            api_name: api.name,
            status_code: statusCode,
            response_time: responseTime,
            status: status,
            checked_at: new Date().toISOString().slice(0, 19).replace('T', ' '),
        };

        monitorHistory.push(historyEntry);

        // Update API last status
        api.lastStatus = status;

        // Show toast
        if (status === 'Healthy') {
            showToast('success', 'API Healthy', `${api.name} responded in ${responseTime}ms`);
        } else if (status === 'Slow') {
            showToast('warning', 'API Slow', `${api.name} responded in ${responseTime}ms`);
        } else {
            showToast('error', 'API Failed', `${api.name} is not responding`);
        }

        // Refresh current page
        const activePage = document.querySelector('.page.active')?.id?.replace('page-', '');
        if (activePage) {
            refreshPageData(activePage);
        }
    }, simulatedDelay);
}

/**
 * Check all APIs sequentially
 */
function checkAllAPIs() {
    if (apiList.length === 0) {
        showToast('info', 'No APIs', 'Add some APIs first before checking.');
        return;
    }

    showToast('info', 'Checking All', `Running checks on ${apiList.length} APIs...`);

    apiList.forEach((api, index) => {
        setTimeout(() => {
            checkSingleAPI(api.id);
        }, index * 600); // Stagger checks
    });
}

// Check All buttons
document.getElementById('btn-check-all-dashboard').addEventListener('click', checkAllAPIs);
document.getElementById('btn-check-all-monitor').addEventListener('click', checkAllAPIs);

// ========== VIEW API HISTORY ==========

function viewAPIHistory(apiId) {
    // Navigate to history page with filter
    navigateTo('history');

    // Set filter to this API
    const filterSelect = document.getElementById('history-api-filter');
    filterSelect.value = apiId.toString();
    renderHistoryTable();
}

// ========== HISTORY ==========

function populateHistoryFilters() {
    const apiFilter = document.getElementById('history-api-filter');
    const currentValue = apiFilter.value;

    // Clear and rebuild
    apiFilter.innerHTML = '<option value="all">All APIs</option>';
    apiList.forEach(api => {
        apiFilter.innerHTML += `<option value="${api.id}">${escapeHtml(api.name)}</option>`;
    });

    // Restore selection if still valid
    if (currentValue !== 'all' && apiList.some(a => a.id.toString() === currentValue)) {
        apiFilter.value = currentValue;
    }
}

function renderHistoryTable() {
    const tbody = document.getElementById('history-table-body');
    const emptyState = document.getElementById('history-empty');
    const apiFilter = document.getElementById('history-api-filter').value;
    const statusFilter = document.getElementById('history-status-filter').value;

    let filtered = [...monitorHistory].sort((a, b) => new Date(b.checked_at) - new Date(a.checked_at));

    if (apiFilter !== 'all') {
        filtered = filtered.filter(h => h.api_id.toString() === apiFilter);
    }

    if (statusFilter !== 'all') {
        filtered = filtered.filter(h => h.status === statusFilter);
    }

    if (filtered.length === 0) {
        tbody.parentElement.parentElement.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    tbody.parentElement.parentElement.style.display = 'block';
    emptyState.style.display = 'none';

    tbody.innerHTML = filtered.map((entry, index) => `
        <tr>
            <td>${index + 1}</td>
            <td><strong>${escapeHtml(entry.api_name)}</strong></td>
            <td>
                <span class="status-code-display ${getStatusCodeClass(entry.status_code)}">
                    ${formatStatusCode(entry.status_code)}
                </span>
            </td>
            <td class="check-time ${entry.status.toLowerCase()}">
                ${entry.status === 'Failed' ? '—' : entry.response_time + ' ms'}
            </td>
            <td><span class="status-badge ${entry.status.toLowerCase()}">${entry.status}</span></td>
            <td>${formatDate(entry.checked_at)}</td>
        </tr>
    `).join('');
}

// History filter events
document.getElementById('history-api-filter').addEventListener('change', renderHistoryTable);
document.getElementById('history-status-filter').addEventListener('change', renderHistoryTable);

// ========== ANALYTICS ==========

function populateAnalyticsFilters() {
    const apiFilter = document.getElementById('analytics-api-filter');
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
    const filter = document.getElementById('analytics-api-filter').value;
    let data = filter === 'all'
        ? monitorHistory
        : monitorHistory.filter(h => h.api_id.toString() === filter);

    const validChecks = data.filter(h => h.status !== 'Failed' && h.response_time > 0);
    const avgResponse = validChecks.length > 0
        ? Math.round(validChecks.reduce((sum, h) => sum + h.response_time, 0) / validChecks.length)
        : 0;

    const successCount = data.filter(h => h.status !== 'Failed').length;
    const failCount = data.filter(h => h.status === 'Failed').length;
    const slowest = validChecks.length > 0
        ? Math.max(...validChecks.map(h => h.response_time))
        : 0;

    document.getElementById('analytics-avg-response').textContent = avgResponse + ' ms';
    document.getElementById('analytics-success-count').textContent = successCount;
    document.getElementById('analytics-fail-count').textContent = failCount;
    document.getElementById('analytics-slowest').textContent = slowest + ' ms';
}

// Analytics charts instances
let responseTimeChartInstance = null;
let successFailChartInstance = null;
let apiComparisonChartInstance = null;

function renderAnalyticsCharts() {
    renderResponseTimeChart();
    renderSuccessFailChart();
    renderAPIComparisonChart();
}

function renderResponseTimeChart() {
    const canvas = document.getElementById('response-time-chart');
    if (responseTimeChartInstance) responseTimeChartInstance.destroy();

    const filter = document.getElementById('analytics-api-filter').value;
    let data = filter === 'all'
        ? monitorHistory
        : monitorHistory.filter(h => h.api_id.toString() === filter);

    // Sort chronologically
    data = [...data].sort((a, b) => new Date(a.checked_at) - new Date(b.checked_at));

    const labels = data.map(h => formatTimeShort(h.checked_at));
    const values = data.map(h => h.response_time);
    const colors = data.map(h => {
        if (h.status === 'Healthy') return '#34d399';
        if (h.status === 'Slow') return '#fbbf24';
        return '#f87171';
    });

    const tc = getChartColors();

    responseTimeChartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Response Time (ms)',
                data: values,
                backgroundColor: colors.map(c => c + '40'),
                borderColor: colors,
                borderWidth: 1.5,
                borderRadius: 6,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: tc.tooltipBg,
                    titleColor: tc.tooltipTitle,
                    bodyColor: tc.tooltipBody,
                    borderColor: tc.tooltipBorder,
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 10,
                    titleFont: { family: 'Inter', weight: 600 },
                    bodyFont: { family: 'Inter' },
                    callbacks: {
                        title: (items) => {
                            const idx = items[0].dataIndex;
                            return data[idx]?.api_name || '';
                        },
                        label: ctx => `Response: ${ctx.parsed.y} ms`
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: tc.gridColor, drawBorder: false },
                    ticks: { color: tc.tickColor, font: { family: 'Inter', size: 10 }, maxRotation: 45 },
                },
                y: {
                    grid: { color: tc.gridColor, drawBorder: false },
                    ticks: {
                        color: tc.tickColor,
                        font: { family: 'Inter', size: 11 },
                        callback: val => val + ' ms',
                    },
                    beginAtZero: true,
                },
            },
        },
    });

    canvas.parentElement.style.height = '300px';
}

function renderSuccessFailChart() {
    const canvas = document.getElementById('success-fail-chart');
    if (successFailChartInstance) successFailChartInstance.destroy();

    const filter = document.getElementById('analytics-api-filter').value;
    let data = filter === 'all'
        ? monitorHistory
        : monitorHistory.filter(h => h.api_id.toString() === filter);

    const healthy = data.filter(h => h.status === 'Healthy').length;
    const slow = data.filter(h => h.status === 'Slow').length;
    const failed = data.filter(h => h.status === 'Failed').length;

    const tc = getChartColors();

    successFailChartInstance = new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Healthy', 'Slow', 'Failed'],
            datasets: [{
                data: [healthy, slow, failed],
                backgroundColor: ['#16a34a40', '#ca8a0440', '#dc262640'],
                borderColor: ['#16a34a', '#ca8a04', '#dc2626'],
                borderWidth: 2,
                hoverOffset: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: tc.legendColor,
                        font: { family: 'Inter', size: 12, weight: 500 },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        padding: 16,
                    },
                },
                tooltip: {
                    backgroundColor: tc.tooltipBg,
                    titleColor: tc.tooltipTitle,
                    bodyColor: tc.tooltipBody,
                    borderColor: tc.tooltipBorder,
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 10,
                    titleFont: { family: 'Inter', weight: 600 },
                    bodyFont: { family: 'Inter' },
                }
            },
        },
    });
}

function renderAPIComparisonChart() {
    const canvas = document.getElementById('api-comparison-chart');
    if (apiComparisonChartInstance) apiComparisonChartInstance.destroy();

    // Calculate avg response time per API
    const apiStats = apiList.map(api => {
        const checks = monitorHistory.filter(h => h.api_id === api.id && h.status !== 'Failed');
        const avg = checks.length > 0
            ? Math.round(checks.reduce((sum, h) => sum + h.response_time, 0) / checks.length)
            : 0;
        return { name: api.name, avg: avg };
    });

    const colors = ['#818cf8', '#34d399', '#fbbf24', '#f87171', '#c084fc', '#38bdf8', '#fb923c'];

    const tc = getChartColors();

    apiComparisonChartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: apiStats.map(s => s.name),
            datasets: [{
                label: 'Avg Response Time (ms)',
                data: apiStats.map(s => s.avg),
                backgroundColor: apiStats.map((_, i) => colors[i % colors.length] + '30'),
                borderColor: apiStats.map((_, i) => colors[i % colors.length]),
                borderWidth: 2,
                borderRadius: 6,
                borderSkipped: false,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: tc.tooltipBg,
                    titleColor: tc.tooltipTitle,
                    bodyColor: tc.tooltipBody,
                    borderColor: tc.tooltipBorder,
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 10,
                    titleFont: { family: 'Inter', weight: 600 },
                    bodyFont: { family: 'Inter' },
                    callbacks: {
                        label: ctx => `Average: ${ctx.parsed.x} ms`
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: tc.gridColor, drawBorder: false },
                    ticks: {
                        color: tc.tickColor,
                        font: { family: 'Inter', size: 11 },
                        callback: val => val + ' ms',
                    },
                    beginAtZero: true,
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        color: tc.tickColor,
                        font: { family: 'Inter', size: 12, weight: 600 },
                    },
                },
            },
        },
    });

    canvas.parentElement.style.height = Math.max(200, apiStats.length * 60) + 'px';
}

// Analytics filter change
document.getElementById('analytics-api-filter').addEventListener('change', () => {
    updateAnalyticsStats();
    renderAnalyticsCharts();
});

// ========== TOAST NOTIFICATIONS ==========

/**
 * Show a toast notification
 * @param {'success'|'error'|'warning'|'info'} type
 * @param {string} title
 * @param {string} message
 */
function showToast(type, title, message) {
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle',
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="toast-icon ${icons[type]}"></i>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="removeToast(this.parentElement)">&times;</button>
    `;

    toastContainer.appendChild(toast);

    // Auto remove after 4 seconds
    setTimeout(() => {
        removeToast(toast);
    }, 4000);
}

function removeToast(toast) {
    if (!toast || toast.classList.contains('removing')) return;
    toast.classList.add('removing');
    setTimeout(() => toast.remove(), 300);
}

// ========== UTILITY FUNCTIONS ==========

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatStatusCode(code) {
    if (code === 0) return 'ERR';
    return code.toString();
}

function getStatusCodeClass(code) {
    if (code === 0) return 'failed';
    if (code >= 200 && code < 300) return 'healthy';
    if (code >= 300 && code < 400) return 'slow';
    return 'failed';
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;

    // Less than 1 minute
    if (diff < 60000) return 'Just now';

    // Less than 1 hour
    if (diff < 3600000) {
        const mins = Math.floor(diff / 60000);
        return `${mins}m ago`;
    }

    // Less than 24 hours
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours}h ago`;
    }

    // Otherwise show date
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

function formatTimeShort(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
    });
}

// ========== INITIALIZATION ==========

document.addEventListener('DOMContentLoaded', () => {
    // Load dashboard data on page load
    refreshPageData('dashboard');
    renderAPITable();
});
