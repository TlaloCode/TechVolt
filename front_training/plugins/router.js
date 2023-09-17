export default ({ app, store }) => {
    // Every time the route changes (fired on initialization too)
    const isAuthenticated = store.getters['auth/isAuthenticated']
    app.router.beforeEach((to, from, next) => {
        if (isAuthenticated && to.path === '/auth/login') {
            next({ name: 'cursos' })
        }
        if (isAuthenticated && to.path === '/auth/signup') {
            next({ name: 'cursos' })
        }
        next()
    })
}
