import axios from 'axios';

// Automatically adapt to development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'
    : '/api';
/**
 * Get a prescription quiz question (randomized, not yet answered)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/tcm/prescriptionQuiz/question`
 * Query Parameters:
 *   - lang: string, required (e.g., 'zh' for Chinese or 'en' for English)
 *   - difficulty: number/string, required (1 = easy, 2 = medium, 3 = hard)
 *   - doneQuestionIds: string, comma-separated list of already-answered question IDs
 *
 * Example request:
 *   GET /api/tcm/prescriptionQuiz/question?lang=zh&difficulty=2&doneQuestionIds=1,2,3
 *
 * Example response:
 * {
 *   "id": 12,
 *   "prescriptionName": "四君子汤",
 *   "correctHerbIds": ["人参", "白术", "茯苓", "甘草"],
 *   "difficulty": 2
 * }
 *
 * Error:
 *   (varies; null returned on error)
 *
 * Get a prescription question
 * @param {String} lang - Current language, e.g. 'zh', 'en'
 * @param {Number} Difficulty - Difficulty of the question, 1 (easy) ~ 3 (hard)
 * @param {Array<String>} doneQuestionIds - A list of IDs for completed questions
 * @returns {Promise<Object>} Returns the subject object：{ id， prescriptionName， correctHerbIds， difficulty }
 */
export async function getPrescriptionQuestion(lang, difficulty, doneQuestionIds) {
    try {
        const response = await axios.get(`${API_BASE_URL}/tcm/prescriptionQuiz/question`, {
            params: {
                lang,
                difficulty,
                // Passed as a comma-separated string
                doneQuestionIds: doneQuestionIds.join(',')
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error fetching prescription question:', error);
        return null;
    }
}

/**
 * Submit a prescription quiz/test score and user metadata
 *
 * Request method: POST
 * Request URL: `${API_BASE_URL}/tcm/score`
 * Request Body:
 *   {
 *     "accuracy": number,      // accuracy percentage, e.g. 92
 *     "username": string,      // username (or '' if anonymous)
 *     "totalTime": number,     // total time (in seconds)
 *     "lang": string           // current language, e.g. 'zh' or 'en'
 *   }
 *
 * Example request body:
 * {
 *   "accuracy": 80,
 *   "username": "张三",
 *   "totalTime": 85,
 *   "lang": "zh"
 * }
 *
 * Example response:
 * {
 *   "message": "Input succeed"
 * }
 *
 * Error:
 * {
 *   "message": "No available user"
 * }*/
/**
 * Submit a prescription quiz score
 * @param {Number} accuracy - Percentage number
 * @param {String} username - current username (empty string if not logged in)
 * @param {Number} totalTime - The total time taken to complete the test in seconds
 * @param {String} lang - Current language
 * @returns {Promise<Object>} returns the result of the backend processing
 */
export async function submitPrescriptionQuizScore(accuracy, username, totalTime, lang) {
    try {
        const response = await axios.post(`${API_BASE_URL}/tcm/score`, {
            accuracy,
            username,
            totalTime,
            lang
        });
        return response.data;
    } catch (error) {
        console.error('Error submitting prescription quiz score:', error);
        return null;
    }
}

/**
 * Get an array of randomized herb IDs for quiz options (5 IDs)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/tcm/herb-ids?lang=zh`
 * Query Parameters:
 *   - lang: optional, language ('zh' for Chinese, 'en' for English); default: 'zh'
 *
 * Example request:
 *   GET /api/tcm/herb-ids?lang=en
 *
 * Example response:
 * {
 *   "ids": [12, 54, 33, 90, 17]
 * }*/
/**
 * Get an array of herb IDs
 * @param {String} lang language (default 'zh')
 */
export const getHerbIds = async (lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/tcm/herb-ids`, {
            params: { lang }
        });

        return response.data.ids;
    } catch (error) {
        console.error('获取药材ID失败：', error);
        return [];
    }
};

/**
 * Get herb details for a single herb (used in quiz, includes image and options)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/tcm/herb-detail/{id}?lang=zh`
 * Path Parameters:
 *   - id: required, herb ID
 * Query Parameters:
 *   - lang: optional, language ('zh' for Chinese, 'en' for English); default: 'zh'
 *
 * Example request:
 *   GET /api/tcm/herb-detail/12?lang=zh
 *
 * Example response:
 * {
 *   "imageUrl": "http://example.com/herb12.jpg",
 *   "name": "黄芪",
 *   "options": ["黄芪", "当归", "甘草", "党参"]
 * }*/
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

        return response.data;
    } catch (error) {
        console.error(`获取id为${id}的药材详情失败:`, error);
        return null;
    }
};

/**
 * Submit quiz game result (herb quiz, not prescription quiz)
 *
 * Request method: POST
 * Request URL: `${API_BASE_URL}/tcm/quiz-result`
 * Request Body:
 *   {
 *     "accuracy": number,      // percentage score
 *     "username": string,      // current user's name (or '' if guest)
 *     "totalTime": number,     // total completion time in seconds
 *     "lang": string           // language code ('zh' by default)
 *   }
 *
 * Example request body:
 * {
 *   "accuracy": 100,
 *   "username": "testuser",
 *   "totalTime": 77,
 *   "lang": "en"
 * }
 *
 * Example response:
 * {
 *   "message": "Input succeed"
 * }
 *
 * Error response:
 * {
 *   "message": "No available user"
 * }*/
/**
 * Submit Quiz test results
 * Submissions include quiz's correctness, total time spent, and current user's username
 * @param {Number} accuracy (percentage)
 * @param {String} username The username of the current user
 * @param {Number} totalTime The total time taken to complete the test in seconds
 * @param {String} lang language (default 'zh')
 */
export const submitQuizScore = async (accuracy, username, totalTime, lang = 'zh') => {
    try {
        const response = await axios.post(`${API_BASE_URL}/tcm/quiz-result`, {
            accuracy,
            username,
            totalTime,
            lang
        });
        return response.data;
    } catch (error) {
        console.error('提交 Quiz 结果失败：', error);
        return { error: error.message };
    }
};
