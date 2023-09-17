<template>
    <div class="h-screen flex w-full bg-img">
        <div
            class="vx-col flex items-center justify-center flex-col sm:w-1/2 md:w-3/5 lg:w-3/4 xl:w-1/2 mx-auto text-center"
        >
            <img src="@/assets/images/pages/not-authorized.png" alt="graphic-notAuth" class="mx-auto mb-4 max-w-full" />
            <h1 class="sm:mx-0 mx-4 mb-12 text-5xl d-theme-heading-color">Página no autorizada</h1>
        </div>
    </div>
</template>
<script>
export default {
    name: 'NotAuthorized',
    destroyed() {
        this.$store.commit('UPDATE_SHOW_PAGE_SYSTEM', false)
    },
}
</script>
