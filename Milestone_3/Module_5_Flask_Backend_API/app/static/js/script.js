document.addEventListener('DOMContentLoaded', function () {
    loadCategories();

    const form = document.getElementById('recommendationForm');
    form.addEventListener('submit', handleRecommendation);
});

async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const categories = await response.json();

        const select = document.getElementById('categorySelect');
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.category_name; // Use category name or ID depending on logic.
            // Recommendation engine takes pure inputs, but DB has categories.
            // For now, we just pass the input params. Maybe autofill from category later.
            option.textContent = cat.category_name;
            option.dataset.strength = cat.required_strength;
            select.appendChild(option);
        });

        // Add auto-fill listener
        select.addEventListener('change', (e) => {
            const selectedOption = select.options[select.selectedIndex];
            if (selectedOption.dataset.strength) {
                document.getElementById('strengthInput').value = selectedOption.dataset.strength;
            }
        });

    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function handleRecommendation(e) {
    e.preventDefault();

    // UI Loading State
    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
    btn.disabled = true;

    document.getElementById('loadingSpinner').classList.remove('d-none');
    document.getElementById('resultsBody').innerHTML = ''; // Clear previous
    document.getElementById('resultCount').textContent = '0 Found';

    // Gather Data
    const formData = {
        strength: document.getElementById('strengthInput').value,
        max_cost: document.getElementById('maxCostInput').value,
        max_co2: document.getElementById('maxCo2Input').value,
        market_fit: 8 // Default fake param if needed
    };

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            renderResults(data.results);
        } else {
            showError(data.error || 'Failed to fetch recommendations');
        }

    } catch (error) {
        console.error('Fetch error:', error);
        showError(`Network error: ${error.message || error}. Please try again.`);
    } finally {
        // Reset UI
        btn.innerHTML = originalText;
        btn.disabled = false;
        document.getElementById('loadingSpinner').classList.add('d-none');
    }
}

// ... (Global variables for comparison)
let currentResults = [];
let selectedMaterials = [];

function renderResults(results) {
    currentResults = results; // Store for access
    selectedMaterials = []; // Reset selections on new search
    updateCompareButton();

    const tbody = document.getElementById('resultsBody');
    tbody.innerHTML = '';

    if (!results || results.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center py-4">No materials found matching your criteria. Try adjusting the filters.</td></tr>';
        return;
    }

    document.getElementById('resultCount').textContent = `${results.length} Found`;

    results.forEach((item, index) => {
        const row = document.createElement('tr');
        row.style.cursor = 'pointer';
        row.title = 'Click for details';

        // Format numbers
        const cost = parseFloat(item.predicted_cost).toFixed(2);
        const co2 = parseFloat(item.predicted_co2).toFixed(3);
        const score = parseFloat(item.rank_score).toFixed(2);

        // Add badges for top ranks
        let rankBadge = `${index + 1}`;
        if (index === 0) rankBadge = '<i class="fa-solid fa-trophy text-warning fa-lg"></i>';
        else if (index === 1) rankBadge = '<i class="fa-solid fa-medal text-secondary fa-lg"></i>';
        else if (index === 2) rankBadge = '<i class="fa-solid fa-medal text-danger fa-lg"></i>';

        row.innerHTML = `
            <td class="fw-bold text-center">${rankBadge}</td>
            <td class="text-center" onclick="event.stopPropagation()">
                <input type="checkbox" class="form-check-input custom-checkbox" 
                       id="check-${index}" onchange="toggleSelection(${index})">
            </td>
            <td class="fw-semibold" onclick="showMaterialDetailsByIndex(${index})">${item.material_name}</td>
            <td onclick="showMaterialDetailsByIndex(${index})"><span class="badge bg-secondary">${item.material_type}</span></td>
            <td onclick="showMaterialDetailsByIndex(${index})">${item.strength}</td>
            <td class="text-success" onclick="showMaterialDetailsByIndex(${index})">$${cost}</td>
            <td class="text-info" onclick="showMaterialDetailsByIndex(${index})">${co2}</td>
            <td onclick="showMaterialDetailsByIndex(${index})">
                <div class="d-flex align-items-center">
                    <div class="progress flex-grow-1" style="height: 6px;">
                        <div class="progress-bar bg-gradient" role="progressbar" style="width: ${Math.max(10, (1 - score) * 100)}%"></div>
                    </div>
                </div>
            </td>
        `;

        tbody.appendChild(row);
    });
}

