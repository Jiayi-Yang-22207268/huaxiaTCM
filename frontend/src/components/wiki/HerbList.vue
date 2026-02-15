<template>
  <ChatBot />
  <div class="herb-list">
    <h1>{{ $t('herbs.title') }}</h1>
    <!-- Category Sidebar -->
    <div class="category-sidebar">
      <ul>
        <li
            v-for="name in groupNames"
            :key="name"
            @click="scrollToGroup(name)"
            class="category-item"
        >
          {{ name }}
        </li>
      </ul>
    </div>
    <!-- Toggle Display Mode Button -->
    <button @click="toggleDisplayMode" class="toggle-mode-btn">
      {{ isClassificationMode
        ? $t('herbs.ClassificationMode')
        : $t('herbs.CategoryMode') }}
    </button>
    <!-- Search Bar -->
    <div class="search-bar">
      <input
          type="text"
          v-model="searchQuery"
          :placeholder="$t('herbs.searchPlaceholder')"
          class="search-input"
          @keyup.enter="searchHerbs"
      />
      <button
          v-if="searchQuery"
          @click="clearSearch"
          class="clear-btn"
          title="Clear search"
      >×</button>
      <button @click="searchHerbs" class="search-btn">
        {{ $t('herbs.search') }}
      </button>
    </div>
    <!-- Search Results Section -->
    <div v-if="searchPerformed">
      <div class="group">
        <h2 class="group-title">{{ $t('herbs.searchResults') }}</h2>
        <div class="herb-grid">
          <div
              v-for="herb in searchResults"
              :key="herb.id"
              class="herb-item"
              @mouseenter="loadImage(herb.id, herb.image)"
              @click="viewHerbDetail(herb.id)"
          >
            <img
                v-if="loadedImages[herb.id]"
                :src="loadedImages[herb.id]"
                alt="herb image"
                class="herb-image"
                :style="{ borderColor: herb.color }"
            />
            <div
                class="icon"
                :style="{ backgroundColor: herb.color }"
            >
              {{ herb.name[0] }}
            </div>
            <div class="name">{{ herb.name }}</div>
          </div>
        </div>
      </div>
    </div>
    <!-- Lazy Loading Section for Groups -->
    <div v-else>
      <div
          v-for="groupName in groupNames"
          :key="groupName"
          class="group"
          v-intersect:[groupName]="loadGroup"
      >
        <h2 class="group-title" :id="`group-${groupName}`">
          {{ groupName }}
        </h2>
        <div v-if="!herbsByGroup[groupName]" class="loading">
          加载中…
        </div>
        <div v-else class="herb-grid">
          <div
              v-for="herb in herbsByGroup[groupName]"
              :key="herb.id"
              class="herb-item"
              @mouseenter="loadImage(herb.id, herb.image)"
              @click="viewHerbDetail(herb.id)"
          >
            <img
                v-if="loadedImages[herb.id]"
                :src="loadedImages[herb.id]"
                alt="herb image"
                class="herb-image"
                :style="{ borderColor: herb.color }"
            />
            <div
                class="icon"
                :style="{ backgroundColor: herb.color }"
            >
              {{ herb.name[0] }}
            </div>
            <div class="name">{{ herb.name }}</div>
          </div>
        </div>
      </div>
    </div>
    <!-- No Results Hint -->
    <p v-if="groupNames.length === 0 && !searchPerformed">
      {{ $t('herbs.noResults') }}
    </p>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick, watch } from 'vue';
import { useRoute } from 'vue-router';
import {
  getHerbCategories,
  getHerbClassifications,
  getHerbsByCategory,
  getHerbsByClassification,
  searchHerbsByName
} from '@/api/tcm/herbwiki.js';
import ChatBot from '@/components/AI/ChatBot.vue';
import router from '@/router.js';

// Intersection Observer directive
const intersectDirective = {
  mounted(el, binding) {
    const loadFn = binding.value;
    const groupName = binding.arg;
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          loadFn(groupName);
          observer.unobserve(entry.target);
        }
      }
    }, { rootMargin: '200px' });
    observer.observe(el);
  }
};

