<script setup>
import { ref, onMounted, watch } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { fetchHerbArea } from '/src/api/Map/map.js'; // API method to fetch herb production area data
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';

const route = useRoute();
const { t } = useI18n();
const errorMessage = ref('');
const loading = ref(true); // Controls loading state
let map;
let polygonLayers = [];

// Accepts `herbId` passed from the parent component via props
const props = defineProps({
  herbId: {
    type: Number,
    required: true
  }
});

// Method to load map data
const loadHerbArea = async () => {
  loading.value = true;
  errorMessage.value = '';

  // If the map is already initialized, clear existing polygon layers
  polygonLayers.forEach(layer => map.removeLayer(layer));
  polygonLayers = [];

  // Request API to fetch herb production area data
  const data = await fetchHerbArea(props.herbId, route.params.lang);
  console.log("Fetched area data:", data);

  if (data && data.areas && data.areas.length > 0) {
    // Use `featureGroup` to collect all polygons
    const group = L.featureGroup();

    data.areas.forEach(area => {
      const polygonLayer = L.polygon(area.coordinates, {
        color: '#BA5F39',
        fillColor: '#BA5F39',
        fillOpacity: 0.3,
      }).addTo(map);
      polygonLayers.push(polygonLayer);
      group.addLayer(polygonLayer);
    });

    // FitBounds to the overall boundary of all polygons at once, with padding and a max zoom level
    map.fitBounds(group.getBounds(), {
      padding: [40, 40],
      maxZoom: 10
    });

    errorMessage.value = '';
  } else {
    errorMessage.value = t('map.noData'); // Support for internationalization
  }

  loading.value = false;
};

// Initialize the map after the component is mounted
onMounted(() => {
  map = L.map('herb-map').setView([39.8768, 116.4770], 5);
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, HERE, Garmin, USGS, Intermap…'
  }).addTo(map);

  loadHerbArea();
});

// Watch for language changes and reload map data accordingly
watch(() => route.params.lang, async () => {
  await loadHerbArea();
});
</script>

<template>
  <div>
    <!-- Map Container -->
    <div id="herb-map-container">
      <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner"></div>
        <p>{{ $t('loading') }}</p>
      </div>
      <div id="herb-map"></div>
    </div>
    <!-- Error message display -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<style scoped>
#herb-map-container {
  position: relative;
  width: 100%;
  height: 500px;
}

#herb-map {
  width: 100%;
  height: 100%;
}

/* Loading animation styles */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
  font-weight: bold;
}

/* Rotation animation */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

