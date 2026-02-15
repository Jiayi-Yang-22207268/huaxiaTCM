<template>
  <div class="admin-container">
    <h2>{{ t('admin.title') }}</h2>
    <nav class="admin-nav">
      <button @click="navigateTo('HerbManagement')">
        {{ t('admin.herbManagement') }}
      </button>
      <button @click="navigateTo('PrescriptionManagement')">
        {{ t('admin.prescriptionManagement') }}
      </button>
      <!-- Added: Homepage image management entry -->
      <button @click="navigateTo('HomepageManagement')">
        {{ t('admin.homepageManagement') }}
      </button>
      <button @click="navigateTo('UserManagement')">
        {{ t('admin.userManagement') }}
      </button>
      <button @click="navigateTo('LogManagement')">
        {{ t('admin.logManagement') }}
      </button>
    </nav>
    <div class="admin-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const route = useRoute()
const { t, locale } = useI18n()

const navigateTo = (childRouteName) => {
  router.push({ name: childRouteName, params: { lang: locale.value } })
}

// When accessing /:lang/admin, automatically redirect to the default child route
onMounted(() => {
  if (route.fullPath === `/${locale.value}/admin`) {
    router.push({ name: 'HerbManagement', params: { lang: locale.value } })
  }
})
</script>

<style scoped>
.admin-container {
  padding: 20px;
}
.admin-nav {
  margin-bottom: 20px;
}
.admin-nav button {
  margin-right: 10px;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>

