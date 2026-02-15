import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './components/HomePage.vue'
import NewPage from './components/NewPage.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import PersonalPage from './components/PersonalPage.vue'
import PrescriptionList from './components/wiki/PrescriptionList.vue'
import PrescriptionDetail from './components/wiki/PrescriptionDetail.vue'
import HerbList from './components/wiki/HerbList.vue'
import HerbDetail from './components/wiki/HerbDetail.vue'
import GamePage from './components/game/GamePage.vue'
import QuizPage from './components/quiz/QuizPage.vue'
import AdminPage from './components/admin/AdminPage.vue'
import HerbManagement from './components/admin/HerbManagement.vue'
import PrescriptionManagement from './components/admin/PrescriptionManagement.vue'
import { useAuthStore } from '@/stores/authStore'
import i18n from './i18n'
import UserManagement from "@/components/admin/UserManagement.vue";
// Added the homepage image management page
import HomepageManagement from './components/admin/HomepageManagement.vue'
import NewHomePage from "@/components/NewHomePage.vue";
import story1 from "@/components/story/story1.vue";
import StoryHome from "@/components/story/StoryHome.vue";
import LogManagement from './components/admin/LogManagement.vue'
import HerbGame from "@/components/game/HerbGame.vue";
import PrescriptionGame from "@/components/game/PrescriptionGame.vue";
import storyUncompletePage from "@/components/story/storyUncompletePage.vue";
import Document from '@/components/Document.vue'

const routes = [
    { path: '/:lang/home', name: 'Home', component: HomePage },
    { path: '/:lang/new-page', name: 'NewPage', component: NewPage },
    { path: '/:lang/login', name: 'Login', component: Login },
    { path: '/:lang/register', name: 'Register', component: Register },
    { path: '/:lang/personal', name: 'PersonalPage', component: PersonalPage, meta: { requiresAuth: true } },
    { path: '/:lang/prescriptions', name: 'PrescriptionList', component: PrescriptionList },
    { path: '/:lang/prescriptions/:id', name: 'PrescriptionDetail', component: PrescriptionDetail, props: true },
    { path: '/:lang/herbs', name: 'HerbList', component: HerbList },
    { path: '/:lang/herbs/:id', name: 'HerbDetail', component: HerbDetail, props: true },
    { path: '/:lang/game', name: 'GamePage', component: GamePage },
    { path: '/:lang/quiz', name: 'QuizPage', component: QuizPage },
    { path: '/:lang/story', name: 'Story', component: StoryHome },
    { path: '/:lang/game/herbGame', name: 'HerbGame', component: HerbGame },
    { path: '/:lang/game/prescriptionGame', name: 'PrescriptionGame', component: PrescriptionGame },



    // New: Dynamic routing to load story pages
    {
        path: '/:lang/story/:storyId',  // Dynamic paths that load specific story pages based on the storyId
        name: 'story1',
        component: story1,
        props: true  // Enable props so that the storyId can be passed as a prop for the component
    },
    {
        path: '/:lang/story/UncompletedPage/:storyId',
        name: 'storyUncompletePage',
        component: storyUncompletePage,
        props: true
    },

    // Added management page routing with sub-routes
    {
        path: '/:lang/admin',
        name: 'AdminPage',
        component: AdminPage,
        meta: { requiresAuth: true, requiresAdmin: true },
        redirect: to => `/${to.params.lang}/admin/herbs`, // Automatically redirects to /:lang/admin/herbs when accessing /:lang/admin
        children: [
            { path: 'herbs', name: 'HerbManagement', component: HerbManagement, props: true },
            { path: 'prescriptions', name: 'PrescriptionManagement', component: PrescriptionManagement, props: true },
            { path: 'users', name: 'UserManagement', component: UserManagement, props: true },
            { path: 'log',           name: 'LogManagement',         component: LogManagement,         props: true },
            // New: Homepage image management routing
            { path: 'homepage', name: 'HomepageManagement', component: HomepageManagement, props: true }
        ]
    },
    // Doucment page routing
    {
    path: '/:lang/document',
    name: 'Document',
    component: Document,
    meta: { public: true } // Optional: Mark as a public page
  }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Authentication Route Guard & Language Switching
router.beforeEach(async (to, from, next) => {
    // console.log('目标路由:', to)
    const authStore = useAuthStore()
    const lang = to.params.lang

    // Only 'zh' and 'en' are allowed as languages
    if (!['zh', 'en'].includes(lang)) {
        console.log(`Languages ${lang} are not allowed, redirecting to /zh/home`)
        return next('/zh/home')
    }

    // Toggle the i18n language
    i18n.global.locale = lang
    localStorage.setItem('lang', lang);
    console.log(`当前语言设置为: ${lang}`)

    // If the token exists but the user information is empty, then an attempt is made to load the user information
    if (authStore.token && !authStore.user) {
        try {
            await authStore.fetchUserInfo();
        } catch (error) {
            console.error('failed To Load User Information', error);
        }
    }

    // Check if you need to sign in
    if (to.meta.requiresAuth && !authStore.token) {
        console.log('Login required, but no token, redirects to the login page')
        return next(`/${lang}/login`)
    }

    // Check if administrator privileges are required
    if (to.meta.requiresAdmin && (!authStore.user || authStore.user.role !== 'admin')) {
        console.log('Without admin privileges, redirect to the home page')
        return next(`/${lang}/home`)
    }

    next()
})



export default router
