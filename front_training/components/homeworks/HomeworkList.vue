<template>
    <div class="py-8 max-w-full bg-white text-gray-700 shadow">
        <div class="max-w-screen-xl mx-auto">
            <div class="w-full">
                <div class="flex container md:px-8">
                    <span class="text-green-500 flex-none">
                        <GridPlusIcon />
                    </span>
                    <h2 class="md:px-5 flex items-center text-3xl flex-auto">
                        <span>Tareas</span>
                    </h2>
                    <div class="flex flex-initial justify-end">
                        <NuxtLink
                            class="w-40 text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                            :to="`/gestion/mis-cursos/${courseId}/modulos/${moduleId}/lecciones`"
                        >
                            Regresar
                        </NuxtLink>
                    </div>
                    <div class="flex flex-initial justify-end">
                        <NuxtLink
                            :to="`/gestion/mis-cursos/${courseId}/modulos/${moduleId}/lecciones/${lessonId}/tareas/nuevo`"
                            class="w-40 text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                        >
                            Agregar tarea
                        </NuxtLink>
                    </div>
                </div>
                <div class="flex container md:px-8">
                    <p class="md:px-5 mt-5 flex items-center text-xl flex-auto">
                        <span v-if="homeworksList.length === 0">Agregar una tarea</span>
                        <span v-else>Elija una tarea para editar</span>
                    </p>
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
                <template v-if="homeworksList.length === 0">
                    <p class="text-black-400">No hay registros aún</p>
                </template>
                <ul>
                    <li v-for="(homework, index) in homeworksList" :key="index">
                        <div
                            class="block hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition duration-150 ease-in-out"
                        >
                            <div class="px-4 py-4 sm:px-6">
                                <div class="flex items-center">
                                    <div class="text-sm leading-5 font-medium text-blue-600 truncate grow text-left">
                                        {{ homework.title }}
                                    </div>
                                    <button
                                        class="border hover:bg-red-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-red-300 font-large rounded-full text-sm p-2 text-center inline-flex items-center dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:focus:ring-red-800 relative tooltip mx-2"
                                        @click="deleteHomework(homework.id)"
                                    >
                                        <span class="tooltip-box"> Eliminar tarea </span>
                                        <i class="bx bx-trash text-xl"></i>
                                    </button>
                                    <NuxtLink
                                        :to="`/gestion/mis-cursos/${courseId}/modulos/${moduleId}/lecciones/${lessonId}/tareas/${homework.id}/editar`"
                                        class="border hover:bg-blue-600 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-200 font-medium rounded-full text-sm p-2 text-center inline-flex items-center dark:border-blue-400 dark:text-blue-400 dark:hover:text-white dark:focus:ring-blue-600 relative tooltip mx-2"
                                    >
                                        <span class="tooltip-box"> Editar tarea </span>
                                        <i class="bx bx-edit-alt text-xl"></i>
                                    </NuxtLink>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        <vs-dialog v-model="isOpenDialogDeleteHomework">
            <template #header>
                <h4 class="m-1 font-medium">Confirmar acción</h4>
            </template>

            <div class="text-center">
                <p class="mb-3">¿Está seguro que desea eliminar esta tarea?</p>
                <small> Esta acción no se puede revertir </small>
            </div>

            <template #footer>
                <div class="flex justify-end mt-5">
                    <button
                        class="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
                        @click="submitDeleteHomework"
                    >
                        Eliminar
                    </button>
                    <button
                        class="py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
                        @click="isOpenDialogDeleteHomework = false"
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
    components: {
        GridPlusIcon,
    },
    data() {
        return {
            homeworkToDeleteId: null,
            isOpenDialogDeleteHomework: false,
            dataReturned: '',
            homweorksFilled: false,
            homeworksList: [],
            dummyData: [],
        }
    },
    computed: {
        courseId() {
            return this.$route.params.idCurso
        },
        moduleId() {
            return this.$route.params.idModulo
        },
        lessonId() {
            return this.$route.params.idLeccion
        },
    },
    created() {
        this.getHomeworksSelectedLesson()
    },
    methods: {
        async getHomeworksSelectedLesson() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                this.dataReturned = await this.$store.dispatch('homework/getHomeworks', this.lessonId)
                this.homeworksList = this.dataReturned.results
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
        deleteHomework(homeworkId) {
            this.homeworkToDeleteId = homeworkId
            this.isOpenDialogDeleteHomework = true
        },
        async submitDeleteHomework() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                await this.$store.dispatch('homework/deleteHomework', this.homeworkToDeleteId)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Tarea eliminada',
                    position: 'top-right',
                })
                this.getHomeworksSelectedLesson()
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
                this.isOpenDialogDeleteHomework = false
                loading.close()
            }
        },
    },
}
</script>
