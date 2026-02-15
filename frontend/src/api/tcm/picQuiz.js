import axios from 'axios';

// Automatically adapt to development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'
    : '/api';

/**
 * Get an array of random herb IDs
 * Request method: GET
 * Request URL: '${API_BASE_URL}/tcm/herb-ids'
 * Request parameters:
 * {
 *   "lang": <string>  // Language ('zh' for Chinese, 'en' for English); defaults to 'zh'
 * }
 * Example of backend response:
 * {
 *   "ids": [<int>, <int>, ...]  // Array of random herb IDs
 * }
 * Error responses:
 * {
 *   "error": "<string>"  // Error message if the request fails
 * }
 */
/**
 * Get an array of herb IDs
 * @param {String} lang language (default 'zh')
 */
export const getHerbIds = async (lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/tcm/herb-ids`, {
            params: { lang }
        });
        // Suppose the return format is: { ids: [1, 2, 3, ...] }
        return response.data.ids;
    } catch (error) {
        console.error('获取药材ID失败：', error);
        return [];
    }
};

/**
 * Get herb details based on its ID
 * Request method: GET
 * Request URL: '${API_BASE_URL}/tcm/herb-detail/<id>'
 * Request parameters:
 * {
 *   "id": <number>
 *   "lang": <string>  // Language ('zh' for Chinese, 'en' for English); defaults to 'zh'
 * }
 * Example of backend response:
 * {
 *   "imageUrl": "<string>",  // URL of the herb image
 *   "name": "<string>",      // Name of the herb
 *   "options": [             // Multiple-choice options for the quiz
 *     "<string>",
 *     "<string>",
 *     ...
 *   ]
 * }
 * Error responses:
 * {
 *   "error": "<string>"  // Error message if the request fails
 * }
 */
/**
 * Get herb details based on individual IDs
 * @param {Number} id Herb ID
 * @param {String} lang language (default 'zh')
 */
export const getHerbDetail = async (id, lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/tcm/herb-detail/${id}`, {
            params: { lang }
        });
        // Suppose the return format is: { imageUrl: '...', name: '...', options: ['Herb 1', 'Herb 2', 'Herb 3', 'Herb 4'] }
        return response.data;
    } catch (error) {
        console.error(`获取id为${id}的药材详情失败:`, error);
        return null;
    }
};


/**
 * Submit quiz test results
 * Request method: POST
 * Request URL: '${API_BASE_URL}/tcm/quiz-result'
 * Content type: application/json
 * Request body:
 * {
 *   "accuracy": <number>,    // Quiz accuracy percentage
 *   "username": <string>,    // Username of the current user
 *   "lang": <string>         // Language ('zh' for Chinese, 'en' for English); defaults to 'zh'
 * }
 * Example of backend response:
 * {
 *   "message": "Input succeed"  // Success message
 * }
 * Error responses:
 * {
 *   "error": "<string>"  // Error message if the request fails
 * }
 */
/**
 * Submit Quiz test results
 * Only submit the correct rate of quiz and the username of the current user
 * @param {Number} accuracy (percentage)
 * @param {String} username The username of the current user
 * @param {String} lang language (default 'zh')
 */
export const submitQuizScore = async (accuracy, username, lang = 'zh') => {
    try {
        const response = await axios.post(`${API_BASE_URL}/tcm/quiz-result`, {
            accuracy,
            username,
            lang
        });
        return response.data;
    } catch (error) {
        console.error('提交 Quiz 结果失败：', error);
        return { error: error.message };
    }
};

