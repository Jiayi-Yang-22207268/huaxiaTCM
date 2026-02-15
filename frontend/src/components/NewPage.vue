<!-- NewPage.vue -->
<template>
  <div class="authorize-page">
    <div v-if="status === 'pending'" class="authorize-message">
      <p>正在授权，请稍候...</p>
    </div>
    <div v-else-if="status === 'success'" class="authorize-message">
      <p>🎉 授权成功！您现在可以关闭此页面并继续聊天。</p>
      <button @click="goChat">返回聊天</button>
    </div>
    <div v-else-if="status === 'error'" class="authorize-message">
      <p>❌ 授权失败：{{ errorMessage }}</p>
      <button @click="retry">重试授权</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const status = ref('pending')       // pending, success, error
const errorMessage = ref('')

const goChat = () => {
  // 跳回首页并打开聊天弹窗（如果有）。根据所用路由，可以调整为你的聊天页路径或首页路径
  const lang = route.params.lang || 'zh'
  router.push({ path: `/${lang}/home` })
}

const retry = () => {
  // 跳转到后端获取新的 auth_url
  window.location.href = `${window.location.origin}/api/chat/auth-url`
}

onMounted(async () => {
  const code = route.query.code
  if (code) {
    try {
      await axios.get(`/api/chat/oauth/callback?code=${encodeURIComponent(code)}`)
      status.value = 'success'
    } catch (e) {
      errorMessage.value = e.response?.data.detail || e.message
      status.value = 'error'
    }
  } else {
    status.value = 'error'
    errorMessage.value = '未检测到授权 code'
  }
})
</script>

<style scoped>
/* Light & Dark mode variables */
:root {
  --bg-page: #f9f9f9;
  --bg-card: #ffffff;
  --text-color: #333333;
  --btn-bg: #409eff;
  --btn-hover: #66b1ff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg-page: #121212;
    --bg-card: #1e1e1e;
    --text-color: #eeeeee;
    --btn-bg: #3a8ad3;
    --btn-hover: #559be2;
  }
}

div.authorize-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: var(--bg-page);
  padding: 1rem;
}
.authorize-message {
  text-align: center;
  padding: 2rem;
  background-color: var(--bg-card);
  color: var(--text-color);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 90%;
  width: 320px;
}
.authorize-message p {
  margin: 0 0 1rem;
  font-size: 1.1rem;
}
button {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  background-color: var(--btn-bg);
  color: #ffffff;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
button:hover {
  background-color: var(--btn-hover);
}
button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.5);
}
</style>
