// ========================================
// CryptoGuard - Client-side Interactions
// ========================================

// DOM Elements
const messageInput = document.getElementById("message");
const shiftInput = document.getElementById("shift");

const encryptButton = document.getElementById("encrypt-btn");
const decryptButton = document.getElementById("decrypt-btn");
const clearButton = document.getElementById("clear-btn");

const decreaseShiftButton = document.getElementById("decrease-shift");
const increaseShiftButton = document.getElementById("increase-shift");

const encryptedOutput = document.getElementById("encrypted-output");
const decryptedOutput = document.getElementById("decrypted-output");

const characterCount = document.getElementById("character-count");


// ========================================
// Character Counter
// ========================================

function updateCharacterCount() {
    const count = messageInput.value.length;

    characterCount.textContent =
        `${count} character${count === 1 ? "" : "s"}`;
}

messageInput.addEventListener("input", updateCharacterCount);


// ========================================
// Shift Key Controls
// ========================================

function updateShift(value) {
    let shift = parseInt(value, 10);

    if (isNaN(shift)) {
        shift = 0;
    }

    shift = Math.max(0, Math.min(25, shift));

    shiftInput.value = shift;
}


// Decrease shift
decreaseShiftButton.addEventListener("click", () => {
    updateShift(parseInt(shiftInput.value, 10) - 1);
});


// Increase shift
increaseShiftButton.addEventListener("click", () => {
    updateShift(parseInt(shiftInput.value, 10) + 1);
});


// Keep manually entered values within range
shiftInput.addEventListener("input", () => {
    updateShift(shiftInput.value);
});


// ========================================
// Encrypt
// ========================================

encryptButton.addEventListener("click", async () => {

    const text = messageInput.value.trim();
    const shift = parseInt(shiftInput.value, 10);

    if (!text) {
        showMessage(
            encryptedOutput,
            "Please enter a message to encrypt."
        );
        return;
    }

    setButtonLoading(encryptButton, true);

    try {

        const response = await fetch("/encrypt", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text,
                shift: shift
            })
        });


        const data = await response.json();


        if (!response.ok) {
            throw new Error(data.error || "Encryption failed.");
        }


        encryptedOutput.textContent = data.encrypted;
        encryptedOutput.classList.add("has-result");

    } catch (error) {

        showMessage(
            encryptedOutput,
            error.message
        );

    } finally {

        setButtonLoading(encryptButton, false);

    }
});


// ========================================
// Decrypt
// ========================================

decryptButton.addEventListener("click", async () => {

    const text = messageInput.value.trim();
    const shift = parseInt(shiftInput.value, 10);

    if (!text) {
        showMessage(
            decryptedOutput,
            "Please enter a message to decrypt."
        );
        return;
    }

    setButtonLoading(decryptButton, true);

    try {

        const response = await fetch("/decrypt", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text,
                shift: shift
            })
        });


        const data = await response.json();


        if (!response.ok) {
            throw new Error(data.error || "Decryption failed.");
        }


        decryptedOutput.textContent = data.decrypted;
        decryptedOutput.classList.add("has-result");

    } catch (error) {

        showMessage(
            decryptedOutput,
            error.message
        );

    } finally {

        setButtonLoading(decryptButton, false);

    }
});


// ========================================
// Clear Everything
// ========================================

clearButton.addEventListener("click", () => {

    messageInput.value = "";

    shiftInput.value = 3;

    encryptedOutput.textContent =
        "Your encrypted message will appear here.";

    decryptedOutput.textContent =
        "Your decrypted message will appear here.";

    encryptedOutput.classList.remove("has-result");
    decryptedOutput.classList.remove("has-result");

    updateCharacterCount();

});


// ========================================
// Copy Output
// ========================================

document.querySelectorAll(".copy-btn").forEach(button => {

    button.addEventListener("click", async () => {

        const targetId = button.dataset.target;
        const target = document.getElementById(targetId);

        const text = target.textContent.trim();

        if (
            !text ||
            text.includes("will appear here") ||
            text.includes("Please enter")
        ) {
            return;
        }


        try {

            await navigator.clipboard.writeText(text);

            const originalText = button.textContent;

            button.textContent = "Copied ✓";

            setTimeout(() => {
                button.textContent = originalText;
            }, 1500);

        } catch (error) {

            console.error("Copy failed:", error);

        }

    });

});


// ========================================
// Loading State
// ========================================

function setButtonLoading(button, loading) {

    if (loading) {

        button.dataset.originalText = button.innerHTML;

        button.innerHTML = "Processing...";

        button.disabled = true;

    } else {

        button.innerHTML = button.dataset.originalText;

        button.disabled = false;

    }

}


// ========================================
// Output Messages
// ========================================

function showMessage(element, message) {

    element.textContent = message;

    element.classList.remove("has-result");

}


// ========================================
// Initial State
// ========================================

updateCharacterCount();