import axios from 'axios';

// Automatically adapt to the API root path for development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'  // Development environment
    : '/api'; // Production environment

/**
 * Register a new user
 * Request method: POST
 * Request URL: '${API_BASE_URL}/register'
 * Content type: application/json
 * Request body:
 * {
 *   "username": <string>,  // The username of the user
 *   "password": <string>   // The password of the user
 * }
 * Example of backend response:
 * {
 *   "msg": "Registration is successful"  // Success message
 * }
 * Error responses:
 * {
 *   "msg": "The username and password cannot be empty" // Missing fields
 * }
 * {
 *   "msg": "The username already exists" // Duplicate username
 * }*/
export const register = (username, password) => {
    return axios.post(`${API_BASE_URL}/register`, { username, password });
};

/**
 * Login a user
 * Request method: POST
 * Request URL: '${API_BASE_URL}/login'
 * Content type: application/json
 * Request body:
 * {
 *   "username": <string>,  // The username of the user
 *   "password": <string>   // The password of the user
 * }
 * Example of backend response:
 * {
 *   "access_token": <string>  // JWT token for the authenticated session
 * }
 * Error responses:
 * {
 *   "msg": "The username and password cannot be empty" // Missing fields
 * }
 * {
 *   "msg": "Wrong username or password" // Invalid credentials
 * }*/
export const login = (username, password) => {
    return axios.post(`${API_BASE_URL}/login`, { username, password });
};

/**
 * Get the profile information of the logged-in user
 * Request method: GET
 * Request URL: '${API_BASE_URL}/profile'
 * Request header: Authorization: <token>Bearer
 * Example of backend response:
 * {
 *   "msg": "Welcome <username>，This is your personal information" // Personalized welcome message
 * }
 * Error responses:
 * {
 *   "msg": "Missing Authorization Header"  // Missing or invalid token
 * }*/
export const getProfile = (token) => {
    return axios.get(`${API_BASE_URL}/profile`, {
        headers: { Authorization: `Bearer ${token}` },
    });
};

/**
 * Get complete information about the logged-in user, including height, weight, age, etc.
 * Request method: GET
 * Request URL: '${API_BASE_URL}/user/info'
 * Request header: Authorization: <token>Bearer
 * Example of backend response:
 * {
 *   "code": 0,
 *   "data": {
 *     "id": <int>,          // User ID
 *     "username": <string>, // Username
 *     "height": <float>,    // Height in cm
 *     "weight": <float>,    // Weight in kg
 *     "age": <int>,         // Age in years
 *     "role": <string>      // Role of the user (e.g., admin, user)
 *   },
 *   "message": "Success"
 * }
 * Error responses:
 * {
 *   "msg": "Missing Authorization Header"  // Missing or invalid token
 * }*/
export const getUserInfo = (token) => {
    return axios.get(`${API_BASE_URL}/user/info`, {
        headers: { Authorization: `Bearer ${token}` },
    });
};

/**
 * Update user information (height, weight, age)
 * Request method: PUT
 * Request URL: '${API_BASE_URL}/user/info'
 * Content type: application/json
 * Request header: Authorization: <token>Bearer
 * Request body:
 * {
 *   "height": <float>,  // Height in cm
 *   "weight": <float>,  // Weight in kg
 *   "age": <int>        // Age in years
 * }
 * Example of backend response:
 * {
 *   "code": 0,
 *   "data": {
 *     "id": <int>,          // User ID
 *     "username": <string>, // Username
 *     "height": <float>,    // Updated height
 *     "weight": <float>,    // Updated weight
 *     "age": <int>          // Updated age
 *   },
 *   "message": "Profile updated successfully!"
 * }
 * Error responses:
 * {
 *   "msg": "Missing Authorization Header"  // Missing or invalid token
 * }*/
 export const updateUserInfo = (data, token) => {
    return axios.put(`${API_BASE_URL}/user/info`, data, {
        headers: { Authorization: `Bearer ${token}` },
    });
};

/**
 * Upload a user avatar
 * Request method: POST
 * Request URL: '${API_BASE_URL}/user/avatar'
 * Request header: Authorization: <token>Bearer
 * Content type: multipart/form-data
 * Request body: FormData, field name avatar
 * Example of backend response:
 * {
 * "message": "File uploaded successfully"
 * }
 */
export const uploadAvatar = async (file, token) => {
    try {
        const formData = new FormData();
        formData.append('avatar', file);

        const response = await axios.post(
            `${API_BASE_URL}/user/avatar`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer ${token}`
                }
            }
        );
        return response.data; // { message: 'File uploaded successfully' }
    } catch (error) {
        console.error(`上传头像失败: ${error.message}`);
        throw error;
    }
};
