document.addEventListener("DOMContentLoaded", function () {
  let apiUrl = "/api/chatbot1";
  let activeChatbot = "chatbot1";
  const chatHistories = {
    chatbot1: [],
    chatbot2: [],
    chatbot3: [],
  };

  // Set default active chatbot
  document
    .querySelector(".navbar-nav .nav-link[data-chatbot='chatbot1']")
    .classList.add("active");

  // Handle navbar click and load chat history
  document.querySelectorAll(".navbar-nav .nav-link").forEach((item) => {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      activeChatbot = this.getAttribute("data-chatbot");
      apiUrl = `/api/${activeChatbot}`;
      document
        .querySelectorAll(".navbar-nav .nav-link")
        .forEach((el) => el.classList.remove("active"));
      this.classList.add("active");
      loadChatHistory(activeChatbot);
    });
  });

  // Add event listener for sending message
  const sendMessageDebounced = debounce(sendMessage, 300);

  document
    .getElementById("send-button")
    .addEventListener("click", sendMessageDebounced);

  // Handle "Enter" key press
  document
    .getElementById("message-input")
    .addEventListener("keypress", function (event) {
      if (event.which === 13) {
        event.preventDefault();
        sendMessageDebounced();
      }
    });

  // Debounce function to avoid multiple rapid calls
  function debounce(func, delay) {
    let debounceTimer;
    return function (...args) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => func.apply(this, args), delay);
    };
  }

  async function sendMessage() {
    const message = document.getElementById("message-input").value.trim();
    if (message === "") return;

    console.log(message);
    appendMessage(message, "user");
    chatHistories[activeChatbot].push({ type: "user", text: message });

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const responseData = await response.json();
      const actualResponse = responseData.response;
      appendMessage(actualResponse, "response");
      chatHistories[activeChatbot].push({
        type: "response",
        text: actualResponse,
      });
    } catch (error) {
      console.error("Error sending message:", error);
      appendMessage("Error: Failed to send the message.", "response");
      chatHistories[activeChatbot].push({
        type: "response",
        text: "Error: Failed to send the message.",
      });
    }

    document.getElementById("message-input").value = "";
  }

  function appendMessage(text, type) {
  const logo = type === "user" ? userImage : botImage;

    const messageHtml = `
        <div class="message ${type}">
          <img src="${logo}" alt="${type} logo" class="logo" />
          <div class="message-content">${text}</div>
        </div>`;
    document
      .getElementById("chat-container")
      .insertAdjacentHTML("beforeend", messageHtml);
    document.getElementById("chat-container").scrollTop =
      document.getElementById("chat-container").scrollHeight;
  }

  function loadChatHistory(chatbot) {
    document.getElementById("chat-container").innerHTML = "";
    chatHistories[chatbot].forEach((msg) => {
      appendMessage(msg.text, msg.type);
    });
  }

  loadChatHistory(activeChatbot);
});
