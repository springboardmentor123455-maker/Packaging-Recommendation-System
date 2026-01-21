const API_KEY = "ECO2025";

let materialChart = null;
let productBubbleChart = null;


// ------------------------
// ECO STATUS LOGIC
// ------------------------
function ecoStatus(score) {
  if (score > 0.15) return "Highly Suitable";
  if (score > 0.08) return "Sustainable";
  if (score > 0.04) return "Moderate";
  return "Needs Improvement";
}

// ------------------------
// DOM READY
// ------------------------
document.addEventListener("DOMContentLoaded", () => {

  // Load products
  fetch("/products", { headers: { "x-api-key": API_KEY } })
    .then(r => r.json())
    .then(list => {
      const p = document.getElementById("product");
      list.forEach(x => {
        const o = document.createElement("option");
        o.text = x;
        o.value = x;
        p.add(o);
      });
    });

  // 🌍 GLOBAL ECO MATERIALS (WITH COST + CO2)
  fetch("/dashboard/global-materials", {
    headers: { "x-api-key": API_KEY }
  })
    .then(r => r.json())
    .then(data => {

      let html = `
        <tr>
          <th>#</th>
          <th>Material</th>
          <th>Eco Rank</th>
          <th>Estimated CO₂</th>
          <th>Estimated Cost (₹)</th>
        </tr>
      `;

      data.forEach((r, i) => {
      html += `
      <tr>
      <td>${i + 1}</td>
      <td>${r.material_name}</td>
      <td>${r.eco_rank}</td>
      <td>${r.co2_score}</td>
      <td>${r.estimated_cost}</td>
    </tr>
  `;
});


      document.getElementById("globalTable").innerHTML = html;
    });

  loadDashboard();
});

// ------------------------
// PRODUCT RECOMMENDATION
// ------------------------
function getRecommendations() {

  const product = document.getElementById("product").value;

  // 🔹 AI ranking
  fetch("/rank", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": API_KEY
    },
    body: JSON.stringify({ product_name: product })
  })
    .then(r => r.json())
    .then(data => {

      let html = `
        <tr>
          <th>#</th>
          <th>Material</th>
          <th>Suitability</th>
          <th>Estimated CO₂</th>
          <th>Estimated Cost (₹)</th>
        </tr>
      `;

      // 🔹 fetch ML cost + CO₂ estimates
      fetch(`/dashboard/product-materials?product=${product}`, {
        headers: { "x-api-key": API_KEY }
      })
        .then(r => r.json())
        .then(enriched => {
          
          enriched.forEach((r, i) => {
            html += `
              <tr>
                <td>${i + 1}</td>
                <td>${r.material_name}</td>
                <td>${r.Predicted_Suitability}</td>
                <td>${r.co2_score}</td>
                <td>${r.estimated_cost}</td>
              </tr>
            `;
          });
          renderProductBubbleChart(enriched);
          document.getElementById("productTable").innerHTML = html;

          if (!enriched || enriched.length === 0) {
  document.getElementById("metrics").innerHTML = `
    <div class="metric">⚠️ No recommendations available</div>
  `;
  return;
}

const best = enriched[0];

document.getElementById("metrics").innerHTML = `
  <div class="metric">🥇 Best Material<br>${best.material_name}</div>
  <div class="metric">📈 Suitability<br>${best.Predicted_Suitability}</div>
  <div class="metric">
    🌱 Eco Status<br>${ecoStatus(best.Predicted_Suitability)}
  </div>
`;


        });
    });
}

function renderProductBubbleChart(data) {

  const dataset = data.map(m => ({
    x: Number(m.estimated_cost.replace("₹", "")),
    y: m.co2_score,
    r: Math.max(m.Predicted_Suitability / 3, 12),
    label: m.material_name
  }));

  if (productBubbleChart) productBubbleChart.destroy();

  productBubbleChart = new Chart(
    document.getElementById("productBubbleChart"),
    {
      type: "bubble",
      data: {
        datasets: dataset.map(d => ({
          label: d.label,
          data: [{ x: d.x, y: d.y, r: d.r }]
        }))
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: ctx => {
                const d = ctx.raw;
                return `${ctx.dataset.label}
Cost: ₹${d.x}
CO₂: ${d.y}
Suitability: ${Math.round(d.r * 8)}`;
              }
            }
          }
        },
        scales: {
          x: {
            title: { display: true, text: "Estimated Cost (₹)" }
          },
          y: {
            title: { display: true, text: "Estimated CO₂ Impact" }
          }
        }
      }
    }
  );
}


// ------------------------
// DASHBOARD
// ------------------------
async function loadDashboard() {

  const metrics = await fetch("/dashboard/metrics", {
    headers: { "x-api-key": API_KEY }
  }).then(r => r.json());

  document.getElementById("ecoScore").innerText = metrics.avg_eco_score;
  document.getElementById("topMaterial").innerText = metrics.top_recommended_material;

  const sustainability = await fetch("/dashboard/sustainability-kpis", {
    headers: { "x-api-key": API_KEY }
  }).then(r => r.json());

  document.getElementById("co2Reduction").innerText =
    sustainability.avg_co2_reduction_pct + "%";

  document.getElementById("costSavings").innerText =
    sustainability.avg_cost_savings_pct + "%";

  // 📊 MATERIAL TREND CHART
  const materials = await fetch("/dashboard/material-trends", {
    headers: { "x-api-key": API_KEY }
  }).then(r => r.json());

  const labels = materials.map(m => m.material_name);
  const values = materials.map(m => Math.abs(m.Final_Rank_Score));


  if (materialChart) materialChart.destroy();

  materialChart = new Chart(document.getElementById("materialChart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: "#22c55e"
      }]
    },
    options: {
      plugins: { legend: { display: false } }
    }
  });

  // GLOBAL MATERIAL ANALYSIS
  await loadAllMaterialImpact();
}

// ------------------------
// GLOBAL MATERIAL IMPACT CHARTS
// ------------------------
async function loadAllMaterialImpact() {

  const data = await fetch("/dashboard/material-full-impact", {
    headers: { "x-api-key": API_KEY }
  }).then(r => r.json());

  const labels = data.map(d => d.material_name);
  const co2 = data.map(d => d.co2);
  const cost = data.map(d => d.cost);

  new Chart(document.getElementById("co2AllChart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "CO₂ Impact Index (Lower = Better)",
        data: co2
      }]
    },
    options: {
      indexAxis: "y"
    }
  });

  new Chart(document.getElementById("costAllChart"), {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Cost Index (₹)",
        data: cost,
        tension: 0.3
      }]
    }
  });
}

// ------------------------
// EXPORTS
// ------------------------
function downloadPDF() {
  const product = document.getElementById("product").value;

  fetch(`/dashboard/export/pdf?product=${product}`, {
    headers: { "x-api-key": API_KEY }
  })
  .then(res => res.blob())
  .then(blob => {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "EcoPack_Sustainability_Report.pdf";
    a.click();
  });
}

function downloadExcel() {
  const product = document.getElementById("product").value;

  fetch(`/dashboard/export/excel?product=${product}`, {
    headers: { "x-api-key": API_KEY }
  })
  .then(res => res.blob())
  .then(blob => {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "EcoPack_Sustainability_Report.xlsx";
    a.click();
  });
}
