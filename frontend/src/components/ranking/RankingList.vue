<template>
  <div class="ranking-list">
    <h2>{{ $t('ranking.title') }}</h2>
    <ul v-if="rankingData.length">
      <li v-for="(user, index) in rankingData" :key="user.username">
        <img :src="user.avatar" alt="avatar" class="avatar" />
        <span class="rank">{{ index + 1 }}</span>
        <span class="username">{{ user.username }}</span>
        <span class="accuracy">
          {{ $t('ranking.accuracyLabel') }}: {{ user.accuracy }}%
        </span>
        <span class="score">
          {{ $t('ranking.scoreLabel') }}: {{ user.score }}
        </span>
      </li>
    </ul>
    <p v-else>
      {{ $t('ranking.noData') }}
    </p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { fetchRankingData } from '@/api/tcm/ranking.js';

export default {
  name: 'RankingList',
  setup() {
    const rankingData = ref([]);

    const loadRanking = async () => {
      rankingData.value = await fetchRankingData();
    };

    onMounted(loadRanking);

    return {
      rankingData
    };
  }
};
</script>

<style scoped>
/* Default (Light Mode) */
.ranking-list {
  width: 100%;
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: rgba(172, 145, 94, 0.7); /* Default transparency */
  color: #333; /* Default text color */
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 8px;
}
/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .ranking-list {
    background-color: rgba(172, 145, 94, 0.7); /* Transparency in dark mode */
    color: #fff; /* Make text white to improve contrast */
  }
  li {
    border-bottom: 1px solid rgba(255, 255, 255, 0.2); /* Adjust border color for dark mode */
  }
}
h2 {
  text-align: center;
  margin-bottom: 10px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}
.rank {
  font-weight: bold;
  color: #ff9800;
}
.username {
  flex: 1;
  text-align: center;
}
.accuracy {
  font-weight: bold;
}
</style>