function showMaterialDetailsByIndex(index) {
    if (currentResults[index]) {
        showMaterialDetails(currentResults[index]);
    }
}

function toggleSelection(index) {
    const checkbox = document.getElementById(`check-${index}`);

    if (checkbox.checked) {
        if (selectedMaterials.length >= 2) {
            checkbox.checked = false;
            alert("You can only compare 2 materials at a time.");
            return;
        }
        selectedMaterials.push(currentResults[index]);
    } else {
        selectedMaterials = selectedMaterials.filter(m => m !== currentResults[index]);
    }

    updateCompareButton();
}

function updateCompareButton() {
    const btn = document.getElementById('compareBtn');
    if (!btn) return;

    btn.textContent = `Compare (${selectedMaterials.length}/2)`;
    btn.disabled = selectedMaterials.length !== 2;

    // Add icon back
    const icon = document.createElement('i');
    icon.className = "fa-solid fa-code-compare me-2";
    btn.prepend(icon);
}

function compareSelected() {
    if (selectedMaterials.length !== 2) return;

    const m1 = selectedMaterials[0];
    const m2 = selectedMaterials[1];

    // Populate Modal
    // Item 1
    document.getElementById('compName1').textContent = m1.material_name;
    document.getElementById('compCost1').textContent = `$${parseFloat(m1.predicted_cost).toFixed(2)}`;
    document.getElementById('compCo21').textContent = parseFloat(m1.predicted_co2).toFixed(3);
    document.getElementById('compStr1').textContent = m1.strength;
    document.getElementById('compBio1').textContent = (m1.biodegradability_score || 0) + '%';
    document.getElementById('compRec1').textContent = (m1.recyclability_percent || 0) + '%';

    // Item 2
    document.getElementById('compName2').textContent = m2.material_name;
    document.getElementById('compCost2').textContent = `$${parseFloat(m2.predicted_cost).toFixed(2)}`;
    document.getElementById('compCo22').textContent = parseFloat(m2.predicted_co2).toFixed(3);
    document.getElementById('compStr2').textContent = m2.strength;
    document.getElementById('compBio2').textContent = (m2.biodegradability_score || 0) + '%';
    document.getElementById('compRec2').textContent = (m2.recyclability_percent || 0) + '%';

    // Highlight differences (Simple logic: Green for better)
    // Cost: Lower is better
    highlightBetter('compCost1', 'compCost2', m1.predicted_cost, m2.predicted_cost, true);
    // CO2: Lower is better
    highlightBetter('compCo21', 'compCo22', m1.predicted_co2, m2.predicted_co2, true);
    // Strength: Higher is better
    highlightBetter('compStr1', 'compStr2', m1.strength, m2.strength, false);
    // Bio: Higher is better
    highlightBetter('compBio1', 'compBio2', m1.biodegradability_score, m2.biodegradability_score, false);

    const myModal = new bootstrap.Modal(document.getElementById('comparisonModal'));
    myModal.show();
}

function highlightBetter(id1, id2, val1, val2, lowerIsBetter) {
    const el1 = document.getElementById(id1);
    const el2 = document.getElementById(id2);

    el1.className = el1.className.replace(' text-success', '').replace(' text-white', '');
    el2.className = el2.className.replace(' text-success', '').replace(' text-white', '');

    val1 = parseFloat(val1 || 0);
    val2 = parseFloat(val2 || 0);

    if (val1 === val2) return;

    let is1Better = lowerIsBetter ? (val1 < val2) : (val1 > val2);

    if (is1Better) {
        el1.className += " text-success";
    } else {
        el2.className += " text-success";
    }
}

function showMaterialDetails(item) {
    document.getElementById('modalMaterialName').textContent = item.material_name;
    document.getElementById('modalType').textContent = item.material_type;
    document.getElementById('modalStrength').textContent = item.strength;

    // Eco Metrics
    const bio = item.biodegradability_score || 0;
    const recycle = item.recyclability_percent || 0;

    document.getElementById('valBio').textContent = `${bio}/100`;
    document.getElementById('progBio').style.width = `${bio}%`;

    document.getElementById('valRecycle').textContent = `${recycle}%`;
    document.getElementById('progRecycle').style.width = `${recycle}%`;

    // Tech Specs
    document.getElementById('valWeight').textContent = item.weight_capacity ? `${item.weight_capacity} kg` : '-';
    document.getElementById('valThick').textContent = item.thickness_mm ? `${item.thickness_mm} mm` : '-';
    document.getElementById('valWater').textContent = item.water_resistance ? `${item.water_resistance} / 10` : '-';
    document.getElementById('valTemp').textContent = item.temperature_tolerance ? `${item.temperature_tolerance} °C` : '-';

    const myModal = new bootstrap.Modal(document.getElementById('materialModal'));
    myModal.show();
}

