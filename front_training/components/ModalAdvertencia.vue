<template>
    <div class="fixed top-0 left-0 right-0 bottom-0 flex justify-items-center modal-mask">
        <div
            class="fixed top-52 left-1/3 right-0 bottom 0 flex-col justify-center bg-white text-gray-700 shadow w-fit rounded-xl"
        >
            <div class="p-5 text-center text-red-700 text-3xl">
                <span><b>Advertencia</b></span>
            </div>
            <div class="p-5 text-center text-xl">
                <slot></slot>
            </div>
            <div class="flex flex-row justify-between p-5">
                <button
                    class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                    @click="regresa()"
                >
                    Regresar
                </button>
                <button
                    class="text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                    @click="lanzaGuardar()"
                >
                    Guardar
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ModalAdvertencia',
    methods: {
        regresa() {
            this.$emit('cierraModal')
        },
        lanzaGuardar() {
            this.$emit('guardaTarea')
        },
    },
}
</script>

<style scoped>
.modal-mask {
    z-index: 9998;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity 0.3s ease;
}
</style>
