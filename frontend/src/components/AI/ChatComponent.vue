<template>
  <div class="chat-container">
    <h1>{{ $t('chat.title') }}</h1>
    <!-- Input field and send button -->
    <div class="chat-input">
      <input
          type="text"
          v-model="userInput"
          :placeholder="$t('chat.input')"
          @keyup.enter="handleSend"
      />
      <button @click="handleSend">{{$t('chat.send')}}</button>
    </div>
    <!-- Chat history display -->
    <div class="chat-messages">
      <div v-for="(msg, index) in messages" :key="index" class="chat-message">
        <div v-if="msg.type === 'user'" class="user-message">{{ msg.content }}</div>
        <div v-if="msg.type === 'ai'" class="assistant-message">{{ msg.content }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { sendUserMessage } from '@/api/ai/chatApi.js';

// Used to store user input
const userInput = ref('');

// Used to store conversation messages, format: { type: 'user' | 'ai' | 'loading', content: '消息内容' }
const messages = ref([]);

// Default language, can be set to 'zh' or 'en' based on requirements
const lang = ref('zh');

// Send a message to the backend and add the reply to the message list
const handleSend = async () => {
  if (!userInput.value.trim()) return;

  // Save the current user input
  const inputMessage = userInput.value;

  // Add the user's message to the conversation list
  messages.value.push({ type: 'user', content: inputMessage });

  // Immediately clear the input field
  userInput.value = '';

  // Add a "loading" placeholder message and record its position in the array
  messages.value.push({ type: 'loading', content: '正在加载...' });
  const loadingIndex = messages.value.length - 1;

  try {
    // Send the user input and language to the backend
    const response = await sendUserMessage(lang.value, inputMessage);

    // Update the loading message with the actual reply based on the backend's response format { message: 'AI reply content' }
    if (response.data && response.data.message) {
      messages.value[loadingIndex] = { type: 'ai', content: response.data.message };
    }
  } catch (error) {
    console.error('发送消息失败：', error);

    // If an error occurs, update the loading message with an error prompt
    messages.value[loadingIndex] = { type: 'ai', content: '回复失败，请重试' };
  }
};
</script>

<style scoped>
.chat-container {
  padding: 20px;
  width: 400px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  height: 500px; /* Set fixed height */
}

/* Set chat.title (h1) to green */
.chat-container h1 {
  color: green;
}

.chat-input {
  display: flex;
  margin-bottom: 15px;
}

.chat-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.chat-input button {
  padding: 8px 12px;
  border: 1px solid #ccc;
  background-color: #4CAF50;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.chat-messages {
  max-height: 400px; /* Set maximum height for chat box */
  overflow-y: auto; /* Show scroll bar when content exceeds */
  padding-right: 5px; /* Prevent scroll bar from covering text */
}

.chat-message {
  margin-bottom: 10px;
}

.user-message {
  text-align: right;
  background-color: #daf5d4;
  padding: 8px;
  border-radius: 5px;
  word-wrap: break-word; /* Force line breaks */
  max-width: 90%; /* Limit message width to avoid overly wide text */
}

.assistant-message {
  text-align: left;
  background-color: #f0f0f0;
  padding: 8px;
  border-radius: 5px;
  word-wrap: break-word; /* Force line breaks */
  max-width: 90%; /* Limit message width to avoid overly wide text */
}
</style>