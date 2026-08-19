const API_URL = "http://127.0.0.1:8000";

const resultEl = document.getElementById("result");
const expressionEl = document.getElementById("expression");
const errorEl = document.getElementById("error");
const historyEl = document.getElementById("history");
const calcBtn = document.getElementById("calcBtn");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");

let firstValue = "";
let secondValue = "";
let currentOperator = null;
let waitingForSecondValue = false;

const numberButtons = document.querySelectorAll(".key--number");
const operatorButtons = document.querySelectorAll(".key--operator");
const decimalButton = document.querySelector(".key--decimal");
const clearButton = document.querySelector('[data-action="clear"]');
const deleteButton = document.querySelector('[data-action="delete"]');
const sqrtButton = document.querySelector('[data-action="sqrt"]');

function updateDisplay() {
  const displayValue = secondValue || firstValue || "0";
  resultEl.textContent = displayValue;

  if (currentOperator && firstValue) {
    expressionEl.textContent = `${firstValue} ${symbolFor(currentOperator)}`;
  } else {
    expressionEl.textContent = firstValue || "0";
  }
}

function resetCalculatorState() {
  firstValue = "";
  secondValue = "";
  currentOperator = null;
  waitingForSecondValue = false;
  errorEl.textContent = "";
  updateDisplay();
}

function addDigit(value) {
  if (waitingForSecondValue) {
    secondValue = secondValue ? secondValue + value : value;
    updateDisplay();
    return;
  }

  if (currentOperator && !firstValue) {
    firstValue = "0";
  }

  firstValue = firstValue ? firstValue + value : value;
  updateDisplay();
}

function addDecimal() {
  if (waitingForSecondValue) {
    if (!secondValue) {
      secondValue = "0.";
    } else if (!secondValue.includes(".")) {
      secondValue += ".";
    }
    updateDisplay();
    return;
  }

  if (!firstValue) {
    firstValue = "0.";
  } else if (!firstValue.includes(".")) {
    firstValue += ".";
  }
  updateDisplay();
}

function setOperator(nextOperator) {
  errorEl.textContent = "";

  if (!firstValue) {
    return;
  }

  if (currentOperator && !waitingForSecondValue) {
    calculateFromInputs();
  }

  currentOperator = nextOperator;
  waitingForSecondValue = true;
  secondValue = "";
  expressionEl.textContent = `${firstValue} ${symbolFor(currentOperator)}`;
}

async function calculateFromInputs() {
  if (!firstValue || !currentOperator || !secondValue) {
    if (firstValue && currentOperator && !secondValue) {
      const a = parseFloat(firstValue);
      if (Number.isNaN(a)) {
        errorEl.textContent = "Please enter a valid number.";
      }
    }
    return;
  }

  const a = parseFloat(firstValue);
  const b = parseFloat(secondValue);

  if (Number.isNaN(a) || Number.isNaN(b)) {
    errorEl.textContent = "Please enter valid numbers.";
    return;
  }

  try {
    const response = await fetch(`${API_URL}/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ a, b, operator: currentOperator }),
    });

    const data = await response.json();

    if (!response.ok) {
      errorEl.textContent = data.detail || "Something went wrong.";
      return;
    }

    resultEl.textContent = formatValue(data.result);
    expressionEl.textContent = `${a} ${symbolFor(currentOperator)} ${b} =`;
    firstValue = formatValue(data.result);
    secondValue = "";
    currentOperator = null;
    waitingForSecondValue = false;
    await loadHistory();
  } catch (error) {
    errorEl.textContent = "Could not reach the server. Is the backend running?";
  }
}

function formatValue(value) {
  if (!Number.isFinite(value)) {
    return "Error";
  }

  const formatted = Number(value);
  return Number.isInteger(formatted) ? String(formatted) : formatted.toFixed(2).replace(/\.00$/, "").replace(/(\.\d)0$/, "$1");
}

function symbolFor(operator) {
  return { add: "+", subtract: "−", multiply: "×", divide: "÷", sqrt: "√" }[operator] || operator;
}

function formatHistoryItem(item) {
  if (item.operator === "sqrt") {
    return `√${formatValue(item.a)} = ${formatValue(item.result)}`;
  }

  return `${formatValue(item.a)} ${symbolFor(item.operator)} ${formatValue(item.b)} = ${formatValue(item.result)}`;
}

numberButtons.forEach((button) => {
  button.addEventListener("click", () => {
    addDigit(button.dataset.value);
  });
});

decimalButton.addEventListener("click", addDecimal);

operatorButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setOperator(button.dataset.value);
  });
});

clearButton.addEventListener("click", resetCalculatorState);

async function calculateSquareRoot() {
  const rawValue = firstValue || secondValue;

  if (!rawValue) {
    errorEl.textContent = "Enter a number first.";
    return;
  }

  const value = parseFloat(rawValue);

  if (Number.isNaN(value)) {
    errorEl.textContent = "Please enter a valid number.";
    return;
  }

  if (value < 0) {
    errorEl.textContent = "Cannot take square root of a negative number.";
    return;
  }

  try {
    const response = await fetch(`${API_URL}/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ a: value, b: 0, operator: "sqrt" }),
    });

    const data = await response.json();

    if (!response.ok) {
      errorEl.textContent = data.detail || "Something went wrong.";
      return;
    }

    const result = formatValue(data.result);
    resultEl.textContent = result;
    expressionEl.textContent = `√${formatValue(value)} =`;
    firstValue = result;
    secondValue = "";
    currentOperator = null;
    waitingForSecondValue = false;
    errorEl.textContent = "";
    await loadHistory();
  } catch (error) {
    errorEl.textContent = "Could not reach the server. Is the backend running?";
  }
}

