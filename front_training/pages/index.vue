<template>
    <div />
</template>

<script>
export default {
    components: {},
    layout: 'base',
    computed: {
        showPageSystem() {
            return this.$store.state.showPageSystem
        },
    },
    mounted() {
        if (!localStorage.getItem('accessToken')) {
            this.$router.push('/auth/login')
        }
    },
}
</script>
