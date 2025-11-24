const generateBtn = document.getElementById("generate");
const promptEl = document.getElementById("prompt");
const resultEl = document.getElementById("result");
const resultArea = document.getElementById("result-area");
const statusEl = document.getElementById("status");
const maxLenEl = document.getElementById("max_length");

// URL da sua API Python (FastAPI)
/* API endpoint (use a secure backend to keep your API key secret; do NOT commit real keys in client-side code) */
const API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent";

/* Replace with your key or, preferably, have a backend inject it */
const API_KEY = "<REPLACE_WITH_YOUR_API_KEY_OR_USE_BACKEND>";

async function generate() {
  const prompt = promptEl.value.trim();
  if (!prompt) {
    statusEl.textContent = "Digite um prompt.";
    return;
  }

  statusEl.textContent = "Gerando... Aguarde!";
  generateBtn.disabled = true;
  resultArea.classList.add("hidden");

  try {
    const payload = {
      prompt,
      max_length: parseInt(maxLenEl.value, 10) || 120,
      mode: "brainstorm",
    };
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Erro desconhecido" }));
      throw new Error(err.detail || "Erro na requisição.");
    }
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-goog-api-key": API_KEY },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    statusEl.textContent = `Erro: ${e.message}`;
  } finally {
    generateBtn.disabled = false;
  }
}

generateBtn.addEventListener("click", generate);
