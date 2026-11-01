document.addEventListener("DOMContentLoaded", () => {

    const analyzeBtn = document.getElementById("analyze-btn");
    const userEditor = document.getElementById("user-editor");
    const correctedEditor = document.getElementById("corrected-editor");
    const inputLines = document.getElementById("line-numbers");
    const outputLines = document.getElementById("output-lines");

    const scoreEl = document.querySelector(".score");

    const mcValues = document.querySelectorAll(".mc-value");
    const qualityVal = mcValues[0];
    const complexityVal = mcValues[1];
    const securityVal = mcValues[2];

    const fills = document.querySelectorAll(".fill");

    // ---------- Line numbers ----------
    function updateLineNumbers(text, target) {
        const count = Math.max(1, text.split("\n").length);
        let out = "";
        for (let i = 1; i <= count; i++) {
            out += i + "\n";
        }
        target.textContent = out;
    }

    userEditor.addEventListener("input", () => {
        updateLineNumbers(userEditor.value, inputLines);
    });

    userEditor.addEventListener("scroll", () => {
        inputLines.scrollTop = userEditor.scrollTop;
    });

    correctedEditor.addEventListener("scroll", () => {
        outputLines.scrollTop = correctedEditor.scrollTop;
    });

    updateLineNumbers("", inputLines);
    updateLineNumbers("", outputLines);

    // ---------- Analyze ----------
    async function analyzeCode() {

        const userCode = userEditor.value.trim();

        if (!userCode) {
            alert("Please enter some code before analyzing.");
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.innerText = "ANALYZING...";
        correctedEditor.textContent = "";
        updateLineNumbers("", outputLines);

        try {
            const response = await fetch("/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code: userCode })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                const msg = "Error: " + (data.detail || data.error || "Unknown error");
                correctedEditor.textContent = msg;
                updateLineNumbers(msg, outputLines);
                return;
            }

            // Corrected code
            correctedEditor.textContent = data.output;
            updateLineNumbers(data.output, outputLines);

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
            correctedEditor.textContent = "Error connecting to backend";
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerText = "ANALYZE";
        }
    }

    analyzeBtn.addEventListener("click", analyzeCode);

});
