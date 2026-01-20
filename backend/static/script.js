function getRecommendation() {
    const product = document.getElementById("product").value;
    const weight = document.getElementById("weight").value;
    const fragility = document.getElementById("fragility").value;

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product: product,
            weight: weight,
            fragility: fragility
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = `
            <tr>
                <td>${data.material}</td>
                <td>${data.type}</td>
                <td>${data.strength}</td>
                <td>${data.weight}</td>
                <td>${data.score}</td>
            </tr>
        `;
    })
    .catch(error => {
        console.error(error);
        alert("Error occurred");
    });
}