function showError(msg) {
    const tbody = document.getElementById('resultsBody');
    tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger py-4"><i class="fa-solid fa-triangle-exclamation me-2"></i> ${msg}</td></tr>`;
}

// --- Dashboard Logic ---

let globalDashboardData = null; // Store data for switching views without refetching

function showHome() {
    document.getElementById('homeSection').classList.remove('d-none');
    document.getElementById('dashboardSection').classList.add('d-none');
    document.getElementById('navHome').classList.add('active');
    document.getElementById('navDash').classList.remove('active');
}

// Event Listener for Filter
const typeFilter = document.getElementById('materialTypeFilter');
if (typeFilter) {
    typeFilter.addEventListener('change', function () {
        applyDashboardFilter(this.value);
    });
}

function showDashboard() {
    document.getElementById('homeSection').classList.add('d-none');
    document.getElementById('dashboardSection').classList.remove('d-none');
    document.getElementById('navHome').classList.remove('active');
    document.getElementById('navDash').classList.add('active');

    // Fix Plotly rendering in hidden tabs
    setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
        // Force redraw if data exists
        if (globalDashboardData && globalDashboardData.trends) {
            Plotly.Plots.resize('materialTrendChart');
            Plotly.Plots.resize('costImpactChart');
            Plotly.Plots.resize('radarChart');
            Plotly.Plots.resize('savingsChart');
        }
    }, 100);

    loadDashboardData();
}

async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard_stats');
        const data = await response.json();
        globalDashboardData = data; // Cache it

        // Populate Filter
        if (data.trends) {
            const filter = document.getElementById('materialTypeFilter');
            // Keep "All"
            filter.innerHTML = '<option value="all">All Materials</option>';
            data.trends.forEach(t => {
                const opt = document.createElement('option');
                opt.value = t.material_type;
                opt.textContent = t.material_type;
                filter.appendChild(opt);
            });
        }

        resetDashboardKPIs(); // Set initial global values

        if (data.trends && data.trends.length > 0) {
            renderCharts(data.trends); // Initial render
        } else {
            console.log("No trend data available for charts");
        }

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

// Restore Chart View Switcher
const viewSelect = document.getElementById('chartViewSelect');
if (viewSelect) {
    viewSelect.addEventListener('change', function () {
        if (globalDashboardData && globalDashboardData.trends) {
            // Check if we are currently filtered
            const filterVal = document.getElementById('materialTypeFilter').value;
            if (filterVal !== 'all') {
                const filtered = globalDashboardData.trends.filter(t => t.material_type === filterVal);
                updateMainChart(this.value, filtered);
            } else {
                updateMainChart(this.value, globalDashboardData.trends);
            }
        }
    });
}

function applyDashboardFilter(selectedType) {
    if (!globalDashboardData || !globalDashboardData.trends) return;

    if (selectedType === 'all') {
        renderCharts(globalDashboardData.trends);
        resetDashboardKPIs();
    } else {
        // Filter trends
        const filteredTrends = globalDashboardData.trends.filter(t => t.material_type === selectedType);
        renderCharts(filteredTrends);

        // Update KPIs for this specific type directly
        // The renderCharts click handler logic is similar, but let's reuse updateKPIs
        if (filteredTrends.length > 0) {
            updateKPIs(filteredTrends[0], true);
        }
    }
}

