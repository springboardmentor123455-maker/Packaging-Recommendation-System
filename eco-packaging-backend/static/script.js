function getResults() {
    const weight = document.getElementById("weight").value;
    const fragility = document.getElementById("fragility").value;

    fetch("/material-decision", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            weight: weight,
            fragility: fragility,
            limit: 10
        })
    })
    .then(res => res.json())
    .then(data => {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";

        data.results.forEach((item, index) => {
            resultsDiv.innerHTML += `
                <div class="result-card">
                    <strong>#${index + 1} ${item.material}</strong>
                    <div>Sustainability Score: ${item.score}</div>
                </div>
            `;
        });
    });
}

function getReports() {
    // This triggers the backend route that sends the Excel file
    window.location.href = "/download-excel";
}