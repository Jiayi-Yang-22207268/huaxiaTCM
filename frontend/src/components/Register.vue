<template>
  <div class="register-page">
    <!-- Left-side Hero Section -->
    <section class="hero-container">
      <picture>
        <source media="(prefers-color-scheme: light)" srcset="/hero-static-light.jpg" />
        <img src="/hero-static.png" alt="Static Cover" class="hero-image" />
      </picture>
      <div class="hero-overlay">
        <h1 class="hero-title">{{ $t('homePage.welcome') }}</h1>
        <p class="hero-subtitle">{{ $t('homePage.tagLine') }}</p>
      </div>
    </section>
    <!-- Right-side Registration Form -->
    <div class="register-container">
      <div class="register-box">
        <h1>{{ $t('auth.register') }}</h1>
        <form @submit.prevent="handleRegister">
          <input
              v-model="username"
              type="text"
              :placeholder="$t('auth.username')"
              required
          />
          <input
              v-model="password"
              type="password"
              :placeholder="$t('auth.password')"
              required
          />
          <!-- Password Strength Indicator -->
          <div class="strength-meter">
            <div
                class="strength-bar"
                :style="{
                width: strengthScore + '%',
                backgroundColor: strengthColor
              }"
            ></div>
          </div>
          <input
              v-model="confirmPassword"
              type="password"
              :placeholder="$t('auth.confirmPassword')"
              required
          />
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
          <button type="submit">{{ $t('auth.register') }}</button>
        </form>
        <p>
          {{ $t('auth.haveAccount') }}
          <router-link :to="`/${$route.params.lang}/login`">
            {{ $t('auth.login') }}
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useI18n } from 'vue-i18n';

const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const { t } = useI18n();

// Password strength calculation
const strengthScore = computed(() => {
  let score = 0;
  const pwd = password.value;
  if (pwd.length >= 8) score += 25;
  if (/[A-Z]/.test(pwd)) score += 20;
  if (/[a-z]/.test(pwd)) score += 20;
  if (/[0-9]/.test(pwd)) score += 20;
  if (/[^A-Za-z0-9]/.test(pwd)) score += 15;
  return Math.min(score, 100);
});

const strengthColor = computed(() => {
  const s = strengthScore.value;
  if (s < 40) return '#e03e2d';
  if (s < 70) return '#f5a623';
  return '#4CAF50';
});

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = t('auth.passwordMismatch');
    return;
  }
  errorMessage.value = '';
  await authStore.registerUser(username.value, password.value);
  router.push(`/${route.params.lang}/login`);
};

// Animation circle logic
onMounted(() => {
  const loginBox = document.querySelector('.register-box');
  let span;
  let inTime, outTime;
  let isIn = true;
  let isOut;

  if (!loginBox) return;

  // Use mouseover and mouseout, and check relatedTarget
  loginBox.addEventListener('mouseover', (e) => {
    const related = e.relatedTarget;
    // Only trigger when relatedTarget is not inside loginBox
    if (!related || !loginBox.contains(related)) {
      console.log('true mouseenter triggered');
      isOut = false;
      if (isIn) {
        inTime = new Date().getTime();
        span = document.createElement('span');
        span.classList.add('hover-circle');
        console.log('span created', span);
        loginBox.appendChild(span);

        span.style.animation = 'none';
        span.offsetHeight;
        requestAnimationFrame(() => {
          span.style.animation = 'login-circle-in 0.5s ease-out forwards';
        });

        const rect = loginBox.getBoundingClientRect();
        const top = e.clientY - rect.top;
        const left = e.clientX - rect.left;
        span.style.top = top + 'px';
        span.style.left = left + 'px';

        isIn = false;
        isOut = true;
      }
    }
  });

  loginBox.addEventListener('mouseout', (e) => {
    const related = e.relatedTarget;
    // Only trigger when relatedTarget is not inside loginBox
    if (!related || !loginBox.contains(related)) {
      console.log('true mouseleave triggered');
      if (isOut) {
        outTime = new Date().getTime();
        const passTime = outTime - inTime;

        const leave = () => {
          span.style.animation = 'none';
          span.offsetHeight;
          requestAnimationFrame(() => {
            span.style.animation = 'login-circle-out 0.5s ease-out forwards';
          });

          const rect = loginBox.getBoundingClientRect();
          const top = e.clientY - rect.top;
          const left = e.clientX - rect.left;
          span.style.top = top + 'px';
          span.style.left = left + 'px';

          setTimeout(() => {
            console.log('removing span');
            if (span && loginBox.contains(span)) {
              loginBox.removeChild(span);
            }
            isIn = true;
          }, 500);
        };

        if (passTime < 500) {
          setTimeout(leave, 500 - passTime);
        } else {
          leave();
        }
      }
    }
  });
});
</script>

