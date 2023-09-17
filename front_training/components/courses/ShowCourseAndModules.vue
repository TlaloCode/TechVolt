<template>
    <div>
        <template v-if="loadedData">
            <!--Header-->
            <div class="border-b w-full px-10 py-8 mx-auto bg-white shadow-xl">
                <div class="w-full md:w-12/12">
                    <div class="flex container">
                        <h2 class="flex items-center text-3xl flex-auto">
                            <b>{{ completeCourse.name }} > {{ activeLesson.topic }}</b>
                        </h2>
                        <div class="flex flex-initial w-48 justify-end">
                            <NuxtLink
                                :to="`/cursos/temario/${courseId}`"
                                class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                            >
                                Regresar
                            </NuxtLink>
                        </div>
                    </div>
                    <div class="shadow-lg w-full bg-white dark:bg-gray-700 relative overflow-hidden">
                        <a class="w-full h-full block" href="#" />
                    </div>
                </div>
            </div>
            <!--Panel left-->
            <div class="relative flex w-full h-screen overflow-auto antialiased bg-gray-100">
                <div class="h-screen overflow-auto w-full max-w-xs px-4 py-8 bg-white shadow-xl">
                    <div>
                        <h2 class="flex items-center justify-center text-xl flex-auto">
                            <b>Módulos</b>
                        </h2>
                        <div class="mt-4 mx-auto space-y-6">
                            <!-- Accordion start -->
                            <ul
                                v-for="(module, moduleIndex) in completeCourse.modules"
                                :key="module.topic"
                                class="accordion w-full p-5"
                            >
                                <li class="cursor-pointer my-1">
                                    <span
                                        class="font-bold text-xl tracking-tight text-gray-500 flex flex-row justify-between items-center"
                                        @click="selectedModuleIndexClick(moduleIndex)"
                                    >
                                        <span>{{ module.topic }}</span>
                                        <svg
                                            class="text-gray-500 mr-1"
                                            fill="currentColor"
                                            height="16"
                                            viewBox="0 0 16 16"
                                            width="16"
                                            xmlns="http://www.w3.org/2000/svg"
                                        >
                                            <path
                                                d="M8 4a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L7.5 10.293V4.5A.5.5 0 0 1 8 4z"
                                                fill-rule="evenodd"
                                            />
                                        </svg>
                                    </span>
                                    <div :data-module-id="moduleIndex" class="text-gray-500 text-md p-2 block">
                                        <div v-for="(lesson, lessonIndex) in module.lessons" :key="lessonIndex">
                                            <div class="bg-white hover:bg-gray-50 border-b rounded-lg py-1">
                                                <a
                                                    class="flex flex-row items-center justify-between bg-white border-t cursor-pointer mt-200 py-65"
                                                    @click="changeActiveLesson(lesson, module)"
                                                >
                                                    <div class="py-1 flex justify-between">
                                                        <span class="text-sm font-semibold text-gray-900">
                                                            {{ lesson.topic }}
                                                        </span>
                                                    </div>
                                                    <div
                                                        class="w-6 text-gray-500 rounded-full focus:outline-none hover:text-gray-600 hover:bg-gray-200 tooltip"
                                                    >
                                                        <span
                                                            v-if="checaProgresoLeccion(lesson.id)"
                                                            class="tooltip-box"
                                                        >
                                                            Completado</span
                                                        >
                                                        <span v-else class="tooltip-box">Completar</span>
                                                        <svg
                                                            class="w-6 h-6 fill-current"
                                                            :class="
                                                                checaProgresoLeccion(lesson.id)
                                                                    ? 'text-green-600'
                                                                    : 'text-gray-600'
                                                            "
                                                            fill="currentColor"
                                                            viewBox="0 0 20 20"
                                                            xmlns="http://www.w3.org/2000/svg"
                                                        >
                                                            <path
                                                                clip-rule="evenodd"
                                                                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                                                fill-rule="evenodd"
                                                            />
                                                        </svg>
                                                    </div>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                            <!-- Accordion end -->
                        </div>
                    </div>
                </div>
                <!-- left -->

                <!-- right -->
                <div class="right-0 flex flex-col h-screen overflow-auto pb-2 bg-white border-l border-gray-300 w-full">
                    <div class="flex items-center w-full p-3">
                        <div class="justify-center text-center ml-4 mr-auto text-lg font-medium">
                            {{ activeLesson.topic }}
                        </div>
                    </div>
                    <div id="lessonContainer">
                        <div class="overflow-y-auto">
                            <div class="container mt-3">
                                <!-- eslint-disable vue/no-v-html -->
                                <div
                                    class="overflow-y-auto text-sm font-medium m-8 text-gray-600 text-justify"
                                    v-html="activeLesson.description"
                                />
                                <!--eslint-enable-->
                            </div>
                        </div>
                    </div>
                    <template v-if="activeLesson.resources.length > 0">
                        <ul class="flex flex-row items-center justify-around px-3 mb-1 list-none border-b select-none">
                            <li
                                class="flex-auto px-4 mx-1 -mb-px text-center rounded-t-lg cursor-pointer last:mr-0 hover:bg-gray-200"
                            >
                                <a
                                    class="block py-3 text-xs font-bold leading-normal text-blue-500 uppercase border-b-4 border-blue-500"
                                >
                                    Recursos de la lección
                                </a>
                            </li>
                        </ul>
                        <div v-if="activeLesson.resources.length > 0" class="flex flex-col mt-4 ml-4 mb-4 space-y-2">
                            <template v-for="(resource, resourceIndex) in activeLesson.resources">
                                <button
                                    :key="resourceIndex"
                                    class="cursor-pointer hover:bg-gray-200 px-4 py-3 bg-gray-100 rounded-md text-black outline-none focus:ring-4 shadow-lg transform active:scale-x-75 transition-transform mx-5 flex"
                                    @click="openResource(resource.resource)"
                                >
                                    <div class="flex flex-row">
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke-width="1.75"
                                            stroke="currentColor"
                                            class="w-6 h-6"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                d="M9 8.25H7.5a2.25 2.25 0 00-2.25 2.25v9a2.25 2.25 0 002.25 2.25h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25H15M9 12l3 3m0 0l3-3m-3 3V2.25"
                                            />
                                        </svg>

                                        <span class="whitespace-normal overflow-hidden">Descargar</span>
                                    </div>
                                </button>
                            </template>
                        </div>
                    </template>

                    <template v-if="homeworkList.length > 0">
                        <ul class="flex flex-row items-center justify-around px-3 mb-1 list-none border-b select-none">
                            <li
                                class="flex-auto px-4 mx-1 -mb-px text-center rounded-t-lg cursor-pointer last:mr-0 hover:bg-gray-200"
                            >
                                <a
                                    class="block py-3 text-xs font-bold leading-normal text-blue-500 uppercase border-b-4 border-blue-500"
                                >
                                    Tareas
                                </a>
                            </li>
                        </ul>
                        <div class="text-center px-4 sm:px-6 lg:px-8">
                            <div class="overflow-hidden sm:rounded-md mt-5">
                                <ul>
                                    <li v-for="(homework, index) in homeworkList" :key="index">
                                        <div
                                            class="block hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition duration-150 ease-in-out"
                                        >
                                            <div class="px-4 py-4 sm:px-6 space-y-2">
                                                <div
                                                    class="container flex flex-col flex-wrap items-center justify-between mx-auto md:flex-row max-w-7xl"
                                                >
                                                    <div class="relative flex flex-col md:flex-row">
                                                        <div
                                                            class="text-sm leading-5 font-medium text-blue-600 truncate"
                                                        >
                                                            {{ homework.title }}
                                                        </div>
                                                    </div>
                                                    <div class="inline-flex items-center ml-5 space-x-6 lg:justify-end">
                                                        <button
                                                            class="ml-2 flex-shrink-0 flex"
                                                            @click="openModal(homework)"
                                                        >
                                                            <span
                                                                class="px-5 py-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 transform hover:scale-110"
                                                            >
                                                                Visualizar
                                                            </span>
                                                        </button>
                                                    </div>
                                                </div>
                                                <div class="flex flex-row space-x-2 justify-end">
                                                    <div v-if="evaluacionesNotEmpty">
                                                        <div
                                                            v-if="tareaEntregada(evaluaciones, homework)"
                                                            class="flex flex-row space-x-2"
                                                        >
                                                            <span>Calificación: </span>
                                                            <div v-if="existeEvaluacion(evaluaciones, homework)">
                                                                Pendiente
                                                            </div>
                                                            <div v-else>
                                                                {{ calificacionTarea(evaluaciones, homework) }}
                                                            </div>
                                                        </div>
                                                        <div v-else>Tarea no entregada</div>
                                                    </div>
                                                    <div v-else>Tarea no entregada</div>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </template>
                    <div class="flex justify-end px-4 sm:px-6 lg:px-8">
                        <button
                            class="ml-24 flex flex-row text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                            @click="revisaProgreso(ultimaLeccion())"
                        >
                            <span v-if="ultimaLeccion()">Finalizar curso</span>
                            <span v-else>Siguiente leccion</span>
                        </button>
                    </div>
                </div>
            </div>
            <div v-if="showModal">
                <ModalInfo>
                    <template #content>
                        <div class="flex flex-col px-4 sm:px-6 md:px-8 lg:px-10 py-8 rounded-3xl">
                            <div class="flex w-1/12 h-auto justify-center cursor-pointer" @click="cierraModal()">
                                <svg
                                    class="feather feather-x"
                                    fill="none"
                                    height="24"
                                    stroke="#000000"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    viewBox="0 0 24 24"
                                    width="24"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <line x1="18" x2="6" y1="6" y2="18" />
                                    <line x1="6" x2="18" y1="6" y2="18" />
                                </svg>
                            </div>
                            <div class="font-medium self-center text-xl sm:text-3xl text-gray-800">Descripción</div>
                            <div class="mt-4 self-center text-xl sm:text-md text-gray-800">
                                {{ homeworkData.description }}
                            </div>
                            <span
                                class="mt-4 block py-3 text-xs font-bold leading-normal text-center text-blue-500 uppercase border-b-4 border-blue-500"
                            >
                                Recursos
                            </span>
                            <!-- Adaptar con los recursos de la tarea una vez este resuelto el bug del back (de momento usa el recurso hardcodeado de la lección)-->
                            <div v-if="activeLesson.resources.length > 0" class="flex flex-wrap mt-4 mb-4">
                                <div
                                    v-for="(resource, resourceIndex) in activeLesson.resources"
                                    :key="resourceIndex"
                                    class="grow"
                                >
                                    <button
                                        class="cursor-pointer hover:bg-gray-200 px-4 py-3 bg-gray-100 rounded-md text-black outline-none focus:ring-4 shadow-lg transform active:scale-x-75 transition-transform flex w-full mb-10"
                                        @click="openResourceHomework(resource.resource)"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke-width="1.75"
                                            stroke="currentColor"
                                            class="w-6 h-6"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                d="M9 8.25H7.5a2.25 2.25 0 00-2.25 2.25v9a2.25 2.25 0 002.25 2.25h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25H15M9 12l3 3m0 0l3-3m-3 3V2.25"
                                            />
                                        </svg>
                                        <div class="">
                                            <div class="whitespace-normal overflow-hidden">
                                                <div class="">{{ 'Descargar Material' }}</div>
                                            </div>
                                        </div>
                                    </button>
                                </div>
                            </div>
                            <a
                                class="mt-4 block py-3 text-xs font-bold leading-normal text-center text-blue-500 uppercase border-b-4 border-blue-500"
                            >
                                Entregar
                            </a>
                            <LessonsChat :homework-id="homeworkData.id" :chat-mode="false" />
                            <div
                                v-if="evaluacionesNotEmpty"
                                class="w-10/12 rounded-md bg-white shadow px-2 flex flex-row flex-wrap justify-start items-center space-x-2 mt-5"
                            >
                                <template v-if="!existeEvaluacion(evaluaciones, homeworkData)">
                                    <img
                                        v-if="!profesorImage"
                                        :src="require('@/assets/images/user-avatar.png')"
                                        class="object-none box-border h-10 w-10 rounded-full mt-2"
                                    />
                                    <img
                                        v-if="profesorImage"
                                        :src="
                                            profesorImage.includes('https://')
                                                ? profesorImage
                                                : 'http://localhost:8000' + profesorImage
                                        "
                                        class="object-none box-border h-10 w-10 rounded-full mt-2"
                                    />
                                    <div class="flex flex-col p-2 rounded-md">
                                        <span class="text-xs font-mono">{{ profesorNombreCompleto }}</span>
                                        <span>{{ retroAlimentacionTarea(evaluaciones, homeworkData) }}</span>
                                    </div>
                                </template>
                            </div>
                        </div>
                    </template>
                </ModalInfo>
            </div>
        </template>
    </div>
