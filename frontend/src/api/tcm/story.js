import axios from 'axios';

/**
 * Get data for a specific story segment (episode/node).
 *
 * Request method: GET
 * Request URL: `/api/story/{storyId}`
 * Path Parameters:
 *   - storyId: required, number (ID of the story segment to fetch)
 *
 * Example request:
 *   GET /api/story/10
 *
 * Example response:
 * {
 *   "story_number": 10,
 *   "id": 10,
 *   "label": "Hospital Lobby",
 *   "speaker": "Doctor Wang",
 *   "dialog": "Are you here for a checkup?",
 *   "choices": ["Yes, I have an appointment.", "No, I'm visiting a friend."],
 *   "next_id": [11, 12],
 *   "background": "http://example.com/bg.jpg",
 *   "character_image": ["http://example.com/wang.png"],
 *   "audio": "http://example.com/audio1.mp3",
 *   "speaker_en": "Dr. Wang",
 *   "dialog_en": "Are you here for a checkup?",
 *   "choices_en": ["Yes, I have an appointment.", "No, I'm visiting a friend."]
 * }
 *
 * Error response:
 * {
 *   "message": "Story not found"
 * }*/
export const fetchStoryData = async (storyId) => {
    try {
        const response = await axios.get(`/api/story/${storyId}`);
        console.log("当前剧情数据:", response.data); // Prints the current plot data
        return response.data; // Returns the full data of the current episode
    } catch (error) {
        console.error('获取剧情数据失败:', error);
        return null; // If it fails, null is returned
    }
};

/**
 * Get the next possible story segments (episodes/nodes) after the current one.
 *
 * Request method: GET
 * Request URL: `/api/story/next/{storyId}`
 * Path Parameters:
 *   - storyId: required, number (ID of the current story node)
 *
 * Example request:
 *   GET /api/story/next/10
 *
 * Example response:
 * [
 *   {
 *     "story_number": 11,
 *     "id": 11,
 *     "label": "...",
 *     ...[other fields, as above]...
 *   },
 *   {
 *     "story_number": 12,
 *     "id": 12,
 *     "label": "...",
 *     ...[other fields, as above]...
 *   }
 * ]
 *
 * Error response:
 * {
 *   "message": "Story not found"
 * }*/
export const fetchNextStoryData = async (storyId) => {
    try {
        const response = await axios.get(`/api/story/next/${storyId}`);
        console.log("下一步剧情数据:", response.data); //Print the next plot data
        return response.data; // Returns the array data for the next episode
    } catch (error) {
        console.error('获取下一步剧情数据失败:', error);
        return []; // If it fails, an empty array is returned
    }
};

/**
 * Handle branching in the story based on player choice.
 *
 * Parameters:
 *   - currentStoryId (number): The current story node ID.
 *   - optionIndex (number): The index of the player's selected option (matching its position in the choices array).
 *
 * Process:
 *   1. Calls `/api/story/next/{currentStoryId}` to get all next options.
 *   2. Chooses the next story ID based on the selected option index.
 *   3. Calls `/api/story/{nextStoryId}` to fetch the new current story node's full data.
 *
 * Returns:
 *   The full data (object) for the next story node, or null if the selection is invalid or an error occurs.
 *
 * Sample interaction:
 *   handlePlayerChoice(10, 0) will fetch `/api/story/next/10`, pick the first in the array, and return its details.*/
export const handlePlayerChoice = async (currentStoryId, optionIndex) => {
    try {
        const nextStoryData = await fetchNextStoryData(currentStoryId);
        const nextStoryId = nextStoryData[optionIndex]?.id; // Select the ID of the next episode based on the options index
        if (nextStoryId) {
            return await fetchStoryData(nextStoryId); // Get detailed data for the next episode
        } else {
            console.error('无效的选项');
            return null;
        }
    } catch (error) {
        console.error('处理玩家选择失败:', error);
        return null; // If it fails, null is returned
    }
};
