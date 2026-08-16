const API_URL = "http://127.0.0.1:8000";

const calcBtn = document.getElementById("calcBtn");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");
const historyEl = document.getElementById("history");

calcBtn.addEventListener("click", async () => {
  errorEl.textContent = "";
  resultEl.textContent = "";

  const a = parseFloat(document.getElementById("numA").value);
  const b = parseFloat(document.getElementById("numB").value);
  const operator = document.getElementById("operator").value;

  if (Number.isNaN(a) || Number.isNaN(b)) {
    errorEl.textContent = "Enter both numbers.";
    return;
  }

  try {
    const response = await fetch(`${API_URL}/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ a, b, operator }),
    });

    const data = await response.json();

    if (!response.ok) {
      errorEl.textContent = data.detail || "Something went wrong.";
      return;
    }

    resultEl.textContent = `Result: ${data.result}`;
    loadHistory();
  } catch (err) {
    errorEl.textContent = "Could not reach the server. Is the backend running?";
  }
});

async function loadHistory() {
  const response = await fetch(`${API_URL}/history`);
  const data = await response.json();

  historyEl.innerHTML = "";
  data.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.a} ${symbolFor(item.operator)} ${item.b} = ${item.result}`;
    historyEl.appendChild(li);
  });
}

function symbolFor(operator) {
  return { add: "+", subtract: "−", multiply: "×", divide: "÷" }[operator] || operator;
}

loadHistory();
