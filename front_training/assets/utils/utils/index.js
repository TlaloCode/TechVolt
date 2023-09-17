const index = {
    /**
     * Modifica el string de error para hacerlo más legible.
     *
     * @param {String} msg Cadena de error
     */
    formatMsg(msg) {
        msg = msg.replace('non_field_errors: ', '')
        msg = msg.replace('[object Object]', '')
        msg = msg.replace('name', 'Nombre: ')
        msg = msg.replace('userNombre', 'Email: ')
        msg = msg.replace('password', 'Password: ')
        msg = msg.replace('email', 'Email: ')
        msg = msg.replace('categories', 'Categorías: ')
        msg = msg.replace('topic', 'Nombre: ')
        msg = msg.replace('details', '')
        msg = msg.replace('detail', '')
        msg = msg.replace('courses', 'Cursos: ')
        msg = msg.replace('course', 'Curso: ')
        msg = msg.replace('homework', 'Tarea: ')
        msg = msg.replace('time_taken', 'Tiempo estimado: ')
        return msg
    },
    getErrorDetails(errors) {
        let errorDetails = ''
        let messages = ''
        errors.some((err) => {
            messages = err.message
            const field = err.field
            if (field === 'Error') {
                errorDetails += `${messages} \n`
            } else {
                errorDetails += `${field} ${messages} \n`
            }
            return true
        })

        return index.formatMsg(errorDetails)
    },
    getUrlVars() {
        const vars = {}
        window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
            vars[key] = value
        })
        return vars
    },
    isNumeric(str) {
        if (typeof str === 'number') return true
        if (typeof str !== 'string') return false // we only process strings!
        return (
            !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
            !isNaN(parseFloat(str))
        ) // ...and ensure strings of whitespace fail
    },
}

module.exports = index
