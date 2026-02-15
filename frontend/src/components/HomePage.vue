<template>
  <div class="container">
    <!-- ====== Static cover area ====== -->
    <section class="hero-container reveal">
      <picture>
        <source media="(prefers-color-scheme: light)" srcset="/hero-static-light.jpg" />
        <img src="/hero-static.png" alt="静态封面" class="hero-image" />
      </picture>
      <div class="hero-overlay">
        <h1 class="hero-title">{{ $t('homePage.welcome') }}</h1>
        <p class="hero-subtitle">{{ $t('homePage.tagLine') }}</p>
      </div>
      <div class="scroll-down" @click="scrollToTiles">
        <span class="arrow">&#x25BC;</span>
      </div>
    </section>
    <!-- Phantom-style cards -->
    <section class="tiles reveal">
      <article class="style1">
    <span class="image">
      <img src="/herbWiki.jpeg" alt="Herb Wiki" />
    </span>
        <router-link
            :to="{ name: 'HerbList', params: { lang: locale.value } }"
            class="tile-link"
        >
          <h2>{{ $t('homePage.herbWiki')}}</h2>
          <div class="content">
            <p>{{ $t('homePage.herbWikiDescription') }}</p>
          </div>
        </router-link>
      </article>
      <article class="style3">
    <span class="image">
      <img src="/preWiki.jpg" alt="Prescription Wiki" />
    </span>
        <router-link
            :to="{ name: 'PrescriptionList', params: { lang: locale.value } }"
            class="tile-link"
        >
          <h2>{{ $t('homePage.preWiki')}}</h2>
          <div class="content">
            <p>{{ $t('homePage.preWikiDescription') }}</p>
          </div>
        </router-link>
      </article>
      <article class="style5">
    <span class="image">
      <img src="/quiz.jpg" alt="Quiz Section" />
    </span>
        <router-link
            :to="{ name: 'QuizPage', params: { lang: locale.value } }"
            class="tile-link"
        >
          <h2>{{ $t('homePage.quiz')}}</h2>
          <div class="content">
            <p>{{ $t('homePage.quizDescription') }}</p>
          </div>
        </router-link>
      </article>
      <article class="style2">
    <span class="image">
      <img src="/game.png" alt="Game Section" />
    </span>
        <router-link
            :to="{ name: 'GamePage', params: { lang: locale.value } }"
            class="tile-link"
        >
          <h2>{{ $t('homePage.game')}}</h2>
          <div class="content">
            <p>{{ $t('homePage.gameDescription') }}</p>
          </div>
        </router-link>
      </article>
      <article class="style4">
    <span class="image">
      <img src="/story.webp" alt="TCM Story" />
    </span>
        <router-link
            :to="{ name: 'Story', params: { lang: locale.value } }"
            class="tile-link"
        >
          <h2>{{ $t('homePage.story')}}</h2>
          <div class="content">
            <p>{{ $t('homePage.storyDescription') }}</p>
          </div>
        </router-link>
      </article>
      <article class="style6">
    <span class="image">
      <img src="/BianQue.jpg" alt="Contact Section" />
    </span>
        <a href="#" @click.prevent="scrollToAboutUs" class="tile-link">
          <h2>{{ $t('homePage.contact')}}</h2>
          <div class="content">
            <p>{{ $t('homePage.contactDescription') }}</p>
          </div>
        </a>
      </article>
    </section>
    <!-- Carousel image area-->
    <div class="image-section reveal">
      <div class="text-block">
        <h2>{{ $t('homePage.aboutTcmTitle')}}</h2>
        <hr />
        <p>{{ $t('homePage.aboutTcm')}}</p>
      </div>
      <div class="image-container" v-if="bannerImages.length">
        <button class="arrow-btn left" @click="prevBanner">&#10094;</button>
        <button class="arrow-btn right" @click="nextBanner">&#10095;</button>
        <div
          class="image-slider"
          :style="{ transform: `translateX(-${currentBannerIndex * 100}%)` }"
        >
          <img
            v-for="(img, index) in bannerImages"
            :key="index"
            :src="img.imageUrl"
            alt="养生图片"
            class="image"
          />
        </div>
      </div>
      <div class="image-container" v-else>
        <p>{{ t('banner.noImage') }}</p>
      </div>
    </div>

