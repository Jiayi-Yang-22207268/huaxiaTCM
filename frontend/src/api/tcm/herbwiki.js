import axios from 'axios';

// Automatically adapt to development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000/api'
    : '/api';

/**
 * Get All Herb Categories
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/herbs/categories?lang=zh`
 * Request Query Parameters:
 *   - lang: optional, language ("zh" for Chinese, "en" for English); defaults to "zh"
 *
 * Example request:
 *   GET /api/herbs/categories?lang=zh
 *
 * Example response:
 *   ["根茎类", "叶类", "花类"]
 */
export const getHerbCategories = async (lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/herbs/categories`, {
            params: { lang }  // 传递语言参数
        });
        return response.data; // 例: ["根茎类", "叶类", "花类"]
    } catch (error) {
        console.error(`获取药材分类失败: ${error.message}`);
        return [];
    }
};

/**
 * Get the First Twenty Herbs (Common Herbs)
 *
 * Request method: POST
 * Request URL: `${API_BASE_URL}/herbs/usefulHerbs?lang=zh`
 * Request Query Parameters:
 *   - lang: optional, language ("zh" for Chinese, "en" for English); defaults to "zh"
 * Request Body: (none)
 *
 * Example request:
 *   POST /api/herbs/usefulHerbs?lang=en
 *
 * Example response:
 * [
 *   { "id": 1, "name": "Astragalus", "image": "http://..." },
 *   { "id": 2, "name": "Ginseng", "image": "http://..." },
 *   ...
 * ]
 */
export const getUsefulHerbs = async (lang = 'zh') =>{
    try {
        const response = await axios.post(`${API_BASE_URL}/herbs/usefulHerbs`, null, {
            params: { lang }  // Pass params By lang
        });
        return response.data;
    } catch (error) {
        console.error(`获取常用药材失败: ${error.message}`);
        return [];
    }
};


/**
 * Get All Herbal Flavor (Property) Classifications
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/herbs/classifications?lang=zh`
 * Request Query Parameters:
 *   - lang: optional, language ("zh" for Chinese, "en" for English); defaults to "zh"
 *
 * Example request:
 *   GET /api/herbs/classifications?lang=en
 *
 * Example response:
 *   ["温", "凉", "平", "寒"]
 */
export const getHerbClassifications = async (lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/herbs/classifications`, {
            params: { lang }  // Pass the language parameters
        });
        return response.data;
    } catch (error) {
        console.error(`获取药材性味分类失败: ${error.message}`);
        return [];
    }
};

// Get herbs in a category (get ID, Name, IMAGE)
/**
 * Get Herbs by Category
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/herbs/{category}?lang=zh`
 * Request Query Parameters:
 *   - lang: optional, language ("zh" for Chinese, "en" for English); defaults to "zh"
 *
 * Example request:
 *   GET /api/herbs/根茎类?lang=zh
 *
 * Example response:
 * [
 *   { "id": 1, "name": "黄芪", "image": "http://..." },
 *   { "id": 2, "name": "人参", "image": "http://..." }
 * ]
 *
 * Errors:
 *   { "error": "No herbs found with category 根茎类" }
 */
export const getHerbsByCategory = async (category, lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/herbs/${category}`, {
            params: { lang }  // 传递语言参数
        });
        return response.data.map(h => ({
            id: h.id,
            name: h.name,  // The API returns names in different languages
            image: h.image
        }));
    } catch (error) {
        console.error(`获取药材列表失败: ${error.message}`);
        return [];
    }
};

// Get herbs in a classification (get ID, Name, IMAGE)
/**
 * Get Herbs by Classification
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/herbs/classification/{classification}?lang=zh`
 * Request Query Parameters:
 *   - lang: optional, language ("zh"/"en"); defaults to "zh"
 *
 * Example request:
 *   GET /api/herbs/classification/辛温?lang=zh
 *
 * Example response:
 * [
 *   { "id": 1, "name": "紫苏叶", "image": "http://..." },
 *   { "id": 2, "name": "姜", "image": "http://..." }
 * ]
 *
 * Errors:
 *   { "error": "No herbs found with category 辛温" }
 */
export const getHerbsByClassification = async (classification, lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/herbs/classification/${classification}`, {
            params: { lang }  // Pass the language parameters
        });
        return response.data.map(h => ({
            id: h.id,
            name: h.name,  // The API returns names in different languages
            image: h.image
        }));
    } catch (error) {
        console.error(`获取药材列表失败: ${error.message}`);
        return [];
    }
};

/**
 * Get Details of an Individual Herb
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/herbs/{id}?lang=zh`
 * Request Query Parameters:
 *   - lang: optional, language ("zh"/"en"); defaults to "zh"
 *
 * Example request:
 *   GET /api/herbs/1?lang=en
 *
 * Example response:
 * {
 *   "id": 1,
 *   "name": "Astragalus",
 *   "cnName": "黄芪",
 *   "category": "Rhizomes",
 *   "origin": "...",
 *   "production_regions": "...",
 *   "properties": "...",
 *   "functions": "...",
 *   "image": "http://...",
 *   "relate_prescription": ["处方A", "处方B"],
 *   "relate_prescription_id": [101, 102],
 *   "classification": "Roots and Rhizomes"
 * }
 *
 * Errors:
 *   { "error": "No prescription found" }
 */
export const getHerbDetail = async (id, lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/herbs/${id}`, {
            params: { lang }  // Pass the language parameters
        });
        return response.data;
    } catch (error) {
        console.error(`获取药材详情失败: ${error.message}`);
        return null;
    }
};

/**
 * Batch Get Herb Names by IDs
 *
 * Request method: POST
 * Request URL: `${API_BASE_URL}/herbs/batchNames`
 * Request body:
 *  {
 *    ids: [1, 2, 3],
 *    lang: "zh"
 *  }
 *
 * Response example:
 *  [
 *    { id: 1, name: "黄芪" },
 *    { id: 2, name: "当归" },
 *    { id: 3, name: "白术" }
 *  ]
 *
 * Errors:
 *  返回 null 并打印错误信息
 */
export const getHerbNamesBatch = async (ids, lang = 'zh') => {
    try {
        const response = await axios.post(`${API_BASE_URL}/herbs/batchNames`, {
            ids,
            lang
        });
        return response.data;  // 假设返回直接是数组
    } catch (error) {
        console.error(`批量获取药材名称失败: ${error.message}`);
        return null;
    }
};

// Search for herbs (vague matching based on name)
/**
 * Search for Herbs by Name (Fuzzy Match)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/herbs/search?name={query}&lang=zh`
 * Request Query Parameters:
 *   - name: string, required, search keyword (Chinese or English)
 *   - lang: optional, language ("zh"/"en"); defaults to "zh"
 *
 * Example request:
 *   GET /api/herbs/search?name=芪&lang=zh
 *
 * Example response:
 * [
 *   { "id": 1, "name": "黄芪", "image": "http://..." },
 *   { "id": 2, "name": "党参", "image": "http://..." }
 * ]
 *
 * Errors:
 *   { "error": "No name provided" }
 *   { "error": "..." } // any server error
 */
export const searchHerbsByName = async (query, lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/herbs/search`, {
            params: { name: query, lang }  // Pass the language parameters
        });
        return response.data.map(h => ({
            id: h.id,
            name: h.name,  // The API returns names in different languages
            image: h.image
        }));
    } catch (error) {
        console.error(`搜索药材失败: ${error.message}`);
        return [];
    }
};

/**
 * Get Full Details of an Individual Herb (Admin)
 *
 * Request method: GET
 * Request URL: `${API_BASE_URL}/admin/getHerbDetails/{id}?lang=zh`
 * Request Query Parameters:
 *   - lang: optional, language ("zh" for Chinese, "en" for English); defaults to "zh"
 *   - id: required, herb ID, path parameter
 *
 * Example request:
 *   GET /api/admin/getHerbDetails/1?lang=zh
 *
 * Example response:
 * {
 *   "id": 1,
 *   "name_en": "Astragalus",
 *   "name_zh": "黄芪",
 *   "category_en": "Roots and Rhizomes",
 *   "category_zh": "根茎类",
 *   "origin_en": "...",
 *   "origin_zh": "...",
 *   "production_regions_en": "...",
 *   "production_regions_zh": "...",
 *   "properties_en": "...",
 *   "properties_zh": "...",
 *   "functions_en": "...",
 *   "functions_zh": "...",
 *   "image_en": "http://...",
 *   "image_zh": "http://...",
 *   "classification_en": "...",
 *   "classification_zh": "..."
 * }
 */
export const getHerbDetailAdmin = async (id, lang = 'zh') => {
    try {
        const response = await axios.get(`${API_BASE_URL}/admin/getHerbDetails/${id}`, {
            params: { lang }  // Pass the language parameters
        });
        return response.data;
    } catch (error) {
        console.error(`获取药材详情失败: ${error.message}`);
        return null;
    }
};


/**
 * Edit Herb Details (Admin Version)
 *
 * Request method: PUT
 * Request URL: '${API_BASE_URL}/herbs/admin/{id}? lang=zh'
 * Request Body Format:
 * {
 The * // id field is implicitly passed by the frontend and does not require user input
 * "name_zh": "Astragalus",
 * "name_en": "Astragalus",
 * “image_zh”： “http://example.com/huangqi_zh.jpg”，
 * “image_en”： “http://example.com/huangqi_en.jpg”，
 * "category_zh": "rhizomes",
 * "category_en": "roots and rhizomes",
 * "origin_zh": "somewhere",
 * "origin_en": "somewhere",
 * "production_regions_zh": "Zone 1",
 * "production_regions_en": "Zone 1",
 * "properties_zh": "nature Chinese",
 * "properties_en": "English Attributes",
 * "functions_zh": "Chinese of efficacy",
 * "functions_en": "function in English",
 * "classification_zh": "return to the Chinese",
 * "classification_en": "English classification",
 * "action": 0 // 0 for editing
 * }
 *
 * Example of response format:
 * {
 * “code”： 0，
 * "data": { ... Updated Medicinal Herb Detail Data... },
 * "message": "Update successful"
 * }
 */
export const updateHerbDetailAdmin = async (herbData, lang = 'zh') => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/admin/addHerb`,
            { ...herbData, action: 0 },  // The id is included in the herbData, but it is not displayed in the URL
            { params: { lang } }
        );
        return response.data;
    } catch (error) {
        console.error(`更新药材详情失败: ${error.message}`);
        return null;
    }
};

/**
 * Add new herbs (Admin Version)
 *
 * Request method: PUT
 * Request URL: '${API_BASE_URL}/herbs/admin/? lang=zh'
 * Request Body Format:
 * {
 * // id field is blank or not passed
 * "name_zh": "New Herb Chinese Name",
 * "name_en": "name of the new herb",
 * “image_zh”： “http://example.com/new_herb_zh.jpg”，
 * “image_en”： “http://example.com/new_herb_en.jpg”，
 * "category_zh": "Classification Chinese",
 * "category_en": "English classification",
 * "origin_zh": "Origin Chinese",
 * "origin_en": "English Origin",
 * "production_regions_zh": "Production area Chinese",
 * "production_regions_en": "English production area",
 * "properties_zh": "Medicinal herbs Chinese properties",
 * "properties_en": "English Attributes",
 * "functions_zh": "Chinese of efficacy",
 * "functions_en": "function in English",
 * "classification_zh": "return to the Chinese",
 * "classification_en": "English classification",
 * "action": 1 // 1 indicates addition
 * }
 *
 * Example of response format:
 * {
 * “code”： 0，
 * "data": { ... Newly added medicinal herb details... },
 * "message": "Added successfully"
 * }
 */
export const addHerbDetailAdmin = async (herbData, lang = 'zh') => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/admin/addHerb`,
            { ...herbData, action: 1 },
            { params: { lang } }
        );
        return response.data;
    } catch (error) {
        console.error(`添加药材失败: ${error.message}`);
        return null;
    }
};

/**
 * Delete herbs (Admin version)
 *
 * Request: DELETE
 * Request URL: '${API_BASE_URL}/herbs/admin/?lang=en'
 * Request body format (example):
 * {
 *   "id": 123
 * }
 *
 * Example of response format:
 * {
 *   "code": 0,
 *   "data": null,
 * "message": "Deleted successfully"
 * }
 */
export const deleteHerbDetailAdmin = async (data, lang = 'zh') => {
    try {
        const response = await axios.delete(
            `${API_BASE_URL}/admin/deleteHerb`,
            { params: { lang }, data }
        );
        return response.data;
    } catch (error) {
        console.error(`删除药材失败: ${error.message}`);
        return null;
    }
};