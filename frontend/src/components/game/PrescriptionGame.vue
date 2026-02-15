<template>
  <div class="category-wrapper">
    <!-- Category sidebar: Displayed only when a prescription is selected and in classification mode -->
    <div
        v-if="selectedPrescriptionId && isClassificationMode"
        class="category-sidebar"
    >
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
    <!-- Category sidebar: Displayed only when a prescription is selected and classification mode is false (original sidebar) -->
    <div
        v-if="selectedPrescriptionId && !isClassificationMode"
        class="category-sidebar"
    >
      <div
          v-for="cat in categories"
          :key="cat"
          @click="selectCategory(cat); scrollToGroup(cat)"
          :class="['category-item', { active: cat === selectedCategory }]"
      >
        {{ cat }}
      </div>
    </div>
    <div class="prescription-game">
      <h2 v-if="!selectedPrescriptionId">{{ $t('game.selectPrescription') }}</h2>
      <div v-if="!selectedPrescriptionId" class="search-bar">
        <input
            type="text"
            v-model="searchQuery"
            @keyup.enter="searchPrescriptions"
            :placeholder="$t('game.searchPrescription')"
        />
        <button @click="searchPrescriptions">{{ $t('game.search') }}</button>
      </div>
      <div v-if="!selectedPrescriptionId" class="prescription-list">
        <div
            v-for="(group, letter) in groupedPrescriptions"
            :key="letter"
            class="group"
            :ref="'group-' + letter"
        >
          <div class="group-title">{{ letter }}</div>
          <div class="prescription-grid">
            <div
                v-for="prescription in group"
                :key="prescription.id"
                :class="['prescription-item', { active: prescription.id === selectedPrescriptionId }]"
                @click="selectPrescriptionAndScroll(prescription.id)"
            >
              <div
                  class="icon"
                  :style="{ backgroundColor: `hsl(${(letter.charCodeAt(0) - 65) * 35 % 360}, 60%, 80%)` }"
              >
                {{ letter }}
              </div>
              <div class="name">{{ prescription.name }}</div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="selectedPrescriptionId" class="prescription-herbs">
        <button class="back-btn" @click="deselectPrescription">
          ← {{ $t('game.backToPrescription') }}
        </button>
        <div class="selected-info">
          <p><strong>{{ $t('game.selectedPrescription') }}:</strong> {{ getPrescriptionName(selectedPrescriptionId) }}</p>
          <p><strong>{{ $t('game.selectedHerbs') }}</strong>
            <span v-if="selectedPrescriptionHerbs.length === 0">{{ $t('game.none') }}</span>
            <span v-else>{{ getSelectedHerbNames.join('、') }}</span>
          </p>
        </div>
        <h3>{{ $t('game.selectPrescriptionHerbs') }}</h3>
        <!-- Toggle classification/flavor mode button -->
        <button @click="toggleDisplayMode" class="toggle-mode-btn">
          {{ isClassificationMode
            ? $t('herbs.ClassificationMode')
            : $t('herbs.CategoryMode') }}
        </button>
        <div class="herb-list">
          <button
              v-for="herb in herbs"
              :key="herb.id"
              :class="{ selected: selectedPrescriptionHerbs.some(h => h.id === herb.id) }"
              @click="togglePrescriptionHerb(herb.id)"
          >
            {{ herb.name }}
          </button>
        </div>
        <button @click="submitPrescriptionGameAndScroll" class="submit-btn">
          {{ $t('game.submit') }}
        </button>
        <!-- Structured result display -->
        <div v-if="prescriptionGameResult" class="result">
          <!-- Backend error -->
          <p v-if="prescriptionGameResult.error" class="error">
            {{ prescriptionGameResult.error }}
          </p>
          <!-- Normal result -->
          <template v-else>
            <h3>{{ $t('game.extraHerbs') }}</h3>
            <ul>
              <li v-if="extraNames.length === 0">{{ $t('game.none') }}</li>
              <li v-for="(name, idx) in extraNames" :key="'e-'+idx">{{ name }}</li>
            </ul>
            <h3>{{ $t('game.lackHerbs') }}</h3>
            <ul>
              <li v-if="lackNames.length === 0">{{ $t('game.none') }}</li>
              <li v-for="(name, idx) in lackNames" :key="'l-'+idx">{{ name }}</li>
            </ul>
            <h3>{{ $t('game.result') }}</h3>
            <p>
              {{ prescriptionGameResult.result === 'failure'
                ? $t('game.matchFailure')
                : $t('game.matchSuccess') }}
            </p>
          </template>
        </div>
      </div>
    </div>
    <!-- Help Button and Modal -->
    <button class="help-btn" @click="showHelp = true">{{ $t('game.help') }}</button>
    <div v-if="showHelp" class="help-modal-overlay">
      <div class="help-modal">
        <h2>{{ $t('game.helpTitle') }}</h2>
        <div v-for="(line, idx) in $tm('game.helpContentPre')" :key="idx" class="help-line">
          {{ line }}
        </div>
        <button class="close-btn" @click="showHelp = false">{{ $t('game.close') }}</button>
      </div>
    </div>
    <button class="back-btn1" @click="$router.push({ name: 'GamePage', params: { lang: route.params.lang } })">
      {{ $t('game.back') }}
    </button>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import {
  getHerbCategories,
  getHerbsByCategory,
  getHerbClassifications,
  getHerbsByClassification,
  getHerbDetail,
  getHerbNamesBatch
} from '@/api/tcm/herbwiki.js';
import { getPrescriptions } from '@/api/tcm/prewiki.js';
import { checkHerbSelection } from '@/api/tcm/gameApi.js';
import { pinyin } from 'pinyin-pro';

