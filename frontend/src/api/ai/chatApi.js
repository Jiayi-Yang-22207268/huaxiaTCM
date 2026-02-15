import axios from 'axios';

// // Automatically adapt to the API root path for development and production environments
// const API_BASE_URL = window.location.origin.includes('localhost')
//     ? 'http://127.0.0.1:5000/api'  // Development environment
//     : '/api'; // Production environment (assuming that the backend is deployed under the same domain name)
// 1. 创建一个 axios 实例，baseURL 指向后端的 /api/chat
const api = axios.create({
    baseURL: window.location.origin.includes('localhost')
        ? 'http://127.0.0.1:5000/api/chat'  // 开发时指向本地 Flask
        : '/api/chat'                       // 生产时走同域
})

// 添加响应拦截器，捕获所有 401 错误
api.interceptors.response.use(
    response => response,
    error => {
        const res = error.response;
        // 当后端返回 401（需要重新授权）时，跳转到后端发起授权
        if (res && res.status === 401) {
            // 根据当前环境，拼出后端授权链接地址
            const backendBase = window.location.origin.includes('localhost')
                ? 'http://127.0.0.1:5000'
                : '';
            window.location.href = `${backendBase}/api/chat/auth-url`;
            // 返回一个永远 pending 的 Promise，阻止后续 then/catch
            return new Promise(() => {});
        }
        return Promise.reject(error);
    }
);


/**
 * 发送聊天请求
 * @param {string} lang     zh 或 en（你目前其实没用到 lang，但留着也无妨）
 * @param {string} question 用户的问题
 */
export function sendUserMessage(lang, question) {
    return api.post('/BianQue', { lang, question })
}

/**
 * Request Method: POST
 *
 * Request URL: ${API_BASE_URL}/api/chat/BianQue
 *
 * Request Parameters: {
 *   "lang": "zh", // or "en", depending on the language preference
 *   "question": "User's question here"
 * }
 *
 * Example Backend Response: {
 *   "message": "AI response to the user's question in the requested language"
 * }  */
// export const sendUserMessage = (lang, question) => {
//     return axios.post('/api/chat/BianQue', {
//         lang: lang, // 'zh' or 'en'
//         question: question, // Problems with user input
//     });
// };