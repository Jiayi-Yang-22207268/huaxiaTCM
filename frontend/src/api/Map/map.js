import polyline from 'polyline';

// Automatically adapt to development and production environments
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://127.0.0.1:5000'
    : '';

/**
 * Fetch the geographic production areas of a specific herb
 * Request method: GET
 * Request URL: '${API_BASE_URL}/api/areas/herb/<herbId>?lang=<lang>'
 * Request parameters:
 * - herbId: <int> (Required) The unique ID of the herb
 * - lang: <string> (Optional) Language preference ('zh' for Chinese, 'en' for English); defaults to 'zh'
 * Example URL:
 * - '${API_BASE_URL}/api/areas/herb/1?lang=zh'
 *
 * Example of backend response:
 * {
 *   "areas": [
 *     {
 *       "type": "Polygon",
 *       "coordinates": [
 *         [lat1, lon1],
 *         [lat2, lon2],
 *         ...
 *       ]
 *     },
 *     {
 *       "type": "MultiPolygon",
 *       "coordinates": [
 *         [
 *           [lat1, lon1],
 *           [lat2, lon2],
 *           ...
 *         ],
 *         ...
 *       ]
 *     }
 *   ]
 * }
 *
 * Error responses:
 * - HTTP status code 500: Server error, e.g., "几何类型不支持" (Unsupported geometry type)
 */
export async function fetchHerbArea(herbId, lang = 'zh') {
    try {
        const response = await fetch(`${API_BASE_URL}/api/areas/herb/${herbId}?lang=${lang}`);
        if (!response.ok) {
            throw new Error(`HTTP 错误！状态码: ${response.status}`);
        }
        const data = await response.json();
        console.log("获取的产区数据：", data);  // Prints the returned appellation data
        return data;
    } catch (error) {
        console.error(`获取药材产区数据失败: ${error.message}`);
        return null;
    }
}

// Get Tags in Database
export async function fetchMarkers() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/markers`);
        if (!response.ok) {
            throw new Error(`HTTP 错误！状态码: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`获取数据库标记失败: ${error.message}`);
        return { markers: [] };
    }
}

// Get the location of the employee in the database
export async function fetchWorkers() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/workers`);
        if (!response.ok) {
            throw new Error(`HTTP 错误！状态码: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`获取员工位置失败: ${error.message}`);
        return { workers: [] };
    }
}


// Get the region in the database
export async function fetchAreas() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/areas`);
        if (!response.ok) {
            throw new Error(`HTTP 错误！状态码: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`获取区域数据失败: ${error.message}`);
        return { areas: [] };
    }
}

// Get the route data
export async function getRoute(start, end) {
    try {
        const url = `https://router.project-osrm.org/route/v1/driving/${start[1]},${start[0]};${end[1]},${end[0]}?overview=full&steps=true`;
        const response = await fetch(url);
        if (!response.ok) return [];

        const data = await response.json();
        return data.routes && data.routes.length > 0 ? polyline.decode(data.routes[0].geometry) : [];
    } catch (error) {
        console.error(`获取路径失败: ${error.message}`);
        return [];
    }
}

// Get multiple paths in the database
export async function fetchRoutes() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/dispatch`);
        if (!response.ok) {
            throw new Error(`HTTP 错误！状态码: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`获取路径数据失败: ${error.message}`);
        return { routes: [] };
    }
}



