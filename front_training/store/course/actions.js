export default {
    createCourse({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/courses/`
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
    uploadImage({ commit }, { data }) {
        return new Promise((resolve, reject) => {
            const url = `/course-image/`
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
    createModule({ commit }, { data, id }) {
        return new Promise((resolve, reject) => {
            const url = `/courses/${id}/add-module/`
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
    getCourse({ commit }, id) {
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
    getCourseList({ commit }, params = null) {
        return new Promise((resolve, reject) => {
            let url = `/courses/`
            if (params) {
                url += params
            }
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
    getModules({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/modules/?course=${id}`
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
    updateCourse({ commit }, { data, id }) {
        return new Promise((resolve, reject) => {
            const url = `/courses/${id}/`
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
    deleteCourse({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/courses/${id}/`
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
    suscribeUserToCourse({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/student-course/`
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
    getCoursesUserParam({ commit }, params = null) {
        return new Promise((resolve, reject) => {
            let url = `/student-course/`
            if (params) {
                url += params
            }
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
    getCoursesUser({ commit }, userId) {
        return new Promise((resolve, reject) => {
            const url = `/student-course/?user=${userId}`
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
    saveUserProgress({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/courses-progress/generate-progress/`
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
    updateUserProgress({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/student-course/`
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
    getUserProgress({ commit }, courseId) {
        return new Promise((resolve, reject) => {
            const url = `/courses-progress/${courseId}/lessons-progress/`
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
