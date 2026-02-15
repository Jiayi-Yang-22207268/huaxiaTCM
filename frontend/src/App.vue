<template>
  <div v-if="isLoading" class="global-loader">
    <div class="loader-overlay"></div>
    <div class="loader-content">
      <div class="spinner"></div>
      <p>loading...</p>
    </div>
  </div>
  <!-- Collapse status icon bar, only show when the sidebar is closed -->
  <div :class="{ 'force-dark-nav': route.name === 'HerbGame' || route.name === 'GamePage' || route.name === 'PrescriptionGame' || route.name === 'story1' }">
  <aside
      class="sidebar-collapsed"
      v-if="!isSidebarOpen"
  >
    <!-- Upper half icon -->
    <div class="icon-group">
      <button class="icon-btn" @click="navigateTo('Home')" :title="$t('nav.home')">
        <HomeIcon />
      </button>
      <button class="icon-btn" @click="navigateTo('PrescriptionList')" :title="$t('nav.prescriptions')">
        <ClipboardDocumentListIcon />
      </button>
      <button class="icon-btn" @click="navigateTo('HerbList')" :title="$t('nav.herbs')">
        <SparklesIcon />
      </button>
      <button class="icon-btn" @click="navigateTo('GamePage')" :title="$t('nav.game')">
        <PuzzlePieceIcon />
      </button>
      <button class="icon-btn" @click="navigateTo('QuizPage')" :title="$t('nav.quiz')">
        <QuestionMarkCircleIcon />
      </button>
      <!-- Added the Story Mode icon -->
      <button class="icon-btn" @click="navigateTo('Story')" :title="$t('nav.newPage')">
        <BookOpenIcon />
      </button>

      <!-- Admin-only -->
      <button
          v-if="authStore.token && authStore.user?.role === 'admin'"
          class="icon-btn"
          @click="navigateTo('AdminPage')"
          :title="$t('nav.admin')"
      >
        <Cog6ToothIcon />
      </button>

      <!-- Login/Register -->
      <button v-if="!authStore.user" class="icon-btn" @click="navigateTo('Login')" :title="$t('nav.login')">
        <KeyIcon />
      </button>
      <button v-if="!authStore.user" class="icon-btn" @click="navigateTo('Register')" :title="$t('nav.register')">
        <PencilSquareIcon />
      </button>

      <!-- Personal Center/Exit -->
      <button v-if="authStore.user" class="icon-btn" @click="navigateTo('PersonalPage')" :title="$t('nav.personal')">
        <UserIcon />
      </button>
      <button v-if="authStore.user" class="icon-btn" @click="handleLogout" :title="$t('nav.logout')">
        <ArrowRightOnRectangleIcon />
      </button>

      <!-- Language Switching -->
      <button class="icon-btn" @click="switchLanguage" :title="$t('switch_language')">
        <GlobeAltIcon />
      </button>
    </div>

    <!-- Expand button at the bottom -->
    <button class="hamburger" @click="toggleSidebar" :title="$t('nav.open')">
      <Bars3Icon />
    </button>
  </aside>
  </div>
  <!-- Expand the status sidebar (legacy style) -->
  <aside class="sidebar" :class="{ open: isSidebarOpen }">
    <button class="close-btn" @click="toggleSidebar">×</button>
    <nav class="sidebar-nav">
      <button @click="navigateTo('Home')">{{ $t('nav.home') }}</button>
      <button @click="navigateTo('PrescriptionList')">{{ $t('nav.prescriptions') }}</button>
      <button @click="navigateTo('HerbList')">{{ $t('nav.herbs') }}</button>
      <button @click="navigateTo('GamePage')">{{ $t('nav.game') }}</button>
      <button @click="navigateTo('QuizPage')">{{ $t('nav.quiz') }}</button>
      <button @click="navigateTo('Story')">{{ $t('nav.newPage') }}</button>
      <button
          v-if="authStore.token && authStore.user?.role === 'admin'"
          @click="navigateTo('AdminPage')"
      >{{ $t('nav.management') }}</button>
      <button v-if="!authStore.user" @click="navigateTo('Login')">{{ $t('nav.login') }}</button>
      <button v-if="!authStore.user" @click="navigateTo('Register')">{{ $t('nav.register') }}</button>
      <button v-if="authStore.user" @click="navigateTo('PersonalPage')">{{ $t('nav.personal') }}</button>
      <button v-if="authStore.user" @click="handleLogout">{{ $t('nav.logout') }}</button>
      <button @click="switchLanguage">{{ $t('switch_language') }}</button>
    </nav>
  </aside>

  <!-- Mask Layer > Main Content Area Remains Unchanged -->
  <transition name="overlay-fade">
    <div class="overlay" v-if="isSidebarOpen" @click="toggleSidebar"></div>
  </transition>
  <main>
    <keep-alive include="HerbGame">
      <router-view />
    </keep-alive>
  </main>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useI18n } from 'vue-i18n'
import { computed, ref, nextTick } from 'vue'

