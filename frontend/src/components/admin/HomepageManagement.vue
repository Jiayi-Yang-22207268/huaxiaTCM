<template>
  <div class="homepage-management">
    <h2>{{ t('homepageManagement.title') }}</h2>
    <!-- Image List (Displays all images in Chinese and English) -->
    <div class="image-list" v-if="images.length">
      <div v-for="img in images" :key="img.id" class="image-item">
        <img :src="img.imageUrl" alt="Homepage Image" />
        <p>{{ t('homepageManagement.lang') }}: {{ img.lang }}</p>
        <button class="delete-btn" @click="deleteImage(img.id)">
          {{ t('homepageManagement.delete') }}
        </button>
      </div>
    </div>
    <div v-else>
      <p>{{ t('homepageManagement.noImage') }}</p>
    </div>
    <!-- Add New Image Section -->
    <div class="add-image">
      <h3>{{ t('homepageManagement.addImageTitle') }}</h3>
      <!-- Mode Selection -->
      <div class="form-group mode-select">
        <label>
          <input type="radio" value="url" v-model="inputMode" />
          {{ t('homepageManagement.urlMode') }}
        </label>
        <label>
          <input type="radio" value="upload" v-model="inputMode" />
          {{ t('homepageManagement.uploadMode') }}
        </label>
      </div>
      <!-- URL Input Mode -->
      <div v-if="inputMode === 'url'">
        <div class="form-group">
          <label>{{ t('homepageManagement.newImageUrlZh') }}:</label>
          <input type="text" v-model="newImageUrlZh" placeholder="Enter Chinese image URL" />
        </div>
        <div class="form-group">
          <label>{{ t('homepageManagement.newImageUrlEn') }}:</label>
          <input type="text" v-model="newImageUrlEn" placeholder="Enter English image URL" />
        </div>
      </div>
      <!-- File Upload Mode -->
      <div v-else-if="inputMode === 'upload'">
        <div class="form-group">
          <label>{{ t('homepageManagement.uploadImageZh') }}:</label>
          <input type="file" @change="handleFileChangeZh" />
        </div>
        <div class="form-group">
          <label>{{ t('homepageManagement.uploadImageEn') }}:</label>
          <input type="file" @change="handleFileChangeEn" />
        </div>
      </div>
      <button class="add-btn" @click="addImage">
        {{ t('homepageManagement.add') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'; // Importing Vue composition API functions
import { useI18n } from 'vue-i18n'; // Importing i18n for internationalization
import {
  getHomepageImages,
  addHomepageImages,
  deleteHomepageImage,
  uploadHomepageImages
} from '@/api/admin/homeManagement.js'; // Importing API functions for homepage image management

// Initialize i18n for localization
const { t } = useI18n();

// Reactive variables
const images = ref([]); // Stores the list of images displayed on the homepage
const inputMode = ref('url'); // Determines the mode for adding images: 'url' or 'upload'
const newImageUrlZh = ref(''); // Stores the URL of the new image in Chinese
const newImageUrlEn = ref(''); // Stores the URL of the new image in English
const fileZh = ref(null); // Stores the uploaded image file in Chinese
const fileEn = ref(null); // Stores the uploaded image file in English

// Function to fetch images from the server for both Chinese and English versions
const fetchImages = async () => {
  const zhImages = await getHomepageImages('zh'); // Get images for Chinese homepage
  const enImages = await getHomepageImages('en'); // Get images for English homepage
  images.value = [...zhImages, ...enImages]; // Combine both lists into a single array
};

// Function to handle file selection for Chinese image upload
const handleFileChangeZh = (e) => {
  fileZh.value = e.target.files[0]; // Store the selected file
};

// Function to handle file selection for English image upload
const handleFileChangeEn = (e) => {
  fileEn.value = e.target.files[0]; // Store the selected file
};

// Function to add a new image to the homepage
const addImage = async () => {
  // If the input mode is 'upload', handle file uploads
  if (inputMode.value === 'upload') {
    if (!fileZh.value || !fileEn.value) {
      return alert(t('homepageManagement.emptyFile')); // Alert if files are not selected
    }
    const res = await uploadHomepageImages(fileZh.value, fileEn.value); // Upload files
    res
      ? (alert(t('homepageManagement.addSuccess')), await fetchImages()) // Show success message and refresh images
      : alert(t('homepageManagement.addFail')); // Show failure message
    return;
  }

  // If the input mode is 'url', handle URL-based image addition
  if (!newImageUrlZh.value || !newImageUrlEn.value) {
    return alert(t('homepageManagement.emptyUrl')); // Alert if URLs are empty
  }
  const res = await addHomepageImages(newImageUrlZh.value, newImageUrlEn.value); // Add images using URLs
  res
    ? (alert(t('homepageManagement.addSuccess')), (newImageUrlZh.value = '', newImageUrlEn.value = '', await fetchImages())) // Show success message, clear input fields, and refresh images
    : alert(t('homepageManagement.addFail')); // Show failure message
};

// Function to delete an image from the homepage
const deleteImage = async (id) => {
  if (!confirm(t('homepageManagement.confirmDelete'))) return; // Ask for confirmation before deleting
  const res = await deleteHomepageImage(id); // Delete image by ID
  res
    ? (alert(t('homepageManagement.deleteSuccess')), await fetchImages()) // Show success message and refresh images
    : alert(t('homepageManagement.deleteFail')); // Show failure message
};

// Fetch images when the component is mounted
onMounted(fetchImages);
</script>

<style scoped>
.homepage-management {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  --accent: #ba5f39;
  --card-bg: #fff;
  background: var(--bg, #faf5ee);
  color: var(--text, #5d5d5a);
}

@media (prefers-color-scheme: dark) {
  .homepage-management {
    --bg: #121212;
    --text: #e0e0e0;
    --card-bg: #1f1f1f;
  }
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.image-item {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  text-align: center;
  flex: 1 1 calc(33% - 20px);
}
.image-item img {
  max-width: 100%;
  height: auto;
  margin-bottom: 5px;
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 4px;
}

.add-image {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
  background: var(--card-bg);
}

.mode-select {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.form-group input[type="text"],
.form-group input[type="file"] {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  background: var(--card-bg);
  color: inherit;
}

.add-btn {
  background-color: var(--accent);
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
.add-btn:hover {
  background-color: #9c4a2d;
}
</style>