export default {
  name: 'PrescriptionGame',
  props: {
    lang: {
      type: String,
      default: 'zh'
    }
  },
  setup() {
    const { t } = useI18n();
    const route = useRoute();

    const searchQuery = ref('');
    const prescriptions = ref([]);
    const selectedPrescriptionId = ref(null);
    // Store array of { id, name } objects for selected herbs
    const selectedPrescriptionHerbs = ref([]);
    const prescriptionGameResult = ref(null);

    const categories = ref([]);
    const selectedCategory = ref('');
    const herbs = ref([]);

    const isClassificationMode = ref(false);
    const classifications = ref([]);
    const selectedClassification = ref('');

    const showHelp = ref(false);

    const extraNames = computed(() => {
      const msg = prescriptionGameResult.value?.message || '';
      const matches = [...msg.matchAll(/{\s*([^}]*)\s*}/g)].map(m => m[1]);
      if (!matches[0]) return [];
      return matches[0]
          .split(/'\s*,\s*'/)
          .map(s => s.replace(/'/g, '').trim());
    });
    const lackNames = computed(() => {
      const msg = prescriptionGameResult.value?.message || '';
      const matches = [...msg.matchAll(/{\s*([^}]*)\s*}/g)].map(m => m[1]);
      if (!matches[1]) return [];
      return matches[1]
          .split(/'\s*,\s*'/)
          .map(s => s.replace(/'/g, '').trim());
    });

    const loadGameData = async () => {
      categories.value = await getHerbCategories(route.params.lang);
      if (categories.value.length > 0) {
        await selectCategory(categories.value[0]);
      }
      prescriptions.value = await getPrescriptions(route.params.lang);
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
      prescriptionGameResult.value = null;
    };

    const selectCategory = async (category) => {
      selectedCategory.value = category;
      herbs.value = await getHerbsByCategory(category, route.params.lang);
    };

    const selectClassification = async (classf) => {
      selectedClassification.value = classf;
      herbs.value = await getHerbsByClassification(classf, route.params.lang);
    };

    const selectPrescription = (id) => {
      selectedPrescriptionId.value = id;
      selectedPrescriptionHerbs.value = [];
      prescriptionGameResult.value = null;
    };

    // Toggle herb selection: store as { id, name }
    const togglePrescriptionHerb = (id) => {
      const existing = selectedPrescriptionHerbs.value.find(h => h.id === id);
      if (existing) {
        selectedPrescriptionHerbs.value = selectedPrescriptionHerbs.value.filter(h => h.id !== id);
      } else {
        const herb = herbs.value.find(h => h.id === id);
        if (herb) selectedPrescriptionHerbs.value.push({ id: herb.id, name: herb.name });
      }
    };

    const submitPrescriptionGame = async () => {
      if (!selectedPrescriptionId.value) {
        alert(t('game.alertSelectPrescription'));
        return;
      }
      if (selectedPrescriptionHerbs.value.length === 0) {
        alert(t('game.alertSelectHerb'));
        return;
      }
      // Only pass array of IDs to API
      const result = await checkHerbSelection(
          selectedPrescriptionId.value,
          selectedPrescriptionHerbs.value.map(h => h.id),
          route.params.lang
      );
      if (result.error) {
        prescriptionGameResult.value = { error: result.error };
      } else {
        prescriptionGameResult.value = {
          extra: result.extra || [],
          lack: result.lack || [],
          message: result.message,
          result: result.result
        };
      }
    };

    const groupedPrescriptions = computed(() => {
      const groups = {};
      const filtered = prescriptions.value.filter(prescription =>
          prescription.name.includes(searchQuery.value)
      );
      filtered.forEach(prescription => {
        let firstLetter = pinyin(prescription.name[0], {
          type: 'array',
          pattern: 'first',
          toneType: 'none'  // key Setting， Remove Tones
        })[0];

        if (!firstLetter) {
          firstLetter = prescription.name[0].toUpperCase();
        } else {
          firstLetter = firstLetter.toUpperCase();
        }
        if (!groups[firstLetter]) {
          groups[firstLetter] = [];
        }
        groups[firstLetter].push(prescription);
      });
      // Sort groups by letter
      const sortedGroups = {};
      Object.keys(groups).sort().forEach(key => {
        sortedGroups[key] = groups[key];
      });
      return sortedGroups;
    });

    const selectPrescriptionAndScroll = (id) => {
      selectPrescription(id);
      // Scroll to herb selection area
      setTimeout(() => {
        const herbSection = document.querySelector('.prescription-herbs');
        if (herbSection) {
          herbSection.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    };

    const submitPrescriptionGameAndScroll = async () => {
      await submitPrescriptionGame();
      setTimeout(() => {
        const resultSection = document.querySelector('.result');
        if (resultSection) {
          resultSection.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    };

    const searchPrescriptions = () => {
      // The computed groupedPrescriptions will update automatically due to searchQuery reactive binding
    };

    onMounted(loadGameData);

    watch(
        () => route.params.lang,
        async (newLang) => {
          if (!isClassificationMode.value) {
            await loadGameData();
          } else {
            await loadClassificationData();
          }

          if (
              prescriptionGameResult.value &&
              selectedPrescriptionId.value &&
              selectedPrescriptionHerbs.value.length > 0
          ) {
            await submitPrescriptionGame();
          }

          // batch request for herb names
          const ids = selectedPrescriptionHerbs.value.map(h => h.id);
          if (ids.length > 0) {
            const herbsData = await getHerbNamesBatch(ids, newLang);
            // Use returned data to replace names
            const updatedHerbs = selectedPrescriptionHerbs.value.map(h => {
              const found = herbsData.find(item => item.id === h.id);
              return {
                ...h,
                name: found?.name || h.name
              };
            });
            selectedPrescriptionHerbs.value = updatedHerbs;
          }
        }
    );


    // Scroll to group (used when clicking on category in sidebar)
    const scrollToGroup = (cat) => {
      // Here it is assumed that each group's ref is group-categoryName, can be customized
      // Since the herb list is not grouped, you can customize scrolling logic if needed
      // Optional: Can scroll to .herb-list
      const herbList = document.querySelector('.herb-list');
      if (herbList) {
        herbList.scrollIntoView({ behavior: 'smooth' });
      }
    };

    // New: Get prescription name
    const getPrescriptionName = (id) => {
      const match = prescriptions.value.find(p => p.id === id);
      return match ? match.name : '';
    };

    // New: Get selected herb names
    const getSelectedHerbNames = computed(() => {
      // selectedPrescriptionHerbs.value is an array of { id, name }
      return selectedPrescriptionHerbs.value.map(h => h.name || `ID:${h.id}`);
    });

    // New: Back button logic
    const deselectPrescription = () => {
      selectedPrescriptionId.value = null;
      selectedPrescriptionHerbs.value = [];
      prescriptionGameResult.value = null;
    };

    return {
      t,
      route,
      showHelp,
      searchQuery,
      prescriptions,
      groupedPrescriptions,
      selectedPrescriptionId,
      selectPrescriptionAndScroll,
      selectedPrescriptionHerbs,
      togglePrescriptionHerb,
      submitPrescriptionGameAndScroll,
      prescriptionGameResult,
      categories,
      selectedCategory,
      herbs,
      isClassificationMode,
      classifications,
      selectedClassification,
      toggleDisplayMode,
      selectCategory,
      selectClassification,
      extraNames,
      lackNames,
      searchPrescriptions,
      scrollToGroup,
      getPrescriptionName,
      getSelectedHerbNames,
      deselectPrescription,
      getHerbDetail,
      getHerbNamesBatch
    };
  }
};
</script>


<style scoped>
:root {
  --bg: #f9f9f9;
  --text: #333333;
  --card-bg: #ffffff;
  --accent: #4caf50;
  --border: #d6d6d6;
  --category-accent: #c78d59;
}

.prescription-game {
  padding: 20px;
  width: 900px;
  max-width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(4px);
  border-radius: 12px;
  color: var(--text);

}


/* Enable vertical scrolling for the prescription-herbs section */
.prescription-herbs {
  max-height: 100%;
  overflow-y: auto;
  padding-right: 8px; /* prevent content hiding under scrollbar */
  scrollbar-color: #999 transparent;
}
.prescription-herbs::-webkit-scrollbar {
  width: 8px;
}
.prescription-herbs::-webkit-scrollbar-track {
  background: transparent;
}
.prescription-herbs::-webkit-scrollbar-thumb {
  background-color: #999;
  border-radius: 4px;
}
.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  border: 1px solid #ba5f39;
  border-radius: 8px;
  padding: 8px;
  background-color: var(--card-bg);
}
.search-bar input[type="text"] {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid var(--accent);
  border-radius: 5px;
  font-size: 1em;
  background: var(--card-bg);
  color: var(--text);
}
.search-bar button {
  padding: 8px 15px;
  background-color: #ba5f39;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: inset 0 0 0 1px #ba5f39;
}
.prescription-list {
  margin-bottom: 20px;
  max-height: 580px;
  overflow-y: auto;
  border: 1px solid var(--accent);
  border-radius: 5px;
  padding: 10px;
  background-color: var(--card-bg);
  scrollbar-color: #999 transparent;
}
.prescription-list::-webkit-scrollbar {
  width: 8px;
}
.prescription-list::-webkit-scrollbar-track {
  background: transparent;
}
.prescription-list::-webkit-scrollbar-thumb {
  background-color: #999;
  border-radius: 4px;
}
.group {
  margin-bottom: 10px;
}
.group-title {
  font-weight: 600;
  font-size: 1.1em;
  color: var(--accent);
  margin-bottom: 5px;
  border-bottom: 1px solid var(--accent);
  padding-bottom: 4px;
}
.prescription-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); /* Ensure alignment */
  gap: 16px;
}

.prescription-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: var(--card-bg);
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  color: var(--text);
  min-height: 56px;
  overflow: hidden;
}
.prescription-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
}

.icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-weight: bold;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #494949;
}

.name {
  flex: 1;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.toggle-mode-btn {
  margin-bottom: 15px;
  padding: 8px 15px;
  background-color: var(--card-bg);
  border: 1px solid var(--accent);
  border-radius: 5px;
  cursor: pointer;
  color: var(--text);
  font-size: 0.95em;
  transition: background-color 0.2s ease, color 0.2s ease;
  box-shadow: inset 0 0 0 1px #ba5f39;
}
.categories,
.classifications {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}
.categories button,
.classifications button {
  padding: 8px 15px;
  background-color: var(--card-bg);
  box-shadow: inset 0 0 0 1px var(--category-accent);
  border: 1px solid var(--category-accent);
  border-radius: 5px;
  cursor: pointer;
  color: var(--text);
  font-size: 0.95em;
  transition: background-color 0.2s ease, color 0.2s ease;
}
.categories button.active,
.classifications button.active {
  background-color: var(--category-accent);
  box-shadow: inset 0 0 0 1px var(--category-accent);
}
.herb-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}
.herb-list button {
  padding: 8px 15px;
  background-color: var(--card-bg);
  border: 1px solid var(--accent);
  border-radius: 5px;
  cursor: pointer;
  color: var(--text);
  font-size: 0.95em;
  transition: background-color 0.2s ease, color 0.2s ease;
  box-shadow: inset 0 0 0 1px #ba5f39;
}
.herb-list button.selected {
  background-color: #ba5f39;
  box-shadow: inset 0 0 0 1px #ba5f39;
}
.submit-btn {
  margin-top: 10px;
  padding: 8px 20px;
  background-color: #ba5f39;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s ease;
  box-shadow: inset 0 0 0 1px #ba5f39;
}
.result {
  margin-top: 20px;
  text-align: left;
}
.result h3 {
  margin: 10px 0 5px;
  color: var(--accent);
}
.result ul {
  padding-left: 20px;
  margin-bottom: 10px;
}
.result li {
  margin-bottom: 4px;
  color: var(--text);
}
.error {
  color: #f44336;
  font-weight: bold;
}
.detail {
  font-size: 0.9em;
  color: #666666;
}

/* Sidebar category list styles */
.category-sidebar {
  position: fixed;
  top: 120px;
  left: 100px;
  width: 150px;
  height: 500px;
  overflow-y: auto;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(4px);
  border-radius: 8px;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}
.category-item {
  padding: 8px 12px;
  margin-bottom: 8px;
  background-color: var(--card-bg);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  text-align: center;
  transition: background 0.2s;
}

.category-item.active,
.category-item:hover {
  background-color: #ba5f39;
  color: white;
}
/* Sidebar category list styles */
.category-sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.back-btn {
  margin-bottom: 12px;
  width: fit-content;
  padding: 14px 24px;
  background-color: transparent;
  border: 1px solid var(--accent);
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
  transition: background-color 0.2s;
}
.back-btn:hover {
  background-color: var(--accent);
  color: #1e1e1e;
}

/* night mode */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1e1e1e;
    --text: #e0e0e0;
    --card-bg: #2a2a2a;
    --accent: #81c784;
    --border: #444444;
    --category-accent: #d2a679;
  }
  .category-sidebar::-webkit-scrollbar {
    width: 8px;
  }
  .category-sidebar::-webkit-scrollbar-track {
    background: transparent;
  }
  .category-sidebar::-webkit-scrollbar-thumb {
    background-color: #666;
    border-radius: 4px;
  }
  .category-sidebar {
    scrollbar-color: #666 transparent;
    background-color: rgba(30, 30, 30, 0.85);
    backdrop-filter: blur(4px);
    border-color: var(--category-accent);
    box-shadow: 0 2px 8px rgba(210, 166, 121, 0.12);
  }
  .category-item {
    color: var(--text);
    background: none;
  }
  .category-item.active,
  .category-item:hover {
    background: #ba5f39;
    color: #fff;
  }
  .prescription-game {
    background-color: rgba(30, 30, 30, 0.85);
    backdrop-filter: blur(4px);
    color: var(--text);
  }
  .prescription-list button,
  .toggle-mode-btn,
  .categories button,
  .classifications button,
  .herb-list button,
  .submit-btn,
  .search-bar input[type="text"],
  .search-bar button {
    background-color: var(--card-bg);
    color: var(--text);
    border-color: var(--accent);
  }
  .prescription-list button.active,
  .categories button.active,
  .classifications button.active,
  .submit-btn,
  .search-bar button {
    background-color: #ba5f39;
  }
  .result h3 {
    color: var(--accent);
  }
  .result li {
    color: #ccc;
  }
  .detail {
    color: #aaa;
  }
  .back-btn:hover{
    color:#aaaaaa;
  }
}

/* Added: Flex layout to wrap the sidebar and main content */
.category-wrapper {
  display: flex;
  justify-content: center;     /* horizontally CenteredContent */
  align-items: flex-start;
  gap: 20px;

  width: 100vw;
  height: 100vh;                /* the Fixed Height Is The Viewport Height */
  overflow: hidden;            /* prevent Content From Stretching Up Or Overflowing */
  padding: 40px;
  box-sizing: border-box;

  background-image: url('/PrescriptionGame_background.png');
  background-size: cover;      /* the Background Image Covers The Entire Container */
  background-position: center;
  background-repeat: no-repeat;
}
/* Added: Selected information styles */
.selected-info {
  margin-bottom: 12px;
  font-size: 1.1rem;
  color: var(--text);
  font-weight: bold;
}
.selected-info p {
  margin: 6px 0;
}


.back-btn1 {
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

.back-btn1:hover {
  background-color: #a44e2f;
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
.close-btn {
  margin-top: 20px;
  padding: 8px 20px;
  background-color: #ba5f39;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
