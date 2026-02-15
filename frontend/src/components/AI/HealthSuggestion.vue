<template>
  <div>
    <!-- Not logged-in state -->
    <div v-if="!user">
      <p>{{ $t('suggestion.loginPrompt') }}</p>
    </div>
    <!-- Logged-in state, displaying health suggestions retrieved from the backend -->
    <div v-else>
      <p>{{ $t('suggestion.healthSuggestionLabel') }}：{{ suggestion }}</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getHealthSuggestion } from '@/api/ai/healthTip.js';
import { useAuthStore } from '@/stores/authStore.js';
import { useI18n } from 'vue-i18n';

export default {
  name: 'HealthSuggestion',
  setup() {
    // Get user information from Pinia (note that useAuthStore must be called within the component)
    const authStore = useAuthStore();
    const user = authStore.user;
    const suggestion = ref('');

    // Get route and i18n information
    const route = useRoute();
    const { t, locale } = useI18n();

    // Retrieve the lang parameter from the route, default to 'zh'
    const currentLang = ref(route.params.lang || 'zh');
    console.log('Initial language:', currentLang.value);

    // Define the function to request health suggestions
    const fetchSuggestion = async () => {
      if (!user) return;
      const currentMonth = new Date().getMonth() + 1;
      const params = {
        month: currentMonth,
        username: user.username,
        age: user.age,
        weight: user.weight,
        height: user.height,
        lang: currentLang.value
      };
      console.log('Fetching suggestion with params:', params);
      try {
        const res = await getHealthSuggestion(params);
        console.log('API response:', res.data);
        suggestion.value = res.data.suggestion;
      } catch (error) {
        console.error('Error fetching suggestion:', error);
        suggestion.value = t('suggestion.fetchError');
      }
    };

    // Call the API when the page loads
    onMounted(() => {
      fetchSuggestion();
    });

    // Watch for language changes and reload data
    watch(() => route.params.lang, async () => {
      currentLang.value = route.params.lang;
      console.log(currentLang.value);
      await fetchSuggestion();
    });

    return {
      user,
      suggestion,
      t
    };
  }
};
</script>

<style scoped>
p {
  font-size: 16px;
  line-height: 1.5;
}
</style>
