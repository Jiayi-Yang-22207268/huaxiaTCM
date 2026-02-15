import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zh from './locales/zh.json'

// Get browser default language (default Chinese if not)
const savedLanguage = localStorage.getItem('lang') || navigator.language.split('-')[0] || 'zh'

const i18n = createI18n({
    legacy: false, // The Vue 3 composable API needs to be set to false
    locale: savedLanguage, // Default language
    fallbackLocale: 'en', // Alternate languages
    messages: { en, zh } // Linguistic data
})

export default i18n
