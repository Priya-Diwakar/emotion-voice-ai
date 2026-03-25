/* ===== EMOTION VOICE AI — FINAL app.js ===== */

/* ================== CONFIG ================== */
const API_URL = "/api/chat";   // IMPORTANT: works for deployment

/* ================== SEND MESSAGE ================== */
async function sendMsg() {
  const input = document.getElementById("msg-input");
  const chatBox = document.getElementById("chat-box");

  const message = input.value.trim();
  if (!message) return;

  // Show user message
  appendMessage("user", message);
  input.value = "";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: message
      })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Server error");
    }

    // Show bot response
    appendMessage("bot", data.reply || "No response");

  } catch (err) {
    console.error("API ERROR:", err);
    appendMessage("bot", "⚠️ Server error. Please try again.");
  }
}

/* ================== APPEND MESSAGE ================== */
function appendMessage(sender, text) {
  const chatBox = document.getElementById("chat-box");

  const msgDiv = document.createElement("div");
  msgDiv.className = sender === "user" ? "msg user" : "msg bot";

  msgDiv.innerHTML = `
    <div class="msg-text">${text}</div>
  `;

  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

/* ================== ENTER KEY SUPPORT ================== */
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("msg-input");

  if (input) {
    input.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        sendMsg();
      }
    });
  }
});

/* ================== OPTIONAL: STATUS CHECK ================== */
async function checkStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();
    console.log("API Status:", data);
  } catch (e) {
    console.error("Status check failed");
  }
}

checkStatus();