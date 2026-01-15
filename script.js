document.addEventListener("DOMContentLoaded", () => {

    const analyzeBtn = document.getElementById("analyze-btn");
    const userEditor = document.getElementById("user-editor");
    const correctedEditor = document.getElementById("corrected-editor");

    const scoreEl = document.querySelector(".score");

    const qualityVal = document.querySelectorAll(".mc-value")[0];
    const complexityVal = document.querySelectorAll(".mc-value")[1];
    const securityVal = document.querySelectorAll(".mc-value")[2];

    const fills = document.querySelectorAll(".fill");

    async function analyzeCode() {

        const userCode = userEditor.value.trim();

        if (!userCode) {
            alert("Please enter some code before analyzing.");
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.innerText = "ANALYZING...";

        try {
            const response = await fetch("http://127.0.0.1:8000/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code: userCode })
            });

            const data = await response.json();

            if (!data.success) {
                correctedEditor.innerText = "Backend Error";
                return;
            }

            // Show corrected code
            correctedEditor.innerText = data.output;

            // Metrics
            const m = data.metrics;

            scoreEl.innerText = m.overall;

            qualityVal.innerText = m.quality;
            complexityVal.innerText = m.complexity;
            securityVal.innerText = m.security;

            fills[0].style.width = m.quality + "%";
            fills[1].style.width = m.complexity + "%";
            fills[2].style.width = m.security + "%";

        } catch (err) {
            console.error(err);
            correctedEditor.innerText = "Error connecting to backend";
        }

        analyzeBtn.disabled = false;
        analyzeBtn.innerText = "ANALYZE";
    }

    analyzeBtn.addEventListener("click", analyzeCode);

});
