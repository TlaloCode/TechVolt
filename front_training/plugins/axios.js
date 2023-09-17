export default function ({ app, store, $axios }) {
    $axios.onRequest((config) => {
        const tokenAccess = store.state.auth.accessToken
        switch (config.url) {
            case '/auth/token/':
            case '/auth/verify/':
            case '/auth/token/refresh/':
                return config
        }
        if (tokenAccess) {
            config.headers.Authorization = `Bearer ${tokenAccess}`
        }
        // Set locale headers
        config.headers['Accept-Language'] = 'es-es'
        return config
    })

    $axios.onResponseError((error) => {
        const { config, response } = error
        const originalRequest = config
        const refreshToken = store.state.auth.refreshToken

        if (error.response.status === 401 && originalRequest.url === '/auth/token/refresh/') {
            store.dispatch('auth/logout')
            app.router.push('/auth/login')
        }
        // If tokenRefresh expired, then redirect to login to start a new session
        if (response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            if (refreshToken) {
                return new Promise((resolve, reject) => {
                    store
                        .dispatch('auth/refreshToken')
                        .then((response) => {
                            resolve(response)
                        })
                        .catch((e) => {
                            // should jump here after facing error from request
                            reject(e)
                        })
                })
                    .then((res) => {
                        return $axios(originalRequest)
                    })
                    .catch((e) => {
                        // store.dispatch('auth/logout')
                        app.router.push('/auth/login')
                    })
            } else {
                app.router.push('/auth/login')
            }
            return Promise.reject(error)
        }
    })
}
