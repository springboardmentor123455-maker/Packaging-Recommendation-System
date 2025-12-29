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

function renderResults(results) {
    const tbody = document.getElementById('resultsBody');
    tbody.innerHTML = '';

    if (!results || results.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4">No materials found matching your criteria. Try adjusting the filters.</td></tr>';
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
            <td class="fw-semibold">${item.material_name}</td>
            <td><span class="badge bg-secondary">${item.material_type}</span></td>
            <td>${item.strength}</td>
            <td class="text-success">$${cost}</td>
            <td class="text-info">${co2}</td>
            <td>
                <div class="d-flex align-items-center">
                    <div class="progress flex-grow-1" style="height: 6px;">
                        <div class="progress-bar bg-gradient" role="progressbar" style="width: ${Math.max(10, (1 - score) * 100)}%"></div>
                    </div>
                </div>
            </td>
        `;

        // Add click event for modal
        row.addEventListener('click', () => showMaterialDetails(item));

        tbody.appendChild(row);
    });
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
