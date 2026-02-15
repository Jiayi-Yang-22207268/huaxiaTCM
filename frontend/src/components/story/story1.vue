<template>
  <div class="story-container">
    <!-- Character portrait displayed in the center -->
    <div class="character-portrait" v-if="currentStory.character_image?.length">
      <img :src="getImageUrl(currentStory.character_image[0])" alt="Character" />
    </div>
    <!-- Button to return to the homepage -->
    <div class="back-button">
      <button @click="goBackHome">{{ $t('story.back_to_home') }}</button>
    </div>

    <!-- Dialog box (click to skip typing or move to the next segment) -->
    <div class="story-dialog-box" @click="handleDialogClick">
      <p><strong>{{ currentStory.speaker }}</strong></p>
      <p class="typewriter">{{ displayedDialog }}</p>
    </div>
    <!-- Option buttons -->
    <div
        class="choices"
        v-if="!isTyping && currentStory.choices?.length && showChoicesNormally"
    >
      <button
          v-for="(choice, index) in currentStory.choices"
          :key="index"
          @click="handleChoice(index)"
      >
        {{ choice }}
      </button>
    </div>
    <!-- Play audio -->
    <audio v-if="currentStory.audio" :src="currentStory.audio" autoplay></audio>
    <!-- Loading indicator -->
    <div v-if="isLoading"></div>
  </div>
</template>

<script>
import { fetchStoryData, handlePlayerChoice } from '@/api/tcm/story.js';
import { useI18n } from 'vue-i18n';

export default {
  data() {
    return {
      currentStory: {},
      currentStoryId: 1,
      isLoading: true,
      displayedDialog: '',
      typewriterTimer: null,
      isTyping: false
    };
  },
  mounted() {
    this.loadStory(this.currentStoryId);
  },
  watch: {
    // Watch for language switching
    '$i18n.locale'(newLang) {
      this.loadStory(this.currentStoryId);
    }
  },
  computed: {
    // Use i18n's locale to control language logic
    language() {
      return this.$i18n.locale;
    },
    showChoicesNormally() {
      // If there are options, and at least one is not "继续" or "Continue", show the button
      return this.currentStory.choices?.some(
          text => text.trim().toLowerCase() !== '继续' && text.trim().toLowerCase() !== 'continue'
      );
    }
  },
  methods: {
    async loadStory(storyId) {
      this.isLoading = true;
      const storyData = await fetchStoryData(storyId);
      if (storyData) {
        this.currentStory = {
          ...storyData,
          speaker: this.language === 'en' ? storyData.speaker_en : storyData.speaker,
          dialog: this.language === 'en' ? storyData.dialog_en : storyData.dialog,
          choices: this.language === 'en' ? storyData.choices_en : storyData.choices,
          character_image: Array.isArray(storyData.character_image)
              ? storyData.character_image
              : storyData.character_image ? [storyData.character_image] : []
        };
        this.setBackgroundImage(this.getImageUrl(storyData.background));
        this.animateTypewriter(this.currentStory.dialog);
        this.isLoading = false;
      } else {
        console.error('加载剧情失败');
      }
    },
    async handleChoice(optionIndex) {
      const nextStoryData = await handlePlayerChoice(this.currentStoryId, optionIndex);
      if (nextStoryData) {
        this.currentStoryId = nextStoryData.id;
        this.loadStory(this.currentStoryId);
      }
    },
    getImageUrl(imagePath) {
      const baseURL = window.location.origin.includes('localhost')
          ? 'http://localhost:5000'
          : window.location.origin;
      return `${baseURL}${imagePath}`;
    },
    setBackgroundImage(imageUrl) {
      document.documentElement.style.setProperty('--background-image', `url('${imageUrl}')`);
    },
    animateTypewriter(text) {
      clearInterval(this.typewriterTimer);
      this.displayedDialog = '';
      this.isTyping = true;
      let index = 0;
      this.typewriterTimer = setInterval(() => {
        if (index < text.length) {
          this.displayedDialog += text[index++];
        } else {
          clearInterval(this.typewriterTimer);
          this.isTyping = false;
        }
      }, 40);
    },
    handleDialogClick() {
      if (this.isTyping) {
        clearInterval(this.typewriterTimer);
        this.displayedDialog = this.currentStory.dialog;
        this.isTyping = false;
      } else if (
          !this.currentStory.choices?.length ||
          !this.showChoicesNormally // When all options are "继续" or "continue"
      ) {
        this.handleChoice(0);
      }
    },
    goBackHome() {
      this.$router.push({ name: 'Story', params: { lang: this.language } });
    }
  }
};
</script>


<style scoped>
.typewriter {
  white-space: pre-wrap;
  overflow-wrap: break-word;
  caret-color: transparent; /* Hide the cursor insertion point */
}

.story-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 100px;
  box-sizing: border-box;
  color: white;
  z-index: 1;
}

/* Background fills the screen */
.story-container::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background-image: var(--background-image);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
  transition: background-image 0.3s ease;
}

/* Language buttons */
.language-selector {
  position: fixed;
  top: 30px;
  right: 30px;
  z-index: 10;
}

.language-selector button {
  padding: 10px 18px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.language-selector button:hover {
  background-color: #45a049;
}

.story-dialog-box {
  position: fixed;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.6);
  width: 100%;
  height: 160px;
  max-width: 960px;
  padding: 24px 36px;
  border-radius: 12px 12px 0 0;
  font-size: 20px;
  line-height: 1.8;
  user-select: none;
  cursor: pointer;
  box-shadow: 0 -5px 12px rgba(0, 0, 0, 0.4);
  z-index: 2;
}

.story-dialog-box:hover {
  background: rgba(0, 0, 0, 0.7);
}

.typewriter {
  white-space: pre-wrap;
  overflow-wrap: break-word;
}

/* Option container positioned near the bottom */
.choices {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  z-index: 2;
}

/* Option button styles */
.choices button {
  padding: 12px 24px;
  font-size: 16px;
  background-color: rgba(255, 165, 0, 0.7); /* Semi-transparent orange */
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  backdrop-filter: blur(4px);
  transition: background 0.3s;
}

.choices button:hover {
  background-color: rgba(255, 140, 0, 0.9);
}

/* Modify the language switch button styles */
.language-selector button {
  padding: 10px 18px;
  font-size: 16px;
  background-color: rgba(255, 165, 0, 0.7); /* Semi-transparent orange */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  backdrop-filter: blur(4px);
}

.language-selector button:hover {
  background-color: rgba(255, 140, 0, 0.9);
}

.character-portrait {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -60%);
  z-index: 1;
  pointer-events: none;
  user-select: none;
  caret-color: transparent;
}

.character-portrait:focus {
  outline: none;
}

.character-portrait img {
  height: 60vh;
  max-width: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 10px rgba(0,0,0,0.3));
}

.back-button {
  position: fixed;
  top: 30px;
  left: 30px;
  z-index: 10;
}

.back-button button {
  padding: 10px 18px;
  font-size: 16px;
  background-color: rgba(255, 165, 0, 0.7); /* Semi-transparent orange */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  backdrop-filter: blur(4px);
}

.back-button button:hover {
  background-color: rgba(255, 140, 0, 0.9);
}


</style>
