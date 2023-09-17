<template>
    <div v-if="loading" class="loading-page flex flex-wrap items-center justify-center">
        <div class="loading" />
    </div>
</template>
<script>
export default {
    data: () => ({
        loading: false,
    }),
    methods: {
        start() {
            this.loading = true
        },
        finish() {
            this.loading = false
        },
    },
}
</script>
<style scoped>
.loading-page {
    background: #000000;
    width: 100%;
    height: 100%;
    filter: alpha(opacity=50);
    opacity: 0.5;
    margin: 0px;
    position: absolute;
    justify-content: center;
    align-items: center;
    left: 0px;
    top: 0px;
    right: 0px;
    z-index: 1000;
    cursor: wait;
    margin: 0px;
    padding: 0px;
    /* display: none;*/
}
.loading {
    width: 4.5rem;
    height: 4.5rem;
    border: 4px solid #1375e6;
    border-radius: 50%;
    border-top-color: rgba(131, 206, 12, 0.705);
    animation: spin 1s ease-in-out infinite;
}
@keyframes spin {
    to {
        -webkit-transform: rotate(360deg);
    }
}
</style>
