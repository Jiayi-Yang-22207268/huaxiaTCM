<template>
  <div class="prescription-list">
    <h1>{{ $t('prescriptions.title') }}</h1>
    <!-- Search bar -->
    <div class="search-bar">
      <input
          type="text"
          v-model="searchQuery"
          :placeholder="$t('prescriptions.searchPlaceholder')"
          class="search-input"
          @keyup.enter="searchPrescriptions"
      />
      <button
          v-if="searchQuery"
          @click="clearSearch"
          class="clear-btn"
          title="Clear search"
      >
        ×
      </button>
      <button @click="searchPrescriptions" class="search-btn">
        {{ $t('prescriptions.searchButton') }}
      </button>
    </div>
    <!-- Group titles + Card grid -->
    <div v-if="Object.keys(groupedPrescriptions).length && prescriptionsToShow.length">
      <div
          v-for="(items, letter) in groupedPrescriptions"
          :key="letter"
          class="group"
      >
        <h2 class="group-title">{{ letter }}</h2>
        <div class="prescription-grid">
          <div
              v-for="prescription in items"
              :key="prescription.id"
              class="prescription-item"
              @click="viewDetail(prescription.id)"
          >
            <div
                class="icon"
                :style="{ backgroundColor: `hsl(${getHue(letter)}, 60%, 80%)` }"
            >
              {{ letter }}
            </div>
            <div class="name">{{ prescription.name }}</div>
          </div>
        </div>
      </div>
    </div>
    <p v-else-if="searchPerformed">
      {{ $t('prescriptions.noResults') }}
    </p>
    <ChatBot />
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getPrescriptions, searchPrescriptionsByName } from '@/api/tcm/prewiki.js';
import ChatBot from '@/components/AI/ChatBot.vue';
// ① Import pinyin
import { pinyin } from 'pinyin-pro';

export default {
  components: { ChatBot },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const prescriptions = ref([]);
    const searchQuery = ref('');
    const searchResults = ref([]);
    const searchPerformed = ref(false);

    const loadPrescriptions = async () => {
      prescriptions.value = await getPrescriptions(route.params.lang);
      searchPerformed.value = false;
      searchResults.value = [];
    };

    watch(() => route.params.lang, loadPrescriptions);
    onMounted(loadPrescriptions);

    const searchPrescriptions = async () => {
      const q = searchQuery.value.trim();
      if (!q) {
        searchPerformed.value = false;
        searchResults.value = [];
      } else {
        searchResults.value = await searchPrescriptionsByName(
            q,
            route.params.lang
        );
        searchPerformed.value = true;
      }
    };

    const prescriptionsToShow = computed(() =>
        searchPerformed.value ? searchResults.value : prescriptions.value
    );

    // ② Group by first letter: use the first letter of the pinyin in Chinese mode
    const groupedPrescriptions = computed(() => {
      const map = {};
      prescriptionsToShow.value.forEach((p) => {
        let letter = '';
        if (route.params.lang === 'en') {
          // English: Directly use the first letter of the English name
          letter = p.name.charAt(0).toUpperCase();
        } else {
          // Chinese: Get the pinyin of the first character of the name, and use the first letter
          const pyArr = pinyin(p.name.charAt(0), {
            toneType: 'none',
            type: 'array',
          });
          letter = pyArr[0]
              ? pyArr[0].charAt(0).toUpperCase()
              : '#'; // If pinyin cannot be retrieved, group under '#'
        }
        if (!map[letter]) map[letter] = [];
        map[letter].push(p);
      });
      // Return sorted by letter
      return Object.keys(map)
          .sort()
          .reduce((obj, l) => {
            obj[l] = map[l];
            return obj;
          }, {});
    });

    const getHue = (letter) => {
      const code = letter.charCodeAt(0) - 65;
      return ((code * 35) % 360) + 20;
    };

    const viewDetail = (id) => {
      router.push(`/${route.params.lang}/prescriptions/${id}`);
    };

    const clearSearch = () => {
      searchQuery.value = '';
      searchResults.value = [];
      searchPerformed.value = false;
      isSearchMode.value = false;
    };

    return {
      searchQuery,
      searchPerformed,
      searchPrescriptions,
      prescriptionsToShow,
      groupedPrescriptions,
      getHue,
      viewDetail,
      clearSearch,
    };
  },
};
</script>
<style scoped>
/* Define default (light mode) variables */
.prescription-list {
  padding: 20px;
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
  width: 1000px;
  /* Or set to a larger value, such as 1400px */
  margin: 0 auto;
  /* Default card background color is white */
  --card-bg: #ffffff;
}
/* Light/Dark mode toggle */
@media (prefers-color-scheme: dark) {
  .prescription-list {
    /* Dark mode background & text colors */
    --bg: #121212;
    --text: #e0e0e0;
    /* Dark mode card background */
    --card-bg: #1f1f1f;
  }
}
/* Search bar */
.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}
.search-input {
  width: 280px;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  background: var(--card-bg);
  color: var(--text);
}
.search-btn {
  padding: 8px 16px;
  background-color: var(--accent, #ba5f39);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}
.search-btn:hover {
  background-color: #9c4a2d;
}
/* Group title */
.group {
  margin-bottom: 32px;
}
.group-title {
  font-size: 1.3rem;
  margin: 16px 0 8px;
  border-left: 4px solid var(--accent, #ba5f39);
  padding-left: 8px;
  color: var(--text);
}
/* Card grid */
.prescription-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}
/* Individual card */
.prescription-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  color: var(--text);
}
.prescription-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12);
}
/* Letter badge */
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
/* Name text */
.name {
  flex: 1;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.clear-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--text);
  padding: 4px;
}
.clear-btn:hover {
  color: #ba5f39;
}
</style>
