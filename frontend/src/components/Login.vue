<template>
  <div class="login-page">
    <!-- Left-side Hero section -->
    <section class="hero-container">
      <picture>
        <source media="(prefers-color-scheme: light)" srcset="/hero-static-light.jpg" />
        <img src="/hero-static.png" alt="Static cover" class="hero-image" />
      </picture>
      <div class="hero-overlay">
        <h1 class="hero-title">{{ $t('homePage.welcome') }}</h1>
        <p class="hero-subtitle">{{ $t('homePage.tagLine') }}</p>
      </div>
    </section>
    <!-- Right-side login form -->
    <div class="login-container">
      <div class="login-box">
        <h1>{{ $t('auth.login') }}</h1>
        <form @submit.prevent="handleLogin">
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
          <button type="submit">{{ $t('auth.login') }}</button>
        </form>
        <p>
          {{ $t('auth.noAccount') }}
          <router-link :to="`/${$route.params.lang}/register`">
            {{ $t('auth.register') }}
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const username = ref('');
const password = ref('');
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const handleLogin = async () => {
  await authStore.loginUser(username.value, password.value);
  if (authStore.token) {
    await authStore.fetchUserInfo();
    router.push(`/${route.params.lang}/personal`);
  }
};

// Animation circle logic
onMounted(() => {
  const loginBox = document.querySelector('.login-box');
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
.login-page {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Hero Section */
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

/* Login Form Section */
.login-container {
  flex: 0.8;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-background);
}

/* Login form box, ensures the animated content won't be clipped */
.login-box {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  height: 60%;
  max-width: 360px;
  background: var(--color-background-soft);
  backdrop-filter: blur(4px);
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  overflow: hidden;
  background-color: #f6f6f6;
}
.login-box h1 {
  margin-bottom: 30px;
  margin-top: 30px;
  z-index: 11;
}
.login-box form {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 16px;
  z-index: 11;
}
.login-box p {
  margin-top: 20px;
  z-index: 11;
}

/* Form Elements */
input {
  width: 100%;
  padding: 12px;
  margin: 0;
  border: 1px solid var(--color-border);
  border-radius: 5px;
  font-size: 16px;
  background: var(--color-background-mute);
  color: var(--color-text);
  transition: border-color 0.3s;
  z-index: 11;
}
input:focus {
  border-color: var(--vt-c-indigo);
  outline: none;
  z-index: 11;
}
.login-box button {
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
  position: relative;
  z-index: 11;
}
.login-box button:hover {
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

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .login-box {
    background: rgba(32, 32, 32, 0.8);
  }
  .login-box h1,
  .login-box form,
  .login-box p,
  .login-box input,
  .login-box a {
    position: relative;
    z-index: 11;
  }
  .login-box input {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: #eee;
  }
  .login-box button {
    background: #57606f;
    color: #fff;
    z-index: 11;
  }
  .login-box button:hover {
    background: #4a535f;
    z-index: 11;
  }
  .login-box p, h2 {
    color: #f0f0f0;
    z-index: 11;
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
}

/* Small Screen Adaptation */
@media (max-width: 768px) {
  .login-page { flex-direction: column; }
  .hero-container { flex: none; height: 40vh; }
  .login-container { flex: none; height: 60vh; }
}
</style>
<style>
.login-page .hover-circle {
  position: absolute;
  width: 0;
  height: 0;
  background-color: var(--hover-circle-color);
  /* Removed mix-blend-mode to ensure pure color overlay */
  transform: translate(-50%, -50%);
  border-radius: 50%;
  pointer-events: none;
  z-index: 1;
  opacity: 0.8;
  animation-fill-mode: forwards;
  will-change: width, height;
  animation-play-state: running;
}
:root {
  --hover-circle-color: #ffcf80; /* Use light color during the day */
}
@media (prefers-color-scheme: dark) {
  :root {
    --hover-circle-color: #213243; /* Use bright color at night */
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
