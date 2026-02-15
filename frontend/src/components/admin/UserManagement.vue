<template>
  <div class="user-management">
    <div class="header">
      <h2>{{ t('userManagement.title') }}</h2>
      <!-- Built-in add user button, aligned with the title -->
      <button class="add-user-btn" @click="addNewUser">+</button>
    </div>
    <!-- User list -->
    <ul class="user-list">
      <li v-for="user in users" :key="user.id" class="user-item">
        <!-- Avatar upload -->
        <div class="user-avatar">
          <img
              :src="user.avatar || defaultAvatar"
              alt="avatar"
              class="avatar-img"
              @load="onImgLoad(user)"
              @error="onImgError(user)"
          />
          <label class="avatar-upload-label">
            {{ t('userManagement.changeAvatar') }}
            <input
                type="file"
                accept="image/*"
                @change="onAvatarChange($event, user.id)"
            />
          </label>
        </div>
        <!-- User information -->
        <div class="user-info">
          <p>
            <strong>ID:</strong> {{ user.id }} |
            <strong>{{ t('userManagement.role') }}:</strong> {{ user.role }}
          </p>
          <p>
            <strong>{{ t('userManagement.name') }}:</strong>
            {{ user.username }}
          </p>
          <p>
            <strong>{{ t('userManagement.height') }}:</strong>
            {{ user.height }} cm,
            <strong>{{ t('userManagement.weight') }}:</strong>
            {{ user.weight }} kg,
            <strong>{{ t('userManagement.age') }}:</strong>
            {{ user.age }} {{ t('userManagement.ageUnit') }}
          </p>
          <p>
            <strong>{{ t('userManagement.password') }}:</strong>
            {{ user.password }}
          </p>
        </div>
        <!-- Action buttons -->
        <div class="user-actions">
          <button class="edit-btn" @click="editUser(user)">
            {{ t('userManagement.edit') }}
          </button>
          <button class="delete-btn" @click="confirmDelete(user.id)">
            {{ t('userManagement.delete') }}
          </button>
        </div>
      </li>
    </ul>
    <!-- Edit/Add user modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">×</button>
        <h3>
          {{ isEditing
            ? t('userManagement.editUser')
            : t('userManagement.addUser') }}
        </h3>
        <div class="form-group" v-if="isEditing">
          <label>{{ t('userManagement.id') }}:</label>
          <input type="text" v-model="editData.id" readonly />
        </div>
        <div class="form-group">
          <label>{{ t('userManagement.name') }}:</label>
          <input type="text" v-model="editData.username" />
        </div>
        <div class="form-group">
          <label>{{ t('userManagement.height') }} (cm):</label>
          <input type="number" v-model.number="editData.height" />
        </div>
        <div class="form-group">
          <label>{{ t('userManagement.weight') }} (kg):</label>
          <input type="number" v-model.number="editData.weight" />
        </div>
        <div class="form-group">
          <label>{{ t('userManagement.age') }}:</label>
          <input type="number" v-model.number="editData.age" />
        </div>
        <div class="form-group">
          <label>{{ t('userManagement.role') }}:</label>
          <select v-model="editData.role">
            <option value="admin">{{ t('userManagement.admin') }}</option>
            <option value="client">{{ t('userManagement.client') }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ t('userManagement.password') }}:</label>
          <input
              type="password"
              v-model="editData.password"
              placeholder="Leave blank to keep unchanged"
          />
        </div>
        <div class="form-actions">
          <button class="save-btn" @click="saveUser">
            {{ t('userManagement.save') }}
          </button>
          <button class="cancel-btn" @click="closeModal">
            {{ t('userManagement.cancel') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import defaultAvatar from '/public/BlankAvatar.png';
import {
  getAllUsers,
  updateUser,
  deleteUser,
  createUser,
  changeUserAvatar,
  getAvatar
} from '@/api/admin/userManagement'

const { t } = useI18n()

// State
const users = ref([])
const showModal = ref(false)
const isEditing = ref(false)
const editData = ref({})
const originalPassword = ref('')

// Fetch the user list and print the avatar list
const fetchUsers = async () => {
  const res = await getAllUsers()
  if (res && res.code === 0) {
    users.value = res.data
    console.log('fetched avatar URLs:', users.value.map(u => u.avatar))
  } else {
    console.error('Failed to fetch user information')
  }
}

// Avatar change
const onAvatarChange = async (e, userId) => {
  const file = e.target.files[0]
  if (!file) return
  try {
    const res = await changeUserAvatar(file, userId)
    alert(res.message)
    await fetchUsers()
  } catch {
    alert(t('userManagement.avatarUploadFail'))
  } finally {
    e.target.value = ''
  }
}

// Image loaded successfully
const onImgLoad = (user) => {
  console.log(`avatar loaded for user ${user.id}:`, user.avatar)
}

// Image loading failed
const onImgError = (user) => {
  console.error(`avatar failed to load for user ${user.id}:`, user.avatar)
}

// Edit user
const editUser = (user) => {
  isEditing.value = true
  originalPassword.value = user.password
  editData.value = { ...user, password: '' }
  showModal.value = true
}

// Add new user
const addNewUser = () => {
  isEditing.value = false
  editData.value = {
    username: '',
    height: null,
    weight: null,
    age: null,
    role: 'client',
    password: ''
  }
  showModal.value = true
}

// Save user (Edit/Add)
const saveUser = async () => {
  let result
  if (isEditing.value) {
    if (!editData.value.password) {
      editData.value.password = originalPassword.value
    }
    result = await updateUser(editData.value)
  } else {
    result = await createUser(editData.value)
  }
  console.log('saveUser result:', result)
  if (result.message == "User updated successfully!") {
    alert(result.message || t('userManagement.success'))
    showModal.value = false
    await fetchUsers()
  } else {
    alert(result ? result.message : t('userManagement.fail'))
  }
}

// Delete user
const confirmDelete = async (id) => {
  if (confirm(t('userManagement.confirmDelete'))) {
    const result = await deleteUser(id)
    if (result && result.code === 0) {
      alert(result.message || t('userManagement.deleteSuccess'))
      await fetchUsers()
    } else {
      alert(result ? result.message : t('userManagement.deleteFail'))
    }
  }
}

// Close modal
const closeModal = () => {
  showModal.value = false
}

onMounted(fetchUsers)
</script>

<style scoped>
.user-management {
  padding: 20px;
  background-color: #f5f5f5;
  color: #333;
  --accent: #ba5f39;
}

/* Container for the title and the add button */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-user-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--accent);
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  border: none;
}

