document.getElementById("symptoms-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const symptomsInput = document.getElementById("symptoms-input").value;
    const commonSymptoms = Array.from(document.getElementById("common-symptoms").selectedOptions)
        .map(option => option.value);

    const allSymptoms = symptomsInput.split(",").map(symptom => symptom.trim()).filter(symptom => symptom !== "");
    allSymptoms.push(...commonSymptoms);

    const conditions = getConditions(allSymptoms);

    const resultsSection = document.getElementById("results-section");
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // for Clearing previous results
    resultsSection.style.display = "block";

    if (conditions.length > 0) {
        conditions.forEach(condition => {
            const card = document.createElement("div");
            card.className = "result-card";
            card.textContent = condition;
            resultsDiv.appendChild(card);
        });
    } else {
        resultsDiv.innerHTML = "<p>No conditions found. Please refine your symptoms.</p>";
    }
});

function getConditions(symptoms) {
    // Dummy conditions for demonstration
    const conditionsMap = {
        headache: "Migraine",
        fever: "Influenza",
        nausea: "Food Poisoning",
        fatigue: "Chronic Fatigue Syndrome",
        cough: "Common Cold"
    };

    const conditions = new Set();
    symptoms.forEach(symptom => {
        if (conditionsMap[symptom.toLowerCase()]) {
            conditions.add(conditionsMap[symptom.toLowerCase()]);
        }
    });

    return Array.from(conditions);
}
