export default {
    editHomeworkReview({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson-review/${data.id}/`
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
    createHomeworkReview({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson-review/`
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
    getHomeworkReviewList({ commit }) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson-delivery/`
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
    homeworkListByUser({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/homework-lesson-delivery/?created_by=${id}`
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