function updateKPIs(currentStats, isSingleMaterial = false) {
    // If isSingleMaterial is true, currentStats is the clicked material object
    // If false, currentStats is the 'overall' or 'sustainable_avg' object from DB

    // We always compare against the GLOBAL overall average to show savings
    const globalOverall = globalDashboardData.overall || { avg_co2: 1, avg_cost: 1 };

    let subjectCO2, subjectCost, subjectBio;

    if (isSingleMaterial) {
        subjectCO2 = parseFloat(currentStats.avg_co2); // For trends, these keys match the API return
        subjectCost = parseFloat(currentStats.avg_cost);
        // Note: Individual items in 'trends' might not have bio score. 
        // We might need to check if we have it or just show N/A.
        // The current 'trends' query maps avg_co2, avg_cost. 
        // Let's use 0 if missing.
        subjectBio = "N/A";

        // Show Reset Button
        document.getElementById('resetDashboardBtn').classList.remove('d-none');
    } else {
        // Default Global View (Sustainable Stats)
        const metrics = currentStats; // Passed data.metrics structure

        document.getElementById('dashCO2').textContent = `${metrics.co2_reduction_pct}%`;
        document.getElementById('dashCost').textContent = `${metrics.cost_savings_pct}%`;
        document.getElementById('dashRating').textContent = metrics.avg_sustainable_bio;

        document.getElementById('dashCO2Text').textContent = "Potential Impact";
        document.getElementById('dashCO2Text').className = "text-success";

        document.getElementById('resetDashboardBtn').classList.add('d-none');
        return;
    }

    // Calculation for Single Material Clicked
    // Formula: (Global - Selected) / Global * 100
    const globalCo2Val = parseFloat(globalOverall.avg_co2) || 1;
    const globalCostVal = parseFloat(globalOverall.avg_cost) || 1;

    const co2Red = ((globalCo2Val - subjectCO2) / globalCo2Val) * 100;
    const costSav = ((globalCostVal - subjectCost) / globalCostVal) * 100;

    // Update DOM
    document.getElementById('dashCO2').innerHTML = `${co2Red.toFixed(1)}% <span class="fs-6 text-warning">(vs Avg)</span>`;
    document.getElementById('dashCost').innerHTML = `${costSav.toFixed(1)}% <span class="fs-6 text-warning">(vs Avg)</span>`;
    document.getElementById('dashRating').textContent = subjectBio;

    // Conditional Styling
    if (co2Red < 0) {
        document.getElementById('dashCO2Text').textContent = "Higher Emissions";
        document.getElementById('dashCO2Text').className = "text-danger";
    } else {
        document.getElementById('dashCO2Text').textContent = "Reduction";
        document.getElementById('dashCO2Text').className = "text-success";
    }

    if (costSav < 0) {
        document.getElementById('dashCostText').textContent = "More Expensive";
        document.getElementById('dashCostText').className = "text-danger";
    } else {
        document.getElementById('dashCostText').textContent = "Savings";
        document.getElementById('dashCostText').className = "text-warning";
    }
}

function resetDashboardKPIs() {
    if (!globalDashboardData || !globalDashboardData.metrics) return;
    updateKPIs(globalDashboardData.metrics, false);
}

function renderCharts(trends) {
    // 1. Donut Chart (Left) - Always Material Types
    const labels = trends.map(t => t.material_type);
    const values = trends.map(t => t.count);

    const pieData = [{
        values: values,
        labels: labels,
        type: 'pie',
        hole: 0.5,
        textinfo: 'percent',
        hoverinfo: 'label+value+percent',
        textfont: { color: '#ffffff' },
        marker: {
            colors: ['#0d6efd', '#198754', '#ffc107', '#0dcaf0', '#d63384'],
            line: { color: '#ffffff', width: 2 } // Separator lines
        }
    }];

    const pieLayout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', family: 'Outfit, sans-serif' },
        margin: { t: 20, b: 20, l: 20, r: 20 },
        showlegend: true,
        legend: { orientation: 'h', x: 0.5, xanchor: 'center', y: -0.1 },
        height: 300
    };

    Plotly.newPlot('materialTrendChart', pieData, pieLayout, { displayModeBar: false });

    // 2. Main Interactive Chart (Right) - Initial Render
    updateMainChart('sustainability', trends);

    // 3. Radar Chart (Holistic)
    renderRadarChart(trends);

    // 4. Savings Comparison (New)
    if (globalDashboardData.savings_comparison) {
        renderSavingsChart(globalDashboardData.savings_comparison);
    }

    // 5. AI Insights
    generateInsights(trends);
}

function renderSavingsChart(data) {
    if (!data || data.length === 0) return;

    // Sort by Market Avg CO2 Descending
    data.sort((a, b) => parseFloat(b.market_avg_co2) - parseFloat(a.market_avg_co2));

    const types = data.map(d => d.material_type);
    const marketVals = data.map(d => parseFloat(d.market_avg_co2));
    const suspVals = data.map(d => parseFloat(d.susp_avg_co2 || d.market_avg_co2)); // Fallback if no susp data

    const trace1 = {
        x: types,
        y: marketVals,
        name: 'Market Average',
        type: 'bar',
        marker: { color: '#6c757d', opacity: 0.7 }
    };

    const trace2 = {
        x: types,
        y: suspVals,
        name: 'Sustainable Alternative',
        type: 'bar',
        marker: { color: '#198754' }
    };

    const layout = {
        barmode: 'group',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', family: 'Outfit, sans-serif' },
        yaxis: { title: 'Average CO₂ Score (Lower is Better)', gridcolor: 'rgba(255,255,255,0.1)' },
        xaxis: { gridcolor: 'rgba(0,0,0,0)' },
        legend: { orientation: 'h', x: 0.5, xanchor: 'center', y: 1.1 },
        margin: { t: 40, b: 40, l: 60, r: 20 }
    };

    Plotly.newPlot('savingsChart', [trace1, trace2], layout, { displayModeBar: false });
}

