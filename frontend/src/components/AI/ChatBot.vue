<template>
  <div>
    <!-- Traditional Chinese Medicine character button -->
    <div class="chatbot-icon" @click="toggleChat">
      <img src="/master.png" alt="中医形象" />
    </div>
    <!-- Initial welcome message popup -->
    <div v-if="showWelcomeMessage" class="welcome-message">
      <div class="welcome-text">
        <p class="message-zh">欢迎来到中药学习网站！我是中医扁鹊，点击我的头像即可与我对话</p>
        <p class="message-en">Welcome to Chinese medicine learning website! I am Bian Que, click on my profile picture to talk to me</p>
      </div>
      <button class="close-btn" @click="closeWelcomeMessage">x</button>
    </div>
    <!-- Chat dialog -->
    <div
        v-if="hasOpenedOnce"
        v-show="isChatOpen || dialogClass === 'fade-out'"
        :class="['chatbot-dialog', dialogClass]"
    >
      <div class="chat-container">
        <div class="chat-messages">
          <div
              v-for="(msg, index) in messages"
              :key="index"
              class="chat-message"
              :class="msg.type"
          >
            <span>{{ msg.content }}</span>
          </div>
        </div>
        <div class="chat-input">
          <input
              type="text"
              v-model="userInput"
              :placeholder="$t('chat.input')"
              @keyup.enter="handleSend"
          />
          <button @click="handleSend">{{ $t('chat.send') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { sendUserMessage } from '@/api/ai/chatApi.js';
import { useRoute } from "vue-router";
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

// User input and message storage
const userInput = ref('');
const messages = ref([]);
const isChatOpen = ref(false);
const showWelcomeMessage = ref(false); // Controls the display of the welcome message
const route = useRoute();
const hasOpenedOnce = ref(false);

// Default language, can be set to 'zh' or 'en' based on requirements
const lang = route.params.lang;

// Message sending handler
const handleSend = async () => {
  if (!userInput.value.trim()) return;

  const inputMessage = userInput.value;
  messages.value.push({ type: 'user', content: inputMessage });
  userInput.value = '';

  messages.value.push({ type: 'loading', content: locale.value === 'zh' ? '正在加载...' : 'Loading...' });
  const loadingIndex = messages.value.length - 1;

  try {
    const response = await sendUserMessage(locale.value, inputMessage);
    if (response.data && response.data.message) {
      messages.value[loadingIndex] = { type: 'ai', content: response.data.message };
    }
  } catch (error) {
    console.error('发送消息失败：', error);
    messages.value[loadingIndex] = { type: 'ai', content: locale.value === 'zh' ? '回复失败，请重试' : 'Failed to respond, please try again' };
  }
};

// Toggle dialog display
const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
  if (isChatOpen.value) hasOpenedOnce.value = true;
  showWelcomeMessage.value = false;
};

// Manually close the welcome message
const closeWelcomeMessage = () => {
  showWelcomeMessage.value = false;
  localStorage.setItem('welcomeLastShown', Date.now().toString());
};

// Initialize welcome message display (with localStorage check)
onMounted(() => {
  const lastShown = localStorage.getItem('welcomeLastShown');
  const now = Date.now();
  if (!lastShown || now - parseInt(lastShown) > 3600000) {
    showWelcomeMessage.value = route.name === 'Home';
  }
});

// Watch for route changes, display the welcome message when returning to the homepage (with localStorage check)
watch(() => route.name, (newName) => {
  const lastShown = localStorage.getItem('welcomeLastShown');
  const now = Date.now();
  if (newName === 'Home' && (!lastShown || now - parseInt(lastShown) > 3600000)) {
    showWelcomeMessage.value = true;
    localStorage.setItem('welcomeLastShown', now.toString());
    hasOpenedOnce.value = false;
  }
});

// Compute class binding
const dialogClass = computed(() => isChatOpen.value ? 'fade-in' : 'fade-out');
</script>

<style scoped>
.chatbot-icon {
  position: fixed;
  left: 0;
  bottom: 0;
  cursor: pointer;
  width: clamp(80px, 10vw, 150px); /* Minimum 80px for small screens, maximum 150px for large screens */
  height: clamp(80px, 10vw, 150px);
  overflow: hidden;
  z-index: 999;
  user-select: none;
  transition: all 0.3s ease;
  border: none;
  border-radius: 0;
}
.chatbot-icon:hover {
  filter: brightness(0.8);
}
.chatbot-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  -webkit-user-drag: none; /* Disable dragging of the image */
  user-select: none; /* Disable selecting the image */
  transform: scaleX(-1);
}
.welcome-message {
  position: fixed;
  bottom: 20px;
  left: 150px;
  background-color: #fff;
  color: #000;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-size: 14px;
  z-index: 1001;
  max-width: 280px;
  word-wrap: break-word;
  animation: popIn 0.4s ease forwards;
  border: 1px solid #ccc;
}
@keyframes popIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.welcome-message::after {
  content: '';
  position: absolute;
  top: 50%;
  left: -10px;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-right: 10px solid #fff;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  filter: drop-shadow(-1px -1px 0 #ccc) drop-shadow(-1px 1px 0 #ccc);
}
.welcome-text {
  text-align: center;
  line-height: 1.5; /* Increase line height */
}
.message-zh, .message-en {
  margin: 0;
}
.close-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: transparent;
  border: none;
  color: #000;
  font-size: 16px;
  cursor: pointer;
}
.chatbot-dialog {
  opacity: 0;
  transform: translateY(20px);
  animation: slideIn 0.3s ease forwards;
  position: fixed;
  bottom: 20px;
  left: 150px;
  width: 330px;
  height: 400px;
  border: 1px solid #ccc;
  background-color: #fff;
  border-bottom-right-radius: 12px;
  border-top-right-radius: 12px;
  border-top-left-radius: 12px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}
