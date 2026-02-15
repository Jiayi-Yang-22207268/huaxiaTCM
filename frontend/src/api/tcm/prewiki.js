import axios from 'axios';

// Automatically adapt to development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'
    : '/api';

/**
 * Get All Prescriptions (IDs and Names)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/prescriptions?lang=zh`
 * Query Parameters:
 *   - lang: optional, language ("zh" for Chinese, "en" for English); defaults to "zh"
 *
 * Example request:
 *   GET /api/prescriptions?lang=en
 *
 * Example response:
 * [
 *   { "id": 1, "name": "四君子汤" },
 *   { "id": 2, "name": "六味地黄丸" }
 * ]*/
export const getPrescriptions = async (lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/prescriptions`, {
            params: { lang }  // Pass the language parameters
        });
        return response.data.map(p => ({
            id: p.id,
            name: p.name  // The API returns names in different languages
        }));
    } catch (error) {
        console.error(`获取药方列表失败: ${error.message}`);
        return [];
    }
};

/**
 * Get Individual Prescription Details (full data)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/prescriptions/{id}?lang=zh`
 * Path Parameters:
 *   - id: required, prescription ID
 * Query Parameters:
 *   - lang: optional, language ("zh" or "en"); defaults to "zh"
 *
 * Example request:
 *   GET /api/prescriptions/1?lang=zh
 *
 * Example response:
 * {
 *   "id": 1,
 *   "name": "四君子汤",
 *   "cnName": "四君子汤",
 *   "constitute": "人参; 白术; 茯苓; 甘草",
 *   "constituteId": [1, 2, 3, 4],
 *   "action": "补气",
 *   "indication": "气虚"
 * }
 *
 * Error:
 *   { "error": "No prescription found" }*/
export const getPrescriptionDetail = async (id, lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/prescriptions/${id}`, {
            params: { lang }  // Pass the language parameters
        });
        return response.data;
    } catch (error) {
        console.error(`获取药方详情失败: ${error.message}`);
        return null;
    }
};
/**
 * Get Individual Prescription Details for Admin (Both English and Chinese Data)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/admin/getPrescriptionDetails/{id}?lang=zh`
 * Path Parameters:
 *   - id: required, prescription ID
 * Query Parameters:
 *   - lang: optional ("zh" or "en"); defaults to "zh"
 *
 * Example request:
 *   GET /api/admin/getPrescriptionDetails/1?lang=zh
 *
 * Example response:
 * {
 *   "id": 1,
 *   "name_en": "Si Jun Zi Tang",
 *   "name_zh": "四君子汤",
 *   "constitute_en": "Ginseng; Atractylodes; Poria; Licorice",
 *   "constitute_zh": "人参; 白术; 茯苓; 甘草",
 *   "action_en": "Tonifies Qi",
 *   "action_zh": "补气",
 *   "indication_en": "Qi deficiency",
 *   "indication_zh": "气虚"
 *   // ...other fields as per your backend...
 * }*/
export const getPrescriptionDetailAdmin = async (id, lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/admin/getPrescriptionDetails/${id}`, {
            params: { lang }  // Pass the language parameters
        });
        return response.data;
    } catch (error) {
        console.error(`获取药方详情失败: ${error.message}`);
        return null;
    }
};
/**
 * Search Prescriptions by Name (Fuzzy Search)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/prescriptions/search?name={query}&lang=zh`
 * Query Parameters:
 *   - name: required, search keyword
 *   - lang: optional ("zh" or "en"); defaults to "zh"
 *
 * Example request:
 *   GET /api/prescriptions/search?name=四君&lang=zh
 *
 * Example response:
 * [
 *   { "id": 1, "name": "四君子汤" }
 * ]
 *
 * Error:
 *   { "error": "No name provided" }
 *   { "error": "...internal error..." }*/
export const searchPrescriptionsByName = async (query, lang) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/prescriptions/search`, {
            params: { name: query, lang }
        });
        return response.data;
    } catch (error) {
        console.error(`搜索方剂失败: ${error.message}`);
        return [];
    }
};
/**
 * Add Prescription (Admin)
 *
 * Request method: POST
 * Request URL: `${API_BASE_URL}/admin/addPrescription?lang=zh`
 * Query Parameters:
 *   - lang: optional ("zh" or "en"); defaults to "zh"
 * Request Body:
 *   {
 *     // No `id` field
 *     "name_zh": "新方剂名",
 *     "name_en": "New Prescription Name",
 *     "constitute_zh": "...",
 *     "constitute_en": "...",
 *     "action_zh": "...",
 *     "action_en": "...",
 *     "indication_zh": "...",
 *     "indication_en": "...",
 *     "action": 1 // 1 indicates addition
 *   }
 *
 * Example response:
 * {
 *   "code": 0,
 *   "data": { ...newly created prescription info... },
 *   "message": "Added successfully"
 * }*/
export const addPrescription = async (data, lang = 'zh') => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/admin/addPrescription`,
            {...data, action: 1},
            {params: { lang }
        });
        return response.data;
    } catch (error) {
        console.error(`添加药方失败: ${error.message}`);
        return null;
    }
};

/**
 * Update Prescription (Admin)
 *
 * Request method: POST
 * Request URL: `${API_BASE_URL}/admin/addPrescription?lang=zh`
 * Query Parameters:
 *   - lang: optional ("zh" or "en"); defaults to "zh"
 * Request Body:
 *   {
 *     "id": 123,
 *     "name_zh": "四君子汤",
 *     "name_en": "Si Jun Zi Tang",
 *     // ... other fields ...
 *     "action": 0 // 0 indicates update
 *   }
 *
 * Example response:
 * {
 *   "code": 0,
 *   "data": { ...updated prescription info... },
 *   "message": "Update successful"
 * }*/
export const updatePrescription = async (data, lang = 'zh') => {
    try {
        const response = await axios.post(`${API_BASE_URL}/admin/addPrescription`,
            {...data, action: 0},
            {params: { lang }
        });
        return response.data;
    } catch (error) {
        console.error(`更新药方失败: ${error.message}`);
        return { code: -1, message: '更新失败' };
    }
};

/**
 * Delete Prescription (Admin)
 *
 * Request method: DELETE
 * Request URL: `${API_BASE_URL}/admin/deletePrescription`
 * Request Body:
 *   {
 *     "id": 123,  // prescription ID
 *     "lang": "zh"
 *   }
 *
 * Example response:
 * {
 *   "code": 0,
 *   "data": null,
 *   "message": "Deleted successfully"
 * }*/
export const deletePrescription = async (id, lang = 'zh') => {
    try {
        const response = await axios.delete(`${API_BASE_URL}/admin/deletePrescription`, {
            data: { id, lang }
        });
        return response.data;
    } catch (error) {
        console.error(`删除药方失败: ${error.message}`);
        return { code: -1, message: '删除失败' };
    }
};