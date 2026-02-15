<template>
  <div class="prescription-quiz">
    <div class="category-sidebar">
      <ul>
        <li
            v-for="group in groups"
            :key="group.name"
            @click="scrollToGroup(group.name)"
            class="category-item"
            :class="{ active: selectedGroup === group.name }"
        >
          {{ group.name }}
        </li>
      </ul>
    </div>
    <div v-if="feedback" class="feedback-modal">
      <div class="feedback-content">
        <p>{{ feedback }}</p>
        <button class="next-btn" @click="handleNextQuestion">
          {{ $t('quiz.nextQuestion') }}
        </button>
      </div>
    </div>
    <div class="quiz-main">
      <button class="back-button" @click="goBack">
        {{ $t('quiz.backToMenu') }}
      </button>
      <div v-if="quizState === 'inProgress'" class="quiz-container">
        <h2>
          {{ $t('quiz.prescriptionTitle') }}: {{ currentQuestion.prescriptionName }}
        </h2>
        <div class="question-info">
          {{ $t('quiz.questionId') }}: {{ currentQuestion.id }}
          {{ $t('quiz.difficulty') }}: {{ currentQuestion.difficulty }}
        </div>
        <div class="selected-herbs">
          <strong>{{ $t('quiz.selectedHerbs') }}</strong>
          <span v-if="selectedHerbs.length">
    <span
        v-for="id in selectedHerbs"
        :key="id"
        class="selected-herb"
        @click="toggleHerb(id)"
    >
      {{ allHerbs.find(h => h.id === id)?.name || id }}
    </span>
  </span>
          <span v-else>
    {{ $t('quiz.noneSelected') }}
  </span>
        </div>
        <div class="herb-selection">
          <div class="search-bar">
            <input
                type="text"
                v-model="searchQuery"
                :placeholder="$t('herbs.searchPlaceholder')"
                class="search-input"
                @keyup.enter="searchHerbs"
            />
            <button
                v-if="searchPerformed"
                @click="clearSearch"
                class="clear-btn"
                :title="$t('herbs.clearSearch')"
            >
              ×
            </button>
            <button @click="searchHerbs" class="search-btn">
              {{ $t('herbs.search') }}
              <span v-if="isLoading" class="loading-spinner"></span>
            </button>
            <button @click="toggleDisplayMode" class="toggle-mode-btn">
              {{ isClassificationMode
                ? $t('herbs.ClassificationMode')
                : $t('herbs.CategoryMode') }}
            </button>
            <button @click="submitAnswer" class="submit-btn">
              {{ $t('quiz.submit') }}
            </button>
          </div>
          <!-- Loading animation (fullscreen or partial) -->
          <div v-if="isLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
            <p>Loading...</p>
          </div>
          <div v-if="searchPerformed">
            <div class="group">
              <h2 class="group-title">
                {{ $t('herbs.searchResults') }}
              </h2>
              <div class="herb-grid">
                <div
                    v-for="herb in searchResults"
                    :key="herb.id"
                    :class="['herb-item', { selected: selectedHerbs.includes(herb.id) } ]"
                    @mouseenter="loadImage(herb.id, herb.image)"
                    @click="toggleHerb(herb.id)"
                >
                  <img
                      v-if="loadedImages[herb.id]"
                      :src="loadedImages[herb.id]"
                      alt="herb image"
                      class="herb-image"
                  />
                  <div class="icon" :style="{ backgroundColor: herb.color }">
                    {{ herb.name[0] }}
                  </div>
                  <div class="name">{{ herb.name }}</div>
                </div>
              </div>
            </div>
          </div>
          <div v-else-if="groups.length">
            <div class="herb-grid-wrapper">
              <div class="herb-grid">
                <div
                    v-for="herb in displayHerbs"
                    :key="herb.id"
                    :class="['herb-item', { selected: selectedHerbs.includes(herb.id) } ]"
                    @mouseenter="loadImage(herb.id, herb.image)"
                    @click="toggleHerb(herb.id)"
                >
                  <img
                      v-if="loadedImages[herb.id]"
                      :src="loadedImages[herb.id]"
                      alt="herb image"
                      class="herb-image"
                  />
                  <div class="icon" :style="{ backgroundColor: herb.color }">
                    {{ herb.name[0] }}
                  </div>
                  <div class="name">{{ herb.name }}</div>
                </div>
              </div>
            </div>
          </div>
          <p v-else-if="searchPerformed">
            {{ $t('herbs.noResults') }}
          </p>
        </div>
      </div>
      <div v-else-if="quizState === 'finished'" class="result-screen">
        <h2>{{ $t('quiz.resultTitle') }}</h2>
        <ul>
          <li v-for="(item, index) in results" :key="item.questionId">
            <div class="result-item-header">
              <div class="result-left">
                {{ $t('quiz.question') }} {{ index + 1 }}: {{ $t('quiz.prescriptionTitle') }}
                "{{ item.prescriptionName }}"
              </div>
              <div class="result-center">
                <div>
                  <strong>{{ $t('quiz.yourAnswer') }}:</strong>
                  {{ item.selectedHerbs
                    .map(id => {
                      const herb = allHerbs.find(h => h.id === id);
                      return herb ? herb.name : id;
                    })
                    .join(', ') }}
                </div>
                <div>
                  <strong>{{ $t('quiz.correctAnswer') }}:</strong>
                  {{ item.correctHerbIds
                    .map(id => {
                      const herb = allHerbs.find(h => h.id === id);
                      return herb ? herb.name : id;
                    })
                    .join(', ') }}
                </div>
              </div>
              <div class="result-right">
                <span :class="['badge', item.correct ? 'correct' : 'incorrect']">
                  {{ item.correct ? $t('quiz.correct') : $t('quiz.incorrect') }}
                </span>
              </div>
            </div>
          </li>
        </ul>
        <p>{{ $t('quiz.accuracy') }}: {{ accuracy }}%</p>
        <div class="time-info">
          {{ $t('quiz.totalTime') }}: {{ totalTime }} {{ $t('quiz.seconds') }}
        </div>
        <button @click="resetQuiz" class="restart-btn">{{ $t('quiz.restart') }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/stores/authStore.js';
import {
  getHerbCategories,
  getHerbsByCategory,
  getHerbClassifications,
  getHerbsByClassification,
  searchHerbsByName
} from '@/api/tcm/herbwiki.js';
import { getPrescriptionQuestion, submitPrescriptionQuizScore } from '@/api/tcm/quiz.js';

const { t } = useI18n();
const route = useRoute();
const authStore = useAuthStore();
const emit = defineEmits(['back']);

// State
const groups = ref([]);                 // [{ name, herbs: [] }]
const selectedGroup = ref('');
const categoryColors = reactive({});    // name -> hue
const idToCategory = reactive({});      // herbId -> category name
const allHerbs = ref([]);

const searchQuery = ref('');
const searchResults = ref([]);
const searchPerformed = ref(false);
const isClassificationMode = ref(false);
const selectedHerbs = ref([]);
const loadedImages = reactive({});

const isLoading = ref(false);

// Computed
const displayHerbs = computed(() => {
  const grp = groups.value.find(g => g.name === selectedGroup.value);
  return grp ? grp.herbs : [];
});

// Quiz
const quizState = ref('inProgress');
const currentIndex = ref(0);
const totalQuestions = 5;
const currentDifficulty = ref(1);
const currentQuestion = ref({ id: '', prescriptionName: '', correctHerbIds: [], difficulty: 1, correctHerbNames: [] });
const results = ref([]);
const feedback = ref('');
const accuracy = ref(0);
const quizStartTime = ref(0);
const totalTime = ref(0);

// Helpers
const getHue = key => {
  let hash = 0;
  for (let i = 0; i < key.length; i++) {
    hash = key.charCodeAt(i) + ((hash << 5) - hash);
  }
  return hash % 360;
};

// Load herbs for a specific group
const loadGroupHerbs = async name => {
  const herbs = isClassificationMode.value
      ? await getHerbsByClassification(name, route.params.lang)
      : await getHerbsByCategory(name, route.params.lang);
  const hue = categoryColors[name];
  const groupIndex = groups.value.findIndex(g => g.name === name);
  const processed = herbs.map(h => {
    idToCategory[h.id] = name;
    return { ...h, color: `hsl(${hue},60%,80%)` };
  });
  groups.value[groupIndex].herbs = processed;
  processed.forEach(h => {
    if (!allHerbs.value.some(a => a.id === h.id)) {
      allHerbs.value.push({ id: h.id, name: h.name });
    }
  });
};

// Initialize categories or classifications
const loadCategories = async () => {
  const cats = await getHerbCategories(route.params.lang);
  cats.forEach(cat => { categoryColors[cat] = getHue(cat); });
  groups.value = cats.map(cat => ({ name: cat, herbs: [] }));
  if (groups.value.length) {
    selectedGroup.value = groups.value[0].name;
    await loadGroupHerbs(selectedGroup.value);
  }
};
const loadClassifications = async () => {
  const clss = await getHerbClassifications(route.params.lang);
  clss.forEach(cls => { categoryColors[cls] = getHue(cls); });
  groups.value = clss.map(cls => ({ name: cls, herbs: [] }));
  if (groups.value.length) {
    selectedGroup.value = groups.value[0].name;
    await loadGroupHerbs(selectedGroup.value);
  }
};

// Handlers
const scrollToGroup = async name => {
  if (searchPerformed.value) return;
  const grp = groups.value.find(g => g.name === name);
  if (!grp.herbs.length) await loadGroupHerbs(name);
  selectedGroup.value = name;
  const el = document.getElementById(`group-${name}`);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
};
const goBack = () => emit('back');
const toggleDisplayMode = async () => {
  isClassificationMode.value = !isClassificationMode.value;
  searchQuery.value = '';
  searchResults.value = [];
  searchPerformed.value = false;
  if (isClassificationMode.value) await loadClassifications();
  else await loadCategories();
};

// 搜索逻辑：按需加载分组，保证映射和颜色一致
// const searchHerbs = async () => {
//   if (!searchQuery.value.trim()) return;
//   // 1) 执行搜索
//   const res = await searchHerbsByName(searchQuery.value, route.params.lang);
//   // 2) 对未映射的药材，按需加载它所属的分组
//   for (const h of res) {
//     if (!idToCategory[h.id]) {
//       for (const g of groups.value) {
//         if (!g.herbs.length) {
//           await loadGroupHerbs(g.name);
//         }
//         if (idToCategory[h.id]) break;
//       }
//     }
//   }
//   // 3) 赋色
//   searchResults.value = res.map(h => {
//     const cat = idToCategory[h.id] || h.name;
//     const hue = categoryColors[cat] ?? getHue(cat);
//     return { ...h, color: `hsl(${hue},60%,80%)` };
//   });
//   searchPerformed.value = true;
// };

const searchHerbs = async () => {
  isLoading.value = true;

  if (!searchQuery.value.trim()) {
    isLoading.value = false;
    return;
  }
  try {
    // 1) 执行搜索
    const res = await searchHerbsByName(searchQuery.value, route.params.lang);
    // 2) 对未映射的药材，按需加载它所属的分组
    for (const h of res) {
      if (!idToCategory[h.id]) {
        for (const g of groups.value) {
          if (!g.herbs.length) {
            await loadGroupHerbs(g.name);
          }
          if (idToCategory[h.id]) break;
        }
      }
    }
    // 3) 赋色
    searchResults.value = res.map(h => {
      const cat = idToCategory[h.id] || h.name;
      const hue = categoryColors[cat] ?? getHue(cat);
      return {...h, color: `hsl(${hue},60%,80%)`};
    });
    searchPerformed.value = true;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

const clearSearch = () => {
  searchQuery.value = '';
  searchResults.value = [];
  searchPerformed.value = false;
};

const loadImage = (id, url) => { if (!loadedImages[id]) loadedImages[id] = url; };
const toggleHerb = id => {
  const idx = selectedHerbs.value.indexOf(id);
  if (idx >= 0) selectedHerbs.value.splice(idx, 1);
  else selectedHerbs.value.push(id);
};

// Quiz flow
const loadNextQuestion = async () => {
  if (currentIndex.value >= totalQuestions) {
    totalTime.value = Math.floor((Date.now() - quizStartTime.value) / 1000);
    quizState.value = 'finished';
    return;
  }
  selectedHerbs.value = [];
  feedback.value = '';
  const doneIds = results.value.map(r => r.questionId);
  const q = await getPrescriptionQuestion(route.params.lang, currentDifficulty.value, doneIds);
  if (q) currentQuestion.value = { id: q.id, prescriptionName: q.prescriptionName, correctHerbIds: q.correctHerbIds, difficulty: q.difficulty, correctHerbNames: q.correctHerbNames };
  else quizState.value = 'finished';
};

const startQuiz = async () => {
  quizStartTime.value = Date.now();
  currentIndex.value = 0;
  currentDifficulty.value = 1;
  results.value = [];
  quizState.value = 'inProgress';
  await loadCategories();
  await loadNextQuestion();
};

const submitAnswer = () => {
  if (!selectedHerbs.value.length) return alert(t('quiz.selectAtLeastOneHerb'));
  const userSet = new Set(selectedHerbs.value);
  const correctSet = new Set(currentQuestion.value.correctHerbIds);
  console.log('correctSet', correctSet)
  console.log('userSet', userSet)
  const correct = userSet.size === correctSet.size && [...correctSet].every(i => userSet.has(i));
  if (correct && currentDifficulty.value < 3) currentDifficulty.value++;
  if (!correct && currentDifficulty.value > 1) currentDifficulty.value--;
  results.value.push({ questionId: currentQuestion.value.id, prescriptionName: currentQuestion.value.prescriptionName, selectedHerbs: [...selectedHerbs.value], correctHerbIds: [...currentQuestion.value.correctHerbIds], correct });
  feedback.value = correct ? t('quiz.answerCorrect') : t('quiz.answerIncorrect', { correctAnswer: currentQuestion.value.correctHerbNames.join(', ') });
};

const handleNextQuestion = () => { feedback.value = ''; currentIndex.value++; loadNextQuestion(); };
const resetQuiz = () => { quizState.value='inProgress'; currentIndex.value=0; currentDifficulty.value=1; results.value=[]; feedback.value=''; selectedHerbs.value=[]; startQuiz(); };

watch(quizState, async s => {
  if (s === 'finished') {
    const total = results.value.length;
    accuracy.value = total ? Math.round(results.value.filter(r => r.correct).length / total * 100) : 0;
    const user = authStore.user?.username || '';
    await submitPrescriptionQuizScore(accuracy.value, user, totalTime.value, route.params.lang);
  }
});

watch(() => route.params.lang, async () => {
  if (searchPerformed.value) await searchHerbs();
  else if (isClassificationMode.value) await loadClassifications();
  else await loadCategories();
});

onMounted(startQuiz);
</script>



<style scoped>
/* Loading animation */
/* Small spinning animation inside the button */
.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s linear infinite;
  margin-left: 8px;
}

/* Full-screen loading overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.loading-overlay .loading-spinner {
  width: 40px;
  height: 40px;
  border-width: 4px;
  margin-bottom: 16px;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.search-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.prescription-quiz {
  position: relative;
  height: 100%;
  text-align: center;
  width: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Fixed back button at the top-left corner */
.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  padding: 8px 12px;
  background-color: #9c4a2d;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
}

/* Container to center the main content */
.quiz-main {
  position: absolute;
  width: 1000px;
  height: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
  padding-top: 20px;
}

/* Remaining original styles */
.start-screen,
.result-screen {
  margin-top: 20px;
}
.question-info {
  margin-bottom: 10px;
  font-size: 14px;
  color: #555;
}
.herb-selection {
  margin: 20px;
}
.toggle-mode-btn {
  margin-bottom: 15px;
  padding: 8px 15px;
  background-color: var(--accent, #ba5f39);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.95rem;
}
.categories,
.classifications {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: center;
}
.categories button,
.classifications button {
  padding: 8px 15px;
  background-color: white;
  border: 1px solid #4CAF50;
  border-radius: 5px;
  cursor: pointer;
}
.categories button.active,
.classifications button.active {
  background-color: #4CAF50;
  color: white;
}
.herb-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: center;
}
.herb-list button {
  padding: 8px 15px;
  background-color: white;
  border: 1px solid #4CAF50;
  border-radius: 5px;
  cursor: pointer;
}
.herb-list button.selected {
  background-color: #4CAF50;
  color: white;
}
.feedback {
  margin-top: 10px;
  font-weight: bold;
}
.time-info {
  margin-top: 15px;
  font-size: 1.2em;
}

/* New styles for result screen */
.result-screen button {
  margin-top: 20px;
  padding: 10px 24px;
  background-color: #ba5f39;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}
.result-screen button:hover {
  background-color: #9c4a2d;
  transform: translateY(-2px);
}
.result-screen ul {
  list-style: none;
  padding: 0;
  margin: 0 auto;
  width: 80%;
  text-align: left;
}
.result-screen li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
}
.result-screen li:last-child {
  border-bottom: none;
}
.result-screen .badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.85em;
  font-weight: bold;
}
.result-screen .correct {
  background-color: #d4edda;
  color: #155724;
}
.result-screen .incorrect {
  background-color: #f8d7da;
  color: #721c24;
}

