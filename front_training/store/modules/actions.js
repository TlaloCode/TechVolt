export default {
    updateModules({ commit }, { data }) {
        return new Promise((resolve, reject) => {
            const url = `/modules/${data.id}/`
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
    deleteModule({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/modules/${id}/`
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
    createModule({ commit }, { data }) {
        return new Promise((resolve, reject) => {
            const url = `/modules/`
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
    getModule({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/modules/${id}/`
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
