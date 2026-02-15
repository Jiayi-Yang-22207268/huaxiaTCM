<template>
  <div class="quiz-page">
    <!-- Menu state: two-column layout -->
    <div v-if="!quizActive" class="quiz-menu" :class="quizMenuClass"
         @mouseleave="setHover('')">
      <div class="quiz-column left" @mouseenter="setHover('left')">
        <div class="content-overlay">
          <h1>{{ $t('quiz.imageHerbQuiz') }}</h1>
          <p class="quiz-description">{{ $t('quiz.imageHerbQuizDesc') }}</p>
          <RankingList />
          <button class="image-text-button" @click="startQuiz('imageHerb')">
            <img src="/button1.png" alt="Start Quiz" />
            <span>{{ $t('quiz.startQuiz') }}</span>
          </button>
        </div>
      </div>
      <div class="quiz-column right" @mouseenter="setHover('right')">
        <div class="content-overlay">
          <h1>{{ $t('quiz.prescriptionQuiz') }}</h1>
          <p class="quiz-description">{{ $t('quiz.prescriptionQuizDesc') }}</p>
          <PrescriptionRankingList />
          <button class="image-text-button" @click="startQuiz('prescription')">
            <img src="/button1.png" alt="Start Quiz" />
            <span>{{ $t('quiz.startQuiz') }}</span>
          </button>
        </div>
      </div>
      <!-- Language change hint -->
      <div class="language-hint">
        <small>{{ $t('quiz.languageChangeHint') }}</small>
      </div>
    </div>
    <!-- After starting the quiz, display the corresponding component and listen for the back event -->
    <div v-else class="quiz-container">
      <component :is="activeQuizComponent"
                 :key="route.params.lang"
                 @back="handleBack" />
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import ImageHerbQuiz from './ImageHerbQuiz.vue';
import PrescriptionQuiz from './PrescriptionQuiz.vue';
import ChatBot from "@/components/AI/ChatBot.vue";
import PrescriptionRankingList from "@/components/ranking/PrescriptionRankingList.vue";
import RankingList from "@/components/ranking/RankingList.vue";

export default {
  name: 'QuizPage',
  components: {
    RankingList,
    PrescriptionRankingList,
    ChatBot,
    ImageHerbQuiz,
    PrescriptionQuiz
  },
  setup() {
    const route = useRoute();
    // Whether the user has started the quiz state
    const quizActive = ref(false);
    // The currently loaded quiz component
    const activeQuizComponent = ref(null);

    const quizMenuClass = ref('');
    const setHover = (side) => {
      quizMenuClass.value = side ? `hover-${side}` : '';
    };

    // Start the corresponding quiz based on the selection
    const startQuiz = (quizType) => {
      if (quizType === 'imageHerb') {
        activeQuizComponent.value = ImageHerbQuiz;
      } else if (quizType === 'prescription') {
        activeQuizComponent.value = PrescriptionQuiz;
      }
      quizActive.value = true;
    };

    // Handle the "back" event sent from the child component
    const handleBack = () => {
      quizActive.value = false;
      activeQuizComponent.value = null;
    };

    return {
      route,
      quizActive,
      activeQuizComponent,
      startQuiz,
      handleBack,
      quizMenuClass,
      setHover
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Zhi+Mang+Xing&display=swap');
/* Set the page to occupy the entire screen */
.quiz-page {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* Menu page layout with two columns */
.quiz-menu {
  display: flex;
  height: 100%;
  position: relative;
}

.quiz-menu::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  width: 200%; /* Make it horizontally long enough */
  height: 2px; /* Transform it into a horizontal line */
  background: rgba(0, 0, 0, 0.3);
  transform: rotate(20deg) translate(-50%, 0); /* Rotate and center it */
  transform-origin: center;
  z-index: 2;
  pointer-events: none;
}

/* Each column takes up half the screen and sets a background image */
.quiz-column {
  flex: 1;
  position: relative;
  background-size: cover;
  background-position: center;
  transition: flex 0.4s ease, filter 0.4s ease, clip-path 0.4s ease;
}

/* Background image for the left column (change the URL below to your actual image address) */
.quiz-column.left {
  background-image: url('/herbQuiz.png');
  z-index: 1;
  mask-image: linear-gradient(to right, #ac915e 80%, transparent 100%);
  -webkit-mask-image: linear-gradient(to right, #ac915e 99%, transparent 100%);
}

/* Background image for the right column (change the URL below to your actual image address) */
.quiz-column.right {
  background-image: url('/preQuiz.png');
  z-index: 1;
  mask-image: linear-gradient(to left, #ac915e 80%, transparent 100%);
  -webkit-mask-image: linear-gradient(to left, #ac915e 99%, transparent 100%);
}

/* Content overlay layer to enhance text and button readability */
.content-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.2); /* Semi-transparent white background */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* Title styling */
.quiz-column h1 {
  margin-bottom: 20px;
  font-family: 'Zhi Mang Xing', cursive;
  font-size: 64px;
  color: #fff8dc; /* Bright beige for contrast with the brownish-yellow background */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6); /* Enhance readability */
}

.quiz-description {
  font-size: 18px;
  color: #fff8dc;
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  max-width: 80%;
}

.image-text-button {
  position: relative;
  background: none;
  border: none;
  padding: 0;
  margin-top: 20px;
  cursor: pointer;
  display: inline-block;
  transition: transform 0.2s ease;
}

.image-text-button img {
  display: block;
  width: 100%;
  height: auto;
  max-width: 200px;
}

.image-text-button span {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff8dc;
  font-size: 24px;
  font-weight: bold;
  font-family: 'Zhi Mang Xing', cursive;
  pointer-events: none;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
}

.image-text-button:hover {
  transform: scale(1.05);
}

/* Container styling during quiz state */
.quiz-container {
  height: 100%;
  overflow-y: auto;
}

.quiz-menu.hover-left .left {
  flex: 2;
  filter: brightness(1);
}

.quiz-menu.hover-left .right {
  flex: 1;
  filter: brightness(0.5);
}

.quiz-menu.hover-right .left {
  flex: 1;
  filter: brightness(0.5);
}

.quiz-menu.hover-right .right {
  flex: 2;
  filter: brightness(1);
}
.language-hint {
  position: absolute;
  bottom: 16px;
  width: 100%;
  text-align: center;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  z-index: 1;
}
</style>