<template>
  <div v-if="prescription">
    <div class="prescription-detail">
      <!-- Title -->
      <h1 class="detail-title">{{ prescription.name }}</h1>
      <!-- Chinese name and pinyin in English mode -->
      <div v-if="route.params.lang === 'en'" class="cn-name-container">
        <div class="cn-label">
          <strong>{{ $t('prescription.cnName') }}：</strong>
        </div>
        <div class="cn-name">
          <div class="pinyin-text">
            <span v-for="(py, index) in pinyinArray" :key="index" class="pinyin-item">
              {{ py }}
            </span>
          </div>
          <div class="chinese-text">
            <span v-for="(char, index) in prescription.cnName" :key="index" class="chinese-item">
              {{ char }}
            </span>
            <button @click="speakText" class="speak-button">🔊</button>
          </div>
        </div>
      </div>
      <!-- Prescription composition -->
      <section class="detail-section section-constitute">
        <h2 class="section-title">{{ $t('prescription.constitute') }}</h2>
        <p class="section-content">
          <template v-if="prescription.constitute">
            <span v-for="(herb, index) in herbLinks" :key="index">
              <template v-if="herb.id === -1">
                {{ herb.name }}
              </template>
              <template v-else>
                <router-link :to="`/${route.params.lang}/herbs/${herb.id}`">
                  {{ herb.name }}
                </router-link>
              </template>
              <span v-if="index < herbLinks.length - 1">, </span>
            </span>
          </template>
          <template v-else>
            {{ $t('prescription.noData') }}
          </template>
        </p>
      </section>
      <!-- Effects -->
      <section class="detail-section section-action">
        <h2 class="section-title">{{ $t('prescription.action') }}</h2>
        <p class="section-content">
          {{ prescription.action || $t('prescription.noData') }}
        </p>
      </section>
      <!-- Indications -->
      <section class="detail-section section-indication">
        <h2 class="section-title">{{ $t('prescription.indication') }}</h2>
        <p class="section-content">
          {{ prescription.indication || $t('prescription.noData') }}
        </p>
      </section>
      <!-- Back button -->
      <div class="back-container">
        <router-link :to="`/${route.params.lang}/prescriptions`" class="back-btn">
          {{ $t('prescription.backToList') }}
        </router-link>
      </div>
    </div>
  </div>
  <div v-else>
    <p class="loading-text">{{ $t('loading') }}</p>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { getPrescriptionDetail } from '@/api/tcm/prewiki.js';
import { useRoute } from 'vue-router';
import { pinyin } from 'pinyin-pro';

export default {
  setup() {
    const prescription = ref(null);
    const route = useRoute();

    const loadPrescriptionDetail = async () => {
      prescription.value = await getPrescriptionDetail(
          route.params.id,
          route.params.lang
      );
    };

    watch(
        () => route.params.lang,
        loadPrescriptionDetail
    );
    onMounted(loadPrescriptionDetail);

    const pinyinArray = computed(() => {
      if (!prescription.value?.cnName) return [];
      return pinyin(prescription.value.cnName, { toneType: 'none', type: 'array' });
    });

    const speakText = () => {
      if (prescription.value?.cnName) {
        const msg = new SpeechSynthesisUtterance();
        msg.text = prescription.value.cnName;
        msg.lang = 'zh-CN';
        window.speechSynthesis.speak(msg);
      }
    };

    const herbLinks = computed(() => {
      if (!prescription.value?.constituteId) return [];
      return prescription.value.constituteId.map((id, idx) => ({
        id,
        name: prescription.value.constitute.split('; ')[idx]
      }));
    });

    return { prescription, route, pinyinArray, speakText, herbLinks };
  },
};
</script>

<style scoped>
/* Global container */
.prescription-detail {
  width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
  --accent: #ba5f39;
  --card-bg: #ffffff;
}
@media (prefers-color-scheme: dark) {
  .prescription-detail {
    --bg: #121212;
    --text: #e0e0e0;
    --card-bg: #1f1f1f;
  }
}

/* Title */
.detail-title {
  font-size: 2rem;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--accent);
}

/* Pinyin row */
.cn-name-container {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  background: var(--card-bg);
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}
.cn-label { font-size: 1.1rem; font-weight: bold; color: var(--accent); margin-right: 10px; }
.cn-name { display: table; }
.pinyin-text, .chinese-text { display: table-row; }
.pinyin-item, .chinese-item { display: table-cell; padding: 0 4px; text-align: center; font-size: 1rem; }
.pinyin-item { color: #3498db; font-weight: bold; }
.speak-button { background: none; border: none; cursor: pointer; font-size: 1.2em; margin-left: 10px; }

/* Basic structure for detail sections */
.detail-section {
  background: var(--card-bg);
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
  border-left: 4px solid transparent;
}
.section-title {
  position: relative;
  padding-left: 1.6em;
  font-size: 1.2rem;
  margin-bottom: 8px;
}
.section-content { font-size: 1rem; line-height: 1.6; }

/* Colored border & icons for different sections */
.section-constitute { border-left-color: #27ae60; }
.section-action { border-left-color: #e67e22; }
.section-indication { border-left-color: #c0392b; }

.section-constitute .section-title::before { content: '⚗️'; }
.section-action    .section-title::before { content: '✨'; }
.section-indication .section-title::before { content: '🏥'; }

.section-title::before {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2em;
}

/* Links */
.section-content a { color: var(--accent); text-decoration: none; transition: color 0.2s; }
.section-content a:hover { color: #9c4a2d; text-decoration: underline; }

/* Back button */
.back-container { text-align: center; margin-top: 32px; }
.back-btn {
  display: inline-block;
  padding: 8px 20px;
  background: var(--accent);
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  transition: background 0.2s;
  border: none;
  cursor: pointer;
}
.back-btn:hover { background: #9c4a2d; }

/* Loading text */
.loading-text { text-align: center; margin-top: 50px; font-size: 1rem; color: var(--text); }
</style>