<!--    <div class="content-container">-->
<!--      <div class="left-container">-->
<!--        &lt;!&ndash; 显示常见药材 &ndash;&gt;-->
<!--        <div class="herb-list">-->
<!--          <h3>{{ $t('homePage.usefulHerbs') }}</h3>-->
<!--          <div class="herb-items-container">-->
<!--            <div-->
<!--                v-for="herb in herbs"-->
<!--                :key="herb.id"-->
<!--                @click="viewHerbDetail(herb.id)"-->
<!--                class="herb-card"-->
<!--            >-->
<!--              <img :src="herb.image" alt="药材图片" class="herb-image" />-->
<!--              {{ herb.name }}-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->

<!--        &lt;!&ndash; 药方列表 &ndash;&gt;-->
<!--        <div class="prescription-list">-->
<!--          <h3>{{ $t('homePage.classicPrescriptions') }}</h3>-->
<!--          <div class="prescription-items-container">-->
<!--            <div-->
<!--                v-for="prescription in prescriptions"-->
<!--                :key="prescription.id"-->
<!--                @click="viewPrescriptionDetail(prescription.id)"-->
<!--                class="prescription-item"-->
<!--            >-->
<!--              {{ prescription.name }}-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->

<!--      <div class="right-container">-->
<!--        &lt;!&ndash; 显示养生信息 &ndash;&gt;-->
<!--        <HealthSuggestion />-->

<!--        &lt;!&ndash; 显示药材排名 &ndash;&gt;-->
<!--        <RankingList />-->

<!--        &lt;!&ndash; 显示药方排名 &ndash;&gt;-->
<!--        <PrescriptionRankingList />-->
<!--      </div>-->
    </div>


  <!-- About Us Section -->
  <section id="about-us" class="about-us reveal">
    <h2>{{ $t('homePage.aboutUs')}}</h2>
    <div class="about-us-content">
      <p>
        {{ $t('homePage.aboutUsContent')}}
      </p>
    </div>
    <div class="about-us-images">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="/huaxia-dark.png" />
        <img src="/huaxia.png" alt="info 1" />
      </picture>
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="/togawa-dark.png" />
        <img src="/togawa.png" alt="info 2" />
      </picture>
    </div>
  </section>

  <ChatBot></ChatBot>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import HealthSuggestion from './AI/HealthSuggestion.vue';
import RankingList from './ranking/RankingList.vue';
import PrescriptionRankingList from './ranking/PrescriptionRankingList.vue';
import ChatBot from "@/components/AI/ChatBot.vue";
import { getPrescriptions } from "@/api/tcm/prewiki.js";
import { getUsefulHerbs } from "@/api/tcm/herbwiki.js";
import { useRoute, useRouter } from "vue-router";

// Assume there is an API method for fetching banner images
import { getHomepageImages } from '@/api/admin/homeManagement.js';

const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();

// Store data for herbs and prescriptions
const herbs = ref([]);
const prescriptions = ref([]);

// Carousel images-related data
const bannerImages = ref([]);
const currentBannerIndex = ref(0);
let bannerTimer = null;

// Load banner images (based on the current language)
const fetchBannerImages = async () => {
  // Call `getBannerImages` to fetch an array of images (each object contains fields like `imageUrl`)
  const images = await getHomepageImages(route.params.lang || 'zh');
  bannerImages.value = images;
};

const navigateTo = (pageName) => {
  router.push({ name: pageName, params: { lang: locale.value } });
}

// Start carousel (if there are multiple images, switch every 3 seconds)
const startBannerCarousel = () => {
  if (bannerImages.value.length > 1) {
    bannerTimer = setInterval(() => {
      currentBannerIndex.value = (currentBannerIndex.value + 1) % bannerImages.value.length;
    }, 3000);
  }
};

const stopBannerCarousel = () => {
  if (bannerTimer) clearInterval(bannerTimer);
};

// Load top 10 useful herbs
const loadUsefulHerbs = async () => {
  herbs.value = await getUsefulHerbs(route.params.lang);
  herbs.value = herbs.value.slice(0, 10);
  console.log(herbs.value);
};

// Load top 18 prescriptions
const loadPrescriptions = async () => {
  const allPrescriptions = await getPrescriptions(route.params.lang);
  prescriptions.value = allPrescriptions.slice(0, 18); // Take the first 18 prescriptions
};

const viewPrescriptionDetail = (id) => {
  router.push(`/${route.params.lang}/prescriptions/${id}`);
};

