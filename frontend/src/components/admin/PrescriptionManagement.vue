<template>
  <div class="admin-prescription">
    <h3>{{ t('prescriptions.title') }}</h3>
    <!-- Search Bar -->
    <div class="search-bar">
      <input v-model="searchQuery" :placeholder="t('prescriptions.searchPlaceholder')" />
      <button @click="handleSearch">{{ t('prescriptions.searchButton') }}</button>
    </div>
    <!-- Prescription List -->
    <ul class="prescription-list">
      <li
        v-for="prescription in prescriptions"
        :key="prescription.id"
        @click="viewDetail(prescription.id)"
        class="prescription-item"
      >
        {{ prescription.name }}
      </li>
    </ul>
    <!-- Floating Add Button -->
    <button class="floating-add-btn" @click="addNew">
      +
    </button>
    <!-- Prescription Detail/Edit/Add Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">×</button>
        <div v-if="(prescriptionDetail && !isAdding) || isAdding">
          <div v-if="!editMode">
            <!-- Read-Only Detail Display -->
            <h2>
              {{ prescriptionDetail.id ? prescriptionDetail.id + ' / ' : '' }}
              {{ prescriptionDetail.name_zh }} / {{ prescriptionDetail.name_en }}
            </h2>
            <p>
              <strong>{{ t('prescription.constitute') }}:</strong>
              {{ prescriptionDetail.constitute_zh || t('prescription.noData') }} /
              {{ prescriptionDetail.constitute_en || t('prescription.noData') }}
            </p>
            <p>
              <strong>{{ t('prescription.action') }}:</strong>
              {{ prescriptionDetail.action_zh || t('prescription.noData') }} /
              {{ prescriptionDetail.action_en || t('prescription.noData') }}
            </p>
            <p>
              <strong>{{ t('prescription.indication') }}:</strong>
              {{ prescriptionDetail.indication_zh || t('prescription.noData') }} /
              {{ prescriptionDetail.indication_en || t('prescription.noData') }}
            </p>
            <!-- Edit and Delete Buttons -->
            <button class="edit-btn" @click="enterEditMode">{{ t('prescriptions.edit') }}</button>
            <button class="delete-btn" @click="handleDelete(prescriptionDetail.id)">{{ t('prescriptions.delete') }}</button>
          </div>
          <div v-else>
            <!-- Edit/Add Form -->
            <h4>{{ isAdding ? t('prescriptions.addNew') : t('prescriptions.editInfo') }}</h4>
            <!-- Edit Form -->
            <div class="form-group">
              <label>{{ t('prescription.name_zh') }}:</label>
              <input type="text" v-model="editData.name_zh" />
            </div>
            <div class="form-group">
              <label>{{ t('prescription.name_en') }}:</label>
              <input type="text" v-model="editData.name_en" />
            </div>
            <div class="form-group">
              <label>{{ t('prescription.constitute') }} (ZH):</label>
              <input type="text" v-model="editData.constitute_zh" />
            </div>
            <div class="form-group">
              <label>{{ t('prescription.constitute') }} (EN):</label>
              <input type="text" v-model="editData.constitute_en" />
            </div>
            <div class="form-group">
              <label>{{ t('prescription.action') }} (ZH):</label>
              <input type="text" v-model="editData.action_zh" />
            </div>
            <div class="form-group">
              <label>{{ t('prescription.action') }} (EN):</label>
              <input type="text" v-model="editData.action_en" />
            </div>
            <div class="form-group">
              <label>{{ t('prescription.indication') }} (ZH):</label>
              <input type="text" v-model="editData.indication_zh" />
            </div>
            <div class="form-group">
              <label>{{ t('prescription.indication') }} (EN):</label>
              <input type="text" v-model="editData.indication_en" />
            </div>
            <!-- Save and Cancel Buttons -->
            <div class="form-actions">
              <button class="save-btn" @click="saveEdit">{{ t('prescriptions.save') }}</button>
              <button class="cancel-btn" @click="cancelEdit">{{ t('prescriptions.cancel') }}</button>
            </div>
          </div>
        </div>
        <div v-else>
          <p>{{ t('loading') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  getPrescriptions,
  searchPrescriptionsByName,
  getPrescriptionDetailAdmin,
  addPrescription,
  updatePrescription,
  deletePrescription
} from '@/api/tcm/prewiki'

export default {
  setup() {
    const { t } = useI18n()
    const route = useRoute()
    const lang = route.params.lang || 'zh'

    const searchQuery = ref('')
    const prescriptions = ref([])
    const showModal = ref(false)
    const prescriptionDetail = ref({})
    const editMode = ref(false)
    const isAdding = ref(false)
    const editData = ref({})

    // Although `formLabels` is not currently used, it can be used later for unified management of form labels
    const formLabels = {
      name_zh: '药方中文名',
      name_en: '药方英文名',
      constitute_zh: '组成（中文）',
      constitute_en: 'Constitute (English)',
      action_zh: '用法（中文）',
      action_en: 'Usage (English)',
      indication_zh: '主治（中文）',
      indication_en: 'Indication (English)'
    }


    // Fetch prescription list
    const fetchList = async () => {
      prescriptions.value = await getPrescriptions(route.params.lang)
    }

    watch(() => route.params.lang, async () => {
      await fetchList()
    })

    // Search prescriptions
    const handleSearch = async () => {
      if (searchQuery.value.trim()) {
        prescriptions.value = await searchPrescriptionsByName(searchQuery.value, lang)
      } else {
        await fetchList()
      }
    }

    // View prescription details (Admin interface)
    const viewDetail = async (id) => {
      const data = await getPrescriptionDetailAdmin(id, lang)
      if (data) {
        prescriptionDetail.value = data
        editData.value = { ...data }
        showModal.value = true
        editMode.value = false
        isAdding.value = false
      }
    }

    // Add new prescription, open the addition popup (triggered by floating button)
    const addNew = () => {
      editData.value = {
        name_zh: '',
        name_en: '',
        constitute_en: '',
        constitute_zh: '',
        action_en: '',
        action_zh: '',
        indication_en: '',
        indication_zh: ''
      }
      showModal.value = true
      editMode.value = true
      isAdding.value = true
    }

    // Save edit or add operation
    const saveEdit = async () => {
      // 新增校验：要求必须填写中英文名称
      if (!editData.value.name_zh || !editData.value.name_en) {
        alert(t('prescriptions.nameRequired') || '请填写处方的中文和英文名称');
        return;
      }
      let result
      if (isAdding.value) {
        result = await addPrescription(editData.value, lang)
      } else {
        result = await updatePrescription(editData.value, lang)
      }
      if (result.message == 'Success!') {
        alert(result.message || '操作成功')
        window.location.reload()
      } else {
        alert(result ? result.message : '操作失败')
      }
    }

    // Delete prescription operation
    const handleDelete = async (id) => {
      if (confirm(t('prescriptions.confirmDelete'))) {
        const result = await deletePrescription(id, lang)
        console.log('Delete result:', result)
        if (result.message == "Prescription group and related herb links deleted successfully!") {
          alert(result.message || '删除成功')
          window.location.reload()
        } else {
          alert(result ? result.message : '删除失败')
        }
      }
    }

    // Close the popup
    const closeModal = () => {
      showModal.value = false
    }

    // Enter edit mode
    const enterEditMode = () => {
      editMode.value = true
    }

    // Cancel edit mode and close the popup
    const cancelEdit = () => {
      editMode.value = false
      showModal.value = false
    }

    onMounted(async () => {
      await fetchList()
    })

    return {
      formLabels,
      t,
      handleDelete,
      handleSearch,
      viewDetail,
      addNew,
      saveEdit,
      closeModal,
      cancelEdit,
      enterEditMode,
      fetchList,
      route,
      lang,
      searchQuery,
      prescriptions,
      showModal,
      prescriptionDetail,
      editMode,
      isAdding,
      editData
    }
  }
}
</script>

<style scoped>
.admin-prescription {
  padding: 20px;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.prescription-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.prescription-item {
  padding: 6px 12px;
  border: 1px solid #ba5f39;
  border-radius: 5px;
  cursor: pointer;
}

.floating-add-btn {
  position: fixed;
  top: 15%;
  right: 5%;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #ba5f39;
  color: white;
  font-size: 2rem;
  border: none;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

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
    /* 与HerbManagement一致，使用beige色 */
    background-color: #faf0e6;
  }
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}

.form-group {
  margin-bottom: 10px;
}
.form-group input {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-actions {
  display: flex;
  justify-content: space-between;
}
.edit-btn, .save-btn, .cancel-btn, .delete-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.edit-btn {
  background-color: #3498db;
  color: white;
  margin-top: 10px;
}
.delete-btn {
  background-color: #e74c3c;
  color: white;
  margin-top: 10px;
  margin-left: 10px;
}
.save-btn {
  background-color: #ba5f39;
  color: white;
}
.cancel-btn {
  background-color: #e74c3c;
  color: white;
}
</style>
