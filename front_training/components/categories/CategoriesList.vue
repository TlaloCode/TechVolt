<template>
    <div class="py-8 max-w-full bg-white text-gray-700 shadow categories--container">
        <div class="max-w-screen-xl mx-auto">
            <div class="w-full">
                <div class="flex container md:px-8">
                    <span class="text-green-500 flex-none">
                        <GridPlusIcon />
                    </span>
                    <h2 class="md:px-5 flex items-center text-3xl flex-auto">
                        <span>Categorías</span>
                    </h2>
                    <div class="flex flex-initial w-48 justify-end">
                        <NuxtLink
                            to="/administracion/catalogos/categorias/nuevo"
                            class="text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                        >
                            Crear categoría
                        </NuxtLink>
                    </div>
                </div>
                <div class="shadow-lg w-full bg-white dark:bg-gray-700 relative">
                    <a href="#" class="w-full h-full block" />
                </div>
            </div>
            <div class="flex items-center w-full md:w-1/2 space-x-4">
                <div class="w-1/2" />
            </div>
        </div>
        <div class="max-w-screen-xl mx-auto text-center px-4 sm:px-6 lg:px-8">
            <div class="sm:rounded-md mt-5">
                <template v-if="categoriesList.length === 0">
                    <p class="text-black-400">No hay registros aún</p>
                </template>
                <ul v-else>
                    <li v-for="(category, index) in categoriesList" :key="index">
                        <div
                            class="block hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition duration-150 ease-in-out"
                        >
                            <div class="px-4 py-4 sm:px-6">
                                <div class="flex items-center">
                                    <div class="text-sm leading-5 font-medium text-blue-600 truncate grow text-left">
                                        {{ category.name }}
                                    </div>
                                    <button
                                        class="border hover:bg-red-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-red-300 font-large rounded-full text-sm p-2 text-center inline-flex items-center dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:focus:ring-red-800 relative tooltip mx-2"
                                        @click="deleteCategory(category.id)"
                                    >
                                        <span class="tooltip-box"> Eliminar categoría </span>
                                        <i class="bx bx-trash text-xl"></i>
                                    </button>
                                    <NuxtLink
                                        :to="`/administracion/catalogos/categorias/${category.id}/editar`"
                                        class="border hover:bg-blue-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2 text-center inline-flex items-center dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800 relative tooltip mx-2"
                                    >
                                        <span class="tooltip-box"> Editar categoría </span>
                                        <i class="bx bx-edit-alt text-xl"></i>
                                    </NuxtLink>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        <vs-dialog v-model="isOpenDialogDeleteCategory">
            <template #header>
                <h4 class="m-1 font-medium">Confirmar acción</h4>
            </template>

            <div class="text-center">
                <p class="mb-3">¿Está seguro que desea eliminar esta categoría?</p>
                <small> Esta acción no se puede revertir </small>
            </div>

            <template #footer>
                <div class="flex justify-end mt-5">
                    <button
                        class="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
                        @click="submitDeleteCategory"
                    >
                        Eliminar
                    </button>
                    <button
                        class="py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
                        @click="isOpenDialogDeleteCategory = false"
                    >
                        Cancelar
                    </button>
                </div>
            </template>
        </vs-dialog>
    </div>
</template>

<script>
import { getErrorDetails } from '@/assets/utils/utils'
import GridPlusIcon from '@/components/icons/GridPlus.vue'

export default {
    name: 'CategoriesList',
    components: {
        GridPlusIcon,
    },
    data() {
        return {
            categoriesList: [],
            dataReturned: {},
            categoryToDeleteId: null,
            isOpenDialogDeleteCategory: false,
        }
    },
    mounted() {
        this.getCategoriesData()
    },
    methods: {
        async getCategoriesData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                this.dataReturned = await this.$store.dispatch('categories/getCategories')
                this.categoriesList = this.dataReturned
            } catch (err) {
                let res = ''
                if (err.response) {
                    res = getErrorDetails(err.response.data.errors)
                } else {
                    res = err.message
                }
                this.$vs.notification({
                    title: 'Ops..',
                    text: `${res}`,
                    color: 'danger',
                    position: 'top-right',
                })
            } finally {
                loading.close()
            }
        },
        /**
         * Ejecuta un diálogo para confirmar la eliminación de una categoría
         */
        deleteCategory(categoryId) {
            this.categoryToDeleteId = categoryId
            this.isOpenDialogDeleteCategory = true
        },
        /**
         * Realiza la petición para eliminar una categoría
         */
        async submitDeleteCategory() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                await this.$store.dispatch('categories/deleteCategory', this.categoryToDeleteId)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Categoría eliminada',
                    position: 'top-right',
                })
                this.getCategoriesData()
            } catch (err) {
                let res = ''
                if (err.response) {
                    res = getErrorDetails(err.response.data.errors)
                } else {
                    res = err.message
                }
                this.$vs.notification({
                    title: 'Ops..',
                    text: `${res}`,
                    color: 'danger',
                    position: 'top-right',
                })
            } finally {
                this.isOpenDialogDeleteCategory = false
                loading.close()
            }
        },
    },
}
</script>

<style lang="scss">
.categories--container .tooltip-box {
    right: -60px !important;
}
</style>
