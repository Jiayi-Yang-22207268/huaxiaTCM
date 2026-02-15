<template>
  <div v-if="herb">
    <div class="herb-detail">
      <!-- Back Button -->
      <div class="back-container">
        <router-link :to="`/${route.params.lang}/herbs`" class="back-btn">
          {{ $t('herb.backToList') }}
        </router-link>
      </div>
      <!-- Title -->
      <h1 class="detail-title">{{ herb.name }}</h1>
      <!-- Chinese Name and Pinyin in English Mode -->
      <div v-if="route.params.lang === 'en'" class="cn-name-container">
        <div class="cn-label"><strong>{{ $t('herb.cnName') }}：</strong></div>
        <div class="cn-name">
          <div class="pinyin-text">
            <span v-for="(py, index) in pinyinArray" :key="index" class="pinyin-item">
              {{ py }}
            </span>
          </div>
          <div class="chinese-text">
            <span v-for="(char, index) in herb.cnName" :key="index" class="chinese-item">
              {{ char }}
            </span>
            <button @click="speakText" class="speak-button">🔊</button>
          </div>
        </div>
      </div>
      <!-- Herb Image -->
      <section class="detail-section image-section">
        <div v-if="!isImageLoaded" class="spinner"></div>
        <img
            v-if="herb.image"
            :src="herb.image"
            :alt="herb.name"
            class="herb-image"
            @load="isImageLoaded = true"
            v-show="isImageLoaded"
        />
      </section>
      <!-- Attribute Sections -->
      <section
          v-for="(value, key) in fields"
          :key="key"
          :id="key"
          :class="['detail-section', `section-${key}`]"
      >
        <h2 class="section-title">{{ $t(`herb.${key}`) }}</h2>
        <p class="section-content">{{ value || $t('herb.noData') }}</p>
      </section>
      <!-- Related Prescriptions -->
      <section class="detail-section">
        <h2 class="section-title">{{ $t('herb.related_prescriptions') }}</h2>
        <div v-if="herb.relate_prescription_id && herb.relate_prescription_id.length">
          <ul class="related-list">
            <li v-for="(pid, idx) in herb.relate_prescription_id" :key="pid">
              <router-link :to="`/${route.params.lang}/prescriptions/${pid}`">
                {{ herb.relate_prescription[idx] }}
              </router-link>
            </li>
          </ul>
        </div>
        <p v-else class="section-content">{{ $t('herb.noData') }}</p>
      </section>
      <!-- Map Component -->
      <section class="detail-section map-section">
        <Map :herbId="herb.id" />
      </section>
    </div>
  </div>
  <div v-else>
    <p class="loading-text">{{ $t('loading') }}</p>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { getHerbDetail } from '@/api/tcm/herbwiki.js';
import { useRoute } from 'vue-router';
import { pinyin } from 'pinyin-pro';
import Map from '@/components/generalComponents/Map.vue';

export default {
  components: { Map },
  setup() {
    const herb = ref(null);
    const route = useRoute();
    const isImageLoaded = ref(false);

    // Load herb details
    const loadHerbDetail = async () => {
      herb.value = await getHerbDetail(route.params.id, route.params.lang);
    };

    watch(() => route.params.lang, loadHerbDetail);
    onMounted(loadHerbDetail);

    // Pinyin array
    const pinyinArray = computed(() => {
      if (!herb.value?.cnName) return [];
      return pinyin(herb.value.cnName, { toneType: 'none', type: 'array' });
    });

    const speakText = () => {
      if (herb.value?.cnName) {
        const msg = new SpeechSynthesisUtterance();
        msg.text = herb.value.cnName;
        msg.lang = 'zh-CN';
        window.speechSynthesis.speak(msg);
      }
    };

    // Field mapping: category, origin, production_regions, properties, functions, classification
    const fields = computed(() => ({
      category: herb.value?.category,
      origin: herb.value?.origin,
      production_regions: herb.value?.production_regions,
      properties: herb.value?.properties,
      functions: herb.value?.functions,
      classification: herb.value?.classification,
    }));

    return { herb, route, isImageLoaded, pinyinArray, speakText, fields };
  },
};
</script>

<style scoped>
/* Container and theme variables */
.herb-detail {
  width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
  --accent: #ba5f39;
  --card-bg: #ffffff;
}
@media (prefers-color-scheme: dark) {
  .herb-detail {
    --bg: #121212;
    --text: #e0e0e0;
    --card-bg: #1f1f1f;
  }
}

/* Back button */
.back-container {
  margin-bottom: 16px;
}
.back-btn {
  display: inline-block;
  padding: 8px 16px;
  background: var(--accent);
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.2s, transform 0.2s;
}
.back-btn:hover {
  background: #9c4a2d;
  transform: translateY(-2px);
}

/* Title */
.detail-title {
  font-size: 2rem;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--accent);
}

/* Pinyin and Chinese name */
.cn-name-container {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  background: var(--card-bg);
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.cn-label {
  font-size: 1.1rem;
  font-weight: bold;
  color: var(--accent);
  margin-right: 8px;
}
.cn-name {
  display: table;
}
.pinyin-text, .chinese-text {
  display: table-row;
}
.pinyin-item, .chinese-item {
  display: table-cell;
  padding: 0 4px;
  text-align: center;
  font-size: 1rem;
}
.pinyin-item {
  color: #3498db;
  font-weight: bold;
}
.speak-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2em;
  margin-left: 8px;
}

/* Image section */
.image-section {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24px;
}
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #ccc;
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.herb-image {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

/* Content block */
/* First, give all detail-section a basic border width */
.detail-section {
  border-left: 4px solid transparent;
  /* …existing styles… */
  padding-left: 16px;
  background: var(--card-bg);
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  margin-bottom: 24px;
}
/* Override border-color based on field type */
.section-category {
  border-left-color: #ba5f39;
}          /* Main color, Category */
.section-origin {
  border-left-color: #5d8aa8;
}            /* Origin */
.section-production_regions {
  border-left-color: #f39c12;
} /* Production */
.section-properties {
  border-left-color: #3498db;
}        /* Properties */
.section-functions {
  border-left-color: #27ae60;
}         /* Functions */
.section-classification {
  border-left-color: #9b59b6;
}    /* Classification */

/* Add icons before the title */
.section-category  .section-title::before {
  content: '🌱';
}
.section-origin    .section-title::before {
  content: '📍';
}
.section-production_regions .section-title::before {
  content: '🏭';
}
.section-properties .section-title::before {
  content: '⚖️';
}
.section-functions  .section-title::before {
  content: '💡';
}
.section-classification .section-title::before {
  content: '📑';
}

/* Unified icon styles */
.section-title {
  position: relative;
  padding-left: 1.6em; /* Leave space for the icon */
  font-size: 1.2rem;
  margin-bottom: 8px;
  color: var(--accent);
}
.section-title::before {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2em;
  content: '';
  display: inline-block;
  width: 1em; height: 1em;
  margin-right: 8px;
  background-size: contain;
}
.section-content {
  font-size: 1rem;
  line-height: 1.6;
}

/* Related links list */
.related-list {
  list-style: disc inside;
}
.related-list li a {
  color: var(--accent);
  text-decoration: none;
  transition: color 0.2s;
}
.related-list li a:hover {
  color: #9c4a2d;
  text-decoration: underline;
}

/* Map section */
.map-section {
  margin-bottom: 0;
}

/* Loading text */
.loading-text {
  text-align: center;
  margin-top: 50px;
  font-size: 1rem;
  color: var(--text);
}

</style>
