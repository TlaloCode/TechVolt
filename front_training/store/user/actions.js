export default {
    /**
     * Método de obtención de usuario publico.
     *
     * @returns {Promise<Object>}
     */
    fetchUser({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/profile/${id}/`
            this.$axios
                .get(url)
                .then((response) => {
                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    /**
     * Método de obtención de usuario propio.
     *
     * @returns {Promise<Object>}
     */
    fetchUserMe({ commit }) {
        return new Promise((resolve, reject) => {
            const url = `/profile/get-me-profile/`
            this.$axios
                .get(url)
                .then((response) => {
                    const userData = response.data
                    commit('auth/SET_USER', userData, { root: true })

                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    /**
     * Actualiza la información de un usuario en la BDD
     */
    updateUser({ commit }, { data, id }) {
        return new Promise((resolve, reject) => {
            const url = `/profile/${id}/`
            this.$axios
                .put(url, data)
                .then((response) => {
                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    /**
     * Actualiza la imagen de perfil de un usuario
     */
    updatePictureUser({ commit }, { data, id }) {
        return new Promise((resolve, reject) => {
            const url = `/profile/${id}/update-picture-profile/`
            this.$axios
                .put(url, data)
                .then((response) => {
                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    /**
     * Método de invitacion de Usuario .
     */
    sendInvitation({ commit }, data) {
        // Formatea el data
        data.email = data.email.toLowerCase()
        return new Promise((resolve, reject) => {
            const url = `/auth/invitation/`
            this.$axios
                .post(url, data)
                .then((response) => {
                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    /**
     * Método de obtención de tabla de Usuarios.
     */
    getUsers({ commit }) {
        return new Promise((resolve, reject) => {
            const url = `/profile/users/`
            this.$axios
                .get(url)
                .then((response) => {
                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    /**
     * Método de obtención de tabla de Invitaciones de Usuarios.
     */
    getUserInvitations({ commit }) {
        return new Promise((resolve, reject) => {
            const url = `/auth/get-invitations/`
            this.$axios
                .get(url)
                .then((response) => {
                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
}
