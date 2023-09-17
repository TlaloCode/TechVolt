export default {
    createScheduleClass({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/course-schedule-class/`
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
    editScheduleClass({ commit }, data) {
        return new Promise((resolve, reject) => {
            const url = `/course-schedule-class/${data.id}/`
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
    getScheduleClass({ commit }) {
        return new Promise((resolve, reject) => {
            const url = `/course-schedule-class/get-schedule-general/`
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
    deleteScheduleClass({ commit }, id) {
        return new Promise((resolve, reject) => {
            const url = `/course-schedule-class/${id}/`
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
