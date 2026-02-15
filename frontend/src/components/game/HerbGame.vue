<template>
  <div class="herb-game">
    <div style="display: none;">
      <img src="/process1.png" />
      <img src="/process2.png" />
      <img src="/process3.png" />
    </div>
    <div class="herb-game-herbs">
      <!-- Toggle between Classification Mode / Category Mode -->
      <button @click="toggleDisplayMode" class="toggle-mode-btn">
        {{ isClassificationMode
          ? $t('herbs.ClassificationMode')
          : $t('herbs.CategoryMode') }}
      </button>
      <!-- In Classification Mode -->
      <div v-if="isClassificationMode">
        <div class="classifications">
          <button
              v-for="classf in classifications"
              :key="classf"
              @click="selectClassification(classf)"
              :class="{ active: classf === selectedClassification }"
          >
            {{ classf }}
          </button>
        </div>
      </div>
      <!-- In Category Mode -->
      <div v-else>
        <div class="categories">
          <button
              v-for="cat in categories"
              :key="cat"
              @click="selectCategory(cat)"
              :class="{ active: cat === selectedCategory }"
          >
            {{ cat }}
          </button>
        </div>
      </div>
      <!-- Herb List -->
      <div class="herb-list">
        <button
            v-for="herb in paginatedHerbs"
            :key="herb.id"
            :class="{ selected: selectedHerbs.some(h => h.id === herb.id) }"
            @click="toggleHerb(herb.id)"
        >
          <div v-if="!imageLoaded[herb.id]" class="custom-spinner"></div>
          <img
              :src="herb.image"
              class="herb-image"
              @load="imageLoaded[herb.id] = true"
              v-show="imageLoaded[herb.id]"
          />
          <span>{{ herb.name }}</span>
        </button>
        <div class="pagination-controls">
          <button @click="prevPage" :disabled="currentPage === 1">‹</button>
          <span class="pagination-info">{{ currentPage }} / {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">›</button>
        </div>
      </div>
    </div>
    <div class="herb-submit">
      <!-- Display selected herbs -->
      <div class="selected-herbs">
        <div class="selected-herbs__content">
          <div class="selected-herb-list">
            <div
                v-for="(herb, index) in selectedHerbs"
                :key="herb.id"
                class="herb-handwriting"
                :style="{ animationDelay: `${index * 0.2}s` }"
                @click="removeHerb(herb.id)"
            >
              {{ herb.name }}
            </div>
          </div>
        </div>
      </div>
      <!-- Cauldron Button -->
      <div class="cauldron-wrapper">
        <button class="submit-btn" @click="startPharmacyProcess">
          {{ $t('game.submit') }}
        </button>
      </div>
      <!-- Game Result Modal -->
      <div v-if="showResultModal" class="result-modal-overlay">
        <div class="result-modal">
          <h2>{{ $t('game.result') }}</h2>
          <div class="result-section">
            <h3>{{ $t('game.made') }}</h3>
            <ul>
              <li v-if="!herbGameResult || !herbGameResult.precisionResult || herbGameResult.precisionResult.length === 0">
                {{ $t('game.none') }}
              </li>
              <li v-else v-for="item in herbGameResult.precisionResult" :key="'p-' + item.id">
                <a :href="`/${route.params.lang}/prescriptions/${item.id}`" target="_blank" rel="noopener noreferrer">
                  {{ item.name }}
                </a>
              </li>
            </ul>
            <h3>{{ $t('game.guess') }}</h3>
            <ul>
              <li v-if="!herbGameResult || !herbGameResult.guessResult || herbGameResult.guessResult.length === 0">
                {{ $t('game.none') }}
              </li>
              <li v-else v-for="item in herbGameResult.guessResult" :key="'g-' + item.id">
                <a :href="`/${route.params.lang}/prescriptions/${item.id}`" target="_blank" rel="noopener noreferrer">
                  {{ item.name }}
                </a>
              </li>
            </ul>
          </div>
          <button class="close-btn" @click="showResultModal = false">
            {{ $t('game.close') }}
          </button>
        </div>
      </div>
    </div>
    <!-- Process Images Overlay -->
    <div v-if="currentProcessStep > 0" class="process-images-overlay">
      <div class="process-images">
        <img v-if="currentProcessStep === 1" src="/process1.png" alt="Step 1" />
        <img v-if="currentProcessStep === 2" src="/process2.png" alt="Step 2" />
        <img v-if="currentProcessStep === 3" src="/process3.png" alt="Step 3" />
      </div>
    </div>
    <!-- Help Button and Modal -->
    <button class="help-btn" @click="showHelp = true">{{ $t('game.help') }}</button>
    <div v-if="showHelp" class="help-modal-overlay">
      <div class="help-modal">
        <h2>{{ $t('game.helpTitle') }}</h2>
        <div v-for="(line, idx) in $tm('game.helpContent')" :key="idx" class="help-line">
          {{ line }}
        </div>
        <button class="close-btn" @click="showHelp = false">{{ $t('game.close') }}</button>
      </div>
    </div>
    <!-- Back Button -->
    <button class="back-btn" @click="$router.push({ name: 'GamePage', params: { lang: route.params.lang } })">
      {{ $t('game.back') }}
    </button>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, onBeforeRouteLeave, onBeforeRouteUpdate } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {
  getHerbCategories,
  getHerbsByCategory,
  getHerbClassifications,
  getHerbsByClassification
} from '@/api/tcm/herbwiki.js';
import { getFuzzyPrescription } from '@/api/tcm/gameApi.js';
import ChatBot from "@/components/AI/ChatBot.vue";

