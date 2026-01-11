function getRecommendations() {
    const weight = document.getElementById("productWeight").value;
    const strength = document.getElementById("strengthRequired").value;

    fetch("http://127.0.0.1:5000/api/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_weight: parseFloat(weight),
            strength_required: parseFloat(strength)
        })
    })
    .then(response => response.json())
    .then(data => {
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
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to fetch recommendations");
    });
}