function deleteLastCharacter() {
  if (waitingForSecondValue && secondValue) {
    secondValue = secondValue.slice(0, -1);
  } else if (currentOperator && !waitingForSecondValue) {
    currentOperator = null;
  } else if (firstValue) {
    firstValue = firstValue.slice(0, -1);
  }

  if (!firstValue && !secondValue && !currentOperator) {
    resultEl.textContent = "0";
    expressionEl.textContent = "0";
  } else {
    updateDisplay();
  }
}

function handleCalculate() {
  if (currentOperator && secondValue) {
    calculateFromInputs();
    return;
  }

  if (firstValue && !currentOperator) {
    resultEl.textContent = firstValue;
    expressionEl.textContent = firstValue;
    return;
  }

  errorEl.textContent = "Please complete the calculation.";
}

sqrtButton.addEventListener("click", calculateSquareRoot);
deleteButton.addEventListener("click", deleteLastCharacter);
calcBtn.addEventListener("click", handleCalculate);

document.addEventListener("keydown", (event) => {
  // Let native button keyboard activation work when a button has focus.
  if (
    event.target instanceof HTMLElement &&
    event.target.closest("button") &&
    (event.key === "Enter" || event.key === " ")
  ) {
    return;
  }

  if (/^\d$/.test(event.key)) {
    event.preventDefault();
    addDigit(event.key);
    return;
  }

  const operatorForKey = {
    "+": "add",
    "-": "subtract",
    "*": "multiply",
    "/": "divide",
  };

  if (operatorForKey[event.key]) {
    event.preventDefault();
    setOperator(operatorForKey[event.key]);
    return;
  }

  switch (event.key) {
    case ".":
      event.preventDefault();
      addDecimal();
      break;
    case "Enter":
    case "=":
      event.preventDefault();
      handleCalculate();
      break;
    case "Backspace":
      event.preventDefault();
      deleteLastCharacter();
      break;
    case "Escape":
    case "Delete":
    case "c":
    case "C":
      event.preventDefault();
      resetCalculatorState();
      break;
    case "r":
    case "R":
      event.preventDefault();
      calculateSquareRoot();
      break;
  }
});

async function clearHistory() {
  try {
    const response = await fetch(`${API_URL}/history`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const data = await response.json();
      errorEl.textContent = data.detail || "Could not clear history.";
      return;
    }

    errorEl.textContent = "";
    historyEl.innerHTML = "";
  } catch (error) {
    errorEl.textContent = "Could not clear history.";
  }
}

async function loadHistory() {
  try {
    const response = await fetch(`${API_URL}/history`);
    const data = await response.json();

    historyEl.innerHTML = "";
    data.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = formatHistoryItem(item);
      historyEl.appendChild(li);
    });
  } catch (error) {
    historyEl.innerHTML = "<li>History unavailable.</li>";
  }
}

clearHistoryBtn.addEventListener("click", clearHistory);

resetCalculatorState();
loadHistory();
