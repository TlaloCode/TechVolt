<template>
    <div class="py-8 max-w-full bg-white text-gray-700 shadow">
        <div class="flex my-6 items-center w-full space-y-4 md:space-x-4 md:space-y-0 flex-col md:flex-row">
            <div class="w-full md:w-12/12">
                <div class="flex items-center md:px-8">
                    <span class="text-green-500">
                        <svg
                            class="h-10"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path fill="#fff" d="M12 14l9-5-9-5-9 5 9 5z" />
                            <path
                                fill="#fff"
                                d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"
                            />
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"
                            />
                        </svg>
                    </span>
                    <h2 class="md:px-5 flex items-center text-4xl">
                        <b>
                            {{ componentInfo.title }}
                        </b>
                    </h2>
                </div>
                <div class="shadow-lg w-full bg-white dark:bg-gray-700 relative overflow-hidden">
                    <a href="#" class="w-full h-full block" />
                </div>
            </div>
            <div class="flex items-center w-full md:w-1/2 space-x-4">
                <div class="w-1/2" />
            </div>
        </div>
        <div class="flex items-center justify-center px-12 py-5">
            <div class="mx-auto w-full">
                <ValidationObserver v-slot="{ invalid }">
                    <div class="mb-5">
                        <label for="name" class="mb-3 block text-base font-medium text-[#07074D]"> Categoría </label>
                        <ValidationProvider v-slot="{ errors }" name="Categoría" rules="required|max:120|min:2">
                            <input
                                v-model="categoryData.name"
                                name="name"
                                class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                @keyup.enter="submitCategory"
                            />
                            <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div>
                        <div class="flex items-center mb-5">
                            <button
                                type="button"
                                :disabled="invalid"
                                class="text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-green-500 dark:hover:bg-green-600 dark:focus:ring-green-600"
                                :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                @click="submitCategory"
                            >
                                {{ componentInfo.title }}
                            </button>
                            <NuxtLink
                                to="/administracion/catalogos/categorias/"
                                class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                            >
                                Regresar
                            </NuxtLink>
                        </div>
                    </div>
                </ValidationObserver>
            </div>
        </div>
    </div>
</template>

<script>
import { TYPE_VIEW } from 'assets/utils/enums'
import { getErrorDetails } from '@/assets/utils/utils'

export default {
    props: {
        type: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            showModules: false,
            categoryData: {
                name: '',
            },
            componentInfo: {
                title: '',
            },
        }
    },
    created() {
        this.setComponentInfo()
    },
    mounted() {
        if (this.type === TYPE_VIEW.EDIT) {
            this.getCategoryData()
        }
    },
    methods: {
        setComponentInfo() {
            if (this.type === TYPE_VIEW.EDIT) {
                this.componentInfo.title = 'Editar categoría'
            } else {
                this.componentInfo.title = 'Crear categoría'
            }
        },
        async getCategoryData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                this.categoryData = await this.$store.dispatch('categories/getCategory', this.$route.params.idCategoria)
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
         * Create or edit an existen category
         * @returns {Promise<void>}
         */
        async submitCategory() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const payload = {
                    data: this.categoryData,
                }
                let resultMsg = ''

                if (this.type === TYPE_VIEW.EDIT) {
                    payload.id = this.$route.params.idCategoria
                    resultMsg = 'Categoría actualizada'
                    await this.$store.dispatch('categories/updateCategory', payload)
                } else {
                    resultMsg = 'Categoría creada'
                    await this.$store.dispatch('categories/createCategory', payload)
                }
                this.$router.push({ path: `/administracion/catalogos/categorias` })
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: resultMsg,
                    position: 'top-right',
                })
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
    },
}
</script>
