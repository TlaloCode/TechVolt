<template>
    <div class="py-8 max-w-full bg-white text-gray-700 shadow">
        <div class="max-w-screen-xl mx-auto">
            <div class="w-full md:w-12/12">
                <div class="flex container md:px-8">
                    <span class="mt-2 text-green-500 flex-none">
                        <CapIcon />
                    </span>
                    <h2 class="md:px-5 flex items-center text-4xl flex-auto">
                        <b>{{ titleForm }}</b>
                    </h2>
                    <nuxt-link
                        :to="`/gestion/mis-cursos/${courseId}/modulos/${moduleId}/lecciones/${lessonId}/tareas`"
                        class="'w-28 text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900'"
                    >
                        Regresar
                    </nuxt-link>
                </div>
            </div>
            <div class="shadow-lg w-full bg-white dark:bg-gray-700 relative overflow-hidden">
                <a href="#" class="w-full h-full block" />
            </div>
            <div class="flex items-center w-full md:w-1/2 space-x-4">
                <div class="w-1/2" />
            </div>
        </div>
        <div>
            <ValidationObserver v-slot="{ invalid }">
                <div class="max-w-screen-xl mx-auto flex items-center justify-center px-10 py-5">
                    <div class="mx-auto w-full">
                        <div class="mb-5">
                            <label class="mb-3 block text-base font-medium text-[#07074D]"> Título de la tarea </label>
                            <ValidationProvider v-slot="{ errors }" name="Nombre" rules="required|min:4|max:50">
                                <input
                                    v-model="homeworkData.title"
                                    name="name"
                                    class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                />
                                <span class="block text-red-700 text-sm mt-1 ml-1 h-5">{{ errors[0] }}</span>
                            </ValidationProvider>
                        </div>
                        <div class="mb-5">
                            <label class="mb-3 block text-base font-medium text-[#07074D]"> Descripción </label>
                            <ValidationProvider v-slot="{ errors }" name="Descripción" rules="required|max:500|min:4">
                                <textarea
                                    v-model="homeworkData.description"
                                    rows="4"
                                    placeholder="En esta tarea haremos..."
                                    class="w-full resize-none rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                />
                                <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                            </ValidationProvider>
                        </div>
                        <div v-if="type === TYPE_VIEW.EDIT" class="px-4 py-2 font-semibold">
                            Material de ayuda cargado a tarea
                        </div>
                        <div v-if="type === TYPE_VIEW.EDIT" class="px-4 py-2 font-semibold text-blue-600 text-sm">
                            {{ fileresource }}
                        </div>
                        <div class="grid grid-cols-1 space-y-2">
                            <label class="px-4 py-2 font-semibold space-y-4">Subir material de Ayuda *</label>
                            <div class="flex items-center justify-center w-full">
                                <label
                                    class="flex flex-col rounded-lg border-4 border-dashed w-full h-60 p-10 group text-center"
                                >
                                    <div
                                        class="h-full w-full text-center flex flex-col items-center justify-center items-center"
                                    >
                                        <div class="flex flex-auto max-h-48 w-1/5 mx-auto -mt-10">
                                            <img
                                                class="has-mask h-36 object-center"
                                                src="https://img.freepik.com/free-vector/image-upload-concept-landing-page_52683-27130.jpg?size=338&ext=jpg"
                                                alt="freepik image"
                                            />
                                        </div>
                                        <p class="pointer-none text-gray-500">
                                            <span class="text-blue-600 text-sm hover:underline">
                                                Selecciona un archivo de tu equipo
                                            </span>
                                        </p>
                                    </div>
                                    <input type="file" class="hidden" @change="droppedFiles($event)" />
                                </label>
                            </div>
                        </div>
                        <p class="text-sm text-gray-300">
                            <span>Tipos permitidos: doc, pdf, imágenes</span>
                        </p>
                        <div class="px-4 py-2 font-semibold">Archivos a subir</div>
                        <img
                            v-if="fileType === 'image/jpg' || fileType === 'image/png' || fileType === 'image/jpeg'"
                            :src="fileURL"
                            class="w-1/3"
                            alt="IMG"
                        />
                        <p>{{ fileName }}</p>
                        <div class="max-w-screen-xl mx-auto text-center px-4 sm:px-6 lg:px-8">
                            <div class="bg-white shadow overflow-hidden sm:rounded-md mt-5">
                                <ul>
                                    <li v-for="(file, index) in files" :key="index">
                                        <a
                                            href="#"
                                            class="block hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition duration-150 ease-in-out"
                                        >
                                            <div class="px-4 py-4 sm:px-6">
                                                <div class="flex items-center justify-between">
                                                    <div class="text-sm leading-5 font-medium text-blue-600 truncate">
                                                        {{ file.name }}
                                                    </div>
                                                    <div class="ml-2 flex-shrink-0 flex">
                                                        <span
                                                            class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-pink-100 text-red-800"
                                                            @click="removeFile(file)"
                                                        >
                                                            borrar
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div
                            v-if="type === TYPE_VIEW.CREATE"
                            class="justify-end flex items-center space-x-4 mt-12 mb-16"
                        >
                            <button
                                :disabled="invalid"
                                class="flex items-center text-white text-md border-black-300 border bg-green-400 hover:bg-green-300 px-10 py-2 rounded-full"
                                :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                @click="saveHomework"
                            >
                                Crear Tarea
                            </button>
                        </div>
                        <div v-if="type === TYPE_VIEW.EDIT" class="justify-end flex items-center space-x-4 mt-12 mb-16">
                            <button
                                :disabled="invalid"
                                class="flex items-center text-white text-md border-black-300 border bg-green-400 hover:bg-green-300 px-10 py-2 rounded-full"
                                :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                @click="editHomework"
                            >
                                Guardar Tarea
                            </button>
                        </div>
                    </div>
                </div>
            </ValidationObserver>
        </div>
    </div>