.add-user-btn:hover {
  background-color: #9c4a2d;
}

.user-list {
  list-style: none;
  padding: 0;
  margin-bottom: 20px;
}

.user-item {
  display: flex;
  align-items: flex-start;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  margin-bottom: 10px;
}

/* Avatar area */
.user-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 16px;
}

.avatar-img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 6px;
  border: 1px solid #ccc;
}

.avatar-upload-label {
  font-size: 12px;
  color: #555;
  cursor: pointer;
}

.avatar-upload-label input {
  display: none;
}

/* User information */
.user-info {
  flex: 1;
}

/* Action buttons */
.user-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.edit-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #3498db;
  color: white;
}

.delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #e74c3c;
  color: white;
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
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
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
  margin-bottom: 12px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 4px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}

.save-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: var(--accent);
  color: white;
}

.save-btn:hover:not(:disabled) {
  background-color: #9c4a2d;
}

.cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #e74c3c;
  color: white;
}

/* Dark mode styles */
@media (prefers-color-scheme: dark) {
  .user-management {
    background-color: #2b2b2b;
    color: #e0e0e0;
    --accent: #ba5f39;
  }

  .user-item {
    background-color: #3a3a3a;
    border-color: #555;
  }

  .avatar-img {
    border-color: #555;
  }

  .avatar-upload-label {
    color: #ccc;
  }

  .user-info p {
    color: #e0e0e0;
  }

  .edit-btn {
    background-color: #1e88e5;
  }

  .delete-btn {
    background-color: #c62828;
  }

  .modal-content {
    background-color: #424242;
  }

  .form-group input,
  .form-group select {
    background-color: #555;
    border-color: #666;
    color: #e0e0e0;
  }

  .save-btn {
    background-color: var(--accent);
  }

  .save-btn:hover:not(:disabled) {
    background-color: #9c4a2d;
  }

  .cancel-btn {
    background-color: #c62828;
  }
}
</style>  