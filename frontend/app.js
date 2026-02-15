const form = document.getElementById("ai-form");
const output = document.getElementById("output");
const button = document.getElementById("submit-btn");

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/service-worker.js")
    .then(() => console.log("Service Worker registered"))
    .catch(err => console.log("SW registration failed:", err));
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    button.disabled = true;
    button.textContent = "Generating...";

    const payload = {
        claim: document.getElementById("claim").value
    };

    const API_BASE = "https://psy-lnf4.onrender.com"

    try {
					const res = await fetch("/generate_question", {
        		console.log(res)
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
					});
					if (!res.ok) {
							throw new Error("Network response was not ok: " + res.status);
					}
        const data = await res.json();
        output.classList.add("visible");
        console.log("Received from backend:", data);
                // Display observation + question
        output.textContent = data.observation + (data.question ? " " + data.question : "");
    } catch (err) {
        output.textContent = "Error: " + err.message;
        output.classList.add("visible");
    } finally {
        button.disabled = false;
        button.textContent = "Generate Question";
    }
});

