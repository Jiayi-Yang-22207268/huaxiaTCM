import axios from 'axios';

// Automatically adapt to development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'
    : '/api';

/**
 * Get homepage image (for admins)
 * Request method: GET
 * Request URL: '${API_BASE_URL}/banner'
 * Request parameter: language parameter (e.g. ?lang=zh)
 * Example of backend response:
 * {
 *   "code": 0,
 *   "data": [
 *       { "imageUrl": "http://.../zh.jpg", "id": 1 },
 *       { "imageUrl": "http://.../zh2.jpg", "id": 2 },
 *       ...
 *   ],
 *   "message": "Success"
 * }
 *
 * For front-end display, a lang field is added for each image object when it returns.
 */
export async function getHomepageImages(lang = 'zh') {
    try {
        const response = await axios.get(`${API_BASE_URL}/mainImage/banner`, {
            params: { lang }
        });
        if (response.data && response.data.code === 0 && response.data.data) {
            // Add a lang field for each object for easy front-end display
            return response.data.data.map(image => ({ ...image, lang }));
        }
        return [];
    } catch (error) {
        console.error(`获取首页图片失败: ${error.message}`);
        return [];
    }
}

/**
 * Add a homepage image (for admins)
 * Request method: POST
 * Request URL: '${API_BASE_URL}/admin/addMainImages'
 * Request parameters: { imageUrlZh, imageUrlEn }
 * Example of backend response:
 * {
 *   "code": 0,
 *   "data": {},
 * "message": "Added successfully"
 * }
 */
export async function addHomepageImages(imageUrlZh, imageUrlEn) {
    try {
        const response = await axios.post(`${API_BASE_URL}/admin/addMainImage`, {
            imageUrl_en: imageUrlEn,   // The URL of the image in English received by the backend
            imageUrl_zh: imageUrlZh    // The Chinese image URL received by the backend
        });
        // Here, success is judged based on the message returned by the backend
        if (response.data && response.data.message === 'Image added successfully!') {
            return true;
        }
        return false;
    } catch (error) {
        console.error(`添加首页图片失败: ${error.message}`);
        return false;
    }
}

/**
 * Delete the homepage image (for admins, delete according to the image ID)
 * Request: DELETE
 * Request URL: '${API_BASE_URL}/admin/deleteMainImage'
 * Request parameter: { imageId } (passed via request body)
 * Example of backend response:
 * {
 *   "code": 0,
 *   "image_id": {},
 * "message": "Deleted successfully"
 * }
 */
export async function deleteHomepageImage(imageId) {
    try {
        // Turn the imageId to a number
        const id = Number(imageId);
        const response = await axios.post(`${API_BASE_URL}/admin/deleteMainImage`, {
            image_id: id
        });
        return response.data && response.data.message === 'Image deleted successfully!';
    } catch (error) {
        console.error(`删除首页图片失败: ${error.message}`);
        return false;
    }
}

/**
 * Upload images (for admins to add images via file upload)
 * Request method: POST
 * URL: ${API_BASE_URL}/admin/uploadImages
 * Request parameters: FormData format, containing two files:
 * - 'image_zh': Chinese picture
 * - 'image_en': English image
 */
export async function uploadHomepageImages(fileZh, fileEn) {
    try {
        const formData = new FormData();
        formData.append('image_zh', fileZh);
        formData.append('image_en', fileEn);
        const response = await axios.post(`${API_BASE_URL}/admin/uploadImages`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data && response.data.message === 'File uploaded successfully';
    } catch (error) {
        console.error(`上传图片失败: ${error.message}`);
        return false;
    }
}