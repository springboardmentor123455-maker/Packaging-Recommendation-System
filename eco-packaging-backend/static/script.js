function getResults() {
    const category = document.getElementById("category").value;
    const limit = document.getElementById("limit").value;

    fetch("/material-decision", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category, limit })
    })
    .then(res => res.json())
    .then(data => {
        const results = document.getElementById("results");
        results.innerHTML = "";

        data.forEach((item, index) => {
            let medal = index === 0 ? "🥇" :
                        index === 1 ? "🥈" :
                        index === 2 ? "🥉" : "";

            results.innerHTML += `
                <div class="card">
                    <span class="rank">${medal}</span>
                    <strong>${item.material_type}</strong>
                    <p>Score: ${item.score}</p>
                    <p>CO₂: ${item.co2_emission_score}</p>
                    <p>Recyclability: ${item.recyclability_percent}%</p>
                </div>
            `;
        });
    });
}
