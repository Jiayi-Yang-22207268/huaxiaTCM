<template>
  <div class="admin-herb-list">
    <h1>{{ $t('herbs.title') }}</h1>

    <!-- Search mode toggle button -->
    <button @click="toggleSearchMode" class="toggle-mode-btn">
      {{ isSearchMode ? $t('herbs.backToCategory') : $t('herbs.enterSearchMode') }}
    </button>

    <!-- Group display mode toggle button, only shown in non-search mode -->
    <button @click="toggleDisplayMode" class="toggle-mode-btn" v-if="!isSearchMode">
      {{ isClassificationMode ? $t('herbs.ClassificationMode') : $t('herbs.CategoryMode') }}
    </button>

    <!-- Search mode -->
    <div v-if="isSearchMode" class="search-mode">
      <input
        type="text"
        v-model="searchQuery"
        :placeholder="$t('herbs.searchPlaceholder')"
        class="search-input"
      />
      <button @click="searchHerbs" class="search-btn">{{ $t('herbs.search') }}</button>
      <!-- Search results -->
      <ul v-if="searchResults.length > 0" class="herb-items">
        <li
          v-for="herb in searchResults"
          :key="herb.id"
          class="herb-item"
          @click="openDetailModal(herb.id)"
        >
          <span>{{ herb.name }}</span>
        </li>
      </ul>
      <p v-else-if="searchPerformed">{{ $t('herbs.noResults') }}</p>
    </div>
    <!-- Group display mode -->
    <div v-else>
      <!-- Group navigation -->
      <div class="groups">
        <button
          v-for="group in groups"
          :key="group"
          @click="selectGroup(group)"
          :class="{ active: group === selectedGroup }"
        >
          {{ group }}
        </button>
      </div>
      <!-- Herb list for the current group -->
      <ul class="herb-items">
        <li
          v-for="herb in herbs"
          :key="herb.id"
          class="herb-item"
          @click="openDetailModal(herb.id)"
        >
          <span>{{ herb.name }}</span>
        </li>
      </ul>
    </div>
    <!-- Floating add button -->
    <button class="floating-add-btn" @click="openAddModal">
      +
    </button>
    <!-- Herb detail/edit/add modal -->
    <div v-if="showDetailModal" class="modal">
      <div class="modal-content detail-modal">
        <button class="close-btn" @click="closeDetailModal">×</button>
        <div v-if="(herbDetail && !isAdding) || isAdding">
          <div v-if="!editMode">
            <!-- Read-only detail display -->
            <h2>{{ herbDetail.id ? herbDetail.id + ' / ' : '' }}{{ herbDetail.name_zh }} / {{ herbDetail.name_en }}</h2>
            <div class="images">
              <img :src="herbDetail.image_zh" :alt="herbDetail.name_zh" class="herb-image" v-if="herbDetail.image_zh" />
              <img :src="herbDetail.image_en" :alt="herbDetail.name_en" class="herb-image" v-if="herbDetail.image_en" />
            </div>
            <p>
              <strong>{{ $t('herb.category') }}：</strong>
              {{ herbDetail.category_zh || $t('herb.noData') }} / {{ herbDetail.category_en || $t('herb.noData') }}
            </p>
            <p>
              <strong>{{ $t('herb.origin') }}：</strong>
              {{ herbDetail.origin_zh || $t('herb.noData') }} / {{ herbDetail.origin_en || $t('herb.noData') }}
            </p>
            <p>
              <strong>{{ $t('herb.production_regions') }}：</strong>
              {{ herbDetail.production_regions_zh || $t('herb.noData') }} / {{ herbDetail.production_regions_en || $t('herb.noData') }}
            </p>
            <p>
              <strong>{{ $t('herb.properties') }}：</strong>
              {{ herbDetail.properties_zh || $t('herb.noData') }} / {{ herbDetail.properties_en || $t('herb.noData') }}
            </p>
            <p>
              <strong>{{ $t('herb.functions') }}：</strong>
              {{ herbDetail.functions_zh || $t('herb.noData') }} / {{ herbDetail.functions_en || $t('herb.noData') }}
            </p>
            <p>
              <strong>{{ $t('herb.classification') }}：</strong>
              {{ herbDetail.classification_zh || $t('herb.noData') }} / {{ herbDetail.classification_en || $t('herb.noData') }}
            </p>
            <!-- Edit and delete buttons -->
            <button class="edit-btn" @click="enterEditMode">{{ $t('herbs.edit') }}</button>
            <button class="delete-btn" @click="deleteHerb">{{ $t('herbs.delete') }}</button>
          </div>
          <div v-else>
            <!-- Edit/add form -->
            <h2>{{ isAdding ? $t('herbs.addNew') : $t('herbs.editInfo') }}</h2>
            <!-- ID is implicitly passed, not displayed in the form -->
            <div class="form-group">
              <label>{{ $t('herb.name_zh') }}：</label>
              <input type="text" v-model="editData.name_zh" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.name_en') }}：</label>
              <input type="text" v-model="editData.name_en" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.image_zh') }}：</label>
              <input type="text" v-model="editData.image_zh" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.image_en') }}：</label>
              <input type="text" v-model="editData.image_en" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.category') }} (ZH)：</label>
              <input type="text" v-model="editData.category_zh" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.category') }} (EN)：</label>
              <input type="text" v-model="editData.category_en" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.origin') }} (ZH)：</label>
              <input type="text" v-model="editData.origin_zh" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.origin') }} (EN)：</label>
              <input type="text" v-model="editData.origin_en" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.production_regions') }} (ZH)：</label>
              <input type="text" v-model="editData.production_regions_zh" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.production_regions') }} (EN)：</label>
              <input type="text" v-model="editData.production_regions_en" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.properties') }} (ZH)：</label>
              <input type="text" v-model="editData.properties_zh" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.properties') }} (EN)：</label>
              <input type="text" v-model="editData.properties_en" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.functions') }} (ZH)：</label>
              <input type="text" v-model="editData.functions_zh" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.functions') }} (EN)：</label>
              <input type="text" v-model="editData.functions_en" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.classification') }} (ZH)：</label>
              <input type="text" v-model="editData.classification_zh" />
            </div>
            <div class="form-group">
              <label>{{ $t('herb.classification') }} (EN)：</label>
              <input type="text" v-model="editData.classification_en" />
            </div>
            <!-- Save and cancel buttons -->
            <div class="form-actions">
              <button class="save-btn" @click="saveEdit">{{ $t('herbs.save') }}</button>
              <button class="cancel-btn" @click="cancelEdit">{{ $t('herbs.cancel') }}</button>
            </div>
          </div>
        </div>
        <div v-else>
          <p>{{ $t('loading') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n'
import {
  getHerbCategories,
  getHerbClassifications,
  getHerbsByCategory,
  getHerbsByClassification,
  searchHerbsByName,
  getHerbDetailAdmin,
  updateHerbDetailAdmin,
  addHerbDetailAdmin,
  deleteHerbDetailAdmin
} from '@/api/tcm/herbwiki';

export default {
  setup() {
    const route = useRoute();
    const { t } = useI18n();

    // Group and list data
    const groups = ref([]);
    const selectedGroup = ref('');
    const herbs = ref([]);

    // Search mode-related
    const isSearchMode = ref(false);
    const searchQuery = ref('');
    const searchResults = ref([]);
    const searchPerformed = ref(false);

    // Grouping method: false for default by category, true for taste classification
    const isClassificationMode = ref(false);

    // Herb detail modal and editing state
    const showDetailModal = ref(false);
    const herbDetail = ref(null);
    const editMode = ref(false);
    const isAdding = ref(false);
    const editData = ref({});

    // Load category data (default by category)
    const loadCategories = async () => {
      groups.value = await getHerbCategories(route.params.lang);
      if (groups.value.length > 0) {
        await selectGroup(groups.value[0]);
      }
    };

    // Load taste classification data
    const loadClassifications = async () => {
      groups.value = await getHerbClassifications(route.params.lang);
      if (groups.value.length > 0) {
        await selectGroup(groups.value[0]);
      }
    };

    // Toggle group display mode
    const toggleDisplayMode = async () => {
      isClassificationMode.value = !isClassificationMode.value;
      searchQuery.value = '';
      searchResults.value = [];
      searchPerformed.value = false;
      if (isClassificationMode.value) {
        await loadClassifications();
      } else {
        await loadCategories();
      }
    };

    // Load herb data based on the current group
    const selectGroup = async (group) => {
      selectedGroup.value = group;
      if (isClassificationMode.value) {
        herbs.value = await getHerbsByClassification(group, route.params.lang);
      } else {
        herbs.value = await getHerbsByCategory(group, route.params.lang);
      }
    };

    // Toggle search mode
    const toggleSearchMode = () => {
      isSearchMode.value = !isSearchMode.value;
      searchQuery.value = '';
      searchResults.value = [];
      searchPerformed.value = false;
    };

    // Execute search
    const searchHerbs = async () => {
      if (!searchQuery.value.trim()) return;
      searchResults.value = await searchHerbsByName(searchQuery.value, route.params.lang);
      searchPerformed.value = true;
    };

    // Open detail modal (edit or read-only)
    const openDetailModal = async (id) => {
      showDetailModal.value = true;
      editMode.value = false;
      isAdding.value = false;
      herbDetail.value = null;
      herbDetail.value = await getHerbDetailAdmin(id, route.params.lang);
    };

    // Close detail modal
    const closeDetailModal = () => {
      showDetailModal.value = false;
      herbDetail.value = null;
      editMode.value = false;
      isAdding.value = false;
    };

    // Enter edit mode (copy detail data to the edit form)
    const enterEditMode = () => {
      editMode.value = true;
      editData.value = { ...herbDetail.value };
    };

    // Cancel edit mode
    const cancelEdit = () => {
      editMode.value = false;
      editData.value = { ...herbDetail.value };
    };

    // Save edit or add operation
    const saveEdit = async () => {
      /// Add validation: both Chinese and English names must be provided
      if (!editData.value.name_zh || !editData.value.name_en) {
        alert(t('herbs.nameRequired') || '请填写药材的中文和英文名称');
        return;
      }
      let result = null;
      if (isAdding.value) {
        // Add operation
        result = await addHerbDetailAdmin(editData.value, route.params.lang);
      } else {
        // Edit operation
        result = await updateHerbDetailAdmin(editData.value, route.params.lang);
      }
      if (result.message == 'Success!') {
        if (isAdding.value) {
          alert(result.message || 'Success!');
          window.location.reload();
        } else {
          alert(result.message || 'Success!');
          window.location.reload();
        }
        editMode.value = false;
        isAdding.value = false;
      } else {
        alert(result ? result.message : 'Operation failed');
      }
    };

    // Delete operation
    const deleteHerb = async () => {
      if (confirm(t('herbs.confirmDelete'))) {
        const result = await deleteHerbDetailAdmin({ id: herbDetail.value.id }, route.params.lang);
        console.log('Delete result:', result);
        if (result.code === 0) {
          alert(result.message || 'Deleted successfully');
          window.location.reload(); // Refresh the entire page
        } else {
          alert(result ? result.message : 'Deletion failed');
        }
      }
    };

    // Open modal to add new herb
    const openAddModal = () => {
      showDetailModal.value = true;
      editMode.value = true;
      isAdding.value = true;
      // Initialize empty data, excluding id
      editData.value = {
        name_zh: '',
        name_en: '',
        image_zh: '',
        image_en: '',
        category_zh: '',
        category_en: '',
        origin_zh: '',
        origin_en: '',
        production_regions_zh: '',
        production_regions_en: '',
        properties_zh: '',
        properties_en: '',
        functions_zh: '',
        functions_en: '',
        classification_zh: '',
        classification_en: ''
      };
      // Clear detail data
      herbDetail.value = {};
    };

    onMounted(async () => {
      await loadCategories();
    });

    watch(() => route.params.lang, async () => {
      if (isClassificationMode.value) {
        await loadClassifications();
      } else {
        await loadCategories();
      }
    });

    return {
      groups,
      selectedGroup,
      herbs,
      selectGroup,
      isSearchMode,
      toggleSearchMode,
      isClassificationMode,
      toggleDisplayMode,
      searchQuery,
      searchResults,
      searchPerformed,
      searchHerbs,
      openDetailModal,
      closeDetailModal,
      showDetailModal,
      herbDetail,
      editMode,
      editData,
      enterEditMode,
      cancelEdit,
      saveEdit,
      openAddModal,
      isAdding,
      deleteHerb,
      route
    };
  }
};
</script>

<style scoped>
.admin-herb-list {
  padding: 20px;
}
/* Toggle mode button */
.toggle-mode-btn {
  margin-bottom: 15px;
  padding: 8px 15px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
}

/* Group navigation */
.groups {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

/* Herb Items centered display */
.herb-items {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.herb-item {
  cursor: pointer;
  padding: 8px 15px;
  /* Theme color changed to orange */
  border: 1px solid #ba5f39;
  border-radius: 5px;
  margin: 10px;
  transition: background-color 0.3s;
}
.herb-item:hover {
  background-color: #f6eadf; /* Light orange hover effect */
}

/* Toggle mode button */
.toggle-mode-btn {
  margin-bottom: 15px;
  padding: 8px 15px;
  background-color: #faf0e6; /* Light orange beige */
  border: 1px solid #d6b08c; /* Slightly darker shade */
  border-radius: 5px;
  cursor: pointer;
}

/* Floating add button */
.floating-add-btn {
  position: fixed;
  top: 15%;
  right: 5%;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  /* Theme color orange */
  background-color: #ba5f39;
  color: white;
  font-size: 2rem;
  border: none;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}
.floating-add-btn:hover {
  background-color: #9c4a2d;
}

/* Search mode */
.search-mode {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Search input box */
.search-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Search button */
.search-btn {
  padding: 8px;
  /* Theme color orange */
  background-color: #ba5f39;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.search-btn:hover {
  background-color: #9c4a2d;
}

/* Modal styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: #404040;
  padding: 20px;
  border-radius: 5px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

/* Light mode modal styles */
@media (prefers-color-scheme: light) {
  .modal {
    background-color: rgba(255, 255, 255, 0.5);
  }
  .modal-content {
    /* Use beige background to align with orange theme */
    background-color: #faf0e6;
  }
}

/* Detail modal title */
.detail-modal h2 {
  margin-top: 0;
}

/* Herb detail image */
.herb-image {
  width: 100%;
  max-height: 300px;
  object-fit: contain;
  margin: 10px 0;
}

/* Close button */
.close-btn {
  position: absolute;
  top: 5px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

/* Edit form styles */
.form-group {
  margin-bottom: 10px;
}
.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
.form-group input {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Action buttons */
.form-actions {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
}
.edit-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #3498db; /* Keep original blue */
  color: white;
}
.delete-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #e74c3c; /* Keep original red */
  color: white;
}
.save-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  /* Theme color orange */
  background-color: #ba5f39;
  color: white;
}
.cancel-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #e74c3c; /* Keep original red */
  color: white;
}
</style>