// The correct Heroicons v2 outline icon name
import {
  HomeIcon,
  ClipboardDocumentListIcon,
  SparklesIcon,
  PuzzlePieceIcon,
  QuestionMarkCircleIcon,
  Cog6ToothIcon,
  KeyIcon,
  PencilSquareIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  GlobeAltIcon,
  Bars3Icon,
  BookOpenIcon    // ← 新增
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { locale } = useI18n()

const fullscreenPages = ['NewHome']
const isFullscreenPage = computed(() => fullscreenPages.includes(route.name))

const isSidebarOpen = ref(false)
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const navigateTo = (pageName) => {
  router.push({ name: pageName, params: { lang: locale.value } })
}

const handleLogout = () => {
  authStore.logout()
  router.push(`/${locale.value}/login`)
}

const switchLanguage = () => {
  const newLang = locale.value === 'zh' ? 'en' : 'zh'
  locale.value = newLang
  localStorage.setItem('lang', newLang) // save The Language Selection
  router.push({ path: `/${newLang}${route.path.substring(3)}` })
}

const isLoading = ref(true)

router.beforeEach((to, from, next) => {
  isLoading.value = true
  next()
})


/**
 * Waits until all images in the document have finished loading.
 * Returns a Promise that resolves when all images are complete.
 */
function waitForAllImagesToLoad() {
  const images = Array.from(document.images);
  // If no images, resolve immediately
  if (images.length === 0) return Promise.resolve();
  // Filter images that are not complete
  const notLoadedImages = images.filter(img => !img.complete);
  if (notLoadedImages.length === 0) return Promise.resolve();
  return Promise.all(
    notLoadedImages.map(
      img =>
        new Promise(resolve => {
          img.addEventListener('load', resolve, { once: true });
          img.addEventListener('error', resolve, { once: true });
        })
    )
  );
}

router.afterEach(async () => {
  // Ensure at least 1 frame for loader, then wait for images, then hide loader
  await new Promise(resolve => requestAnimationFrame(resolve));
  await waitForAllImagesToLoad();
  isLoading.value = false;
});

</script>

<style scoped>
/* — Collapse status icon bar — */
.sidebar-collapsed {
  position: fixed;
  top: 0;
  right: 0;
  height: 100%;
  width: 60px;
  background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0.0),  /* Left side transparent */
      rgba(255, 255, 255, 0.6)   /* Opaque on the right */
  );
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  z-index: 1001;
}

/* Upper Half Icon Group */
.sidebar-collapsed .icon-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

/* Specify the size and stroke color of the SVG inside the button */
.sidebar-collapsed .icon-btn svg {
  width: 24px;
  height: 24px;
  stroke: currentColor;
}

/* Default icon gray, hover white */
.sidebar-collapsed .icon-btn {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: #1c1c1c;
}
.sidebar-collapsed .icon-btn:hover {
  color: #fff;
}

/* Bottom Expand Button */
.sidebar-collapsed .hamburger {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #333;
}
.sidebar-collapsed .hamburger svg {
  width: 32px;
  height: 32px;
  stroke: currentColor;
}

/* — Expand the status sidebar — */
.sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 25%;
  height: 100%;
  background-color: #f4f4f4; /* Light Mode Background Color */
  transform: translateX(100%);
  transition: transform 0.3s ease;
  z-index: 1001;
  padding: 20px;
}
.sidebar.open {
  transform: translateX(0);
}

.close-btn {
  background: none;
  border: none;
  font-size: 64px;
  color: #aaaaaa;
  cursor: pointer;
  display: block;
  margin-left: auto;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}
.sidebar-nav button {
  background: none;
  border: none;
  color: #333; /* Light Mode Button Text Color */
  text-align: left;
  padding: 10px 0;
  font-size: 18px;
  width: 100%;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
.sidebar-nav button:hover {
  background: rgba(0, 0, 0, 0.1); /* Light mode button hover color */
}

/* Mask Layer */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(4px);
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 1000;
}


/* Sidebar adaptation in dark mode */
@media (prefers-color-scheme: dark) {
  .sidebar-collapsed {
    background: linear-gradient(
        to right,
        rgba(51, 51, 51, 0.0), /* Left Transparent */
        rgba(51, 51, 51, 0.6)  /* Opaque on the right */
    );
  }

  .sidebar {
    background-color: #222; /* Sidebar background color in dark mode */
  }

  .sidebar-nav button {
    color: #ddd; /* Button text color in dark mode */
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .sidebar-nav button:hover {
    background: rgba(255, 255, 255, 0.2); /* Button hover color in dark mode */
  }

  .sidebar-collapsed .hamburger {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    color: #ddd;
  }


}

/* Sidebar adaptation in light mode */
@media (prefers-color-scheme: light) {
  .sidebar-collapsed {
    background: linear-gradient(
        to right,
        rgba(51, 51, 51, 0.0), /* Left Transparent */
        rgba(51, 51, 51, 0.6)  /* Opaque on the right */
    );
  }

  .sidebar {
    background-color: #f4f4f4; /* Sidebar background color in light mode */
  }

  .sidebar-nav button {
    color: #333; /* Button text color in light mode */
  }

  .sidebar-nav button:hover {
    background: rgba(0, 0, 0, 0.1); /* Button hover color in light mode */
  }
}

/* Other global layouts (unchanged) */
header {
  background-color: transparent;
  padding: 0;
  height: auto;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}
@media (prefers-color-scheme: dark) {
  header {
    background-color: #000;
    color: white;
  }
  .sidebar-collapsed .icon-btn {
    color: #aaa;
  }
}
main {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  height:100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

.global-loader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2000;
}

.loader-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(8px);
  background-color: rgba(0, 0, 0, 0.3);
}

.loader-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

  .force-dark-nav .sidebar-collapsed {
    background: rgba(0, 0, 0, 0.7) !important;
  }
  .force-dark-nav .sidebar-collapsed .icon-btn {
    color: white !important;
  }
  .force-dark-nav .sidebar-collapsed .icon-btn:hover {
    color: #ccc !important;
  }
  .force-dark-nav .sidebar {
    background-color: #000 !important;
  }
  .force-dark-nav .sidebar-nav button {
    color: white !important;
  }
  .force-dark-nav .sidebar-nav button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
  }


</style>
