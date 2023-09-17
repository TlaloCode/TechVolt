import Vue from 'vue'

Vue.filter('getFilename', function (value) {
    return value.split('/').pop()
})
