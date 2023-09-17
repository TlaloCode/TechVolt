export default {
    async loginJWT({ commit, dispatch }, payload) {
        // make an API call to login the user with an email address and password
        const { data } = await this.$axios.post('/auth/token/', payload)
        // commit the user and tokens to the state
        commit('SET_PAYLOAD', data)
    },

    async register({ commit }, payload) {
        // make an API call to register the user
        const {
            data: {
                data: { user, res },
            },
        } = await this.$axios.post('/api/auth/register/', payload)

        // commit the user and tokens to the state
        commit('SET_USER', user)
        commit('SET_PAYLOAD', res)
    },

    // given the current refresh token, refresh the user's access token to prevent expiry
    refreshToken({ commit, state }) {
        return new Promise((resolve, reject) => {
            const { refreshToken } = state
            // make an API call using the refresh token to generate a new access token
            this.$axios
                .post('/auth/token/refresh/', { refresh: refreshToken })
                .then((response) => {
                    const { data } = response
                    commit('SET_ACCESS_TOKEN', data)
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },

    // logout the user
    logout({ commit, state }) {
        commit('LOGOUT')
    },

    async recoverPasswordByEmail({ commit }, data) {
        await this.$axios.post('/auth/recover-password-email/', data)
    },

    recoverPasswordJwt({ commit }, payload) {
        return new Promise((resolve, reject) => {
            // Check confirm password
            if (payload.password !== payload.passwordConfirmation) {
                reject(new Error('Las contraseñas no coinciden. Por favor reintente.'))
            }

            this.$axios
                .post('auth/recover-password/', payload)
                .then((response) => {
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    registerUserJWT({ commit }, { payload }) {
        const { password, passwordConfirmation } = payload.userDetails

        return new Promise((resolve, reject) => {
            // Check confirm password
            if (password !== passwordConfirmation) {
                reject(new Error('Las contraseñas no coinciden. Por favor reintente.'))
            }

            this.$axios
                .post('/auth/signup/', payload.userDetails)
                .then((response) => {
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    userActivation({ commit }, payload) {
        return new Promise((resolve, reject) => {
            this.$axios
                .post('/auth/verify/', { token: payload.token })
                .then((response) => {
                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
}
