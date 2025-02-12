// // Theme handling
// function initTheme() {
//     const theme = localStorage.getItem('theme') || 'light';
//     document.documentElement.setAttribute('data-theme', theme);
// }

// function toggleTheme() {
//     const currentTheme = document.documentElement.getAttribute('data-theme');
//     const newTheme = currentTheme === 'light' ? 'dark' : 'light';
//     document.documentElement.setAttribute('data-theme', newTheme);
//     localStorage.setItem('theme', newTheme);
// }

// document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
// initTheme();

// Initialize the theme from local storage
function initTheme() {
  const theme = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", theme);
  const toggle = document.getElementById("theme-toggle");
  toggle.checked = theme === "dark"; // Sync the toggle button
}

// Toggle theme when the checkbox changes
document.getElementById("theme-toggle").addEventListener("change", function () {
  const isDarkMode = this.checked;
  const newTheme = isDarkMode ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
});

// Call initTheme on page load
initTheme();

// Helpline dropdown functionality
function toggleHelplineMenu() {
  const menu = document.getElementById("helplineMenu");
  menu.classList.toggle("show");

  // Close menu when clicking outside
  document.addEventListener("click", function closeMenu(e) {
    if (!e.target.closest(".helpline-dropdown")) {
      menu.classList.remove("show");
      document.removeEventListener("click", closeMenu);
    }
  });
}

// Message handling with animations
function replaceMessage(oldMessage, newContent, isUser = false) {
  const messages = document.getElementById("messages");
  const index = Array.from(messages.children).indexOf(oldMessage);

  oldMessage.classList.add("fade-out");
  setTimeout(() => {
    oldMessage.remove();
    appendMessage(newContent, isUser, false, index);
  }, 300);
}

function appendMessage(
  content,
  isUser = false,
  isEditable = false,
  index = -1
) {
  const messagesContainer = document.getElementById("messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user" : "bot"}`;
  messageDiv.dataset.query = isUser ? content : "";

  const messageContent = document.createElement("div");
  messageContent.className = "message-content";

  if (!isUser) {
    const botIcon = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "svg"
    );
    botIcon.setAttribute("class", "bot-icon");
    botIcon.setAttribute("width", "16");
    botIcon.setAttribute("height", "16");
    botIcon.setAttribute("viewBox", "0 0 16 16");
    botIcon.setAttribute("fill", "currentColor");
    botIcon.innerHTML =
      '<path d="M5.065.158A1.5 1.5 0 0 1 5.736 0h4.528a1.5 1.5 0 0 1 .67.158l3.237 1.618a1.5 1.5 0 0 1 .83 1.342V13.5a2.5 2.5 0 0 1-2.5 2.5h-9A2.5 2.5 0 0 1 1 13.5V3.118a1.5 1.5 0 0 1 .828-1.342zM2 9.372V13.5A1.5 1.5 0 0 0 3.5 15h4V8h-.853a.5.5 0 0 0-.144.021zM8.5 15h4a1.5 1.5 0 0 0 1.5-1.5V9.372l-4.503-1.35A.5.5 0 0 0 9.353 8H8.5zM14 8.328v-5.21a.5.5 0 0 0-.276-.447l-3.236-1.618A.5.5 0 0 0 10.264 1H5.736a.5.5 0 0 0-.223.053L2.277 2.67A.5.5 0 0 0 2 3.118v5.21l1-.3V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v3.028zm-2-.6V5H8.5v2h.853a1.5 1.5 0 0 1 .431.063zM7.5 7V5H4v2.728l2.216-.665A1.5 1.5 0 0 1 6.646 7zm-1-5a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm-3 8a.5.5 0 1 0 0 1 .5.5 0 0 0 0-1m9 0a.5.5 0 1 0 0 1 .5.5 0 0 0 0-1M5 13a1 1 0 1 1-2 0 1 1 0 0 1 2 0m7 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2"/>';
    messageContent.appendChild(botIcon);
  }

  let textElement;
  if (isEditable) {
    textElement = document.createElement("textarea");
    textElement.className = "editable-message";
    textElement.value = content;
    textElement.addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });
    textElement.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        const newQuery = this.value.trim();
        if (newQuery) {
          const botResponse = this.closest(".message").nextElementSibling;
          if (botResponse) {
            takeUserQuery(newQuery, botResponse);
          }
        }
      }
    });
  } else {
    // textElement = document.createElement("p");
    // textElement.textContent = content;
    textElement = document.createElement("div");
    textElement.innerHTML = content; // Set content as innerHTML for bot messages
  }
  messageContent.appendChild(textElement);

  if (!isUser) {
    const speakButton = document.createElement("button");
    speakButton.className = "speak-button";
    speakButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path><path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path></svg>`;
    speakButton.onclick = () => textToSpeech(content);
    messageContent.appendChild(speakButton);
  }

  messageDiv.appendChild(messageContent);

  if (index !== -1 && index < messagesContainer.children.length) {
    messagesContainer.insertBefore(
      messageDiv,
      messagesContainer.children[index]
    );
  } else {
    messagesContainer.appendChild(messageDiv);
  }

  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  if (isEditable) {
    textElement.style.height = textElement.scrollHeight + "px";
    textElement.focus();
  }
}

