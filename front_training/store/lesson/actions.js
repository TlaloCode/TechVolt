export default {
    /**
     * Método de obtención de curso.
     *
     * @returns {Promise<Object>}
     */
    // eslint-disable-next-line no-unused-vars
    fetchCourse({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/courses/${id}/`
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
     * Crear leccion
     */
    createLesson({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/lessons/`
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
     * Actualiza la información de una leccion en la BDD
     */
    updateLesson({ commit }, { data, id }) {
        return new Promise((resolve, reject) => {
            const url = `/lessons/${id}/`
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
     * Obtiene las Lecciones de un módulo
     */
    getLessons({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/lessons/?module=${id}`
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
     * Obtiene una lección por medio de su ID
     */
    getLesson({ commit }, lessonId) {
        return new Promise((resolve, reject) => {
            const url = `/lessons/${lessonId}/`
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
     * Permite generar la creación de un nuevo recurso para una lección
     *
     */
    postLessonResource({ commit }, { data }) {
        return new Promise((resolve, reject) => {
            const url = `/lessons-resource/`
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

    deleteLesson({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/lessons/${id}/`
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
    getCourseModulesAndLessons({ commit }, courseId) {
        return new Promise((resolve, reject) => {
            const url = `/courses/${courseId}/course-lessons/`
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
