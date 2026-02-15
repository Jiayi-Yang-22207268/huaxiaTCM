import axios from 'axios';

const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'
    : '/api';

/**
 * Fuzzy matching of prescriptions based on the herbs selected by the user
 * Request method: POST
 * Request URL: '${API_BASE_URL}/tcm/getFuzzyPrescription'
 * Content type: application/json
 * Request body:
 * {
 *   "herbs": [<int>, <int>, ...],  // Array of herb IDs selected by the user
 *   "lang": <string>               // Language ('zh' for Chinese, 'en' for English); defaults to 'zh'
 * }
 * Example of backend response:
 * {
 *   "precisionResult": [
 *     { "id": <int>, "name": <string> },  // Exact match prescriptions
 *     ...
 *   ],
 *   "guessResult": [
 *     { "id": <int>, "name": <string> },  // Fuzzy match prescriptions
 *     ...
 *   ]
 * }
 * Error responses:
 * {
 *   "error": "<string>"  // Error message if the request fails
 * }
 /**
 * Fuzzy matching of prescriptions based on the herbs selected by the user
 * @param {Array} herbs user-selected herb ID array
 * @param {String} lang language (default 'zh')
 */
export const getFuzzyPrescription = async (herbs, lang = 'zh') => {
    try {
        const response = await axios.post(`${API_BASE_URL}/tcm/getFuzzyPrescription`, { herbs, lang });
        return response.data;
    } catch (error) {
        console.error('获取模糊药方失败：', error);
        return { error: error.message };
    }
};

/**
 * Check whether the herbs selected by the user meet the requirements of the specified prescription
 * Request method: POST
 * Request URL: '${API_BASE_URL}/tcm/checkHerbSelection'
 * Content type: application/json
 * Request body:
 * {
 *   "prescriptionId": <string>,    // ID of the prescription to check
 *   "selectedHerbs": [<int>, ...], // Array of herb IDs selected by the user
 *   "lang": <string>               // Language ('zh' for Chinese, 'en' for English); defaults to 'zh'
 * }
 * Example of backend response:
 * {
 *   "result": "success" | "failure",  // Indicates whether the selection is correct
 *   "message": "<string>",            // Success or failure message
 *   "lack": [<int>, ...],             // IDs of missing herbs (if any)
 *   "extra": [<int>, ...]             // IDs of extra herbs (if any)
 * }
 * Error responses:
 * {
 *   "error": "<string>"  // Error message if the request fails
 * }
 */
/**
 * Check whether the herbs selected by the user meet the requirements of the specified prescription
 * @param {String} prescriptionId prescription id
 * @param {Array} selectedHerbs Array of herb ids selected by the user
 * @param {String} lang language (default 'zh')
 */
export const checkHerbSelection = async (prescriptionId, selectedHerbs, lang = 'zh') => {
    try {
        const response = await axios.post(`${API_BASE_URL}/tcm/checkHerbSelection`, { prescriptionId, selectedHerbs, lang });
        return response.data;
    } catch (error) {
        console.error('检查药材选择失败：', error);
        return { error: error.message };
    }
};
