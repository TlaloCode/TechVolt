const development = process.env.NODE_ENV !== 'production'

export default {
    // Target: https://go.nuxtjs.dev/config-target
    target: 'static',
    ssr: false,
    // Global page headers: https://go.nuxtjs.dev/config-head
    head: {
        title: 'FYG Training',
        htmlAttrs: {
            lang: 'es',
        },
        meta: [
            { charset: 'utf-8' },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            { hid: 'description', name: 'description', content: '' },
            { name: 'format-detection', content: 'telephone=no' },
        ],
        link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },

    // Global CSS: https://go.nuxtjs.dev/config-css
    css: [
        // SCSS file in the project
        '~/assets/scss/main.scss',
        'boxicons/css/boxicons.min.css',
    ],

    // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
    plugins: [
        { src: '~/plugins/axios', mode: 'client' },
        { src: '~/plugins/vuex-persist', mode: 'client' },
        { src: '~/plugins/vue-good-table', mode: 'client' },
        { src: '~/plugins/vue-cookie-law', mode: 'client' },
        { src: '~/plugins/vuesax', mode: 'client' },
        { src: '~/plugins/vee-validate', mode: 'client' },
        { src: '~/plugins/v-calendar', mode: 'client' },
        { src: '~/plugins/router', mode: 'client' },
        { src: '~/plugins/filters', mode: 'client' },
    ],

    // Auto import components: https://go.nuxtjs.dev/config-components
    components: true,
    loading: '@/components/LoadingBar.vue',

    // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
    buildModules: [
        // https://go.nuxtjs.dev/eslint
        '@nuxtjs/eslint-module',
        // https://go.nuxtjs.dev/tailwindcss
        '@nuxtjs/tailwindcss',
    ],
    eslint: {
        fix: true,
    },

    // Modules: https://go.nuxtjs.dev/config-modules
    modules: [
        // https://go.nuxtjs.dev/axios
        '@nuxtjs/axios',
    ],

    // Axios module configuration: https://go.nuxtjs.dev/config-axios
    axios: {
        baseURL: development ? 'http://localhost:8000/api' : process.env.VUE_APP_API_BACK,
    },

    // Build Configuration: https://go.nuxtjs.dev/config-build
    build: {
        // Add exception
        transpile: ['vee-validate/dist/rules'],
    },

    server: {
        port: 3080,
    },

    watchers: {
        webpack: {
            aggregateTimeout: 300,
            poll: 1000,
        },
    },
    env: {
        VUE_APP_API_BACK: development ? 'http://localhost:8000/api' : process.env.VUE_APP_API_BACK,
    },

    devServerHandlers: [],
}
