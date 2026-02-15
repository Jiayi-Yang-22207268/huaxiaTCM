import axios from 'axios';

// Automatically adapt API base URL for development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
  ? 'http://127.0.0.1:5000/api'
  : '/api';

/**
 * Get the URL of the API documentation PDF (for iframe or a tag)
 * @returns {string}
 */
export function getInterfaceDocumentUrl() {
  return `${API_BASE_URL}/document/interface`;
}

/**
 * Get the binary stream of the API documentation PDF (for download or etc.)
 * @returns {Promise<Blob|null>}
 */
export async function fetchInterfaceDocumentBlob() {
  try {
    const response = await axios.get(`${API_BASE_URL}/document/interface`, {
      responseType: 'blob'
    });
    return response.data;
  } catch (err) {
    console.error('获取接口文档PDF失败:', err);
    return null;
  }
}