export default {
  components: { ChatBot },
  directives: { intersect: intersectDirective },

  setup() {
    const route = useRoute();
    const groupNames = ref([]);
    const herbsByGroup = reactive({});
    const loadedImages = reactive({});
    const isClassificationMode = ref(false);

    // Search state
    const searchQuery = ref('');
    const searchResults = ref([]);
    const searchPerformed = ref(false);

    // Toggle between group/classification mode
    const toggleDisplayMode = async () => {
      isClassificationMode.value = !isClassificationMode.value;
      groupNames.value = [];
      Object.keys(herbsByGroup).forEach(k => delete herbsByGroup[k]);
      await loadGroupNames();
    };

    // Load group names
    const loadGroupNames = async () => {
      groupNames.value = isClassificationMode.value
          ? await getHerbClassifications(route.params.lang)
          : await getHerbCategories(route.params.lang);
      await nextTick();
    };

    // Lazy load a single group
    const loadGroup = async (groupName) => {
      if (herbsByGroup[groupName]) return;
      const fetcher = isClassificationMode.value
          ? getHerbsByClassification
          : getHerbsByCategory;
      const herbs = await fetcher(groupName, route.params.lang);
      const groupColor = getGroupColor(groupName);
      herbs.forEach(h => h.color = groupColor);
      herbsByGroup[groupName] = herbs;
    };

    // Generate fixed group colors
    const getGroupColor = (groupName) => {
      let hash = 0;
      for (let i = 0; i < groupName.length; i++) {
        hash = groupName.charCodeAt(i) + ((hash << 5) - hash);
      }
      return `hsl(${hash % 360},60%,80%)`;
    };

    // Load images on hover
    const loadImage = (id, url) => {
      if (!loadedImages[id]) loadedImages[id] = url;
    };

    // Navigate to details & scroll
    const viewHerbDetail = id => router.push(`/${route.params.lang}/herbs/${id}`);
    const scrollToGroup = name => {
      const el = document.getElementById(`group-${name}`);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    // —— Search logic: Load all groups first, then assign colors ——
    const searchHerbs = async () => {
      if (!searchQuery.value.trim()) return;
      // 1) Search results
      const results = await searchHerbsByName(searchQuery.value, route.params.lang);
      // 2) Ensure all groups are loaded
      await Promise.all(groupNames.value.map(g => loadGroup(g)));
      // 3) Find the group each herb belongs to and assign color
      results.forEach(h => {
        const grp = Object.entries(herbsByGroup)
            .find(([_, herbs]) => herbs.some(x => x.id === h.id))?.[0];
        h.color = getGroupColor(grp || h.name);
      });
      searchResults.value = results;
      searchPerformed.value = true;
    };

    const clearSearch = () => {
      searchQuery.value = '';
      searchResults.value = [];
      searchPerformed.value = false;
    };

    onMounted(loadGroupNames);
    watch(() => route.params.lang, async () => {
      await loadGroupNames();
      if (searchPerformed.value) {
        await searchHerbs();
      }
    });

    return {
      groupNames,
      herbsByGroup,
      loadedImages,
      isClassificationMode,
      toggleDisplayMode,
      loadGroup,
      loadImage,
      viewHerbDetail,
      scrollToGroup,
      searchQuery,
      searchResults,
      searchPerformed,
      searchHerbs,
      clearSearch
    };
  }
};
</script>

<style scoped>
@import "../../assets/css/component.css";

/* Define default (light mode) variables */
.herb-list {
  padding: 20px;
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
  width: 1000px;
  margin: 0 auto;
  --card-bg: #ffffff;
}

/* Light/Dark mode switch */
@media (prefers-color-scheme: dark) {
  .herb-list {
    --bg: #121212;
    --text: #e0e0e0;
    --card-bg: #1f1f1f;
  }
}

/* Toggle category button */
.toggle-mode-btn {
  margin-bottom: 15px;
  padding: 8px 15px;
  background-color: var(--accent, #ba5f39);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.95rem;
}

.toggle-mode-btn:hover {
  background-color: #9c4a2d;
}

/* Search bar */
.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}

.search-input {
  width: 280px;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  background: var(--card-bg);
  color: var(--text);
}

.search-btn {
  padding: 8px 16px;
  background-color: var(--accent, #ba5f39);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.search-btn:hover {
  background-color: #9c4a2d;
}

/* Group title */
.group {
  margin-bottom: 32px;
}

.group-title {
  font-size: 1.3rem;
  margin: 16px 0 8px;
  border-left: 4px solid var(--accent, #ba5f39);
  padding-left: 8px;
  color: var(--text);
}

/* Card grid */
.herb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

/* Single card */
.herb-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease, height 0.3s ease;
  color: var(--text);
  position: relative;
  overflow: hidden;
  height: 60px; /* Set initial height */
}

.herb-item:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  height: 160px; /* Expand to show the full image */
  align-items: flex-end; /* Push text to bottom */
  padding: 12px;
}

.herb-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 8px;
}

.herb-item:hover .herb-image {
  opacity: 1;
}

/* Keep only position/z-index, remove background-related styles */
.icon, .name {
  position: relative;
  z-index: 1;
}

/* Initial letter badge */
/* Initial letter badge without background, remains unchanged */
.icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-weight: bold;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #494949;
}

/* Herb name */
/* Herb name, default without background */
.name {
  flex: 1;
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.herb-item:hover .name {
  background: rgba(0, 0, 0, 0.7);
  border-radius: 4px;
  padding: 6px 10px;
  white-space: normal;
  overflow: visible;
  text-overflow: initial;
  word-break: break-word;
  text-align: center;
  color: #ffffff; /* Add this line to make text bright */
}

/* Category sidebar */
.category-sidebar {
  position: fixed;
  top: 120px;
  left: 100px;
  width: 150px;
  height: 500px; /* Fixed height */
  overflow-y: auto; /* Enable vertical scrolling */
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

}

.category-sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-item {
  padding: 8px 12px;
  margin-bottom: 8px;
  background-color: var(--card-bg);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  text-align: center;
  transition: background 0.2s;
}

.category-item:hover {
  background-color: #ba5f39;
  color: white;
}

/* Custom scrollbar styles for dark mode */
@media (prefers-color-scheme: dark) {
  .category-sidebar::-webkit-scrollbar {
    width: 8px;
  }

  .category-sidebar::-webkit-scrollbar-track {
    background: transparent;
  }

  .category-sidebar::-webkit-scrollbar-thumb {
    background-color: #666;
    border-radius: 4px;
  }

  .category-sidebar {
    scrollbar-color: #666 transparent;
  }
}

/* Clear button */
.clear-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--text);
  padding: 4px;
}

.clear-btn:hover {
  color: #ba5f39;
}

</style>