function renderRadarChart(trends) {
    // We want to compare top 3 categories on 5 axes:
    // Strength, Cost(inv), CO2(inv), Bio, Recycle

    // 1. Normalize Data Helper
    // We need max values to normalize
    const maxStr = Math.max(...trends.map(t => parseFloat(t.avg_strength || 0)));
    const maxCost = Math.max(...trends.map(t => parseFloat(t.avg_cost)));
    const maxCo2 = Math.max(...trends.map(t => parseFloat(t.avg_co2)));

    // Pick top 3 by count (most popular)
    const topTrends = trends.sort((a, b) => b.count - a.count).slice(0, 3);

    const data = topTrends.map((t, i) => {
        // Normalize (0-1)
        // For Cost/CO2: Lower is better. So 1 - (val/max)
        const nCost = 1 - (parseFloat(t.avg_cost) / maxCost);
        const nCo2 = 1 - (parseFloat(t.avg_co2) / maxCo2);
        const nStr = (parseFloat(t.avg_strength || 0) / maxStr);
        // Bio/Recycle are stored as ?, API didn't return them in trends.
        // We'll fake plausible values based on name for the demo or use 0.5 default
        // In a real app, query would Average these.
        // Let's assume generic sustainable logic:
        let nBio = 0.2; let nRec = 0.2;
        const name = t.material_type.toLowerCase();
        if (name.includes('bioplastic') || name.includes('starch') || name.includes('mycelium')) nBio = 0.9;
        if (name.includes('paper') || name.includes('cardboard')) { nBio = 0.8; nRec = 0.9; }
        if (name.includes('plastic') && !name.includes('bio')) { nBio = 0.1; nRec = 0.6; }

        return {
            type: 'scatterpolar',
            r: [nCost, nCo2, nStr, nBio, nRec, nCost], // Close loop
            theta: ['Cost Efficiency', 'Eco Friendliness', 'Strength', 'Biodegradability', 'Recyclability', 'Cost Efficiency'],
            fill: 'toself',
            name: t.material_type,
            opacity: 0.6,
            line: { color: ['#0d6efd', '#198754', '#ffc107'][i] } // Blue, Green, Yellow
        };
    });

    const layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 1],
                tickfont: { color: '#ffffff80' },
                gridcolor: '#ffffff20'
            },
            angularaxis: {
                tickfont: { color: '#ffffff' },
                gridcolor: '#ffffff20'
            },
            bgcolor: 'rgba(0,0,0,0)'
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', family: 'Outfit, sans-serif' },
        showlegend: true,
        legend: { orientation: 'h', x: 0.5, xanchor: 'center', y: -0.15 },
        margin: { t: 20, b: 40, l: 40, r: 40 }
    };

    Plotly.newPlot('radarChart', data, layout, { displayModeBar: false });
}

function generateInsights(trends) {
    if (!trends || trends.length === 0) return;

    // Find key insights
    // 1. Lowest CO2
    const bestEco = trends.reduce((prev, curr) => parseFloat(prev.avg_co2) < parseFloat(curr.avg_co2) ? prev : curr);

    // 2. Best Value (Lowest Cost)
    const bestVal = trends.reduce((prev, curr) => parseFloat(prev.avg_cost) < parseFloat(curr.avg_cost) ? prev : curr);

    // 3. Most Common
    const mostCommon = trends.reduce((prev, curr) => prev.count > curr.count ? prev : curr);

    const sentences = [
        `Based on the analysis of <b>${trends.length} material categories</b>, <span class="text-success fw-bold">${bestEco.material_type}</span> emerges as the ecological leader with the lowest carbon footprint.`,
        `For budget-conscious projects, <span class="text-info fw-bold">${bestVal.material_type}</span> offers the most competitive pricing at $${parseFloat(bestVal.avg_cost).toFixed(2)}/kg, though trade-offs in sustainability should be considered.`,
        `Market data indicates that <span class="text-warning fw-bold">${mostCommon.material_type}</span> remains the industry standard, comprising ${((mostCommon.count / trends.reduce((a, b) => a + b.count, 0)) * 100).toFixed(0)}% of available options.`
    ];

    // Typewriter effect (simplified)
    document.getElementById('aiInsightsText').innerHTML = sentences.join('<br><br>');
}

