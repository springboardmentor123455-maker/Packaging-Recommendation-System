document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("btn").addEventListener("click", () => {
        getRecommendation();
    });

});

function getRecommendation() {

    const product = document.getElementById("product").value;
    const weight = document.getElementById("weight").value;
    const fragility = document.getElementById("fragility").value;

    fetch("http://127.0.0.1:5000/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            product_name: product,
            weight: weight,
            fragility: fragility
        })
    })
    .then(res => res.json())
    .then(data => {

        const table = document.getElementById("result");
        table.innerHTML = "";

        data.recommendations.forEach(item => {
            table.innerHTML += `
                <tr>
                    <td>${item.material_name}</td>
                    <td>${item.material_type}</td>
                    <td>${item.strength_kg}</td>
                    <td>${item.weight_g_per_m2}</td>
                    <td>${item.ai_score.toFixed(2)}</td>
                </tr>
            `;
        });

    })
    .catch(err => {
        alert("Backend error");
        console.error(err);
    });
}