@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes slideOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(20px);
  }
}
.fade-in {
  animation: slideIn 0.3s ease forwards;
}
.fade-out {
  animation: slideOut 0.3s ease forwards;
}
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-height: 100%;
}
.chat-messages {
  flex: 1;
  overflow-y: auto; /* Ensure the message area has a vertical scrollbar */
  padding: 10px;
  max-height: 100%; /* Ensure it does not exceed the parent container */
}
.chat-message {
  margin: 5px 0;
  padding: 8px;
  border-radius: 20px; /* Rounded bubble style */
  word-wrap: break-word; /* Force line break */
  max-width: 90%; /* Limit the maximum width of the message */
  font-size: 14px;
  color: #000; /* Day mode */
}
.chat-message.user {
  background-color: #daf5d4;
  text-align: right;
  border-bottom-right-radius: 0;
}
.chat-message.ai {
  background-color: #f0f0f0;
  text-align: left;
  border-bottom-left-radius: 0;
}
.chat-message.loading {
  background-color: #f0f0f0;
  text-align: left;
  font-style: italic;
  color: #555;
}
.chat-input {
  display: flex;
  padding: 10px;
  background-color: #f9f9f9;
  border-top: 1px solid #ccc;
  border-bottom-right-radius: 12px;
  position: relative; /* Add relative positioning */
}
.chat-input::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: -10px;
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 0px solid transparent;
  border-right: 10px solid #f9f9f9;
  border-radius: 2px;
  box-sizing: border-box;
  filter: drop-shadow(-1px -1px 0 #ccc) drop-shadow(-1px 1px 0 #ccc);
}
.chat-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.chat-input button {
  margin-left: 5px;
  padding: 8px 12px;
  background-color: #43953c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
@media (prefers-color-scheme: dark) {
  .chatbot-dialog {
    background-color: #1e1e1e;
    border-color: #444;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
  }
  .chat-message {
    color: #fff;
  }
  .chat-message.user {
    background-color: #2e7d32;
  }
  .chat-message.ai, .chat-message.loading {
    background-color: #333;
  }
  .chat-input {
    background-color: #1e1e1e;
    border-color: #444;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
  }
  .chat-input input {
    background-color: #2b2b2b;
    color: #fff;
    border-color: #555;
  }
  .chat-input::after {
    border-right-color: #1e1e1e;
    filter: drop-shadow(-1px -1px 0 #444) drop-shadow(-1px 1px 0 #444);
  }
  .welcome-message {
    background-color: #1e1e1e;
    color: #fff;
    border-color: #444;
  }
  .welcome-message::after {
    border-right-color: #1e1e1e;
    filter: drop-shadow(-1px -1px 0 #444) drop-shadow(-1px 1px 0 #444);
  }
  .close-btn {
    color: #fff;
  }
}
</style>