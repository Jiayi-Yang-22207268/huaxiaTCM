<template>
  <div class="log-management-container">
    <h3 class="page-title">{{ t('admin.logManagement') }}</h3>

    <div class="controls">
      <button class="btn" @click="loadLogs">{{ t('admin.loadLogs') }}</button>
      <button class="btn" @click="exportLogs" :disabled="!accessLogs.length && !errorLogs.length">
        {{ t('admin.exportLogs') }}
      </button>
      <button class="btn" @click="loadStats">
        {{ t('admin.loadLogStats') }}
      </button>
    </div>

    <div class="stats-card">
      <LogStatsChart :stats="logStats" />
    </div>

    <div class="logs-grid">
      <div class="log-card" v-if="accessLogs.length">
        <h4>{{ t('admin.accessLogs') }}</h4>
        <ul class="log-list">
          <li v-for="(line, idx) in accessLogs" :key="'a' + idx">{{ line }}</li>
        </ul>
      </div>

      <div class="log-card" v-if="errorLogs.length">
        <h4>{{ t('admin.errorLogs') }}</h4>
        <ul class="log-list">
          <li v-for="(line, idx) in errorLogs" :key="'e' + idx">{{ line }}</li>
        </ul>
      </div>
    </div>

    <p v-if="!accessLogs.length && !errorLogs.length" class="no-logs-text">
      {{ t('admin.noLogs') }}
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { fetchLogs, fetchLogStats } from '@/api/admin/log.js';
import LogStatsChart from '@/components/generalComponents/LogStatsChart.vue';

const { t } = useI18n();
const accessLogs = ref([]);
const errorLogs = ref([]);
const logStats = ref({});

const loadLogs = async () => {
  const result = await fetchLogs();
  if (result) {
    accessLogs.value = result.access;
    errorLogs.value = result.error;
  } else {
    accessLogs.value = [];
    errorLogs.value = [];
  }
};

const exportLogs = () => {
  const content = [
    '=== Access Logs ===',
    ...accessLogs.value,
    '',
    '=== Error Logs ===',
    ...errorLogs.value
  ].join('\n');
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `server-log-${new Date().toISOString()}.txt`;
  link.click();
  URL.revokeObjectURL(link.href);
};

const loadStats = async () => {
  logStats.value = await fetchLogStats();
};

onMounted(() => {
  loadLogs();
  loadStats();
});
</script>

<style scoped>
/* Light mode */
.log-management-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: #333;
  background-color: #f9f9f9;
}

.page-title {
  font-size: 1.8rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  background-color: #ba5f39;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn:hover:not(:disabled) {
  background-color: #a0492e;
}

.stats-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.logs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.log-card {
  background: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-height: 400px;
  overflow-y: auto;
}

.log-card h4 {
  margin-bottom: 10px;
  font-size: 1.1rem;
  color: #555;
}

.log-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.log-list li {
  line-height: 1.6;
  font-family: monospace;
  font-size: 0.85rem;
  border-bottom: 1px solid #eee;
  padding: 4px 0;
}

.no-logs-text {
  text-align: center;
  color: #777;
  font-style: italic;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .log-management-container {
    color: #ddd;
    background-color: #1e1e1e;
  }
  .page-title {
    color: #fff;
  }
  .btn {
    background-color: #5a350d;
    color: #fff;
  }
  .btn:hover:not(:disabled) {
    background-color: #7a3f12;
  }
  .stats-card,
  .log-card {
    background: #2a2a2a;
    box-shadow: 0 2px 8px rgba(0,0,0,0.5);
  }
  .log-card h4 {
    color: #ccc;
  }
  .log-list li {
    color: #ccc;
    border-bottom: 1px solid #333;
  }
  .no-logs-text {
    color: #aaa;
  }
}
</style>

