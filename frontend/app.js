const form = document.getElementById("ai-form");
const output = document.getElementById("output");
const button = document.getElementById("submit-btn");

const translations = {
  en: {
    title: "Psyche it",
    subtitle: "Analyze This",
    claimPlaceholder: "Enter the claim you want questioned…",
    generate: "Generate"
  },
  it: {
    title: "Psyche it",
    subtitle: "Analizza questo",
    claimPlaceholder: "Inserisci l'affermazione da mettere in discussione…",
    generate: "Genera"
  }
};

const langSelect = document.getElementById("lang-select");

// Load saved language or default to English
const savedLang = localStorage.getItem("lang") || "en";
langSelect.value = savedLang;
setLanguage(savedLang);

// When user changes language
langSelect.addEventListener("change", () => {
  const lang = langSelect.value;
  localStorage.setItem("lang", lang);
  setLanguage(lang);
});

function setLanguage(lang) {
  const dict = translations[lang];

  // Text content
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    if (dict[key]) el.textContent = dict[key];
  });

  // Placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.dataset.i18nPlaceholder;
    if (dict[key]) el.placeholder = dict[key];
  });

  // Optional: update HTML lang attribute
  document.documentElement.lang = lang;
}



if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/service-worker.js")
    .then(() => console.log("Service Worker registered"))
    .catch(err => console.log("SW registration failed:", err));
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    button.disabled = true;
    button.textContent = "Generating...";

    const claim = document.getElementById("claim").value
    const lang = localStorage.getItem("lang") || "en";

    const API_BASE = "https://psy-lnf4.onrender.com"

    try {
					const res = await fetch("/generate_question", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
							claim: claim,
							lang: lang   // 👈 send language to backend
						})
					});
					if (!res.ok) {
							throw new Error("Network response was not ok: " + res.status);
					}
        const data = await res.json();
        output.classList.add("visible");
        console.log("Received from backend:", data);
                // Display observation + question
        output.textContent = data.result;
    } catch (err) {
        output.textContent = "Error: " + err.message;
        output.classList.add("visible");
    } finally {
        button.disabled = false;
        button.textContent = "Generate Question";
    }
});

