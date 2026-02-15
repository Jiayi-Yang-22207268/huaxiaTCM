<template>
  <div class="image-herb-quiz">
    <!-- Add a container to center the main content -->
    <div class="quiz-main">
      <button class="back-button" @click="goBack">{{ $t('quiz.backToMenu') }}</button>

      <!-- Quiz in progress -->
      <div v-if="quizState === 'inProgress'" class="quiz-container">
        <div class="question" v-if="currentDetail">

          <!-- Image loading area -->
          <div class="image-wrapper">
            <h2>{{ $t('quiz.herbQuizTitle')}}</h2>
            <img
                v-show="!imageLoading"
                :src="currentDetail.imageUrl"
                alt="Herb Image"
                @load="imageLoading = false"
            />
            <div v-show="imageLoading" class="spinner">
              <!-- Simple rotating animation, can be implemented using CSS animations -->
              <div class="loader"></div>
            </div>
          </div>
          <div class="options">
            <button
                v-for="option in currentDetail.options"
                :key="option"
                @click="handleAnswer(option)"
                :disabled="imageLoading || answered"
                :class="[
                  'quiz-option',
                  answered && option === currentDetail.name ? 'correct-option' : '',
                  answered && option === selectedOption ? (option === currentDetail.name ? 'correct-option' : 'incorrect-option') : ''
                ]"
            >
              {{ option }}
            </button>
          </div>
          <div class="progress-bar-container">
            <div
                class="progress-bar"
                :style="{ width: ((progressIndex) / 5 * 100) + '%' }"
            ></div>
          </div>
          <div class="feedback" v-if="feedback">{{ feedback }}</div>
        </div>
        <div v-else>
          {{ $t('quiz.loading') }}
        </div>
      </div>

      <!-- Display results after the quiz is completed -->
      <div v-else-if="quizState === 'finished'" class="result-screen">
        <h2>{{ $t('quiz.resultTitle') }}</h2>
        <div class="result-card">
          <ul class="result-list">
            <li v-for="result in results" :key="result.id" class="result-item">
              <img
                  :src="result.imageUrl"
                  alt="herb"
                  class="result-herb-image"
                  v-if="result.imageUrl"
              />
              <div class="result-info">
                <div>{{ $t('quiz.yourAnswer') }}: {{ result.selected }}</div>
                <div>{{ $t('quiz.correctAnswer') }}: {{ result.correctAnswer }}</div>
              </div>
              <span
                  :class="['badge', result.correct ? 'correct' : 'incorrect']"
              >
                {{ result.correct ? $t('quiz.correct') : $t('quiz.incorrect') }}
              </span>
            </li>
          </ul>
        </div>
        <div class="time-info">
          <!-- Display total time taken (unit: seconds) -->
          {{ $t('quiz.totalTime') }}: {{ totalTime }} {{ $t('quiz.seconds') }}
        </div>
        <button @click="resetQuiz">{{ $t('quiz.restart') }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import { getHerbIds, getHerbDetail, submitQuizScore } from '@/api/tcm/quiz.js';
import { useAuthStore } from '@/stores/authStore.js';
import ChatBot from "@/components/AI/ChatBot.vue";

const { t, locale } = useI18n();
const route = useRoute();
const authStore = useAuthStore();

const quizState = ref('inProgress'); // Status: 'inProgress', 'finished'
const herbIds = ref([]);
const currentIndex = ref(0);
const currentDetail = ref(null);
const results = ref([]);
const feedback = ref('');
const imageLoading = ref(true); // Image loading status
const answered = ref(false); // New addition, marks whether the current question has been answered
const progressIndex = ref(0);

// New ref to track the selected option
const selectedOption = ref('');

// Record start time and total elapsed time (unit: seconds)
const quizStartTime = ref(0);
const totalTime = ref(0);

// Define a back event, the parent component will listen for the 'back' event
const emit = defineEmits(['back']);
const goBack = () => {
  emit('back');
};

// Start the quiz
const startQuiz = async () => {
  quizStartTime.value = Date.now();
  herbIds.value = await getHerbIds(route.params.lang);
  if (herbIds.value.length === 0) {
    alert(t('quiz.noData'));
    return;
  }
  currentIndex.value = 0;
  results.value = [];
  quizState.value = 'inProgress';
  loadNextQuestion();
};

// Load the next question
const loadNextQuestion = async () => {
  if (currentIndex.value >= herbIds.value.length) {
    totalTime.value = Math.floor((Date.now() - quizStartTime.value) / 1000);
    quizState.value = 'finished';
    const total = results.value.length;
    const correctCount = results.value.filter(result => result.correct).length;
    const accuracy = total ? (correctCount / total) * 100 : 0;
    const username = authStore.user ? authStore.user.username : "";
    const res = await submitQuizScore(accuracy, username, totalTime.value, route.params.lang);
    console.log('Quiz result submitted:', res);
    return;
  }
  imageLoading.value = true;
  answered.value = false;
  selectedOption.value = '';
  const id = herbIds.value[currentIndex.value];
  currentDetail.value = await getHerbDetail(id, route.params.lang);
  // progressIndex.value = currentIndex.value;
  feedback.value = '';
  if (!currentDetail.value) {
    results.value.push({ id: id, selected: '', correct: false });
    currentIndex.value++;
    setTimeout(() => { loadNextQuestion(); }, 2000);
  }
};

// Handle answer selection
const handleAnswer = (selectedOptionParam) => {
  if (answered.value) return;
  selectedOption.value = selectedOptionParam;
  answered.value = true;
  progressIndex.value = currentIndex.value + 1;
  const correct = selectedOptionParam === currentDetail.value.name;
  results.value.push({
    id: herbIds.value[currentIndex.value],
    selected: selectedOptionParam,
    correctAnswer: currentDetail.value.name,
    imageUrl: currentDetail.value.imageUrl,
    correct: correct
  });
  feedback.value = correct
      ? t('quiz.answerCorrect')
      : t('quiz.answerIncorrect', { correctAnswer: currentDetail.value.name });
  setTimeout(() => {
    currentIndex.value++;
    loadNextQuestion();
  }, 2000);
};

// Reset the quiz
const resetQuiz = () => {
  herbIds.value = [];
  currentIndex.value = 0;
  currentDetail.value = null;
  results.value = [];
  feedback.value = '';
  totalTime.value = 0;
  startQuiz();
};

// Watch for changes in the locale and update the current question's details
watch(
    () => locale.value,
    async (newLang) => {
      if (quizState.value === 'inProgress' && currentDetail.value) {
        const id = herbIds.value[currentIndex.value];
        currentDetail.value = await getHerbDetail(id, newLang);
      }
    }
);

// Start the quiz when the component is mounted
onMounted(() => {
  startQuiz();
});
</script>

<style scoped>
.image-herb-quiz {
  position: relative;
  min-height: 100vh;
  padding: 20px;
  /* Center text */
  text-align: center;
}
/* Keep the back button in the top-left corner */
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
/* Center the main content */
.quiz-main {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60%;
  height: 100%;
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
}
/* Retain the original content styles */
.start-screen,
.result-screen {
  margin-top: 7%;
}
/* Enhance the styling for the question image */
.image-wrapper img {
  width: 70%;
  height: auto;
  border: 6px solid #ba5f39;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
/* Image loading area */
.image-wrapper {
  margin-top: 10%;
  position: relative;
  min-height: 200px;
}
/* Spinner styles and animation */
.spinner {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
.loader {
  border: 6px solid #f3f3f3;
  border-top: 6px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.options {
  width: 65%;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 20px;
}
.options button {
  flex: 1;
  max-width: 25%;
  padding: 16px 12px;
  font-size: 1rem;
  background-color: #ffffff;
  border: 1px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.options button:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.options button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.feedback {
  margin-top: 10px;
  font-weight: bold;
}
.time-info {
  margin-top: 20px;
  font-size: 1.2em;
}
.progress-bar-container {
  width: 60%;
  margin: 10px auto 0;
  height: 20px;
  background-color: #ddd;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  background-color: #af6f4c;
  transition: width 0.3s ease;
}
.result-card {
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  margin-top: 10px;
  margin-left: auto;
  margin-right: auto;
  text-align: left;
  width: 80%;
}
@media (prefers-color-scheme: dark) {
  .result-card {
    background-color: #2b2b2b;
    border: 1px solid #444;
  }
}
.result-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
/* Result item display: image, info, badge */
.result-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
}
.result-herb-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid #ccc;
}
.result-info {
  flex: 1;
}
.result-item:last-child {
  border-bottom: none;
}
.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.85em;
  font-weight: bold;
}

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

.correct {
  background-color: #d4edda;
  color: #155724;
}
.incorrect {
  background-color: #f8d7da;
  color: #721c24;
}

/* Added styles for feedback colors and bounce animation */
.quiz-option.correct-option {
  background-color: #d4edda;
  color: #155724;
  animation: bounce 0.4s ease;
}
.quiz-option.incorrect-option {
  background-color: #f8d7da;
  color: #721c24;
  animation: bounce 0.4s ease;
}

@keyframes bounce {
  0% { transform: scale(1); }
  30% { transform: scale(1.1); }
  60% { transform: scale(0.95); }
  100% { transform: scale(1); }
}
</style>