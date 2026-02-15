import axios from 'axios';

// Automatically adapt to the API root path for development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'
    : '/api';
/**
 * Get server access logs and error logs (viewed by administrators)
 * Request method: POST
 * URL: ${API_BASE_URL}/admin/log
 * Request parameters: None
 * Example of backend response:
 * {
 *   "status": "success",
 *   "Alogs": "2025-05-13 08:00:00 GET /index.html 200\n...",
 *   "Elogs": "2025-05-13 08:00:05 ERROR Traceback...\n..."
 * }
 *
 * @returns {Promise<{ access: string[], error: string[] } | null>}
 * Returns an object containing access logs and error logs (each item is an array of strings split by row) on success and null on failure
 */
export const fetchLogs = async () => {
    try {
        const response = await axios.post(`${API_BASE_URL}/admin/log`);
        const data = response.data;

        if (data.status !== 'success') {
            console.error(`后端返回错误：${data.message}`);
            return null;
        }

        // Split the two logs into arrays by rows
        return {
            access: data.Alogs.split('\n').filter(line => line.trim() !== ''),
            error: data.Elogs.split('\n').filter(line => line.trim() !== '')
        };
    } catch (err) {
        console.error(`获取日志失败: ${err.message}`);
        return null;
    }
};

/**
 * Analyze the fields in the log file <url> and count the number of visits to each URL.
 *
 * Return value:
 * - A JSON object where the key is the URL and the value is the number of visits to that URL.
 * - Data type: Dict[str, int]
 * - Example return value:
 *       {
 *         "http://example.com/page1": 5,
 *         "http://example.com/page2": 3
 *       }
 */
export async function fetchLogStats() {
    try {
        const response = await axios.get(`${API_BASE_URL}/admin/analyze-logs`);
        return response.data || {};
    } catch (err) {
        console.error('获取日志统计失败:', err);
        return {};
    }
}
