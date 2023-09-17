<template>
    <div class="py-8 max-w-full bg-white text-gray-700 shadow">
        <div class="max-w-screen-xl mx-auto">
            <div class="w-full">
                <div class="flex container md:px-8">
                    <span class="text-green-500 flex-none">
                        <GridPlusIcon />
                    </span>
                    <h2 class="md:px-5 flex items-center text-3xl flex-auto">
                        <span>Lista de lecciones</span>
                    </h2>
                    <div class="flex flex-initial justify-end">
                        <NuxtLink
                            :to="`/gestion/mis-cursos/${$route.params.idCurso}/modulos`"
                            class="w-40 text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                        >
                            Regresar
                        </NuxtLink>
                    </div>
                    <div class="flex flex-initial justify-end">
                        <NuxtLink
                            :to="`/gestion/mis-cursos/${courseId}/modulos/${$route.params.idModulo}/lecciones/nuevo`"
                            class="w-40 text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                        >
                            Agregar lección
                        </NuxtLink>
                    </div>
                </div>
                <div class="flex container md:px-8">
                    <p class="md:px-5 mt-5 flex items-center text-xl flex-auto">
                        <span v-if="lessonsList.length === 0">Agregar una lección</span>
                        <span v-else>Elija una lección para editar</span>
                    </p>
                </div>
            </div>
            <template v-if="lessonsList.length === 0">
                <div class="max-w-screen-xl mx-auto text-center px-4 sm:px-6 lg:px-8">
                    <div class="sm:rounded-md mt-5 text-center">
                        <p class="text-black-400">No hay registros aún</p>
                    </div>
                </div>
            </template>
            <div class="flex items-center w-full md:w-1/2 space-x-4">
                <div class="w-1/2" />
            </div>
        </div>
        <div class="max-w-screen-xl mx-auto text-center px-4 sm:px-6 lg:px-8">
            <div class="sm:rounded-md mt-5">
                <ul>
                    <li v-for="(lesson, index) in lessonsList" :key="index">
                        <div
                            class="block hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition duration-150 ease-in-out"
                        >
                            <div class="px-4 py-4 sm:px-6">
                                <div class="flex items-center">
                                    <div class="text-sm leading-5 font-medium text-blue-600 truncate grow text-left">
                                        {{ lesson.topic }}
                                    </div>
                                    <button
                                        class="border hover:bg-red-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-red-300 font-large rounded-full text-sm p-2 text-center inline-flex items-center dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:focus:ring-red-800 relative tooltip mx-2"
                                        @click="deleteLesson(lesson.id)"
                                    >
                                        <span class="tooltip-box"> Eliminar lección </span>
                                        <i class="bx bx-trash text-xl"></i>
                                    </button>
                                    <NuxtLink
                                        :to="`/gestion/mis-cursos/${courseId}/modulos/${moduleId}/lecciones/${lesson.id}/editar`"
                                        class="border hover:bg-blue-600 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-200 font-medium rounded-full text-sm p-2 text-center inline-flex items-center dark:border-blue-400 dark:text-blue-400 dark:hover:text-white dark:focus:ring-blue-600 relative tooltip mx-2"
                                    >
                                        <span class="tooltip-box"> Editar lección </span>
                                        <i class="bx bx-edit-alt text-xl"></i>
                                    </NuxtLink>
                                    <NuxtLink
                                        :to="`/gestion/mis-cursos/${courseId}/modulos/${moduleId}/lecciones/${lesson.id}/tareas/nuevo`"
                                        class="border hover:bg-blue-600 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-200 font-medium rounded-full text-sm p-2 text-center inline-flex items-center dark:border-blue-400 dark:text-blue-400 dark:hover:text-white dark:focus:ring-blue-600 relative tooltip mx-2"
                                    >
                                        <span class="tooltip-box"> Agregar tarea </span>
                                        <i class="bx bx-layer-plus text-xl"></i>
                                    </NuxtLink>
                                    <NuxtLink
                                        :to="`/gestion/mis-cursos/${courseId}/modulos/${moduleId}/lecciones/${lesson.id}/tareas`"
                                        class="border hover:bg-blue-600 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-200 font-medium rounded-full text-sm p-2 text-center inline-flex items-center dark:border-blue-400 dark:text-blue-400 dark:hover:text-white dark:focus:ring-blue-600 relative tooltip mx-2"
                                    >
                                        <span class="tooltip-box"> Tareas </span>
                                        <i class="bx bx-task text-xl"></i>
                                    </NuxtLink>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        <vs-dialog v-model="isOpenDialogDeleteLesson">
            <template #header>
                <h4 class="m-1 font-medium">Confirmar acción</h4>
            </template>

            <div class="text-center">
                <p class="mb-3">¿Está seguro que desea eliminar esta lección?</p>
                <small> Esta acción no se puede revertir </small>
            </div>

            <template #footer>
                <div class="flex justify-end mt-5">
                    <button
                        class="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
                        @click="submitDeleteLesson"
                    >
                        Eliminar
                    </button>
                    <button
                        class="py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
                        @click="isOpenDialogDeleteLesson = false"
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
            lessonToDeleteId: null,
            isOpenDialogDeleteLesson: false,
            dataReturned: '',
            lessonsFilled: false,
            lessonsList: [],
        }
    },
    computed: {
        courseId() {
            return this.$route.params.idCurso
        },
        moduleId() {
            return this.$route.params.idModulo
        },
    },
    mounted() {
        this.getLessonsSelectedModule()
    },
    methods: {
        async getLessonsSelectedModule() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                this.dataReturned = await this.$store.dispatch('lesson/getLessons', this.moduleId)
                this.lessonsList = this.dataReturned.results
                this.lessonsFilled = true
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
        deleteLesson(lessonId) {
            this.lessonToDeleteId = lessonId
            this.isOpenDialogDeleteLesson = true
        },
        async submitDeleteLesson() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                await this.$store.dispatch('lesson/deleteLesson', this.lessonToDeleteId)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Lección eliminada',
                    position: 'top-right',
                })
                this.getLessonsSelectedModule()
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
                this.isOpenDialogDeleteLesson = false
                loading.close()
            }
        },
    },
}
</script>

<style>
.boton {
    background: black;
    color: white;
    margin-top: 50px;
    margin-left: -18px;
}
</style>
