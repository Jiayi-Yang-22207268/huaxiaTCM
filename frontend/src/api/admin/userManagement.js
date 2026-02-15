import axios from 'axios';

// Automatically adapt to the API root path for development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'
    : '/api';

/**
 * Get all user information
 * Request method: GET
 * Request URL: '${API_BASE_URL}/users'
 * Request parameter: An optional language parameter, e.g. ?lang=zh
 * Example of backend response:
 * {
 *   "code": 0,
 *   "data": [
 *     { "id": 1, "username": "user1", "role": "user", ... },
 *     { "id": 2, "username": "admin", "role": "admin", ... }
 *   ],
 * "message": "query successful"
 * }
 */
export const getAllUsers = async (lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/admin/getAllUsers`, {
            params: { lang }
        });
        return response.data;
    } catch (error) {
        console.error(`获取所有用户信息失败: ${error.message}`);
        return null;
    }
};

/**
 * Update user information
 * Request method: PUT
 * Request URL: '${API_BASE_URL}/users/' // id is no longer concatenated in the URL, but is implicitly passed through the request body
 * Request parameter: language parameter (e.g. ?lang=zh)
 * Request body format (example):
 * {
 * "id": 1,
 *   "username": "newUsername",
 *   "role": "user"
 * }
 * Example of backend response:
 * {
 *   "code": 0,
 *   "data": { "id": 1, "username": "newUsername", "role": "user", ... },
 * "message": "Update successful"
 * }
 */
export const updateUser = async (userData, lang = 'zh') => {
    try {
        const response = await axios.put(
            `${API_BASE_URL}/admin/updateUser`,
            userData, // The id field must be included in the userData
            { params: { lang } }
        );
        return response.data;
    } catch (error) {
        console.error(`更新用户信息失败: ${error.message}`);
        return null;
    }
};

/**
 * Delete user information
 * Request: DELETE
 * Request URL: '${API_BASE_URL}/users/' // id is no longer concatenated in the URL
 * Request parameter: language parameter (e.g. ?lang=zh)
 * Request body format (example):
 * {
 *   "id": 1
 * }
 * Example of backend response:
 * {
 *   "code": 0,
 *   "data": null,
 * "message": "Deleted successfully"
 * }
 */
export const deleteUser = async (id, lang = 'zh') => {
    try {
        const response = await axios.delete(
            `${API_BASE_URL}/admin/deleteUser`,
            { params: { lang }, data: { id } } // 使用 axios.delete 的 data 选项隐式传递 id
        );
        return response.data;
    } catch (error) {
        console.error(`删除用户失败: ${error.message}`);
        return null;
    }
};

/**
 * Create a new user (Admin Edition)
 * Request method: POST
 * Request URL: '${API_BASE_URL}/admin/createUser'
 * Request Parameters: Language parameters (e.g. ? lang=zh）
 * Request body format (example):
 * {
 * "Username": "New User",
 * "role": "user", // "admin" or "client"
 * “height”： 170，
 * “weight”： 60，
 * "Age": 25,
 * “password”： “newPassword”
 * }
 * Example of backend response:
 * {
 * “code”： 0，
 * “data”： { “id”： 123， “username”： “newUser”， “role”： “user”， ... }，
 * "message": "Created successfully"
 * }
 */
export const createUser = async (userData, lang = 'zh') => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/admin/addUser`,
            userData,
            { params: { lang } }
        );
        return response.data;
    } catch (error) {
        console.error(`创建用户失败: ${error.message}`);
        return null;
    }
};

/**
 * Modify user avatar (Admin interface)
 * Request method: POST
 * Request URL: '${API_BASE_URL}/admin/changeUserAvatar/${userId}'
 * Request Parameters:
 * - lang (optional, query parameter)
 * Request Body (FormData):
 *   - avatar: File
 */
export const changeUserAvatar = async (file, userId, lang = 'zh') => {
    try {
        const formData = new FormData();
        formData.append('avatar', file);

        const response = await axios.post(
            `${API_BASE_URL}/admin/changeUserAvatar/${userId}`,
            formData,
            {
                params: { lang }
                // Don't set the Content-Type manually, axios will automatically complete the boundary
            }
        );

        return response.data; // { message: 'File uploaded successfully' }
    } catch (error) {
        console.error(`修改用户头像失败: ${error.message}`);
        throw error;
    }
};

/**
 * Get the avatar of the currently logged-in user
 * Request method: GET
 * Request URL: '${API_BASE_URL}/user/getAvatar'
 * Request header: Authorization: <token>Bearer
 * Return: { avatar: string }
 */
export const getAvatar = async (token) => {
    try {
        const response = await axios.get(
            `${API_BASE_URL}/user/getAvatar`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        return response.data.avatar || null;
    } catch (error) {
        console.error(`获取头像失败: ${error.message}`);
        return null;
    }
};