</template>

<script>
import { TYPE_VIEW } from 'assets/utils/enums'
import { getErrorDetails } from '@/assets/utils/utils'
import CapIcon from '@/components/icons/Cap.vue'
import mixins from '@/mixins/globals'

export default {
    components: { CapIcon },
    mixins: [mixins],
    props: {
        type: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            dataReturned: {},
            isHomework: '',
            fileresource: '',
            fileType: '',
            fileName: '',
            files: [],
            idHomework: '',
            resourceObtained: [],
            homeworkData: {
                title: '',
                lesson: '',
                description: '',
            },
        }
    },
    computed: {
        titleForm() {
            return this.type === TYPE_VIEW.CREATE ? 'Crear nueva tarea' : 'Editar tarea'
        },
        courseId() {
            return this.$route.params.idCurso
        },
        moduleId() {
            return this.$route.params.idModulo
        },
        lessonId() {
            return this.$route.params.idLeccion
        },
        homeworkId() {
            return this.$route.params.idTarea
        },
    },
    created() {
        this.setComponentInfo()
    },
    methods: {
        // Método para verificar si estamos en vista de editar
        setComponentInfo() {
            if (this.type === TYPE_VIEW.EDIT) {
                this.setInitialData()
            }
        },
        // Configura la información inicial para vista Editar
        async setInitialData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                this.dataReturned = await this.$store.dispatch('homework/getHomework', this.homeworkId)
                this.homeworkData.title = this.dataReturned.title
                this.homeworkData.description = this.dataReturned.description
                this.homeworkData.lesson = this.dataReturned.lesson
                this.lessonObtained = this.dataReturned.resources.map((i) => i.id)
                for (let i = 0; i < this.dataReturned.resources.length; i++) {
                    const uploadedText = this.dataReturned.resources[i].resource
                    this.fileresource = uploadedText.split('/').slice(-1).toString()
                }
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
        // Método para crear tarea.
        async saveHomework(courseId, moduleId, lessonId) {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                const payload = {
                    title: this.homeworkData.title,
                    description: this.homeworkData.description,
                    lesson: this.lessonId,
                    resources: this.resourceObtained,
                }
                await this.$store.dispatch('homework/createHomework', payload)
                this.readyCreated = 1
                this.$router.push({
                    path: `/gestion/mis-cursos/${this.courseId}/modulos/${this.moduleId}/lecciones/${this.lessonId}/tareas`,
                })
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Tarea creada',
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
        /**
         * Edita una tarea
         * @returns {Promise<void>}
         */
        async editHomework() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                const payload = {
                    data: {
                        title: this.homeworkData.title,
                        description: this.homeworkData.description,
                        lesson: this.lessonId,
                        resources: this.resourceObtained,
                    },
                    id: this.homeworkId,
                }

                await this.$store.dispatch('homework/updateHomework', payload)
                this.$router.go(-1)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Tarea actualizada',
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
        /**
         * Método para agregar recursos a una tarea
         * @param e
         * @returns {Promise<void>}
         */
        async droppedFiles(e) {
            const droppedFiles = event.target.files[0]
            if (!droppedFiles) return
            this.files = [droppedFiles]
            const { files } = event.target
            if (files && files[0]) {
                const form = new FormData()
                form.append('resource', files[0])
                const payload = {
                    data: form,
                }
                const loading = this.$vs.loading({
                    scale: 0.95,
                    type: 'circles',
                    color: '#16a34a',
                })

                try {
                    const fileLoaded = await this.$store.dispatch('homework/createHomeworkResource', payload)
                    this.resourceObtained = []
                    this.resourceObtained.push(fileLoaded.id)
                    this.$vs.notification({
                        color: 'success',
                        title: 'Éxito',
                        text: 'Recurso actualizado',
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
            }
        },
        removeFile(file) {
            this.files = this.files.filter((f) => {
                return f !== file
            })
            this.homeworkData.resource = this.files
        },
    },
}
</script>
