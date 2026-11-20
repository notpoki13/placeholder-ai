
const input = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const newChat = document.getElementById("newChat");

function sendMessage() {
    const text = input.value.trim();

    if (!text) return;

    welcome.style.display = "none";

    // Display user message
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.textContent = text;

    messages.appendChild(userMessage);

    // Temporary development response
    const aiMessage = document.createElement("div");
    aiMessage.className = "message assistant";

    aiMessage.textContent =
        "Placeholder AI is not connected to a language model yet. The website is working!";

    messages.appendChild(aiMessage);

    input.value = "";
}

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

newChat.addEventListener("click", function() {
    messages.innerHTML = "";
    input.value = "";
    welcome.style.display = "block";
});
