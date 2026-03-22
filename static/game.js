// Ontario Lawn Fertilizer Planner - JavaScript

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Deactivate all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Activate button
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Load data if needed
    if (tabName === 'calendar') {
        loadCalendar();
    } else if (tabName === 'history') {
        loadApplications();
    }
}

// Get Recommendations
async function getRecommendations() {
    const grassType = document.getElementById('grassType').value;
    const lawnHealth = document.getElementById('lawnHealth').value;
    const nitrogen = document.getElementById('nitrogen').value;
    const phosphorus = document.getElementById('phosphorus').value;
    const potassium = document.getElementById('potassium').value;
    const lawnSize = document.getElementById('lawnSize').value;

    const soilTest = `${nitrogen},${phosphorus},${potassium}`;

    try {
        const response = await fetch('/api/get-recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                grassType: grassType,
                lawnHealth: lawnHealth,
                soilTest: soilTest,
                lawnSize: lawnSize
            })
        });

        const data = await response.json();
        displayRecommendations(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error getting recommendations. Please try again.');
    }
}

function displayRecommendations(data) {
    const section = document.getElementById('recommendationsSection');
    
    // Show health info
    const healthDiv = document.getElementById('healthInfo');
    healthDiv.textContent = data.health_info;

    // Show soil adjustments if any
    const adjustDiv = document.getElementById('soilAdjustments');
    if (data.soil_adjustments.length > 0) {
        adjustDiv.innerHTML = '<strong>📌 Based on your soil test:</strong><br>' + 
            data.soil_adjustments.map(adj => '• ' + adj).join('<br>');
    } else {
        adjustDiv.innerHTML = '<strong>✅ Your soil is balanced!</strong><br>Follow standard recommendations.';
    }

    // Display recommendations
    const recList = document.getElementById('recommendationsList');
    recList.innerHTML = '';

    data.recommendations.forEach((rec, index) => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.innerHTML = `
            <div class="rec-header">
                <div>
                    <div class="rec-title">${rec.name}</div>
                    <p style="color: var(--text-light); margin-top: 5px;">${rec.description}</p>
                </div>
                <div class="rec-month">${rec.season}</div>
            </div>

            <div class="rec-details">
                <div class="rec-detail">
                    <div class="rec-label">NPK Ratio</div>
                    <div class="rec-value">${rec.npk}</div>
                </div>
                <div class="rec-detail">
                    <div class="rec-label">Rate</div>
                    <div class="rec-value">${rec.total_lbs} lbs</div>
                </div>
                <div class="rec-detail">
                    <div class="rec-label">Timing</div>
                    <div class="rec-value">${rec.timing}</div>
                </div>
            </div>

            <div>
                <strong style="color: var(--primary-green);">Why:</strong>
                <p style="margin-top: 5px; color: var(--text-light);">${rec.why}</p>
            </div>

            <div class="products-list">
                <strong>Recommended Products:</strong>
                <ul>
                    ${rec.products.map(p => `<li>${p}</li>`).join('')}
                </ul>
            </div>

            <button class="btn-secondary" onclick="prepareToLog('${rec.season}', '${rec.name}', ${rec.total_lbs})">
                Log This Application
            </button>
        `;
        recList.appendChild(card);
    });

    section.classList.remove('hidden');
    section.scrollIntoView({ behavior: 'smooth' });
}

// Prepare to log application
function prepareToLog(season, fertilizerName, amount) {
    document.getElementById('appSeason').value = season;
    document.getElementById('appFertilizer').value = fertilizerName;
    document.getElementById('appAmount').value = amount;
    switchTab('history');
}

// Save Application
async function saveApplication() {
    const season = document.getElementById('appSeason').value;
    const fertilizer = document.getElementById('appFertilizer').value;
    const amount = document.getElementById('appAmount').value;
    const notes = document.getElementById('appNotes').value;

    if (!season || !fertilizer || !amount) {
        alert('Please fill in all required fields');
        return;
    }

    try {
        const response = await fetch('/api/save-application', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                season: season,
                fertilizer: fertilizer,
                amount: amount,
                notes: notes
            })
        });

        const data = await response.json();
        if (data.success) {
            alert('Application logged successfully!');
            // Clear form
            document.getElementById('appSeason').value = '';
            document.getElementById('appFertilizer').value = '';
            document.getElementById('appAmount').value = '';
            document.getElementById('appNotes').value = '';
            loadApplications();
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error saving application. Please try again.');
    }
}

// Load Applications History
async function loadApplications() {
    try {
        const response = await fetch('/api/get-applications');
        const data = await response.json();
        displayApplications(data.applications);
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayApplications(applications) {
    const historyDiv = document.getElementById('appsHistoryDiv');
    const noAppsMsg = document.getElementById('noAppsMessage');

    if (applications.length === 0) {
        noAppsMsg.style.display = 'block';
        historyDiv.innerHTML = '';
        return;
    }

    noAppsMsg.style.display = 'none';
    historyDiv.innerHTML = '';

    applications.forEach(app => {
        const appDiv = document.createElement('div');
        appDiv.className = 'app-entry';
        
        const date = new Date(app.date);
        const dateStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();

        appDiv.innerHTML = `
            <div class="app-date">${app.season} - ${dateStr}</div>
            <div class="app-details">
                <div class="app-detail-item">
                    <div class="app-label">Fertilizer</div>
                    <div class="app-value">${app.fertilizer}</div>
                </div>
                <div class="app-detail-item">
                    <div class="app-label">Amount</div>
                    <div class="app-value">${app.amount} lbs</div>
                </div>
            </div>
            ${app.notes ? `<div class="app-notes"><strong>Notes:</strong> ${app.notes}</div>` : ''}
        `;
        historyDiv.appendChild(appDiv);
    });
}

// Load Calendar
async function loadCalendar() {
    try {
        const response = await fetch('/api/get-calendar');
        const data = await response.json();
        displayCalendar(data.calendar);
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayCalendar(calendar) {
    const calendarGrid = document.getElementById('calendarGrid');
    calendarGrid.innerHTML = '';

    const monthNames = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'];

    const grouped = {};
    calendar.forEach(item => {
        if (!grouped[item.month]) {
            grouped[item.month] = item;
        }
    });

    const months = [4, 5, 6, 7, 8, 9, 10, 11];
    months.forEach(month => {
        if (grouped[month]) {
            const item = grouped[month];
            const monthCard = document.createElement('div');
            monthCard.className = 'calendar-month';
            
            let icon = '📅';
            if (month === 4 || month === 5) icon = '🌱';
            else if (month === 6) icon = '☀️';
            else if (month === 7 || month === 8) icon = '🔥';
            else if (month === 9 || month === 10) icon = '🍂';
            else if (month === 11) icon = '❄️';

            monthCard.innerHTML = `
                <strong>${icon} ${monthNames[month]}</strong>
                <p><strong>Season:</strong> ${item.name}</p>
                <p><strong>Focus:</strong> ${item.description}</p>
            `;
            calendarGrid.appendChild(monthCard);
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Ontario Lawn Fertilizer Planner loaded');
});