const viewHerbDetail = (id) => {
  router.push(`/${route.params.lang}/herbs/${id}`);
};

// Scroll to the "About Us" section
const scrollToAboutUs = () => {
  const el = document.getElementById('about-us');
  if (el) el.scrollIntoView({ behavior: 'smooth' });
};

const prevBanner = () => {
  currentBannerIndex.value = (currentBannerIndex.value - 1 + bannerImages.value.length) % bannerImages.value.length;
};

const nextBanner = () => {
  currentBannerIndex.value = (currentBannerIndex.value + 1) % bannerImages.value.length;
};

// Scroll to the tiles section
const scrollToTiles = () => {
  const tiles = document.querySelector('.tiles');
  if (tiles) {
    const offsetTop = tiles.getBoundingClientRect().top + window.pageYOffset + 95;
    window.scrollTo({
      top: offsetTop,
      behavior: 'smooth'
    });
  }
};

watch(() => route.params.lang, async () => {
  await loadPrescriptions();
  await loadUsefulHerbs();
  await fetchBannerImages();
  currentBannerIndex.value = 0;
  stopBannerCarousel();
  startBannerCarousel();
});

onMounted(async () => {
  await loadUsefulHerbs();
  await loadPrescriptions();
  await fetchBannerImages();
  startBannerCarousel();
});

onUnmounted(() => {
  stopBannerCarousel();
});

// IntersectionObserver logic for reveal animations
const revealElements = () => {
  const elements = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  elements.forEach((el) => observer.observe(el));
};

onMounted(() => {
  nextTick(() => {
    revealElements();
  });
});
</script>

<style scoped>
@import '@/assets/css/tile.css';

/* 1. Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans:wght@400&display=swap');

.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  /* Change to min-height, allowing content to scroll if it exceeds the viewport */
  min-height: 100vh;
}

/* 2. Static cover area */
.hero-container {
  position: relative;
  width: 100%;
  height: 100vh; /* Fixed viewport height */
  overflow: hidden; /* Hide overflow area, limit zoom range */
}

.hero-image {
  width: 100%;
  height: auto;
  object-fit: cover;
  margin-top: -15vh; /* Move up by 20% of the viewport height, adjust as needed */
  /* Simple zoom and fade-in animation */
  animation: heroZoomFade 10s ease-out forwards;
}

.hero-container::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50px; /* Adjust height as needed */
  background: linear-gradient(
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,1) 100%
  );
  pointer-events: none;
  z-index: 2;
}

@keyframes heroZoomFade {
  0% {
    transform: scale(1.2);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 3. Text overlay: Centered and with shadow */
.hero-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0,0,0,0.6);
  padding: 0 1rem; /* Small padding to prevent overflow */
}

/* 4. Title: Larger and more prominent Montserrat bold font */
.hero-title {
  font-family: 'Montserrat', sans-serif;
  font-size: 4rem; /* Changed from 3rem -> 4rem */
  font-weight: 700;
  margin-bottom: 0.5rem;
  line-height: 1.1;
  animation: fadeInUp 1s ease-out forwards;
}

/* 5. Subtitle: Comfortable Open Sans body font */
.hero-subtitle {
  font-family: 'Open Sans', sans-serif;
  font-size: 2rem; /* Changed from 1.5rem -> 2rem */
  font-weight: 400;
  line-height: 1.3;
  animation: fadeInUp 1.5s ease-out forwards;
}

