import { createRouter, createWebHistory } from 'vue-router'
import StartSeite from './views/StartSeite.vue'
import k_a_together from './components/k_a_together.vue'
import produkte from './components/produkte.vue'
import auftrag from './components/auftrag.vue'
import DSGVO from './components/DSGVO.vue'

const routes = [
    { path: '/', component: StartSeite },
    { path: '/kunden', component: k_a_together },
    { path: '/produkte', component: produkte },
    { path: '/auftrag', component: auftrag },
    { path: '/DSGVO', component: DSGVO },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router