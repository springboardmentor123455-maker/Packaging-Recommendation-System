const API_BASE = "";



/* =========================
   GET RECOMMENDATIONS
   ========================= */
function getRecommendations() {

    // Read inputs
    const category = document.getElementById("productCategory").value;
    const weight = document.getElementById("productWeight").value;
    const strength = document.getElementById("strengthRequired").value;

    // Priority sliders
    const priorityStrength = document.getElementById("priorityStrength").value;
    const priorityCost = document.getElementById("priorityCost").value;
    const priorityCO2 = document.getElementById("priorityCO2").value;

    // Basic validation
    if (!category || !weight || !strength) {
        alert("Please fill all required fields");
        return;
    }

    fetch(`${API_BASE}/api/recommend`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_category: category,
            product_weight: parseFloat(weight),
            strength_required: parseFloat(strength),
            priority_strength: parseInt(priorityStrength),
            priority_cost: parseInt(priorityCost),
            priority_co2: parseInt(priorityCO2)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        return response.json();
    })

    .then(data => {

        if (data.status !== "success") {
            alert("Failed to get recommendations");
            return;
        }

        /* -------------------------
           TABLE: RECOMMENDATIONS
           ------------------------- */
        const table = document.getElementById("resultsTable");
        table.innerHTML = "";

        data.recommendations.forEach(item => {
            table.innerHTML += `
                <tr>
                    <td>${item.material_name}</td>
                    <td>${item.cost_per_kg}</td>
                    <td>${item.co2_emission_score}</td>
                    <td>${item.strength_mpa}</td>
                    <td>${item.material_score.toFixed(3)}</td>
                </tr>
            `;
        });

        /* -------------------------
           ANALYTICS SUMMARY
           ------------------------- */
        document.getElementById("costSavings").innerText =
            data.analytics.cost_savings_pct + " %";

        document.getElementById("co2Reduction").innerText =
            data.analytics.co2_reduction_pct + " %";

        /* -------------------------
           REFRESH CHARTS (NO CACHE)
           ------------------------- */
        const ts = new Date().getTime();

        document.getElementById("costChart").src =
            `${API_BASE}/charts/cost_comparison.png?t=${ts}`;

        document.getElementById("co2Chart").src =
            `${API_BASE}/charts/co2_comparison.png?t=${ts}`;

        document.getElementById("usageChart").src =
            `${API_BASE}/charts/material_usage.png?t=${ts}`;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to fetch recommendations");
    });
}

/* =========================
   DOWNLOAD PDF REPORT
   ========================= */
function getReport() {

    const payload = getInputPayload();

    fetch(`${API_BASE}/api/report`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.blob())
    .then(blob => {
        triggerDownload(blob, "EcoPackAI_Report.pdf");
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to generate report");
    });
}

/* =========================
   DOWNLOAD EXCEL REPORT
   ========================= */
function downloadExcel() {

    const payload = getInputPayload();

    fetch(`${API_BASE}/api/export/excel`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.blob())
    .then(blob => {
        triggerDownload(blob, "EcoPackAI_Report.xlsx");
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to download Excel");
    });
}

/* =========================
   INPUT PAYLOAD BUILDER
   ========================= */
function getInputPayload() {
    return {
        product_category: document.getElementById("productCategory").value,
        product_weight: parseFloat(document.getElementById("productWeight").value),
        strength_required: parseFloat(document.getElementById("strengthRequired").value),
        priority_strength: parseInt(document.getElementById("priorityStrength").value),
        priority_cost: parseInt(document.getElementById("priorityCost").value),
        priority_co2: parseInt(document.getElementById("priorityCO2").value)
    };
}

/* =========================
   FILE DOWNLOAD HELPER
   ========================= */
function triggerDownload(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}