@import "../../assets/css/component.css";

/* Define default (light mode) variables */
.herb-list {
  padding: 20px;
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
  width: 1000px;
  margin: 0 auto;
  --card-bg: #ffffff;
}

/* Light/dark mode toggle */
@media (prefers-color-scheme: dark) {
  .herb-list {
    --bg: #121212;
    --text: #e0e0e0;
    --card-bg: #1f1f1f;
  }
}

/* Toggle category button */
.toggle-mode-btn {
  padding: 8px 16px;
  background-color: #ffffff;
  color: #2a2a2a;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
  transform: translateY(15px);
}
.toggle-mode-btn:hover {
  background-color: #e3e3e3;
}

/* Search bar */
.search-bar {
  display: flex;
  justify-content: right;
  align-items: flex-end;
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
  background-color: #ffffff;
  color: #2a2a2a;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}
.search-btn:hover {
  background-color: #e3e3e3;
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
.herb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

/* Single card */
.herb-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease, height 0.3s ease;
  color: var(--text);
  position: relative;
  overflow: hidden;
  height: 60px; /* Set initial height */
}
.herb-item:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  height: 160px; /* Expand to show the full image */
  align-items: flex-end; /* Push text to bottom */
  padding: 12px;
}
.herb-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 8px;
}
.herb-item:hover .herb-image {
  opacity: 1;
}

