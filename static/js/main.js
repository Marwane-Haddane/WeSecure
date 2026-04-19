// =====================================================
// 🔐 ADVANCED CRYPTO TOOL
// =====================================================
async function processAdvancedCrypto() {
    const actionVal = document.getElementById('op-selector').value || "encrypt";
    const algorithmVal = document.getElementById('algo-selector').value || "fernet";
    const inputText = document.getElementById('crypto-input').value;
    const keyVal = document.getElementById('key-input').value;

    const outputField = document.getElementById('crypto-output');
    const statusText = document.getElementById('crypto-status');

    if (!inputText.trim()) {
        outputField.value = "Error: Input data required.";
        outputField.classList.add('text-red-500');
        outputField.classList.remove('dark:text-green-400');
        return;
    }

    // Reset UI
    outputField.value = "";
    outputField.classList.remove('text-red-500');
    outputField.classList.add('dark:text-green-400');

    statusText.classList.remove('hidden');
    statusText.textContent = "Processing...";

    try {
        const response = await fetch('/crypto', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: actionVal,
                algorithm: algorithmVal,
                text: inputText,
                key: keyVal
            })
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            outputField.value = data.result;
            statusText.textContent = "Complete.";
        } else {
            outputField.value = "Error: " + (data.message || "Unknown error");
            outputField.classList.add('text-red-500');
            outputField.classList.remove('dark:text-green-400');
            statusText.textContent = "Failed.";
        }
    } catch (error) {
        outputField.value = "Network Error: Could not reach server.";
        outputField.classList.add('text-red-500');
        outputField.classList.remove('dark:text-green-400');
        statusText.textContent = "Error.";
    }

    setTimeout(() => {
        statusText.classList.add('hidden');
    }, 2000);
}


// =====================================================
// 📋 COPY RESULT
// =====================================================
function copyResult() {
    const textToCopy = document.getElementById('crypto-output').value;

    if (!textToCopy || textToCopy.startsWith("Error")) return;

    navigator.clipboard.writeText(textToCopy).then(() => {
        const confirmMsg = document.getElementById('copy-confirm');
        confirmMsg.classList.remove('opacity-0');

        setTimeout(() => {
            confirmMsg.classList.add('opacity-0');
        }, 2000);
    });
}


// =====================================================
// 🌐 ANALYZER TOOL
// =====================================================
async function runAnalysis() {
    const urlInput = document.getElementById('target-url').value;
    let fullUrl = urlInput.trim();

    if (!fullUrl.startsWith("http://") && !fullUrl.startsWith("https://")) {
        fullUrl = "http://" + fullUrl;
    }

    const emailInput = document.getElementById('target-email').value;
    const btnText = document.getElementById('scan-btn-text');
    const alertBox = document.getElementById('analyzer-alert');
    const alertIcon = document.getElementById('alert-icon');
    const alertText = document.getElementById('alert-text');

    btnText.textContent = "Scanning Target...";
    document.getElementById('scan-btn').disabled = true;
    document.getElementById('scan-btn').classList.add('opacity-75', 'cursor-not-allowed');

    alertBox.classList.add('hidden');

    try {
        const response = await fetch('/analyzer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: fullUrl,
                email: emailInput
            })
        });

        const data = await response.json();

        alertBox.classList.remove('hidden');

        if (response.ok && data.status === 'success') {
            alertBox.className =
                "rounded-md p-4 mb-4 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 text-green-800 dark:text-green-400";

            alertIcon.innerHTML =
                `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>`;

            alertIcon.classList.add("text-green-400");
            alertText.textContent = "Report sent successfully!";

            document.getElementById('target-url').value = '';
        } else {
            throw new Error(data.message || "Request failed");
        }

    } catch (error) {
        alertBox.classList.remove('hidden');

        alertBox.className =
            "rounded-md p-4 mb-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-800 dark:text-red-400";

        alertIcon.innerHTML =
            `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>`;

        alertIcon.classList.add("text-red-400");
        alertText.textContent = error.message;
    }

    btnText.textContent = "Initiate Scan";
    document.getElementById('scan-btn').disabled = false;
    document.getElementById('scan-btn').classList.remove('opacity-75', 'cursor-not-allowed');
}


// =====================================================
// 🎛️ CYBER DROPDOWN SYSTEM (CLEAN FIXED VERSION)
// =====================================================

window.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("op-selector")) {
        updateAlgoOptions();
        setDefaultLabels();
    }
});

function setDefaultLabels() {
    const opLabel = document.querySelector("#op-selector")
        ?.closest(".cyber-select")
        ?.querySelector("[data-label]");

    if (opLabel) opLabel.textContent = "Encrypt";
}


// =====================================================
// 🔁 UPDATE ALGO OPTIONS
// =====================================================
function updateAlgoOptions() {
    const op = document.getElementById("op-selector").value;

    const algoOptions = document.getElementById("algo-options");
    const algoHidden = document.getElementById("algo-selector");

    const algoSelect = document.querySelectorAll(".cyber-select")[1];
    const algoLabel = algoSelect?.querySelector("[data-label]");

    algoOptions.innerHTML = "";

    const list = algoMaps[op] || [];

    list.forEach((item, index) => {
        const div = document.createElement("div");
        div.className = "cyber-option";
        div.dataset.value = item.value;
        div.textContent = item.text;

        algoOptions.appendChild(div);

        // default first option
        if (index === 0) {
            algoHidden.value = item.value;
            if (algoLabel) algoLabel.textContent = item.text;
        }
    });

    updateKeyVisibility();
}


// =====================================================
// 🔽 TOGGLE DROPDOWN OPEN/CLOSE
// =====================================================
document.addEventListener("click", (e) => {
    document.querySelectorAll(".cyber-select").forEach(select => {
        const btn = select.querySelector("[data-btn]");
        const options = select.querySelector("[data-options]");

        if (!btn || !options) return;

        if (btn.contains(e.target)) {
            options.classList.toggle("hidden");
        } else if (!select.contains(e.target)) {
            options.classList.add("hidden");
        }
    });
});


// =====================================================
// 🎯 OPTION SELECT (SINGLE CLEAN HANDLER)
// =====================================================
document.addEventListener("click", (e) => {
    const option = e.target.closest(".cyber-option");
    if (!option) return;

    const select = option.closest(".cyber-select");
    const label = select.querySelector("[data-label]");
    const hidden = select.querySelector("input[type='hidden']");
    const options = select.querySelector("[data-options]");

    const value = option.dataset.value;
    const text = option.textContent;

    if (label) label.textContent = text;
    if (hidden) hidden.value = value;

    if (options) options.classList.add("hidden");

    if (hidden.id === "op-selector") {
        updateAlgoOptions();
    }

    if (hidden.id === "algo-selector") {
        updateKeyVisibility();
    }
});