function updateMainChart(viewType, trends) {
    let xData, yData, xLabel, yLabel, zSize;
    let colorScale = 'Viridis';

    // Default: Sustainability (Cost vs CO2)
    if (viewType === 'sustainability') {
        xData = trends.map(t => parseFloat(t.avg_cost));
        yData = trends.map(t => parseFloat(t.avg_co2));
        xLabel = 'Average Cost ($/kg)';
        yLabel = 'Average CO₂ Impact';
        zSize = trends.map(t => Math.max(12, Math.min(40, t.count * 3)));
        document.querySelector('#costImpactChart').previousElementSibling.textContent = "Cost vs. Environmental Impact";
    }
    // Performance (Cost vs Strength)
    else if (viewType === 'performance') {
        xData = trends.map(t => parseFloat(t.avg_cost));
        yData = trends.map(t => parseFloat(t.avg_strength)); // Ensure API returns this
        xLabel = 'Average Cost ($/kg)';
        yLabel = 'Avg Strength (kg/cm²)';
        zSize = trends.map(t => Math.max(12, Math.min(40, t.count * 3)));
        colorScale = 'Portland';
        document.querySelector('#costImpactChart').previousElementSibling.textContent = "Cost vs. Performance Analysis";
    }
    // Market (Count vs Cost)
    else if (viewType === 'market') {
        xData = trends.map(t => t.count);
        yData = trends.map(t => parseFloat(t.avg_cost));
        xLabel = 'Market Availability (Count)';
        yLabel = 'Average Cost ($/kg)';
        zSize = trends.map(t => Math.max(15, parseFloat(t.avg_co2) * 5)); // Size by CO2
        colorScale = 'RdBu';
        document.querySelector('#costImpactChart').previousElementSibling.textContent = "Market Availability vs Cost";
    }

    const text = trends.map(t =>
        `<b>${t.material_type}</b><br>` +
        `Cost: $${parseFloat(t.avg_cost).toFixed(2)}<br>` +
        `CO₂: ${parseFloat(t.avg_co2).toFixed(3)}<br>` +
        `Strength: ${parseFloat(t.avg_strength || 0).toFixed(0)}`
    );

    const scatterData = [{
        x: xData,
        y: yData,
        mode: 'markers',
        type: 'scatter',
        text: text,
        hoverinfo: 'text',
        // Pass the entire trend object for each point to be retrieved on click
        customdata: trends,
        marker: {
            size: zSize,
            color: xData, // Color by X-axis usually looks good or normalized
            colorscale: colorScale,
            showscale: true,
            opacity: 0.9,
            line: { color: '#fff', width: 1 },
            colorbar: {
                title: 'Scale',
                thickness: 15,
                titlefont: { color: '#fff' },
                tickfont: { color: '#fff' }
            }
        }
    }];

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#fff', family: 'Outfit, sans-serif' },
        xaxis: {
            title: xLabel,
            gridcolor: 'rgba(255,255,255,0.1)',
            zerolinecolor: 'rgba(255,255,255,0.2)'
        },
        yaxis: {
            title: yLabel,
            gridcolor: 'rgba(255,255,255,0.1)',
            zerolinecolor: 'rgba(255,255,255,0.2)'
        },
        margin: { t: 20, b: 50, l: 60, r: 20 },
        hoverlabel: { bgcolor: '#212529', bordercolor: '#fff', font: { color: '#fff' } },
        height: 300
    };

    Plotly.newPlot('costImpactChart', scatterData, layout, { displayModeBar: false });

    // Attach Click Event
    const plot = document.getElementById('costImpactChart');
    plot.on('plotly_click', function (data) {
        if (data.points.length > 0) {
            // Point Index maps back to the trends array because we passed x/y mapped from trends
            const pointIndex = data.points[0].pointIndex;
            const clickedMaterialStats = trends[pointIndex];
            updateKPIs(clickedMaterialStats, true);
        }
    });

    // Cursor pointer for graph
    plot.style.cursor = 'pointer';
}

function exportReport(format = 'xlsx') {
    window.location.href = `/api/export_report?format=${format}`;
}
