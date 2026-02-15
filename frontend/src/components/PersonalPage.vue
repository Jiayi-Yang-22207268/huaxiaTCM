<template>
  <div class="personal-page">
    <h2>{{ $t('personal.welcome', { username: authStore.user.username }) }}</h2>
    <!-- Avatar display and upload -->
    <div class="avatar-section card">
      <img
          v-if="avatarPreview"
          :src="avatarPreview"
          alt="User Avatar"
          class="avatar-img"
      />
      <p v-else class="no-avatar">{{ $t('personal.noAvatar') }}</p>
      <div class="upload-section">
        <!-- Custom file selection button, only for preview -->
        <label class="file-btn">
          {{ $t('personal.selectFile') }}
          <input
              type="file"
              accept="image/*"
              @change="onFileChange"
              hidden
          />
        </label>
        <button
            class="btn"
            :disabled="!selectedFile"
            @click="handleAvatarUpload"
        >
          {{ $t('personal.uploadAvatar') }}
        </button>
      </div>
    </div>
    <!-- Height, weight, age editing area -->
    <div class="info-section card">
      <p>
        <strong>{{ $t('personal.username') }}:</strong>
        <span class="readonly-field">{{ authStore.user.username }}</span>
      </p>
      <p>
        <strong>{{ $t('personal.userId') }}:</strong>
        <span class="readonly-field">{{ authStore.user.id }}</span>
      </p>
      <p>
        <strong>{{ $t('personal.role') }}:</strong>
        <span class="readonly-field">{{ authStore.user.role }}</span>
      </p>
      <div class="field-group">
        <label>
          {{ $t('personal.height') }}
          <input
              v-model="height"
              type="number"
              :placeholder="$t('personal.phh')"
          />
        </label>
        <label>
          {{ $t('personal.weight') }}
          <input
              v-model="weight"
              type="number"
              :placeholder="$t('personal.phw')"
          />
        </label>
        <label>
          {{ $t('personal.age') }}
          <input
              v-model="age"
              type="number"
              :placeholder="$t('personal.pha')"
          />
        </label>
      </div>
      <button class="btn" @click="handleUpdate">
        {{ $t('personal.update') }}
      </button>
    </div>
    <button class="btn logout-btn" @click="handleLogout">
      {{ $t('personal.logout') }}
    </button>
    <!-- AI chat component -->
    <ChatBot></ChatBot>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/stores/authStore';
import ChatComponent from '@/components/AI/ChatComponent.vue';
import { updateUserInfo, uploadAvatar } from '@/api/auth/auth.js';
import { getAvatar } from '@/api/admin/userManagement.js';
import ChatBot from "@/components/AI/ChatBot.vue";

const { t } = useI18n();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const selectedFile = ref(null);
const avatarPreview = ref('');
const height = ref('');
const weight = ref('');
const age = ref('');

onMounted(async () => {
  await authStore.fetchUserInfo();
  console.log('user:', authStore.user);
  const avatarUrl = await getAvatar(authStore.token);
  if (avatarUrl) {
    avatarPreview.value = avatarUrl;
    authStore.user.avatar = avatarUrl;
  }
  height.value = authStore.user.height || '';
  weight.value = authStore.user.weight || '';
  age.value = authStore.user.age || '';
});

// Only for preview, not uploading
const onFileChange = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  selectedFile.value = file;
  const reader = new FileReader();
  reader.onload = () => {
    avatarPreview.value = reader.result;
  };
  reader.readAsDataURL(file);
};

// Upload only when the button is clicked
const handleAvatarUpload = async () => {
  if (!selectedFile.value) return;
  try {
    await uploadAvatar(selectedFile.value, authStore.token);
    await authStore.fetchUserInfo();
    alert(t('personal.uploadSuccess'));
    selectedFile.value = null;
  } catch {
    alert(t('personal.uploadFail'));
  }
};

const handleUpdate = async () => {
  try {
    const updatedData = {
      height: Number(height.value),
      weight: Number(weight.value),
      age: Number(age.value),
    };
    const res = await updateUserInfo(updatedData, authStore.token);
    authStore.updateUserInfo(res.data.data);
    alert(t('personal.updateSuccess'));
  } catch {
    alert(t('personal.updateFail'));
  }
};

const handleLogout = () => {
  authStore.logout();
  router.push(`/${route.params.lang}/login`);
};
</script>

<style scoped>
@import "../assets/css/component.css";

/* -- Container -- */
.personal-page {
  padding: 20px;
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
  width: 1000px;
  margin: 0 auto;
  --card-bg: #ffffff;
  --accent: #ba5f39;
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  .personal-page {
    --bg: #121212;
    --text: #e0e0e0;
    --card-bg: #1f1f1f;
  }
}

/* -- Card styling (same as herb-list cards) -- */
.card {
  background: var(--card-bg);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

/* -- Section titles mirror group titles -- */
h2 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  border-left: 4px solid var(--accent);
  padding-left: 0.5rem;
  color: var(--text);
}

/* -- Avatar / Upload -- */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}
.avatar-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
}
.no-avatar {
  color: var(--text);
}
.upload-section {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
}

/* -- Buttons (using the same accent color) -- */
.file-btn,
.btn {
  padding: 8px 15px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}
.file-btn:hover,
.btn:hover:not(:disabled) {
  background: #9c4a2d;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* -- User info form -- */
.info-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.info-section p {
  margin: 0;
  line-height: 1.4;
}
.field-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.field-group label {
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
}
.field-group input {
  margin-top: 0.25rem;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: var(--card-bg);
  color: var(--text);
  width: 120px;
}

/* -- Logout button -- */
.logout-btn {
  display: block;
  margin: 0 auto 2rem;
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
  transition: background 0.2s, color 0.2s;
}
.logout-btn:hover {
  background: var(--accent);
  color: #fff;
}

/* -- Ensure ChatBot sits nicely at the bottom -- */
personal-page > ChatBot,
.ChatBot {
  margin-top: 2rem;
}
</style>
