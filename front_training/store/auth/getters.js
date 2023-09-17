export default {
    // determine if the user is authenticated based on the presence of the access token
    isAuthenticated: (state) => {
        return !!state.accessToken
    },
}
