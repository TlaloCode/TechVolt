export default {
    // store the logged in user in the state
    SET_USER(state, data) {
        state.appActiveUser = data
    },

    // store new or updated token fields in the state
    SET_PAYLOAD(state, { access: accessToken, refresh: refreshToken }) {
        state.accessToken = accessToken
        state.refreshToken = refreshToken
    },

    SET_ACCESS_TOKEN(state, { access: accessToken }) {
        state.accessToken = accessToken
    },

    // clear our the state, essentially logging out the user
    LOGOUT(state) {
        state.accessToken = null
        state.refreshToken = null
        state.appActiveUser = {}
    },
}
