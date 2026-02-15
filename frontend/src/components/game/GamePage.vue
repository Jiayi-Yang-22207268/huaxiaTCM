<template>
  <div class="game-page">
    <div v-if="!entered" class="intro-scene">
      <img
          src="/gamePageBg.png"
          :class="['clinic-bg', { 'fade-in': showBgFadeIn, 'bg-zoom-darken': bgZooming }]"
      />

      <div class="intro-overlay">
        <h1>{{ $t('game.title') }}</h1>
        <p>{{ $t('game.intro') }}</p>
        <button @click="handleClick('herb')" class="enter-btn-herb">{{ $t('game.enterHerbMode') }}</button>
        <button @click="handleClick('prescription')" class="enter-btn-practice">{{ $t('game.enterPrescriptionMode') }}</button>
      </div>
      </div>

    <transition name="fade-zoom">
      <div v-if="entered" class="game-select-scene">
        <div class="game-select">
          <router-link :to="{ name: 'HerbGame', params: { lang } }" class="game-button">
            {{ $t('game.herbMode') }}
          </router-link>
          <router-link :to="{ name: 'PrescriptionGame', params: { lang } }" class="game-button">
            {{ $t('game.prescriptionMode') }}
          </router-link>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const lang = route.params.lang || 'zh';

const entered = ref(false);

const showBgFadeIn = ref(true)
onMounted(() => {
  // Only run fade-in animation on first load
  setTimeout(() => {
    showBgFadeIn.value = false
  }, 2000)
})


const clickedButton = ref(null)
const bgZooming = ref(false)

const handleClick = (mode) => {
  bgZooming.value = true
  setTimeout(() => {
    router.push({ name: mode === 'herb' ? 'HerbGame' : 'PrescriptionGame', params: { lang } })
  }, 900) // Animation duration slightly longer than the transition duration
}

</script>

<style scoped>
.game-page {
  position: fixed;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  overflow-y: auto;
}

.game-select {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  margin-top: 50px;
}
.game-button {
  display: inline-block;
  padding: 15px 30px;
  background-color: #4CAF50;
  color: white;
  font-size: 20px;
  border-radius: 8px;
  text-decoration: none;
  border: none;
}

@media (prefers-color-scheme: dark) {
  .game-page {
    background-color: #1e1e1e;
    color: #f0f0f0;
  }

  .game-button {
    background-color: #4CAF50;
    color: #ffffff;
  }
}

.intro-scene {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.clinic-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 1.5s ease, filter 1.5s ease;
}

.clinic-bg.fade-in {
  animation: bgFadeIn 2s ease-out both;
}



.intro-overlay {
  position: absolute;
  bottom: 10%;
  left: 5%;
  color: white;
  background-color: rgba(0, 0, 0, 0.4);
  padding: 20px;
  border-radius: 12px;
  max-width: 400px;
  animation: overlayFadeIn 1.2s ease-out both;
}

.enter-btn-herb,.enter-btn-practice {
  margin-top: 15px;
  padding: 10px 20px;
  font-size: 18px;
  background-color: #ba5f39;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-left: 10px;
}

.clinic-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease, filter 0.6s ease;
}

.clinic-bg.bg-zoom-darken {
  transform: scale(1.5) translateY(-10%);
  filter: brightness(0.6);
  transition: transform 1.5s ease, filter 1.5s ease;
}


.fade-zoom-enter-active {
  animation: fadeZoomIn 0.8s ease-out;
}

@keyframes fadeZoomIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes overlayFadeIn {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bgFadeIn {
  0% {
    opacity: 0;
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
