import { defineStore } from 'pinia';
import { register, login, getProfile, getUserInfo, updateUserInfo } from '/src/api/auth/auth.js';
import i18n from '@/i18n';

export const useAuthStore = defineStore('auth', {
    // State properties (reactive)
    state: () => ({
        user: null, // Stores user profile/info
        token: localStorage.getItem('token') || '', // JWT token, persisted across reloads
    }),
    // Methods for user authentication logic
    actions: {

        async registerUser(username, password) {
            try {
                await register(username, password);
                // Notify successful registration
                alert(i18n.global.t('auth.registerSuccess'));
            } catch (error) {
                // Show backend-provided error message if available, else show generic failure message.
                const msg = error.response?.data?.msg;
                alert(msg || i18n.global.t('auth.registerFail'));
            }
        },

        async loginUser(username, password) {
            try {
                const { data } = await login(username, password);
                this.token = data.access_token;
                // Persist token in localStorage for auto-login
                localStorage.setItem('token', data.access_token);
            } catch (error) {
                // Show error message on failure
                const msg = error.response?.data?.msg;
                alert(msg || i18n.global.t('auth.loginFail'));
            }
        },

        async fetchProfile() {
            if (!this.token) return; // Skip if there's no token
            try {
                const { data } = await getProfile(this.token);
                this.user = data.msg; // Save retrieved user info
            } catch (error) {
                // Log a failure to fetch
                console.error(i18n.global.t('auth.fetchProfileFail'));
            }
        },

        async fetchUserInfo() {
            if (!this.token) return;
            try {
                const response = await getUserInfo(this.token);
                if (response.data.code === 0) {
                    // Success: store user data
                    this.user = response.data.data;
                } else {
                    // Failure: log and logout
                    console.error(i18n.global.t('auth.fetchUserInfoFail'), response.data.message);
                    this.logout();
                }
            } catch (error) {
                // Any error: log and logout
                console.error(i18n.global.t('auth.fetchUserInfoFail'), error);
                this.logout();
            }
        },

        async updateUserInfo(updatedData) {
            if (!this.token) return;
            try {
                const response = await updateUserInfo(updatedData, this.token);
                if (response.data.code === 0) {
                    // Update was successful, refresh store state
                    this.user = response.data.data;
                    return response.data; // Return API response to caller
                } else {
                    // API signaled an error
                    throw new Error(response.data.message);
                }
            } catch (error) {
                // Log the error and re-throw for caller to handle
                console.error(i18n.global.t('auth.updateUserInfoFail'), error);
                throw error;
            }
        },

        logout() {
            this.token = '';
            this.user = null;
            localStorage.removeItem('token'); // Remove persisted token
        },
    },
});