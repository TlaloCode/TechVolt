<template>
    <div class="py-8 max-w-full bg-white text-gray-700">
        <div
            class="flex my-6 items-center w-full max-w-screen-xl mx-auto space-y-4 md:space-x-4 md:space-y-0 flex-col md:flex-row"
        >
            <div class="w-full md:w-12/12">
                <div class="flex container md:px-8">
                    <span class="text-green-500 flex-none">
                        <GridPlusIcon />
                    </span>
                    <h2 class="md:px-5 flex items-center text-3xl flex-auto">
                        <b>Agregar módulos</b>
                    </h2>
                    <div class="flex flex-initial w-48 justify-end">
                        <button
                            class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                            @click="$router.go(-1)"
                        >
                            Regresar
                        </button>
                    </div>
                </div>
                <div class="shadow-lg w-full bg-white dark:bg-gray-700 relative overflow-hidden">
                    <a href="#" class="w-full h-full block" />
                </div>
            </div>
        </div>
        <div v-if="updateButton">
            <ValidationObserver v-slot="{ invalid }">
                <!-- Empeiza el formulario de Añadir Modulos-->
                <div>
                    <div class="flex items-center max-w-screen-xl mx-auto justify-center p-12">
                        <div class="mx-auto w-full">
                            <div>
                                <div class="mb-5">
                                    <label for="name" class="mb-3 block text-base font-medium text-[#07074D]">
                                        Nombre
                                    </label>
                                    <ValidationProvider
                                        v-slot="{ errors }"
                                        name="Nombre"
                                        rules="required|min:4|max:254"
                                    >
                                        <input
                                            v-model="moduleData.topic"
                                            class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                        />
                                        <span class="block text-red-700 text-sm mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                    </ValidationProvider>
                                </div>
                                <div class="mb-5">
                                    <label class="mb-3 block text-base font-medium text-[#07074D]"> Descripción </label>
                                    <ValidationProvider
                                        v-slot="{ errors }"
                                        name="Descripcion"
                                        rules="required|min:4|max:254"
                                    >
                                        <textarea
                                            v-model="moduleData.description"
                                            rows="4"
                                            placeholder="En este módulo veremos..."
                                            class="w-full resize-none rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                        />
                                        <span class="block text-red-700 text-sm mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                    </ValidationProvider>
                                </div>
                                <div>
                                    <div class="flex items-center juatify-end space-x-4">
                                        <button
                                            :invalid="invalid"
                                            :disabled="invalid"
                                            class="flex items-center text-white-400 text-md border-black-300 bg-green-400 hover:bg-green-300 text-white border background-black px-5 py-2 rounded-full"
                                            :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                            @click="addNewModules"
                                        >
                                            Guardar Módulo
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </ValidationObserver>
        </div>
    </div>
</template>

<script>
import { getErrorDetails } from '@/assets/utils/utils'
import GridPlusIcon from '@/components/icons/GridPlus.vue'
export default {
    components: { GridPlusIcon },
    data() {
        return {
            moduleData: {
                topic: '',
                description: '',
                course: '',
            },
            updateButton: true,
        }
    },
    created() {
        this.resetRedMesageError()
    },
    methods: {
        // guardar los modulos nuevos en el curso
        async addNewModules() {
            this.moduleData.course = this.$route.params.idCurso
            const loading = this.$vs.loading({ scale: 0.65, type: 'radius' })
            try {
                const payload = {
                    data: this.moduleData,
                }
                await this.$store.dispatch('modules/createModule', payload)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Módulo creado',
                    position: 'top-right',
                })
                this.$router.go(-1)
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
                this.resetRedMesageError()
                loading.close()
            }
        },
        resetRedMesageError() {
            this.updateButton = false
            const loading = this.$vs.loading({ scale: 0.65, type: 'radius' })

            setTimeout(() => {
                loading.close()
                this.updateButton = true
            }, 250)
        },
    },
}
</script>