/* Only retain position/z-index, remove background-related properties */
.icon,
.name {
  position: relative;
  z-index: 1;
}

/* Initial letter badge */
/* No background for initial letter badge, keep original style */
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

/* Herb name */
/* Herb name, default without background */
.name {
  flex: 1;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.herb-item:hover .name {
  background: rgba(0, 0, 0, 0.7);
  border-radius: 4px;
  padding: 6px 10px;
  white-space: normal;
  overflow: visible;
  text-overflow: initial;
  word-break: break-word;
  text-align: center;
  color: #ffffff; /* Add this line to make text bright */
}

.category-sidebar {
  position: fixed;
  top: 220px;
  left: 100px;
  width: 150px;
  height: 500px; /* Fixed height */
  overflow-y: auto; /* Enable vertical scrolling */
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.category-sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
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
.category-item:hover {
  background-color: #ba5f39;
  color: white;
}
.category-item.active {
  background-color: #ba5f39;
  color: #fff;
}

.herb-grid-wrapper {
  max-height: 500px;
  overflow-y: auto;
  padding-right: 6px;
  margin-bottom: 20px;
}
.herb-item.selected {
  background-color: #ba5f39;
  color: #fff;
}
.herb-item.selected .name {
  color: #fff;
}
.herb-item.selected .icon {
  color: #fff;
}

.submit-btn {
  margin-top: 20px;
  padding: 10px 24px;
  background-color: var(--accent, #ba5f39);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}
.submit-btn:hover {
  background-color: #9c4a2d;
  transform: translateY(-2px);
}
.selected-herbs {
  margin-top: 20px;
  padding: 10px 16px;
  background: var(--card-bg);
  border-radius: 6px;
  font-size: 0.95rem;
  color: var(--text);
  text-align: left;
}

/* Minimalist rectangular modal with white background and semi-transparent overlay */
.feedback-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4); /* semi-transparent overlay */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
.feedback-content {
  background: var(--card-bg, #ffffff);
  color: var(--text, #333);
  border: 1px solid #ccc;
  border-radius: 12px;
  padding: 24px 32px;
  font-size: 1.1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  max-width: 480px;
  width: 80%;
  text-align: center;
}
@media (prefers-color-scheme: dark) {
  .feedback-content {
    background: var(--card-bg, #1e1e1e);
    color: var(--text, #e0e0e0);
    border: 1px solid #555;
  }
}
.next-btn {
  margin-top: 16px;
  padding: 8px 20px;
  background-color: var(--accent, #ba5f39);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.next-btn:hover {
  background-color: #9c4a2d;
}

.result-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  width: 100%;
}
.result-left {
  flex: 1;
  text-align: left;
}
.result-center {
  flex: 2;
  text-align: center;
}
.result-right {
  flex: 1;
  text-align: right;
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
.selected-herbs strong {
  font-size: 1.1em;
}

.selected-herb {
  display: inline-block;
  margin-right: 8px;
  padding: 4px 8px;
  margin-top: 3px;
  border-radius: 6px;
  background-color: #f0f0f0;
  cursor: pointer;
  font-size: 1.2em;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.selected-herb:hover {
  background-color: #e0e0e0;
  transform: scale(1.05);
}
@media (prefers-color-scheme: dark) {
  .selected-herbs strong {
    font-size: 1.1em;
  }

  .selected-herb {
    display: inline-block;
    margin-right: 8px;
    margin-top: 3px;
    padding: 4px 8px;
    border-radius: 6px;
    background-color: #f0f0f0;
    color:#333;
    cursor: pointer;
    font-size: 1.2em;
    transition: background-color 0.2s ease, transform 0.2s ease;
  }

  .selected-herb:hover {
    background-color: #e0e0e0;
    transform: scale(1.05);
  }
}
</style>
