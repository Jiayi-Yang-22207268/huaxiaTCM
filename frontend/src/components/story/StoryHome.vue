<template>
  <div class="carousel-container">
    <!-- Left and right navigation -->
    <div class="click-zone left-zone" @click="prevSlide">
      <div class="arrow-indicator left-arrow">‹</div>
    </div>
    <div class="click-zone right-zone" @click="nextSlide">
      <div class="arrow-indicator right-arrow">›</div>
    </div>
    <!-- Story card container -->
    <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
      <div
          v-for="(story, idx) in stories"
          :key="idx"
          class="carousel-slide"
          :style="{ backgroundImage: `url(${story.bg})` }"
          @click="enterStory(story.id)"
      >
        <div class="overlay"></div>
        <div class="story-info" :key="currentIndex">
          <h2 class="story-title">{{ stories[currentIndex].name }}</h2>
          <p class="story-prompt blink">{{ $t('story.prompt') }}</p>
        </div>
      </div>
    </div>
    <!-- Dot indicators -->
    <div class="dot-indicator">
      <span
          v-for="(story, idx) in stories"
          :key="'dot-' + idx"
          :class="{ dot: true, active: currentIndex === idx }"
          @click="goToSlide(idx)"
      ></span>
    </div>
    <!-- Left and right click zones, hide button UI, retain click functionality -->
    <div class="click-zone left-zone" @click="prevSlide"></div>
    <div class="click-zone right-zone" @click="nextSlide"></div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      currentIndex: 0,
    };
  },
  computed: {
    stories() {
      return [
        {
          id: 1,
          name: this.$t('story.huoxiang'),
          bg: this.getImageUrl('/static/Story/bg_storm.jpg'),
        },
        {
          id: 2,
          name: this.$t('story.lingzhi'),
          bg: this.getImageUrl('/static/Story/cabin_light.png'),
        },
        {
          id: 3,
          name: this.$t('story.herbheart'),
          bg: this.getImageUrl('/static/Story/discuss.png'),
        },
      ];
    }
  },
  methods: {
    enterStory(storyId) {
      if (storyId === 1) {
        this.$router.push({
          name: 'story1',
          params: {
            storyId,
            lang: this.$route.params.lang,
          },
        });
      } else {
        this.$router.push({
          name: 'storyUncompletePage',
          params: {
            storyId,
            lang: this.$route.params.lang,
          },
        });
      }
    },
    getImageUrl(imagePath) {
      const baseURL = window.location.origin.includes('localhost')
          ? 'http://localhost:5000'
          : window.location.origin;
      return `${baseURL}${imagePath}`;
    },
    nextSlide() {
      if (this.currentIndex < this.stories.length - 1) {
        this.currentIndex++;
      } else {
        this.currentIndex = 0;
      }
    },
    prevSlide() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      } else {
        this.currentIndex = this.stories.length - 1;
      }
    },
    goToSlide(idx) {
      this.currentIndex = idx;
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500&display=swap');

.carousel-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: #111;
}

.carousel-track {
  display: flex;
  transition: transform 0.6s ease-in-out;
  height: 100%;
}

.carousel-slide {
  min-width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(4px) brightness(0.6);
  background: rgba(0, 0, 0, 0.3);
  z-index: 1;
}

@keyframes fadeInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.story-info {
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.1);
  padding: 30px;
  border-radius: 16px;
  backdrop-filter: blur(6px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
  max-width: 70%;
  text-align: center;
  color: white;
  font-family: 'Noto Serif SC', serif;
  animation: fadeInUp 0.9s ease-out;
}

/* More precise control over the animation delay for titles and text */
.story-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  opacity: 0;
  animation: fadeInUp 0.9s ease-out 0.3s forwards;
}

@keyframes slowBlink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

.blink {
  animation: slowBlink 2.5s ease-in-out infinite;
}


.story-prompt {
  font-size: 1.1rem;
  opacity: 0;
  animation: fadeInUp 0.9s ease-out 0.6s forwards;
}


.click-zone {
  position: absolute;
  top: 0;
  width: 40%;
  height: 100%;
  z-index: 8;
}

.left-zone {
  left: 0;
}

.right-zone {
  right: 0;
}


.arrow-indicator {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.6);
  transition: color 0.3s ease;
  pointer-events: none; /* Does not affect the clickable area */
  user-select: none;
}

.left-arrow {
  left: 80px;
}

.right-arrow {
  right: 80px;
}

.click-zone:hover .arrow-indicator {
  color: #fff;
}


.dot-indicator {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  z-index: 5;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}
.dot.active {
  background-color: #ffa45c;
  transform: scale(1.3);
}
</style>
