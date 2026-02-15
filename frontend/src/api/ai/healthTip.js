import axios from 'axios';

// Automatically adapt to the API root path for development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'  // Development environment
    : '/api'; // Production environment (assuming that the backend is deployed under the same domain name)

/**Request Method: POST
 Request URL: ${API_BASE_URL}/health-suggestion
 Request Parameters: Language parameters (e.g. ? lang=zh）
 Request body format (example):
 {
 "month": <Number>,      // Current month (1-12)
 "username": <String>,   // Username (unique identifier)
 "age": <Number>,        // User's age
 "weight": <Number>,     // User's weight in kg
 "height": <Number>,     // User's height in cm
 "lang": <String>        // Language ('en' for English, 'zh' for Chinese)
 }
 Example Backend Response
 Success Response (English):
 { "suggestion": "Based on your profile and the current month, I recommend drinking warm herbal teas and avoiding cold beverages. Make sure to eat more seasonal fruits and vegetables."}
 Success Response (Chinese):
 { "suggestion": "根据您的情况和当前月份，建议多喝温热的养生茶，避免冷饮，并多吃应季的水果和蔬菜。"}

 * Get health advice based on current month and user information
 * @param {Object} params parameter object, containing:
 * - month {Number} The current month
 * - username {String} username, which is used as a unique identifier for the user
 * - age {Number} The age of the user
 * - weight {Number} The weight of the user
 * - height {Number} The height of the user
 * - lang {String} language
 * @returns {Promise} axios request
 */
export const getHealthSuggestion = (params) => {
    const token = localStorage.getItem('token');
    return axios.post(
        `${API_BASE_URL}/health-suggestion`,
        params,
        {
            headers: {
                // Back-end use flask-jwt-extended
                Authorization: `Bearer ${token}`
            }
        }
    );
};