let currentSpeech = null;

// Text-to-Speech functionality
function textToSpeech(text, onComplete = null) {
  // Cancel any existing speech
  if (currentSpeech) {
    if (currentSpeech.pause) {
      currentSpeech.pause();
    }
    currentSpeech = null;
    return;
  }

  const selectedLanguage = document.getElementById("language-select").value;
  const formData = new FormData();
  formData.append("text", text);
  formData.append("lang", selectedLanguage);

  fetch("/text-to-speech/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: formData,
  })
    .then((response) => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.blob();
    })
    .then((blob) => {
      const audio = new Audio(URL.createObjectURL(blob));
      currentSpeech = audio;

      audio.onended = () => {
        currentSpeech = null;
        if (onComplete) onComplete();
      };

      audio.play().catch((error) => {
        console.error("Error playing audio:", error);
        currentSpeech = null;
        if (onComplete) onComplete();
      });
    })
    .catch((error) => {
      console.error("Error with text-to-speech:", error);
      currentSpeech = null;
      if (onComplete) onComplete();
    });
}

// function textToSpeech(text) {
//   const selectedLanguage = document.getElementById("language-select").value;
//   const formData = new FormData();
//   formData.append("text", text);
//   formData.append("lang", selectedLanguage);

//   fetch("/text-to-speech/", {
//     method: "POST",
//     headers: {
//       "X-CSRFToken": getCookie("csrftoken"),
//     },
//     body: formData,
//   })
//     .then((response) => {
//       if (!response.ok) throw new Error("Network response was not ok");
//       return response.blob();
//     })
//     .then((blob) => {
//       const audio = new Audio(URL.createObjectURL(blob));
//       audio.play();
//     })
//     .catch((error) => {
//       console.error("Error with text-to-speech:", error);
//     });
// }

// Voice recording
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

function togglePlayPause() {
  const icon = document.getElementById("iconRecord");

  if (!isRecording) {
    startRecording();
    icon.innerHTML = '<path d="M18 12H6"/>';
    isRecording = true;
  } else {
    stopRecording();
    icon.innerHTML =
      '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/>';
    isRecording = false;
  }
}

function startRecording() {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        if (audioChunks.length > 0) {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          sendSpeechToDjango(audioBlob);
          audioChunks = [];
        }
      };

      mediaRecorder.start();
    })
    .catch((error) => {
      console.error("Error accessing microphone:", error);
      appendMessage(
        "Error accessing microphone. Please check your permissions."
      );
    });
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach((track) => track.stop());
  }
}

// function sendSpeechToDjango(audioBlob) {
//     const formData = new FormData();
//     const selectedLang = document.getElementById('language-select').value;

//     formData.append('audio', audioBlob);
//     formData.append('lang', selectedLang.value);

//     appendMessage('Processing your voice input...', false);

//     fetch('/speech/', {
//         method: 'POST',
//         body: formData,
//         headers: {
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             // Remove the "Processing..." message
//             const messages = document.getElementById('messages');
//             messages.removeChild(messages.lastChild);

//             // Add the recognized text as an editable user message
//             appendMessage(data.text, true, true);

//             // Automatically send the query
//             takeUserQuery(data.text);
//         } else {
//             appendMessage('Error: ' + data.error);
//         }
//     })
//     .catch(error => {
//         console.error('Error sending audio to Django:', error);
//         appendMessage('Sorry, there was an error processing your voice input.');
//     });
// }

// Chat functionality

