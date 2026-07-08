const API_BASE_URL = "http://127.0.0.1:8000";
const body = document.body;
const menuToggle = document.querySelector(".menu-toggle");
const navPanel = document.querySelector(".nav-panel");
const themeToggle = document.querySelector(".theme-toggle");
const themeIcon = document.querySelector(".theme-icon");
const themeLabel = document.querySelector(".theme-label");
const inputText = document.querySelector("#inputText");
const outputText = document.querySelector("#outputText");
const historyList = document.querySelector("#historyList");
const clearHistoryBtn = document.querySelector("#clearHistoryBtn");
const charCounter = document.querySelector("#charCounter");
const sourceLanguage = document.querySelector("#sourceLanguage");
const targetLanguage = document.querySelector("#targetLanguage");
const swapButton = document.querySelector(".swap-button");
const translateButton = document.querySelector(".translate-button");
const loaderArea = document.querySelector(".loader-area");
const statusPill = document.querySelector(".status-pill");
const copyStatus = document.querySelector("#copyStatus");
const actionButtons = document.querySelectorAll(".action-button");
const navLinks = document.querySelectorAll(".nav-panel a");

const maxCharacters = 5000;
let translationHistory = JSON.parse(
    localStorage.getItem("translationHistory")
) || [];

const setMenuState = (isOpen) => {
  menuToggle.classList.toggle("is-open", isOpen);
  navPanel.classList.toggle("is-open", isOpen);
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.setAttribute(isOpen ? "aria-label" : "aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
};

const updateThemeToggle = () => {
  const isDark = body.classList.contains("dark-mode");
  themeIcon.textContent = isDark ? "☀" : "☾";
  themeLabel.textContent = isDark ? "Light" : "Dark";
  themeToggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
};

const showTemporaryStatus = (message) => {
  copyStatus.textContent = message;
  window.clearTimeout(showTemporaryStatus.timeoutId);
  showTemporaryStatus.timeoutId = window.setTimeout(() => {
    copyStatus.textContent = "";
  }, 2200);
};

const updateCharacterCounter = () => {
  charCounter.textContent = `${inputText.value.length} / ${maxCharacters} characters`;
};

async function detectLanguage(text) {

    const response = await fetch(`${API_BASE_URL}/detect`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error("Language detection failed");
    }

    return data.code;
}

async function translateText() {
  const text = inputText.value.trim();

  if (!text) {
    inputText.focus();
    showTemporaryStatus("Enter text first");
    return;
  }

  try {
    translateButton.disabled = true;
    translateButton.textContent = "Translating...";
    loaderArea.classList.add("is-active");
    statusPill.textContent = "Working";
    outputText.value = "";

    let source = sourceLanguage.value;

    if (source === "auto") {
        source = await detectLanguage(text);
    }

    const response = await fetch(`${API_BASE_URL}/translate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: text,
        source: source,
        target: targetLanguage.value
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail?.error || "Translation failed");
    }

    outputText.value = data.translated_text;

    // Decide what source language name to save
    const sourceName =
        sourceLanguage.value === "auto"
            ? "Auto Detect"
            : sourceLanguage.options[sourceLanguage.selectedIndex].text;

    saveHistory(
      text,
      data.translated_text,
      sourceName,
      targetLanguage.options[targetLanguage.selectedIndex].text
    );
    statusPill.textContent = "Complete";
    showTemporaryStatus("Translation ready");

  } catch (error) {
    console.error(error);

    outputText.value = "";
    statusPill.textContent = "Error";
    showTemporaryStatus("Translation failed");
    if (sourceLanguage.value === targetLanguage.value) {
    outputText.value = inputText.value;
    showTemporaryStatus("Source and target languages are the same.");
    return;
}

  } finally {
    loaderArea.classList.remove("is-active");
    translateButton.disabled = false;
    translateButton.textContent = "Translate";
  }
}

const copyOutput = async () => {
  if (!outputText.value.trim()) {
    showTemporaryStatus("Nothing to copy");
    return;
  }

  try {
    await navigator.clipboard.writeText(outputText.value);
    showTemporaryStatus("Copied");
  } catch {
    outputText.select();
    document.execCommand("copy");
    showTemporaryStatus("Copied");
  }
};

const clearFields = () => {
  inputText.value = "";
  outputText.value = "";
  statusPill.textContent = "Ready";
  updateCharacterCounter();
  showTemporaryStatus("Cleared");
  inputText.focus();
};

const downloadTranslation = () => {
  if (!outputText.value.trim()) {
    showTemporaryStatus("Nothing to download");
    return;
  }

  const blob = new Blob([outputText.value], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "translation.txt";
  link.click();
  URL.revokeObjectURL(url);
  showTemporaryStatus("Downloaded");
};

const listenToOutput = () => {

  if (!outputText.value.trim()) {
    alert("Nothing to play");
    return;
  }

  if (!("speechSynthesis" in window)) {
    alert("Speech synthesis not supported");
    return;
  }

  speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(outputText.value);

  const speechLanguageMap = {
      en: "en-US",
      hi: "hi-IN",
      ja: "ja-JP",
      fr: "fr-FR",
      de: "de-DE",
      es: "es-ES",
      it: "it-IT",
      ko: "ko-KR",
      "zh-CN": "zh-CN",
      ar: "ar-SA",
      ru: "ru-RU"
  };
  utterance.lang =
      speechLanguageMap[targetLanguage.value] || "en-US";

  // Select the matching voice if available
  const voices = speechSynthesis.getVoices();

  let matchedVoice;

  if (targetLanguage.value === "hi") {
      matchedVoice = voices.find(v => v.lang.startsWith("hi"));
  } else if (targetLanguage.value === "ja") {
      matchedVoice = voices.find(v => v.lang.startsWith("ja"));
  } else {
      matchedVoice = voices.find(v => v.lang.startsWith(targetLanguage.value));
  }

  if (matchedVoice) {
    utterance.voice = matchedVoice;
  }

  utterance.rate = 1;
  utterance.volume = 1;

  utterance.onstart = () => console.log("Speech started");

  utterance.onend = () => console.log("Speech ended");

  utterance.onerror = (e) => console.error("Speech Error:", e);

  speechSynthesis.speak(utterance);
};

menuToggle.addEventListener("click", () => {
  setMenuState(!navPanel.classList.contains("is-open"));
});

navLinks.forEach((link) => {
  link.addEventListener("click", () => setMenuState(false));
});

themeToggle.addEventListener("click", () => {
  body.classList.toggle("dark-mode");
  localStorage.setItem("aiTranslatorTheme", body.classList.contains("dark-mode") ? "dark" : "light");
   
  updateThemeToggle();
});

inputText.addEventListener("input", updateCharacterCounter);

swapButton.addEventListener("click", () => {
  const currentSource = sourceLanguage.value;
  sourceLanguage.value = targetLanguage.value;
  targetLanguage.value = currentSource;
});

translateButton.addEventListener("click", translateText);

actionButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.action;

    if (action === "copy") copyOutput();
    if (action === "clear") clearFields();
    if (action === "download") downloadTranslation();
    if (action === "listen") listenToOutput();
  });
});
if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener("click", () => {

        translationHistory = [];

        localStorage.removeItem("translationHistory");

        renderHistory();

    });
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setMenuState(false);
  }
});

if (localStorage.getItem("aiTranslatorTheme") === "dark") {
  body.classList.add("dark-mode");
}

updateThemeToggle();
updateCharacterCounter();
renderHistory();

function saveHistory(input, output, source, target) {
    const item = {
        id: Date.now(),
        input,
        output,
        source,
        target,
        time: new Date().toLocaleString()
    };

    translationHistory.unshift(item);

    localStorage.setItem(
        "translationHistory",
        JSON.stringify(translationHistory)
    );

    renderHistory();
}

function renderHistory() {
    historyList.innerHTML = "";

    if (translationHistory.length === 0) {
        historyList.innerHTML = `
            <p class="empty-history">
                No translations yet.
            </p>
        `;
        return;
    }

    let html = "";

    translationHistory.forEach(item => {

        html += `
            <button class="history-item" type="button">

                <span class="language-pair">
                    ${item.source} → ${item.target}
                </span>

                <span class="history-preview">
                    <strong>${item.input}</strong><br>
                    ${item.output}
                </span>

                <time>
                    ${item.time}
                </time>

            </button>
        `;

    });

    historyList.innerHTML = html;
}