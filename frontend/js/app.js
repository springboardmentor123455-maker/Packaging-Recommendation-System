document.getElementById("productForm").addEventListener("submit", function (e) {
    e.preventDefault();

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            weight: document.getElementById("weight").value,
            volume: document.getElementById("volume").value,
            fragility: document.getElementById("fragility").value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Backend error");
        }
        return response.json();
    })
    .then(data => {
        // Show result section
        document.getElementById("resultSection").style.display = "block";

        // Show recommended material
        document.getElementById("recommendedMaterial").innerText =
            "Material ID: " + data.best_material;

        // Show eco score
        document.getElementById("ecoScore").innerText =
            "Eco Score: " + data.best_eco_score;

        // Show REAL INR price
        document.getElementById("estimatedCost").innerText =
            "Relative Cost Score: " + data.best_price_inr;

        // OPTIONAL: show cost efficiency index (only if you added <p id="costIndex"> in HTML)
        if (document.getElementById("costIndex")) {
            document.getElementById("costIndex").innerText =
                "Cost Efficiency Index: " + data.best_cost_index;
        }

        // Fill ranking table
        let rows = "";
        data.ranking.forEach((item, index) => {
            rows += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${item.material}</td>
                    <td>₹${item.price_inr}</td>
                    <td>${item.co2}</td>
                    <td>${item.eco_score}</td>
                </tr>
            `;
        });

        document.getElementById("rankingTable").innerHTML = rows;
    })
    .catch(error => {
        console.error(error);
        alert("Error connecting frontend with backend");
    });
});
