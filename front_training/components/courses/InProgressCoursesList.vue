<template>
    <div class="py-8 max-w-full bg-white text-gray-700 shadow">
        <div class="container mx-auto px-10">
            <div class="w-full">
                <div class="flex container md:px-8">
                    <span class="text-green-500 flex-none">
                        <GridPlusIcon />
                    </span>
                    <h2 class="md:px-5 flex items-center text-3xl flex-auto">
                        <span>Cursos en progreso</span>
                    </h2>
                </div>
                <div class="shadow-lg w-full bg-white dark:bg-gray-700 relative overflow-hidden">
                    <a href="#" class="w-full h-full block" />
                </div>
            </div>
            <div class="flex items-center w-full space-x-4">
                <div class="w-1/2" />
            </div>
            <section class="text-gray-600 body-font">
                <div class="container mx-auto">
                    <div class="flex flex-wrap -mx-2">
                        <template v-if="studentCoursesList.length === 0">
                            <div class="max-w-screen-xl mx-auto text-center px-4 sm:px-6 lg:px-8">
                                <div class="sm:rounded-md mt-5 text-center">
                                    <p class="text-black-400">No hay registros aún</p>
                                </div>
                            </div>
                        </template>
                        <div v-for="(studentCourse, index) in studentCoursesList" :key="index">
                            <div class="p-4">
                                <div class="cards-container">
                                    <div
                                        class="h-full rounded-xl shadow-cla-blue bg-gradient-to-r from-indigo-50 to-blue-50 overflow-hidden"
                                    >
                                        <img
                                            v-if="!!studentCourse.course.courseImage"
                                            class="lg:h-48 md:h-36 w-full object-cover object-center scale-110 transition-all duration-400 hover:scale-100"
                                            :src="studentCourse.course.courseImage.image"
                                            alt="blog"
                                        />
                                        <img
                                            v-else
                                            class="lg:h-48 md:h-36 w-full object-cover object-center scale-110 transition-all duration-400 hover:scale-100"
                                            src="/images/aviv.webp"
                                            alt="blog"
                                        />
                                        <div class="p-6">
                                            <h2
                                                class="tracking-widest text-xs title-font font-medium text-gray-400 mb-1"
                                            >
                                                {{
                                                    studentCourse.course.courseType === 'public'
                                                        ? 'Público'
                                                        : 'Requiere invitación'
                                                }}
                                            </h2>
                                            <h1 class="title-font text-lg font-medium text-gray-600 mb-3">
                                                {{ studentCourse.course.name }}
                                            </h1>
                                            <p class="max-h-28 leading-relaxed mb-3 overflow-auto">
                                                {{ studentCourse.course.description }}
                                            </p>
                                            <p class="tracking-widest text-xs title-font text-gray-400 mb-1">
                                                <span class="font-bold">Profesor:</span>
                                                {{ studentCourse.course.createdByObj.getFullName }}
                                            </p>
                                            <p class="tracking-widest text-xs title-font text-gray-400 mb-1">
                                                <span class="font-bold">Progreso completado:</span>
                                                {{ studentCourse.course.createdByObj.getFullName }}
                                            </p>
                                            <div class="flex items-center flex-wrap">
                                                <button
                                                    class="bg-gradient-to-r from-blue-400 to-blue-500 hover:scale-105 drop-shadow-md shadow-cla-blue px-4 py-1 rounded-lg text-white"
                                                    @click="viewCourse(studentCourse.course.id)"
                                                >
                                                    Ver Curso
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
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
            shortedDescription: '',
            studentCoursesList: [],
            dataReturned: '',
        }
    },
    computed: {
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
    },
    mounted() {
        this.getCourses()
    },
    methods: {
        async getCourses() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                this.dataReturned = await this.$store.dispatch('course/getCoursesUser', this.activeUserInfo.id)
                this.studentCoursesList = this.dataReturned.results
                // Calculamos el tiempo transcurrido
                this.studentCoursesList.map((item) => {
                    console.log(item)
                    return item
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
        viewCourse(id) {
            this.$router.push({ path: `/cursos/temario/${id}` })
        },
    },
}
</script>

<style scoped>
.cards-container {
    max-width: 265px;
    min-width: 260px;
}
</style>
