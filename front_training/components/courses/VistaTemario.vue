<template>
    <div class="flex items-center justify-center bg-gray-100">
        <div class="w-full px-10 py-8 mx-auto bg-white rounded-lg shadow-xl">
            <div class="w-full md:w-12/12">
                <div class="flex container">
                    <h2 class="flex items-center text-3xl flex-auto">
                        <b>Temario de {{ courseModulesAndLessons.name }}</b>
                    </h2>
                    <div v-if="!isSameUser && courseLoaded">
                        <div class="flex flex-initial justify-end">
                            <button
                                v-if="!isUserEnrolled"
                                class="text-blue-700 hover:text-white border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:hover:bg-blue-600 dark:focus:ring-blue-900"
                                @click="startCourse()"
                            >
                                Iniciar Curso
                            </button>
                        </div>
                        <div class="flex flex-initial justify-end">
                            <NuxtLink
                                v-if="isUserEnrolled"
                                class="text-blue-700 hover:text-white border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:hover:bg-blue-600 dark:focus:ring-blue-900"
                                :to="`/cursos/${courseId}/modulo/${moduleId}/leccion/${lessonId}`"
                            >
                                Continuar Curso
                            </NuxtLink>
                        </div>
                    </div>
                    <div v-if="isSameUser" class="flex flex-initial justify-end">
                        <NuxtLink
                            class="text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-900"
                            :to="`/gestion/mis-cursos/${courseId}/editar`"
                        >
                            Editar
                        </NuxtLink>
                    </div>
                    <div class="flex flex-initial justify-end">
                        <NuxtLink
                            class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                            :to="`/cursos`"
                        >
                            Regresar
                        </NuxtLink>
                    </div>
                </div>
                <div class="shadow-lg w-full bg-white dark:bg-gray-700 relative overflow-hidden">
                    <a href="#" class="w-full h-full block" />
                </div>
            </div>
            <div class="mt-8 mx-auto space-y-6">
                <!-- Accordion start -->
                <ul
                    v-for="(modulo, index) in courseModulesAndLessons.modules"
                    :key="modulo.topic"
                    class="accordion w-full p-5"
                >
                    <li class="cursor-pointer my-1">
                        <span
                            class="font-bold text-xl tracking-tight text-gray-500 flex flex-row justify-between items-center"
                            @click="selectedItemClick(index)"
                        >
                            <span>{{ modulo.topic }}</span>
                            <svg
                                class="text-gray-500 mr-1"
                                xmlns="http://www.w3.org/2000/svg"
                                width="16"
                                height="16"
                                fill="currentColor"
                                viewBox="0 0 16 16"
                            >
                                <path
                                    fill-rule="evenodd"
                                    d="M8 4a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1
                   .708-.708L7.5 10.293V4.5A.5.5 0 0 1 8 4z"
                                />
                            </svg>
                        </span>
                        <div :data-module-id="index" class="text-gray-500 text-md p-2 block">
                            <div v-for="(lesson, indexLesson) in modulo.lessons" :key="indexLesson">
                                <div class="bg-white hover:bg-gray-50 mt-4 border-b rounded-lg">
                                    <a class="bg-white py-4 border-t cursor-pointer mt-200 py-65">
                                        <div class="px-4 py-4 flex justify-between">
                                            <span class="text-sm font-semibold text-gray-900">
                                                {{ lesson.topic }}
                                            </span>
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
</template>

<script>
import { getErrorDetails } from '@/assets/utils/utils'

export default {
    data() {
        return {
            isSameUser: false,
            userProgressReturned: [],
            moduleId: null,
            lessonId: null,
            isUserEnrolled: false,
            courseModulesAndLessons: [],
            studentCourseProgress: [],
            courseLoaded: false,
        }
    },
    computed: {
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
        courseId() {
            return this.$route.params.idTemario
        },
    },
    async mounted() {
        await this.getCourseData()
        this.courseLoaded = true
    },
    methods: {
        async getProgressUser() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                this.userProgressReturned = await this.$store.dispatch('course/getUserProgress', this.courseId)
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
            if (this.courseModulesAndLessons.createdBy === this.activeUserInfo.id) {
                this.isSameUser = true
                return
            }
            // Valida si el curso ya está en curso
            const params = `?user=${this.activeUserInfo.id}&course=${this.courseId}`
            this.studentCourseProgress = await this.$store.dispatch('course/getCoursesUserParam', params)
            if (this.studentCourseProgress.count === 0) {
                // Si no está en curso, termina el flujo
                return
            }
            this.isUserEnrolled = true
            console.log('USER ENROLED')
            const progressLesson = this.userProgressReturned.results.map((progress) => progress.lesson)
            const courseLessons = this.courseModulesAndLessons.modules
            let aux = 0
            this.moduleId = this.courseModulesAndLessons.modules[0].id
            const idFirstLesson = this.courseModulesAndLessons.modules[0].lessons[0].id
            this.lessonId = idFirstLesson
            while (aux < courseLessons.length && this.lessonId === idFirstLesson) {
                const curentModule = courseLessons[aux]
                aux++
                const filtrado = curentModule.lessons.filter((lesson) => progressLesson.includes(lesson.id))
                if (filtrado.length > 0) {
                    const { id } = filtrado[filtrado.length - 1]
                    this.lessonId = id
                    this.moduleId = curentModule.id
                }
            }
        },
        async getCourseData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                const getCourseModulesAndLessonsResponse = await this.$store.dispatch(
                    'course/getCourseModulesAndLessons',
                    this.courseId
                )

                getCourseModulesAndLessonsResponse.modules = getCourseModulesAndLessonsResponse.modules.filter(
                    (module) => {
                        return module.lessons.length > 0
                    }
                )

                this.courseModulesAndLessons = getCourseModulesAndLessonsResponse
                await this.getProgressUser()
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
        selectedItemClick(moduleIndex) {
            const moduleInfoElement = document.querySelectorAll('[data-module-id="' + moduleIndex + '"]')[0]
            if (moduleInfoElement.classList.contains('block')) {
                moduleInfoElement.classList.remove('block')
                moduleInfoElement.classList.add('hidden')
            } else {
                moduleInfoElement.classList.remove('hidden')
                moduleInfoElement.classList.add('block')
            }
        },
        async startCourse() {
            const data = {
                course: this.courseId,
                user: this.activeUserInfo.id,
            }
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                await this.$store.dispatch('course/suscribeUserToCourse', data)
                this.goToFirstLesson()
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
         * Función enfocada para guardar el progreso de una lección de un alumno por primera vez.
         * @returns {Promise<void>}
         */
        async goToFirstLesson() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            // Busca la primer lección de un módulo de curso
            const payload = {
                lesson: this.courseModulesAndLessons.modules[0].lessons[0].id,
                progress: 100,
            }
            try {
                // Guarda el progreso del usuario con la primer lección
                await this.$store.dispatch('course/saveUserProgress', payload)
                // Una vez guardado el progreso, actualiza el progreso de nuestro lado
                const params = `?user=${this.activeUserInfo.id}&course=${this.courseId}`
                this.studentCourseProgress = await this.$store.dispatch('course/getCoursesUserParam', params)
                this.moduleId = this.courseModulesAndLessons.modules[0].id
                this.lessonId = this.courseModulesAndLessons.modules[0].lessons[0].id
                this.$router.push({
                    path: `/cursos/${this.courseId}/modulo/${this.moduleId}/leccion/${this.lessonId}`,
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