<style scoped>
.register-page {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Left Hero Section */
.hero-container {
  position: relative;
  flex: 1.2;
  min-width: 0;
  overflow: hidden;
}
.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  filter: blur(0);
}
.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 5%;
  opacity: 0;
  animation: overlayFadeIn 3s ease-in-out forwards;
}
.hero-title {
  font-family: inherit;
  font-size: 3.5rem;
  color: #fff;
  margin: 0 0 1rem;
}
.hero-subtitle {
  font-family: inherit;
  font-size: 1.5rem;
  color: #f0f0f0;
}

/* Right Registration Form */
.register-container {
  flex: 0.8;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background);
}
.register-box {
  position: relative;
  z-index: 3;
  width: 100%;
  max-width: 360px;
  background: var(--color-background-soft);
  backdrop-filter: blur(4px);
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  overflow: hidden;
}

/* Password Strength Indicator */
.strength-meter {
  height: 6px;
  background: var(--color-background-mute);
  border-radius: 3px;
  overflow: hidden;
  margin: 4px 0 12px;
}
.strength-bar {
  height: 100%;
  width: 0;
  transition: width 0.3s, background-color 0.3s;
}

/* Form Elements */
input {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid var(--color-border);
  border-radius: 5px;
  font-size: 16px;
  background: var(--color-background-mute);
  color: var(--color-text);
  transition: border-color 0.3s;
}
input:focus {
  border-color: var(--vt-c-indigo);
  outline: none;
}
.error {
  color: #e03e2d;
  font-size: 14px;
  margin-bottom: 10px;
}
button {
  width: 100%;
  padding: 12px;
  background: var(--vt-c-indigo);
  color: var(--vt-c-white);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background 0.3s, transform 0.2s, box-shadow 0.2s;
}
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  background: #1f2a38;
}
p {
  margin-top: 15px;
  font-size: 14px;
  color: var(--color-text);
}
a {
  color: var(--vt-c-indigo);
  text-decoration: none;
  font-weight: bold;
}
a:hover {
  text-decoration: underline;
}

/* Animation Keyframes */
@keyframes blurBg {
  from { filter: blur(0); }
  to { filter: blur(8px); }
}
@keyframes overlayFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.register-box h1,.register-box form,.register-box p,.register-box input,.register-box a {
  position: relative;
  z-index: 11;
}

/* Dark Mode Adaptation */
@media (prefers-color-scheme: dark) {
  .register-box {
    background: rgba(32, 32, 32, 0.8);
  }
  input {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: #eee;
  }
  .error {
    color: #f28b82;
  }
  button {
    background: #57606f;
    color: #fff;
  }
  button:hover {
    background: #4a535f;
  }
  p, h2 {
    color: #f0f0f0;
  }
  .register-box h1,
  .register-box form,
  .register-box p,
  .register-box input,
  .register-box a {
    position: relative;
    z-index: 11;
  }
}

/* Small Screen Adaptation */
@media (max-width: 768px) {
  .register-page { flex-direction: column; }
  .hero-container { flex: none; height: 40vh; }
  .register-container { flex: none; height: 60vh; }
}
</style>

<style>
/* Hover circle effect for register-box */
.register-page .hover-circle {
  position: absolute;
  width: 0;
  height: 0;
  background-color: var(--hover-circle-color);
  transform: translate(-50%, -50%);
  border-radius: 50%;
  pointer-events: none;
  z-index: 10;
  opacity: 0.8;
  animation-fill-mode: forwards;
  will-change: width, height;
  animation-play-state: running;
}

:root {
  --hover-circle-color: #ffcf80;
}

@media (prefers-color-scheme: dark) {
  :root {
    --hover-circle-color: #213243;
  }
}

@keyframes login-circle-in {
  0% {
    width: 0;
    height: 0;
  }
  100% {
    width: 1200px;
    height: 1200px;
  }
}

@keyframes login-circle-out {
  0% {
    width: 1200px;
    height: 1200px;
  }
  100% {
    width: 0;
    height: 0;
  }
}
</style>