const imageLoaded = ref({});
// Dynamically generate styles for herbs to avoid overlap and arrange them sequentially
const getHerbStyle = (index) => {
  // Calculate container width as 30% of window (right side ~50%)
  const containerWidth = window.innerWidth * 0.3;
  const columns = Math.max(1, Math.floor(containerWidth / 100)); // ~100px per item incl. gap, at least 1 column
  const gap = 20;
  const row = Math.floor(index / columns);
  const col = index % columns;
  return {
    top: `${row * (80 + gap)}px`,
    left: `${col * (80 + gap)}px`
  };
};

export default {
  name: 'HerbGame',
  components: { ChatBot },
  props: {
    lang: {
      type: String,
      default: 'zh'
    }
  },
  setup() {
    const { t } = useI18n();
    const route = useRoute();

    const categories = ref([]);
    const selectedCategory = ref('');
    const herbs = ref([]);

    const isClassificationMode = ref(false);
    const classifications = ref([]);
    const selectedClassification = ref('');

    const selectedHerbs = ref([]);
    const herbGameResult = ref(null);

    const isShaking = ref(false);
    const showSmoke = ref(false);
    const showFlash = ref(false);

    const showResultModal = ref(false);

    // Added: Control whether initialization is complete
    const initialized = ref(false);

    // Cache state variables
    let cachedState = null;

    // --- Pagination ---
    const currentPage = ref(1);
    const itemsPerPage = 20;

    const totalPages = computed(() =>
        Math.ceil(herbs.value.length / itemsPerPage)
    );

    const paginatedHerbs = computed(() =>
        herbs.value.slice(
            (currentPage.value - 1) * itemsPerPage,
            currentPage.value * itemsPerPage
        )
    );

    const nextPage = () => {
      if (currentPage.value < totalPages.value) currentPage.value++;
    };

    const prevPage = () => {
      if (currentPage.value > 1) currentPage.value--;
    };
    // --- End Pagination ---

    const loadGameData = async () => {
      categories.value = await getHerbCategories(route.params.lang);
      if (categories.value.length > 0) {
        await selectCategory(categories.value[0]);
      }
    };

    const loadClassificationData = async () => {
      classifications.value = await getHerbClassifications(route.params.lang);
      if (classifications.value.length > 0) {
        await selectClassification(classifications.value[0]);
      }
    };

    const toggleDisplayMode = async () => {
      isClassificationMode.value = !isClassificationMode.value;
      if (isClassificationMode.value) {
        await loadClassificationData();
      } else if (categories.value.length > 0) {
        await selectCategory(categories.value[0]);
      }
      herbGameResult.value = null;
    };

    const selectCategory = async (category) => {
      selectedCategory.value = category;
      herbs.value = await getHerbsByCategory(category, route.params.lang);
      currentPage.value = 1;
    };

    const selectClassification = async (classf) => {
      selectedClassification.value = classf;
      herbs.value = await getHerbsByClassification(classf, route.params.lang);
      currentPage.value = 1;
    };

    const toggleHerb = (id) => {
      const herb = herbs.value.find(h => h.id === id);
      if (!herb) return;
      const exists = selectedHerbs.value.find(h => h.id === id);
      if (exists) {
        selectedHerbs.value = selectedHerbs.value.filter(h => h.id !== id);
      } else {
        selectedHerbs.value.push({ id: herb.id, name: herb.name });
      }
    };

    const removeHerb = (id) => {
      selectedHerbs.value = selectedHerbs.value.filter(h => h.id !== id);
    };

    const submitHerbGame = async () => {
      if (selectedHerbs.value.length === 0) {
        alert(t('game.alertSelectHerb'));
        return;
      }

      isShaking.value = true;
      showSmoke.value = true;
      showFlash.value = true;
      showResultModal.value = false;

      const herbIds = selectedHerbs.value.map(h => h.id);
      const result = await getFuzzyPrescription(herbIds, route.params.lang);

      isShaking.value = false;
      showSmoke.value = false;
      showFlash.value = false;

      herbGameResult.value = result;
      showResultModal.value = true;
    };

    // Restore cached state
    onMounted(async () => {
      if (cachedState) {
        selectedHerbs.value = [...cachedState.selectedHerbs];
        herbGameResult.value = cachedState.herbGameResult;
        showResultModal.value = cachedState.showResultModal;
        cachedState = null;
      }
      if (!initialized.value) {
        await loadGameData();
        initialized.value = true;
      }
    });

    // Cache state when leaving the page
    onBeforeRouteLeave((to, from, next) => {
      cachedState = {
        selectedHerbs: [...selectedHerbs.value],
        herbGameResult: herbGameResult.value,
        showResultModal: showResultModal.value
      };
      next();
    });

    // Restore cached state when the route updates
    onBeforeRouteUpdate((to, from, next) => {
      if (cachedState) {
        selectedHerbs.value = [...cachedState.selectedHerbs];
        herbGameResult.value = cachedState.herbGameResult;
        showResultModal.value = cachedState.showResultModal;
        cachedState = null;
      }
      next();
    });

    watch(() => route.params.lang, async () => {
      if (!initialized.value) return;

      if (!isClassificationMode.value) {
        await loadGameData();
      } else {
        await loadClassificationData();
      }
      // Update the names of selectedHerbs after the language changes
      if (selectedHerbs.value.length > 0) {
        const selectedIds = selectedHerbs.value.map(h => h.id);
        selectedHerbs.value = selectedIds
            .map(id => herbs.value.find(h => h.id === id))
            .filter(Boolean); // Remove null values
      }
      if (herbGameResult.value && selectedHerbs.value.length > 0) {
        await submitHerbGame();
      }
    });

    // --- New process step ---
    const currentProcessStep = ref(0);
    const showHelp = ref(false);

    // New process: Only show one image at a time, display modal after 3 steps
    const startPharmacyProcess = () => {
      if (selectedHerbs.value.length === 0) {
        alert(t('game.alertSelectHerb'));
        return;
      }
      herbGameResult.value = null;
      currentProcessStep.value = 1;

      setTimeout(() => currentProcessStep.value = 2, 1000);
      setTimeout(() => currentProcessStep.value = 3, 2000);
      setTimeout(() => {
        currentProcessStep.value = 0;
        submitHerbGame();
      }, 3000);
    };
    // --- end new process ---

    return {
      categories,
      selectedCategory,
      herbs,
      isClassificationMode,
      classifications,
      selectedClassification,
      toggleDisplayMode,
      selectCategory,
      selectClassification,
      selectedHerbs,
      toggleHerb,
      removeHerb,
      submitHerbGame,
      herbGameResult,
      getHerbStyle,
      isShaking,
      showSmoke,
      showFlash,
      showResultModal,
      imageLoaded,
      route,
      paginatedHerbs,
      currentPage,
      totalPages,
      nextPage,
      prevPage,
      currentProcessStep,
      startPharmacyProcess,
      showHelp
    };
  }
}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
@import "../../assets/css/component.css";

