<template>
  <div class="chart-container" v-if="hasData">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import 'chart.js/auto'      // Automatically register all components
import { Bar } from 'vue-chartjs'

const props = defineProps({
  stats: { type: Object, required: true }
})

const labels = computed(() => Object.keys(props.stats))
const values = computed(() => Object.values(props.stats))
const hasData = computed(() => labels.value.length > 0)

const chartData = computed(() => ({
  labels: labels.value,
  datasets: [{
    label: 'URL 访问次数',
    data: values.value,
    backgroundColor: '#ba5f39'
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: { ticks: { autoSkip: false } },
    y: { beginAtZero: true }
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
  margin-top: 20px;
}
</style>

