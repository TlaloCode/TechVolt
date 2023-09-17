export default {
    /**
     * Crear leccion
     */
    createHomework({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson/`
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
    deleteHomework({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson/${id}/`
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
    /*
    Petición para guardar recurso de la tarea
    */
    createHomeworkResource({ commit }, { data }) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson-resource/`
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
    /*
    Petición para modificar el recurso de la tarea
    */
    updateHomeworkResource({ commit }, { data, id }) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson-resource/${id}/`
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
     * Actualiza la información de una leccion en la BDD
     */
    updateHomework({ commit }, { data, id }) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson/${id}/`
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
     * Obtiene las Tareas de una Leccion
     */
    getHomeworks({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson/?lesson=${id}`
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
     * Obtiene una Tarea
     */
    getHomework({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson/${id}/`
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
     * Obtiene una Recurso de la tarea
     */
    getHomeworkResource({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson-resource/?homeworkLesson=${id}`
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
    getDeliveryInfo({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson/${id}/messages/`
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
    deliverHomework({ commit }, { data }) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson-delivery/`
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
}
