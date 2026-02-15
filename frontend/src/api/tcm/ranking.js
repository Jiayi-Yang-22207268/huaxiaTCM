import axios from 'axios';

/**
 * Get the Herbal Image Quiz Leaderboard (Top 10)
 *
 * Request method: GET
 * Request URL: `/api/tcm/ranking`
 *
 * Example request:
 *   GET /api/tcm/ranking
 *
 * Example response:
 * {
 *   "status": "success",
 *   "data": [
 *     {
 *       "username": "alice",
 *       "avatar": "http://example.com/avatar/alice.png",
 *       "accuracy": 95,
 *       "score": 93
 *     },
 *     {
 *       "username": "bob",
 *       "avatar": "http://example.com/avatar/bob.png",
 *       "accuracy": 89,
 *       "score": 80
 *     },
 *     ...
 *   ]
 * }
 *
 * The data field is an array of leaderboard entries, with up to 10 records. Each record includes: username, avatar, accuracy (as an integer percentage), and score (the final ranking score). */
export const fetchRankingData = async () => {
    try {
        const response = await axios.get('/api/tcm/ranking');
        console.log("API 响应数据:", response.data); // Print the full data returned by the API
        return response.data.data;
    } catch (error) {
        console.error('获取排名数据失败:', error);
        return [];
    }
};
/**
 * Get the Prescription Quiz Leaderboard (Top 10)
 *
 * Request method: GET
 * Request URL: `/api/tcm/ranking/prescription`
 *
 * Example request:
 *   GET /api/tcm/ranking/prescription
 *
 * Example response:
 * {
 *   "status": "success",
 *   "data": [
 *     {
 *       "username": "carol",
 *       "avatar": "http://example.com/avatar/carol.png",
 *       "accuracy": 100,
 *       "score": 97
 *     },
 *     ...
 *   ]
 * }
 *
 * The data field is an array of leaderboard entries, with up to 10 records. Each record includes: username, avatar, accuracy (as an integer percentage), and score (the final ranking score). */
export const fetchPrescriptionRankingData = async () => {
    try {
        const response = await axios.get('/api/tcm/ranking/prescription');
        return response.data.data;
    } catch (error) {
        console.error('获取药方小测排名数据失败:', error);
        return [];
    }
};
