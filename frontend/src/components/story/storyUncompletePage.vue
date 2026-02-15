<template>
  <div class="background-only" @click="goBackHome">
    <div class="centered-text">{{ $t('story.Coming soon') }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      language: '', // Initialize
      backgroundPath: '', // Initialize as empty
    };
  },
  methods: {
    getImageUrl(imagePath) {
      const baseURL = window.location.origin.includes('localhost')
          ? 'http://localhost:5000'
          : window.location.origin;
      return `${baseURL}${imagePath}`;
    },
    setBackgroundImage(imageUrl) {
      document.documentElement.style.setProperty('--background-image', `url('${imageUrl}')`);
    },
    goBackHome() {
      this.$router.push({ name: 'Story', params: { lang: this.language } });
    },
    resolveBackground(storyId) {
      if (storyId === '2') {
        return '/static/Story/cabin.png';
      } else {
        return '/static/Story/discuss.png';
      }
    },
  },
  mounted() {
    const storyId = this.$route.params.storyId;
    console.log("11111111111",this.$route.params.storyId);
    const lang = this.$route.params.lang;
    this.language = lang;
    this.backgroundPath = this.resolveBackground(storyId);
    this.setBackgroundImage(this.getImageUrl(this.backgroundPath));
  },
};
</script>


<style scoped>
.background-only {
  position: fixed;
  width: 100vw;
  height: 100vh;
  background-image: var(--background-image);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.centered-text {
  font-size: 3rem;
  font-weight: bold;
  color: white;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
  animation:
      fadeInUp 1.5s ease-out forwards,
      breathing 3s ease-in-out infinite 2s;
  pointer-events: none;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes breathing {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.75;
    transform: scale(1.03);
  }
}

</style>
