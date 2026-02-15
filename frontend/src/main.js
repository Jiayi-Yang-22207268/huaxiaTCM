import './assets/css/main.css';
import { createApp } from 'vue';
import { createPinia } from 'pinia'; // Introducing Pinia
import App from './App.vue';
import router from './router';  // Ingestion routes
import { createI18n } from 'vue-i18n'
import animateOnScroll from '/src/assets/directives/animateOnScroll'
import '@/assets/css/base.css';
import '@/assets/css/layout.css';
import '@/assets/css/component.css';
import '@/assets/css/animation.css';
import zhMessages from './locales/zh.json';
import enMessages from './locales/en.json';

const savedLang = localStorage.getItem('lang') || 'zh'

const i18n = createI18n({
    legacy: false,
    locale: savedLang,
    fallbackLocale: 'zh',
    messages: {
        zh: zhMessages,
        en: enMessages
    }
})
const app = createApp(App);
const pinia = createPinia();

app.directive('animate-on-scroll', animateOnScroll)
app.use(i18n)
app.use(pinia); // Sign up for Pinia first
app.use(router); // Then, Register Pinia
app.mount('#app'); // Finally, mount the Vue app