@keyframes fadeInUp {
  0% {
    transform: translateY(20px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.image-section {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 60px;
}

.text-block {
  flex: 1;
  max-width: 500px;
  text-align: left;
  margin-left: 15%;
}

.text-block h2 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.text-block p {
  font-size: 1rem;
  line-height: 1.6;
  color: #444;
}

.text-block hr {
  margin: 1rem 0;
  border: none;
  border-top: 2px solid #ccc;
  width: 50px;
}

.image-container {
  overflow: hidden;
  position: relative;
  width: 500px;
  height: 300px;
  margin: auto auto auto auto;
  border-radius: 12px;
}

.image-slider {
  display: flex;
  width: 100%;
  height: 100%;
  transition: transform 0.6s ease;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: fill;
  flex-shrink: 0;
}

.content-container {
  display: flex;
  width: 100%;
  /* Change to auto to allow content area to expand based on actual height */
  height: auto;
}

.left-container {
  flex: 2;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.right-container {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  padding: 20px;
  align-items: center;
}

/* Styles below remain unchanged */
.prescription-list {
  margin-bottom: 40px;
  display: flex;
  flex-direction: column;
}

.prescription-list h3 {
  margin-bottom: 20px;
  display: block;
}

.prescription-items-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.prescription-item {
  padding: 6px 12px;
  box-shadow: 0 0 0 1px #d3d3d3, 0 0 0 4px #e0e0e0;
  cursor: pointer;
  width: 15%;
  text-align: center;
  margin-bottom: 10px;
  box-sizing: border-box;
  transition: box-shadow 0.3s ease;
}

.prescription-item:hover {
  box-shadow: 0 0 0 1px #4CAF50, 0 0 0 2px #4CAF50;
}

.herb-items-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
}

.herb-card {
  padding: 10px;
  box-shadow: 0 0 0 1px #d3d3d3, 0 0 0 4px #e0e0e0;
  cursor: pointer;
  width: 15%;
  text-align: center;
  margin-bottom: 10px;
  box-sizing: border-box;
  transition: box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.herb-card:hover {
  box-shadow: 0 0 0 1px #4CAF50, 0 0 0 2px #4CAF50;
}

.herb-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  margin-bottom: 10px;
}

ul {
  padding-left: 20px;
}

li {
  margin: 10px 0;
}

tiles {
  padding: 5%;
}

/* About Us Section */
.about-us {
  width: 100%;
  padding: 60px 20px;
  background-color: #eceae4; /* Softer distinguishing color */
  text-align: center;
  margin-top: 40px;
}

.about-us h2 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.about-us-content p {
  max-width: 800px;
  margin: 0 auto 40px;
  line-height: 1.6;
  color: #555;
}

.about-us-images {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.about-us-images img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.arrow-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0,0,0,0.5);
  color: white;
  border: none;
  padding: 10px 16px;
  cursor: pointer;
  font-size: 24px;
  z-index: 5;
  border-radius: 4px;
  user-select: none;
}

.arrow-btn.left {
  left: 10px;
}

.arrow-btn.right {
  right: 10px;
}

.arrow-btn:hover {
  background-color: rgba(0,0,0,0.7);
}

@media (prefers-color-scheme: dark) {
  .container {
    background-color: #121212;
    color: #f0f0f0;
  }

  .prescription-item {
    box-shadow: 0 0 0 1px #444, 0 0 0 4px #333;
    color: #f0f0f0;
    background-color: #1e1e1e;
  }

  .prescription-item:hover {
    box-shadow: 0 0 0 1px #4CAF50, 0 0 0 2px #4CAF50;
  }

  .herb-card {
    box-shadow: 0 0 0 1px #444, 0 0 0 4px #333;
    background-color: #1e1e1e;
    color: #f0f0f0;
  }

  .herb-card:hover {
    box-shadow: 0 0 0 1px #4CAF50, 0 0 0 2px #4CAF50;
  }

  .hero-container::after {
    background: linear-gradient(
      rgba(18, 18, 18, 0) 0%,
      rgba(18, 18, 18, 1) 100%
    );
  }

  .about-us {
    background-color: #1e1e1e; /* Dark background */
  }

  .about-us-content p {
    color: #ccc;
  }

  .about-us h2 {
    color: #fff;
  }

  .about-us-images img {
    box-shadow: 0 2px 8px rgba(0,0,0,0.5);
  }

  .text-block p {
    color: rgba(204, 204, 204, 0.9);
  }
}

/* Reveal animation styles */
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

.revealed {
  opacity: 1;
  transform: translateY(0);
}

.hero-divider {
  width: 0;
  height: 2px;
  background-color: #fff;
  margin: 20px auto;
  animation: expandDivider 2s ease-out forwards;
}

@keyframes expandDivider {
  0% {
    width: 0;
  }
  100% {
    width: 300px;
  }
}

.scroll-down {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  bottom: 20px;
  left: 49%;
  cursor: pointer;
  animation: fadeInUp 2s ease-out forwards;
}

.scroll-down .arrow {
  font-size: 2rem;
  color: #fff;
  animation: bounce 2s infinite;
}

.scroll-down .explore-text {
  color: #fff;
  font-size: 1rem;
  margin-top: 5px;
  font-family: 'Open Sans', sans-serif;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(6px);
  }
  60% {
    transform: translateY(3px);
  }
}
</style>


