export default {
    createCategory({ commit }, { data }) {
        return new Promise((resolve, reject) => {
            const url = `/categories/`
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

    getCategory({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/categories/${id}/`
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
    getCategories({ commit }) {
        return new Promise((resolve, reject) => {
            const url = `/categories/`
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
    updateCategory({ commit }, { data, id }) {
        return new Promise((resolve, reject) => {
            const url = `/categories/${id}/`
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
    deleteCategory({ commit }, categoryId) {
        return new Promise((resolve, reject) => {
            const url = `/categories/${categoryId}/`
            this.$axios
                .delete(url)
                .then((response) => {
                    resolve(response.data)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
}