</template>

<script>
import { getErrorDetails } from '@/assets/utils/utils'
import LessonsChat from '@/components/lessons/LessonsChat.vue'
import ModalInfo from '@/components/ModalInfo'

export default {
    components: { LessonsChat, ModalInfo },
    data() {
        return {
            loadedData: false,
            showModal: false,
            conjuntoEvaluaciones: [],
            profesorNombreCompleto: null,
            profesorImage: null,
            leccionTerminada: null,
            homeworkList: [],
            url: '',
            result: '',
            completeCourse: null,
            modulesReturned: [],
            nameReceived: '',
            dataLessons: '',
            lessonsList: [],
            fileresource: '',
            homeworkData: {
                id: '',
                name: '',
                description: '',
                resource: '',
            },
            activeLesson: {
                resources: [],
            },
        }
    },
    computed: {
        lessonId() {
            return this.$route.params.idLeccion
        },
        courseId() {
            return this.$route.params.idCurso
        },
        moduleId() {
            return this.$route.params.idModulo
        },
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
        evaluaciones() {
            return this.conjuntoEvaluaciones
        },
        evaluacionesNotEmpty() {
            return this.conjuntoEvaluaciones.length > 0
        },
    },
    async mounted() {
        await this.getCourseData()
        this.cargaEvaluacionTareas()
        this.cargaProgresoCurso()
    },
    methods: {
        ultimaLeccion() {
            let finCurso = false // Indica si el usuario se encuentra en la última lección, se inicia en false para mostrar "Siguiente lección" en botón
            if (this.completeCourse !== null) {
                console.log(this.completeCourse)
                const ultimoModulo = this.completeCourse.modules.length - 1
                const lesson = this.completeCourse.modules[ultimoModulo].lessons.length - 1
                console.log(lesson)
                if (lesson > -1) {
                    finCurso = this.completeCourse.modules[ultimoModulo].lessons[lesson].id === parseInt(this.lessonId)
                }
            }
            return finCurso
        },
        checaProgresoLeccion(leccion) {
            let leccionCompletada = false
            if (this.leccionTerminada !== null) {
                if (this.leccionTerminada.filter((item) => item.lesson === leccion).length > 0) {
                    leccionCompletada =
                        this.leccionTerminada.filter((item) => item.lesson === leccion)[0].progress === 100
                }
            }
            return leccionCompletada
        },
        cierraModal() {
            this.showModal = false
            this.cargaEvaluacionTareas()
        },
        existeEvaluacion(evaluaciones, homework) {
            let data = true
            if (evaluaciones.filter((t) => t.homeworkLessonData.id === homework.id).length > 0) {
                data = evaluaciones.filter((t) => t.homeworkLessonData.id === homework.id)[0].homeworkReview === null
            }
            return data
        },
        tareaEntregada(evaluaciones, homework) {
            return evaluaciones.filter((t) => t.homeworkLessonData.id === homework.id).length > 0
        },
        calificacionTarea(evaluaciones, homework) {
            return evaluaciones.filter((t) => t.homeworkLessonData.id === homework.id)[0].homeworkReview.qualification
        },
        profesorId(evaluaciones, homework) {
            return evaluaciones.filter((t) => t.homeworkLessonData.id === homework.id)[0].homeworkReview.createdBy
        },
        retroAlimentacionTarea(evaluaciones, homework) {
            this.cargaProfesor(evaluaciones, homework)
            return evaluaciones.filter((t) => t.homeworkLessonData.id === homework.id)[0].homeworkReview.review
        },
        async cargaProfesor(evaluaciones, homework) {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                const profesorData = await this.$store.dispatch(
                    'user/fetchUser',
                    this.profesorId(evaluaciones, homework)
                )
                this.profesorNombreCompleto = profesorData.getFullName
                this.profesorImage = profesorData.picture
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
         * Petición para obtener la información completa de un curso
         * @returns {Promise<void>}
         */
        async getCourseData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                this.completeCourse = await this.$store.dispatch('course/getCourseModulesAndLessons', this.courseId)
                this.loadedData = true
                await this.getLessonData()
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
         * Recarga la pantalla con el curso correspondiente
         * @param lesson
         * @param modulo
         */
        changeActiveLesson(lesson, modulo) {
            this.$router.push({
                path: `/cursos/${this.courseId}/modulo/${modulo.id}/leccion/${lesson.id}`,
            })
        },
        /**
         * Carga la información de la lección activa
         * @returns {Promise<void>}
         */
        async getLessonData() {
            this.activeLesson = await this.$store.dispatch('lesson/getLesson', this.lessonId)
            if (this.activeLesson.description.indexOf('oembed')) {
                this.activeLesson.description = this.activeLesson.description.replace('oembed', 'iframe')
                this.activeLesson.description = this.activeLesson.description.replace('url', 'src')
                this.activeLesson.description = this.activeLesson.description.replace('watch?v=', 'embed/')
            }
            await this.getHomeworksLesson()
        },
        async getHomeworksLesson() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const dataHomeworks = await this.$store.dispatch('homework/getHomeworks', this.lessonId)
                this.homeworkList = dataHomeworks.results
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
        async cargaEvaluacionTareas() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const evaluaciones = await this.$store.dispatch(
                    'homework-review/homeworkListByUser',
                    this.activeUserInfo.id
                )
                this.conjuntoEvaluaciones = evaluaciones.results.map((item) => ({
                    homeworkReview: item.homeworkLessonReview,
                    homeworkLessonData: item.homeworkLesson,
                }))
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
        async cargaProgresoCurso() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const progreso = await this.$store.dispatch('course/getUserProgress', this.courseId)
                this.leccionTerminada = progreso.results.filter((item) => item.user === this.activeUserInfo.id)
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
        async revisaProgreso(ultimaLeccion) {
            let nextModulo = ''
            let nextLeccion = ''
            if (this.completeCourse !== null && !ultimaLeccion) {
                const indexModulo = this.completeCourse.modules.findIndex((t) => t.id === parseInt(this.moduleId))
                const leccion = this.completeCourse.modules[indexModulo].lessons.findIndex(
                    (t) => t.id === parseInt(this.lessonId)
                )
                const numLecciones = this.completeCourse.modules[indexModulo].lessons.length - 1

                if (leccion === numLecciones) {
                    nextModulo = this.completeCourse.modules[indexModulo + 1].id
                    nextLeccion = this.completeCourse.modules[indexModulo + 1].lessons[0].id
                } else {
                    nextModulo = this.completeCourse.modules[indexModulo].id
                    nextLeccion = this.completeCourse.modules[indexModulo].lessons[leccion + 1].id
                }
            }
            if (
                !(this.leccionTerminada.length > 0) ||
                this.leccionTerminada.filter((item) => item.lesson === parseInt(this.lessonId)) < 1
            ) {
                await this.nextLesson()
            }
            if (ultimaLeccion) {
                this.$router.push({
                    path: `/cursos/temario/${this.courseId}`,
                })
            } else {
                this.$router.push({
                    path: `/cursos/${this.courseId}/modulo/${nextModulo}/leccion/${nextLeccion}`,
                })
            }
        },
        openModal(homework) {
            this.showModal = true
            this.homeworkData.description = homework.description
            this.homeworkData.id = parseInt(homework.id)
            // incluir resource una vez se haya resuelto el back
        },
        openResource(url) {
            window.open(
                url,
                '_blank' // <- This is what makes it open in a new window.
            )
        },
        openResourceHomework(url) {
            window.open(
                url,
                '_blank' // <- This is what makes it open in a new window.
            )
        },
        async nextLesson() {
            const payload = {
                lesson: this.$route.params.idLeccion,
                progress: 100,
            }
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                await this.$store.dispatch('course/saveUserProgress', payload)
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
         * Agrega las animaciones de acordeon a los módulos
         * @param moduleIndex
         */
        selectedModuleIndexClick(moduleIndex) {
            const moduleInfoElement = document.querySelectorAll('[data-module-id="' + moduleIndex + '"]')[0]
            if (moduleInfoElement.classList.contains('block')) {
                moduleInfoElement.classList.remove('block')
                moduleInfoElement.classList.add('hidden')
            } else {
                moduleInfoElement.classList.remove('hidden')
                moduleInfoElement.classList.add('block')
            }
        },
    },
}
</script>

<style lang="scss">
#lessonContainer figure.media iframe {
    width: 100%;
    min-height: 400px;
}
</style>
