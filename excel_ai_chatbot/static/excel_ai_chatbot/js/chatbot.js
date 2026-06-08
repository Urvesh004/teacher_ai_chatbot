document.addEventListener("DOMContentLoaded", function () {
  const chatIcon = document.getElementById("chat-icon");
  const chatBox = document.getElementById("chat-box");
  const closeBtn = document.getElementById("close-chat");
  const sendBtn = document.getElementById("send-btn");
  const messageInput = document.getElementById("chat-message");
  const messagesDiv = document.getElementById("chat-messages");

  if (!chatIcon || !chatBox || !sendBtn || !messageInput || !messagesDiv) {
    console.error("Chatbot: required elements not found.");
    return;
  }

  // ── Open / Close ─────────────────────────────────────────────
  chatIcon.addEventListener("click", () => {
    const isOpen = chatBox.classList.toggle("active");
    chatIcon.classList.toggle("open", isOpen);
    if (isOpen) {
      messageInput.focus();
      // Hide badge on open
      const badge = document.getElementById("chat-badge");
      if (badge) badge.style.display = "none";
    }
  });

  closeBtn?.addEventListener("click", () => {
    chatBox.classList.remove("active");
    chatIcon.classList.remove("open");
  });

  // Close on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && chatBox.classList.contains("active")) {
      chatBox.classList.remove("active");
      chatIcon.classList.remove("open");
    }
  });

  // ── Quick-question chips ──────────────────────────────────────
  document.querySelectorAll(".suggestion-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      messageInput.value = this.dataset.question;
      sendMessage();
    });
  });

  // ── Send on button click or Enter ────────────────────────────
  sendBtn.addEventListener("click", sendMessage);
  messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") { e.preventDefault(); sendMessage(); }
  });

  // ── Core send logic ───────────────────────────────────────────
  function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    messageInput.value = "";
    sendBtn.disabled = true;

    const typingEl = appendTyping();

    fetch("/chatbot/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: `message=${encodeURIComponent(message)}`,
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        typingEl.remove();
        appendMessage("bot", data.answer || "No response.");
      })
      .catch((err) => {
        typingEl.remove();
        appendMessage("bot", "Could not reach the server. Please try again.");
        console.error("Chatbot error:", err);
      })
      .finally(() => {
        sendBtn.disabled = false;
        messageInput.focus();
      });
  }

  // ── DOM helpers ───────────────────────────────────────────────
  function appendMessage(sender, text) {
    const wrap = document.createElement("div");
    wrap.className = sender === "user" ? "msg msg-user" : "msg msg-bot";
    wrap.style.animation = "fadeUp .3s ease both";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = text.replace(/\n/g, "<br>");

    const time = document.createElement("span");
    time.className = "msg-time";
    time.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    wrap.appendChild(bubble);
    wrap.appendChild(time);
    messagesDiv.appendChild(wrap);
    scrollBottom();
    return wrap;
  }

  function appendTyping() {
    const wrap = document.createElement("div");
    wrap.className = "msg msg-bot typing-wrap";
    wrap.style.animation = "fadeUp .3s ease both";
    wrap.innerHTML = `<div class="bubble typing-indicator"><span></span><span></span><span></span></div>`;
    messagesDiv.appendChild(wrap);
    scrollBottom();
    return wrap;
  }

  function scrollBottom() {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  // ── CSRF helper ───────────────────────────────────────────────
  function getCookie(name) {
    for (const cookie of document.cookie.split(";")) {
      const [k, v] = cookie.trim().split("=");
      if (k === name) return decodeURIComponent(v);
    }
    return null;
  }
});