function sendSpeechToDjango(audioBlob) {
  const formData = new FormData();
  const selectedLang = document.getElementById("language-select").value;

  formData.append("audio", audioBlob);
  formData.append("lang", selectedLang); // Ensure correct lang code

  appendMessage("Processing your voice input...", false);

  fetch("/speech/", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const messages = document.getElementById("messages");
        messages.removeChild(messages.lastChild);
        appendMessage(data.text, true, true);
        takeUserQuery(data.text);
      } else {
        appendMessage("Error: " + data.error);
      }
    })
    .catch((error) => {
      console.error("Error sending audio to Django:", error);
      appendMessage("Sorry, there was an error processing your voice input.");
    });
}

function submitForm(event) {
  event.preventDefault();
  const userQuery = document.getElementById("user-query").value.trim();

  if (!userQuery) return;

  appendMessage(userQuery, true, true);
  document.getElementById("user-query").value = "";

  takeUserQuery(userQuery);
}

function takeUserQuery(query, oldResponse = null) {
  const selectedLanguage = document.getElementById("language-select").value;

  fetch("/chatbot/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      userQuery: query,
      selectedLanguage: selectedLanguage,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      const botResponse = data.response || "Sorry, I didn't catch that.";
      if (oldResponse) {
        replaceMessage(oldResponse, botResponse);
      } else {
        appendMessage(botResponse, false);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      appendMessage("Sorry, there was an error processing your request.");
    });
}

// Utility functions
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Auto-resize textarea
document.getElementById("user-query").addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";
});

// Voice Chat Modal Functionality
let isVoiceChatActive = false;
let voiceRecognition = null;
let isProcessing = false;
let isSpeaking = false;