.herb-game {
  background: url('/herbGameBg.png') center center no-repeat;
  background-size: cover;
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: row; /* Changed to horizontal alignment */
}
.herb-game-herbs {
  width: 50%;
  padding: 20px;
}
.herb-submit {
  width: 50%;
  padding: 20px;
}
/* Horizontal scrolling for classifications */
.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}
.classifications {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding-left: 10px;
  max-height: 120px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #ba5f39 transparent;
}
/* For Webkit browsers */
.classifications::-webkit-scrollbar {
  height: 6px;
}
.classifications::-webkit-scrollbar-track {
  background: transparent;
}
.classifications::-webkit-scrollbar-thumb {
  background-color: #ba5f39;
  border-radius: 3px;
}
/* Shared button style for toggle-mode, classifications, categories */
.toggle-mode-btn,.classifications button,.categories button {
  width: auto;
  padding: 0 16px;
  box-sizing: border-box;
  height: 30px;
  background-image: url('/button2.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: center;
  background-color: transparent;
  border: none;
  font-weight: bold;
  font-size: 12px;
  color: #fff8dc;
  text-align: center;
  line-height: 30px;
}
.toggle-mode-btn {
  margin-bottom: 10px;
  background-image: url("/button1.png");
}
/* Active state for classification/category buttons */
.classifications button.active,.categories button.active {
  background-image: url('/button1.png');
  transform: scale(1.05);
  box-shadow: 0 0 6px rgba(255, 255, 255, 0.5);
  color: black;
}
.classifications button:hover,.categories button:hover {
  transform: scale(1.05);
  filter: brightness(1.1);
}
.toggle-mode-btn:hover {
  transform: scale(1.05);
  filter: brightness(1.1);
}
/* Herb list container */
.herb-list {
  position: relative;
  overflow: visible;
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;
  padding-top: 40px;
  margin-left: auto;
  margin-right: auto;
  width: 80%;
  /* Allow vertical scrolling -- removed overflow-y: auto */
  align-items: flex-start;
  align-content: flex-start;
  justify-content: center;
}
/* Square-shaped herb buttons: fixed ratio, cabinet background */
.herb-list button {
  position: relative; /* Needed for absolutely positioned child elements */
  width: 19%;        /* Button width */
  aspect-ratio: 1 / 1; /* Force square shape */
  cursor: pointer;
  text-align: center;
  box-sizing: border-box;
  border: none;
  outline: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: url('/cabinet.png') center center no-repeat; /* Default cabinet background */
  background-size: 80% auto;
  overflow: visible;  /* Allow enlarged images to "overflow" outside */
  z-index: 1;
}
.herb-list button:hover {
  filter: brightness(1.05);
  z-index: 10;
}
.herb-list button span {
  position: static;      /* Maintain flow layout */
  margin-top: -2.75em;    /* Changed to relative unit, 0.5em means "half of font height" */
  color: #b8860b;        /* DarkGoldenRod for text color, resembling herb label */
  font-weight: bold;     /* Bold for a more refined look */
  background: none;      /* Keep background transparent */
  padding: 0;
}
/* Hover state: position span below image */
.herb-list button:hover span {
  position: absolute;
  bottom: 10px;           /* 10px from the bottom of the button, adjustable */
  left: 50%;
  transform: translateX(-50%);
  color: #ffffff;
  background: #b8860b;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
  z-index: 2;
}
/* Herb image: default hidden, fade in on hover */
.herb-list button .herb-image {
  opacity: 0;
  transition: opacity 0.3s ease;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 125%;
  height: auto;
  object-fit: cover;
  z-index: 1;
}
.herb-list button:hover .herb-image {
  opacity: 1;
}
/* Compatibility with old selector (applies only to loaded images) */
.herb-image {
  display: block;
  margin-bottom: 10px;
}
.selected-herbs {
  width: 57%;
  height: 47%;
  position: relative;
  overflow: visible;
  margin-left: 10px;
}
.selected-herbs__content {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 10px;
  box-sizing: border-box;
  /* Use browser default scrollbar color */
  scrollbar-width: thin;
  scrollbar-color: auto;
}
/* Custom scrollbar for Webkit browsers */
.selected-herbs__content::-webkit-scrollbar {
  width: 8px;
}
.selected-herbs__content::-webkit-scrollbar-track {
  background: transparent;
}
.selected-herbs__content::-webkit-scrollbar-thumb {
  background-color: #33302e;
  border-radius: 4px;
}

.selected-herbs::after {
  content: '';
  position: absolute;
  bottom: -10px;
  right: 10%;
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 10px solid #ccc;
}
.selected-herb-list {
  position: relative;
  width: auto;
  height: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
/* Handwriting effect: reveal text using clip-path, width fits content */
.herb-handwriting {
  font-family: 'Patrick Hand', cursive;
  font-size: 25px;
  color: #000000;
  white-space: nowrap;
  overflow: hidden;
  display: inline-block;
  cursor: pointer;
  padding: 0px 0;
  margin-bottom: 2px;
  width: fit-content;
  position: relative;
  clip-path: inset(0 100% 0 0);
  animation: revealText 1s steps(20, end) forwards;
}
.herb-handwriting::after {
  content: '';
  position: absolute;
  top: 50%;
  left: -4px;
  height: 2px;
  background-color: #3e2f1c;
  width: 0;
  transform: translateY(-50%);
  transition: width 0.4s ease;
}
.herb-handwriting:hover::after {
  width: calc(100% + 8px);
}

@keyframes revealText {
  to {
    clip-path: inset(0 0 0 0);
  }
}


.result-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.result-modal {
  background: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 0 10px rgba(0,0,0,0.3);
  animation: fadeIn 0.4s ease;
}

.result-modal h2 {
  margin-bottom: 10px;
  font-size: 20px;
}

.result-modal p {
  font-size: 16px;
  word-break: break-word;
}

.close-btn {
  margin-top: 20px;
  padding: 8px 20px;
  background-color: #ba5f39;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

.result-section {
  text-align: left;
  max-height: 300px;
  overflow-y: auto;
}

.result-section h3 {
  margin-top: 10px;
  font-size: 16px;
  color: #ba5f39;
}

.result-section ul {
  padding-left: 20px;
  margin-bottom: 10px;
}

.result-section li {
  font-size: 14px;
  margin-bottom: 5px;
  color: #333;
}

.result-section a {
  color: #4CAF50;
  text-decoration: underline;
}

.result-section a:hover {
  color: #388e3c;
}

@media (prefers-color-scheme: dark) {
  .herb-game,
  .herb-game-herbs,
  .herb-submit {
    color: #f0f0f0;
  }

  .herb-list button {
    color: #f0f0f0;
  }


  .selected-herbs::after {
    border-top-color: #555;
  }


  .result-modal-overlay {
    background-color: rgba(0, 0, 0, 0.7);
  }

  .result-modal {
    background-color: #2a2a2a;
    color: #f0f0f0;
    box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
  }

  .close-btn {
    background-color: #ba5f39;
    color: white;
  }

  /* Ensure all result-section li elements (including those with {{ $t('game.none') }}) appear white in dark mode */
  .result-section li {
    color: #f0f0f0;
  }
}

.pagination-controls {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.pagination-controls button {
  padding: 4px 8px;
  background-color: #ba5f39;
  color: white;
  font-size: 14px;
  font-weight: bold;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.pagination-info {
  font-size: 14px;
  font-weight: bold;
  color: #cccccc;
  padding: 0 6px;
}

.pagination-controls button:hover {
  background-color: #ba5f39;
  color: white;
}

.pagination-controls button:disabled {
  opacity: 0.5;
  cursor: default;
}

.submit-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
  background-image: url('/button1.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: center;
  background-color: transparent;
  font-weight: bold;
  color: #fff8dc;
  text-align: center;
  line-height: 30px;
}

.submit-btn:hover {
  transform: scale(1.05);
  filter: brightness(1.1);
}

.process-images-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* changed from light to dark overlay */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.process-images {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
.process-images img {
  width: auto;
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}


 .help-btn {
   position: fixed;
   bottom: 20px;
   left: 20px;
   background-color: #ba5f39;
   color: white;
   border: none;
   padding: 8px 16px;
   font-weight: bold;
   border-radius: 4px;
   cursor: pointer;
   z-index: 1001;
 }

.help-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.help-modal {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  box-shadow: 0 0 10px rgba(0,0,0,0.3);
  text-align: left;
}

.help-modal h2 {
  margin-bottom: 10px;
  font-size: 18px;
  color: #2a2a2a;
}


.help-line {
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
  line-height: 1.6;
}

@media (prefers-color-scheme: dark) {
  .help-modal {
    background: #2a2a2a;
    color: #e0e0e0;
  }

  .help-modal h2 {
    color: #e0e0e0;
  }

  .help-line {
    color: #cccccc;
  }
}

.back-btn {
  position: fixed;
  bottom: 20px;
  left: 100px;
  background-color: #ba5f39;
  color: white;
  border: none;
  padding: 8px 16px;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  z-index: 1001;
}

.back-btn:hover {
  background-color: #a44e2f;
}
</style>