function initializeVoiceChat() {
  const voiceChatButton = document.getElementById("voiceChatButton");
  const voiceChatModal = document.getElementById("voiceChatModal");
  const closeVoiceChat = document.getElementById("closeVoiceChat");
  const voiceButton = document.getElementById("voiceButton");
  const voiceStatus = document.getElementById("voiceStatus");
  const voiceWaves = document.getElementById("voiceWaves").children;

  // SVG icons for different states
  const icons = {
    listening: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
            <line x1="12" x2="12" y1="19" y2="22"/>
        </svg>`,
    processing: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
        </svg>`,
    speaking: `<svg viewBox="0 0 24 24" fill="none" width="24" height="24" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff" style="user-select: auto;"><g id="SVGRepo_bgCarrier" stroke-width="0" style="user-select: auto;"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" style="user-select: auto;"></g><g id="SVGRepo_iconCarrier" style="user-select: auto;"> <path d="M16 9C16.5 9.5 17 10.5 17 12C17 13.5 16.5 14.5 16 15M19 6C20.5 7.5 21 10 21 12C21 14 20.5 16.5 19 18M13 3L7 8H5C3.89543 8 3 8.89543 3 10V14C3 15.1046 3.89543 16 5 16H7L13 21V3Z" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="user-select: auto;"></path> </g></svg>`,
  };

  function updateVoiceChatUI(state) {
    const container = document.querySelector(".voice-chat-container");
    voiceButton.innerHTML = icons[state] || icons.listening;

    switch (state) {
      case "listening":
        voiceButton.className = "voice-button listening";
        voiceStatus.textContent = "Listening...";
        container.className = "voice-chat-container listening";
        Array.from(voiceWaves).forEach((wave) => {
          wave.classList.add("listening");
          wave.classList.remove("processing", "speaking");
        });
        break;
      case "processing":
        voiceButton.className = "voice-button processing";
        voiceStatus.textContent = "Processing...";
        container.className = "voice-chat-container processing";
        Array.from(voiceWaves).forEach((wave) => {
          wave.classList.remove("listening", "processing", "speaking");
        });
        break;
      case "speaking":
        voiceButton.className = "voice-button speaking";
        voiceStatus.textContent = "Speaking...";
        container.className = "voice-chat-container speaking";
        Array.from(voiceWaves).forEach((wave) => {
          wave.classList.remove("listening", "processing", "speaking");
        });
        break;
      default:
        voiceButton.className = "voice-button";
        voiceStatus.textContent = "Click the microphone to start speaking";
        container.className = "voice-chat-container";
    }
  }

  function setupVoiceRecognition() {
    if (!("webkitSpeechRecognition" in window)) {
      voiceStatus.textContent =
        "Voice recognition is not supported in your browser.";
      return;
    }

    voiceRecognition = new webkitSpeechRecognition();
    voiceRecognition.continuous = false;
    voiceRecognition.interimResults = true;

    const selectedLanguage = document.getElementById("language-select").value;
    voiceRecognition.lang = getFullLanguageCode(selectedLanguage);

    voiceRecognition.onstart = () => {
      isVoiceChatActive = true;
      isProcessing = false;
      updateVoiceChatUI("listening");
    };

    voiceRecognition.onend = () => {
      if (isVoiceChatActive && !isProcessing && !isSpeaking) {
        setTimeout(() => {
          try {
            voiceRecognition.start();
          } catch (error) {
            console.error("Error restarting recognition:", error);
          }
        }, 100);
      }
    };

    voiceRecognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join("");

      if (event.results[event.results.length - 1].isFinal) {
        isProcessing = true;
        updateVoiceChatUI("processing");
        processVoiceInput(transcript);
      }
    };

    voiceRecognition.onerror = (event) => {
      console.error("Voice recognition error:", event.error);
      if (event.error !== "no-speech") {
        resetVoiceChat();
      }
    };
  }

  function processVoiceInput(transcript) {
    if (!transcript.trim()) {
      isProcessing = false;
      return;
    }

    const selectedLanguage = document.getElementById("language-select").value;
    fetch("/chatbot/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        userQuery: transcript,
        selectedLanguage: selectedLanguage,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        appendMessage(transcript, true);

        if (data.response) {
          appendMessage(data.response, false);
          isSpeaking = true;
          updateVoiceChatUI("speaking");

          // Use textToSpeech with callback
          textToSpeech(data.response, () => {
            isSpeaking = false;
            isProcessing = false;
            if (isVoiceChatActive) {
              updateVoiceChatUI("listening");
              startVoiceChat();
            }
          });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        isProcessing = false;
        if (isVoiceChatActive) {
          updateVoiceChatUI("listening");
          startVoiceChat();
        }
      });
  }

  function startVoiceChat() {
    if (!voiceRecognition) {
      setupVoiceRecognition();
    }

    if (!isProcessing && !isSpeaking) {
      try {
        voiceRecognition.start();
      } catch (error) {
        console.error("Error starting voice chat:", error);
        resetVoiceChat();
        setupVoiceRecognition();
        voiceRecognition.start();
      }
    }
  }

  function stopVoiceChat() {
    isVoiceChatActive = false;
    if (voiceRecognition) {
      try {
        voiceRecognition.stop();
      } catch (error) {
        console.error("Error stopping voice chat:", error);
      }
    }
    if (currentSpeech) {
      currentSpeech.pause();
      currentSpeech = null;
    }
  }

  function resetVoiceChat() {
    isVoiceChatActive = false;
    isProcessing = false;
    isSpeaking = false;
    updateVoiceChatUI("ready");
    if (voiceRecognition) {
      voiceRecognition.abort();
      voiceRecognition = null;
    }
    if (currentSpeech) {
      currentSpeech.pause();
      currentSpeech = null;
    }
  }

  voiceChatButton.addEventListener("click", () => {
    voiceChatModal.classList.add("active");
    startVoiceChat();
  });

  closeVoiceChat.addEventListener("click", () => {
    voiceChatModal.classList.remove("active");
    stopVoiceChat();
    resetVoiceChat();
  });

  function getFullLanguageCode(shortCode) {
    const languageMapping = {
      en: "en-US",
      hi: "hi-IN",
      bn: "bn-IN",
      te: "te-IN",
      mr: "mr-IN",
      ta: "ta-IN",
      ur: "ur-IN",
      gu: "gu-IN",
      kn: "kn-IN",
      ml: "ml-IN",
      fr: "fr-FR",
      es: "es-ES",
      de: "de-DE",
      it: "it-IT",
      pt: "pt-PT",
      ru: "ru-RU",
      ja: "ja-JP",
      ko: "ko-KR",
      zh: "zh-CN",
      ar: "ar-SA",
    };
    return languageMapping[shortCode] || "en-US";
  }

  // Update language when changed
  document
    .getElementById("language-select")
    .addEventListener("change", function () {
      if (voiceRecognition) {
        const wasActive = isVoiceChatActive;
        if (wasActive) {
          stopVoiceChat();
        }
        voiceRecognition.lang = getFullLanguageCode(this.value);
        if (wasActive) {
          startVoiceChat();
        }
      }
    });
}

// Initialize voice chat when the DOM is loaded
document.addEventListener("DOMContentLoaded", initializeVoiceChat);
