<template>
    <div class="bg-gray-100 lessonsEditor--container">
        <ValidationObserver ref="observer" v-slot="{ invalid }" tag="div" class="w-full min-h-full register-container">
            <div class="relative hover-trigger">
                <button
                    class="fixed bottom-0 right-0 w-12 h-12 mr-12 mb-8 text-blue-800 text-sm font-semibold bg-gray-300 rounded-full hover:bg-gray-100 focus:outline-none focus:shadow-outline focus:bg-gray-100 hover:shadow-xs p-3 my-4"
                    @click="showHelp = true"
                >
                    <div class="absolute bg-white border border-grey-100 px-4 py-2 hover-target">Ayuda</div>
                    <svg class="ue on" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
                        <path
                            class="db text-slate-500"
                            d="M8 0C3.6 0 0 3.6 0 8s3.6 8 8 8 8-3.6 8-8-3.6-8-8-8zm0 12c-.6 0-1-.4-1-1s.4-1 1-1 1 .4 1 1-.4 1-1 1zm1-3H7V4h2v5z"
                        />
                    </svg>
                </button>
            </div>
            <div class="container mx-auto my-5 p-5">
                <div class="w-full md:w-full mx-2 h-64">
                    <div class="bg-white p-3 shadow-sm rounded-sm max-w-screen-xl px-10 mx-auto">
                        <div class="flex items-center justify-between">
                            <section class="px-4 py-2 font-semibold flex items-center text-base">
                                <span class="text-green-500">
                                    <svg
                                        class="h-8"
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
                                <span v-if="type === TYPE_VIEW.CREATE">Crear nueva Lección</span><br />
                                <span v-if="type === TYPE_VIEW.EDIT" class="space-x-1">Editar Lección</span>
                            </section>
                            <br />
                            <div class="flex flex-row">
                                <div v-if="type === TYPE_VIEW.EDIT">
                                    <button
                                        class="text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                                        @click="goToEditHomework(lessonId)"
                                    >
                                        Ir a Tareas
                                    </button>
                                </div>
                                <div class="ml-2 flex-shrink-0 flex">
                                    <button @click="$router.go(-1)">
                                        <div
                                            class="'w-28 text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900'"
                                        >
                                            <p>Regresar</p>
                                        </div>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="text-gray-700">
                            <div class="text-sm">
                                <div class="px-4 py-2 font-semibold">Título</div>
                                <ValidationProvider v-slot="{ errors }" name="Nombres" rules="required|max:120|min:4">
                                    <input
                                        v-model="lessonData.topic"
                                        class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-4 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                    />
                                    <span class="block text-red-700 text-xs mt-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </div>
                            <div class="grid grid-cols-2 gap-4 my-4">
                                <div class="px-4 py-2 font-semibold col-span-2">Duración de la lección</div>
                                <ValidationProvider
                                    v-slot="{ errors }"
                                    name="Duración en horas"
                                    rules="required|min_value:0"
                                    tag="div"
                                    class="w-full"
                                >
                                    <div class="flex items-center">
                                        <select
                                            v-model="lessonData.hoursTaken"
                                            class="flex-1 rounded-md border border-[#e0e0e0] bg-white py-3 px-4 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                        >
                                            <option disabled value="">Seleccione el numero de horas</option>
                                            <option value="0">0</option>
                                            <option value="1">1</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option>
                                            <option value="4">4</option>
                                        </select>
                                        <span class="pl-3 pr-10">Horas</span>
                                    </div>
                                    <span class="block text-black-700 text-xs mt-1 h-5">
                                        *Debe seleccionar un mínimo de 0 horas
                                    </span>
                                    <span class="block text-red-700 text-xs mt-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                                <ValidationProvider
                                    v-slot="{ errors }"
                                    name="Duración en minutos"
                                    rules="required|min_value:0|max_value:60"
                                    tag="div"
                                    class="w-full"
                                >
                                    <div class="flex items-center">
                                        <select
                                            v-model="lessonData.minutesTaken"
                                            class="flex-1 rounded-md border border-[#e0e0e0] bg-white py-3 px-4 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                        >
                                            <option disabled value="">Seleccione el numero de minutos</option>
                                            <option value="0">0</option>
                                            <option value="15">15</option>
                                            <option value="30">30</option>
                                            <option value="45">45</option>
                                        </select>
                                        <span class="pl-3">Minutos</span>
                                    </div>
                                    <span class="block text-black-700 text-xs mt-1 h-5">
                                        *Debe seleccionar un mínimo de 0 minutos
                                    </span>
                                    <span class="block text-red-700 text-xs mt-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </div>
                        </div>
                        <div class="px-4 py-2 font-semibold space-y-4">Añada la Descripción</div>
                        <client-only placeholder="Cargando...">
                            <ckeditor-nuxt v-model="lessonData.description" :config="editorConfig" class="h-full" />
                        </client-only>
                        <template v-if="TYPE_VIEW.EDIT">
                            <div class="px-4 py-2 font-semibold">Archivos subidos a Leccion</div>
                            <div class="px-4 py-2 font-semibold text-blue-600 text-sm">
                                <div class="bg-white shadow overflow-hidden sm:rounded-md mt-5">
                                    <ul>
                                        <li v-for="(file, index) in fileresource" :key="index">
                                            <a
                                                href="#"
                                                class="block hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition duration-150 ease-in-out"
                                            >
                                                <div class="px-4 py-4 sm:px-6">
                                                    <div class="flex items-center justify-between">
                                                        <div
                                                            class="text-sm leading-5 font-medium text-blue-600 truncate"
                                                        >
                                                            {{ file.name }}
                                                        </div>
                                                        <div class="ml-2 flex-shrink-0 flex">
                                                            <span
                                                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-pink-100 text-red-800"
                                                                @click="removeFile(file, 'old')"
                                                            >
                                                                <span class="tooltip-box"> Eliminar archivo </span>
                                                                <i class="bx bx-trash text-xl" />
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </template>

                        <div class="grid grid-cols-1 space-y-2">
                            <label class="px-4 py-2 font-semibold space-y-4">Subir recurso de lección</label>
                            <label class="flex items-center justify-center w-full">
                                <div
                                    class="flex flex-col rounded-lg border-4 border-dashed w-full h-60 p-10 group text-center cursor-pointer"
                                >
                                    <div
                                        class="h-full w-full text-center flex flex-col items-center justify-center items-center cursor-pointer"
                                    >
                                        <!---<svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-blue-400 group-hover:text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                        </svg>-->
                                        <div
                                            class="flex flex-auto max-h-48 w-1/5 mx-auto -mt-10 text-center cursor-pointer"
                                        >
                                            <img
                                                class="has-mask h-36 object-center cursor-pointer"
                                                src="https://img.freepik.com/free-vector/image-upload-concept-landing-page_52683-27130.jpg?size=338&ext=jpg"
                                                alt="freepik image"
                                            />
                                        </div>
                                        <p class="cursor-pointer text-gray-500 text-center">
                                            <span class="text-sm-center object-center" /><br />Selecciona un archivo de
                                            tu equipo
                                        </p>
                                    </div>
                                    <input type="file" multiple class="hidden" @change="droppedFiles($event)" />
                                </div>
                            </label>
                        </div>
                        <p class="text-sm text-gray-300">
                            <span>Tipos permitidos: doc, pdf, tipos de imagenes</span>
                        </p>
                        <div class="px-4 py-2 font-semibold">Archivos a subir</div>
                        <img
                            v-if="fileType === 'image/jpg' || fileType === 'image/png' || fileType === 'image/jpeg'"
                            :src="fileURL"
                            class="w-1/3"
                        />
                        <p>{{ fileName }}</p>
                        <div class="max-w-screen-xl mx-auto text-center px-4 sm:px-6 lg:px-8">
                            <div class="bg-white shadow overflow-hidden sm:rounded-md mt-5">
                                <ul>
                                    <li v-for="(file, index) in resourceObtained" :key="index">
                                        <a
                                            href="#"
                                            class="block hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition duration-150 ease-in-out"
                                        >
                                            <div class="px-4 py-4 sm:px-6">
                                                <div class="flex items-center justify-between">
                                                    <div class="text-sm leading-5 font-medium text-blue-600 truncate">
                                                        {{ file.resource }}
                                                    </div>
                                                    <div class="ml-2 flex-shrink-0 flex">
                                                        <span
                                                            class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-pink-100 text-red-800"
                                                            @click="removeFile(file, 'new')"
                                                        >
                                                            <span class="tooltip-box"> Eliminar archivo </span>
                                                            <i class="bx bx-trash text-xl" />
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                            <div class="container mt-3">
                                <div class="flex items-center justify-between">
                                    <div />
                                    <div class="ml-96 flex-shrink-0 flex">
                                        <!-- eslint-disable vue/no-v-html -->

                                        <!--eslint-enable-->
                                    </div>
                                    <button
                                        v-if="type === TYPE_VIEW.CREATE"
                                        :disabled="invalid"
                                        class="w-28 text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-green-500 dark:hover:bg-green-600 dark:focus:ring-green-600"
                                        :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                        @click="saveLesson"
                                    >
                                        Crear
                                    </button>
                                    <button
                                        v-if="type === TYPE_VIEW.EDIT"
                                        :disabled="invalid"
                                        class="w-28 text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-green-500 dark:hover:bg-green-600 dark:focus:ring-green-600"
                                        :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                        @click="editLesson"
                                    >
                                        Guardar
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="showHelp">
                <ModalInfo>
                    <template #content>
                        <div class="flex w-full h-auto justify-center items-center">
                            <div class="flex w-10/12 h-auto py-3 justify-center items-center text-2xl font-bold">
                                Ayuda con el editor de lecciones
                            </div>
                            <div class="flex w-1/12 h-auto justify-center cursor-pointer" @click="showHelp = false">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="#000000"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="feather feather-x"
                                >
                                    <line x1="18" y1="6" x2="6" y2="18" />
                                    <line x1="6" y1="6" x2="18" y2="18" />
                                </svg>
                            </div>
                        </div>
                        <div class="row-span-2 p-6 text-center sm:p-8">
                            <div class="h-full flex flex-col justify-center space-y-4">
                                <p class="text-gray-600 md:text-xl">
                                    <span class="font-serif" />Para insertar una imagen haz clic en el botón de los 3
                                    puntos del editor.
                                    <span class="font-serif" />
                                </p>
                                <img
                                    class="mx-auto"
                                    src="/images/help1.png"
                                    alt="help1"
                                    height="120"
                                    width="120"
                                    loading="lazy"
                                />
                                <p class="text-gray-600 md:text-xl">
                                    <span class="font-serif" />En seguida da clic sobre el icono de imágen. Se te
                                    despliegará una donde podras elegir tu imagen.
                                    <span class="font-serif" />
                                </p>
                                <img
                                    class="mx-auto"
                                    src="/images/help2.png"
                                    alt="help2"
                                    height="220"
                                    width="220"
                                    loading="lazy"
                                />
                                <p class="text-gray-600 md:text-xl">
                                    <span class="font-serif" /> Selecciona tu imagen y da clic en aceptar. Listo :)
                                    fácil, no?
                                    <span class="font-serif" />
                                </p>
                            </div>
                            <button
                                class="mr-1 m-auto my-4 px-6 py-2 focus:outilne-none border border-transparent rounded-lg shadow-sm text-center text-white bg-green-500 hover:bg-green-600 font-medium"
                                @click="showHelp = false"
                            >
                                Ok
                            </button>
                        </div>
                    </template>
                </ModalInfo>
            </div>
        </ValidationObserver>
    </div>
</template>

<script>
import { TYPE_VIEW } from 'assets/utils/enums'
import { getErrorDetails } from '@/assets/utils/utils'
import ModalInfo from '@/components/ModalInfo.vue'
import mixins from '@/mixins/globals'

export default {
    components: {
        'ckeditor-nuxt': () => {
            return import('@blowstack/ckeditor-nuxt')
        },
        ModalInfo,
    },
    mixins: [mixins],
    props: {
        type: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            readyCreated: 0,
            fileresource: [],
            showHelp: false,
            pageX: 0,
            pageY: 0,
            uploadDragoverTracking: false,
            uploadDragoverEvent: false,
            isHomework: false,
            fileType: '',
            fileName: '',
            selectedFile: '',
            fileURL: '',
            editorConfig: {
                removePlugins: ['Title', 'MediaEmbedToolbar'],
                simpleUpload: {
                    uploadUrl: '',
                    headers: {
                        Authorization: 'Bearer <JSON Web Token>',
                    },
                },
            },
            lessonContent: {},
            resourceObtained: [],
            contentHolder: '',
            lessonData: {
                topic: '',
                description: '',
                hoursTaken: '',
                minutesTaken: '',
            },
        }
    },
    computed: {
        moduleId() {
            return this.$route.params.idModulo
        },
        lessonId() {
            return this.$route.params.idLeccion
        },
        courseId() {
            return this.$route.params.idCurso
        },
    },
    created() {
        this.setComponentInfo()
    },
    mounted() {
        this.setPluginImageUrl()
    },
    methods: {
        // Método para verificar si estamos en vista de editar
        setComponentInfo() {
            if (this.type === TYPE_VIEW.EDIT) {
                this.setInitialData()
            }
        },
        // Método para setear la url del back para el plugin de Editor de Textos
        setPluginImageUrl() {
            let url = 'embebed-resources/'
            const baseURL =
                process.env.NODE_ENV !== 'production' ? 'http://localhost:8000/api/' : process.env.VUE_APP_API_BACK
            url = baseURL + url
            this.editorConfig.simpleUpload.uploadUrl = url
            this.editorConfig.simpleUpload.headers.Authorization = `Bearer ${this.$store.state.auth.accessToken}`
            return url
        },
        /**
         * Método para agregar recursos a la lección
         * @param event
         * @returns {Promise<void>}
         */
        async droppedFiles(event) {
            const droppedFiles = event.target.files
            if (droppedFiles !== null) {
                for (let i = 0; i < droppedFiles.length; i++) {
                    const form = new FormData()
                    form.append('resource', droppedFiles[i])
                    const payload = {
                        data: form,
                    }
                    const loading = this.$vs.loading({
                        scale: 0.95,
                        type: 'circles',
                        color: '#16a34a',
                    })

                    try {
                        const fileLoaded = await this.$store.dispatch('lesson/postLessonResource', payload)
                        fileLoaded.resource = fileLoaded.resource.split('/').slice(-1).toString()
                        this.resourceObtained.push(fileLoaded)
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
            }
        },
        /**
         * Permite eliminar un recurso
         * @param file
         */
        removeFile(file, pack) {
            if (pack === 'new') {
                this.resourceObtained = this.resourceObtained.filter((f) => {
                    return f !== file
                })
            } else {
                this.fileresource = this.fileresource.filter((f) => {
                    return f !== file
                })
            }
        },
        /**
         * Método para traer la data de la lección desde el back
         * @returns {Promise<void>}
         */
        async setInitialData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                const dataReturned = await this.$store.dispatch('lesson/getLesson', this.lessonId)
                this.lessonData.topic = dataReturned.topic
                this.lessonData.description = dataReturned.description
                this.lessonData.module = dataReturned.module
                this.lessonData.hoursTaken = Math.floor((dataReturned.timeTaken / 60) % 60)
                this.lessonData.minutesTaken = dataReturned.timeTaken - this.lessonData.hoursTaken * 60
                this.fileresource = dataReturned.resources.map((item) => ({
                    id: item.id,
                    name: item.resource.split('/').slice(-1).toString(),
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
        /**
         * Método para almacenar el curso en el back
         * @returns {Promise<void>}
         */
        async saveLesson() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                if (this.lessonData.hoursTaken === '0' && this.lessonData.minutesTaken === '0') {
                    // Si alguno de los valores no es un número rechaza la operación
                    this.$vs.notification({
                        title: 'Ops..',
                        text: 'Debe ingresar una duración mayor a 0',
                        color: 'danger',
                        position: 'top-right',
                    })
                    return
                }
                const timeTaken = parseInt(this.lessonData.hoursTaken) * 60 + parseInt(this.lessonData.minutesTaken)

                const payload = {
                    topic: this.lessonData.topic,
                    description: this.lessonData.description,
                    module: this.moduleId,
                    resources: this.resourceObtained.map((item) => item.id),
                    timeTaken,
                }
                await this.$store.dispatch('lesson/createLesson', payload)
                this.readyCreated = 1
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Lección creada',
                    position: 'top-right',
                })
                this.$router.push({
                    path: `/gestion/mis-cursos/${this.courseId}/modulos/${this.moduleId}/lecciones`,
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
         * Edita una lección
         * @returns {Promise<void>}
         */
        async editLesson() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            const newResourseId = this.resourceObtained.map((item) => item.id)
            const oldResourceId = this.fileresource.map((item) => item.id)
            Array.prototype.push.apply(newResourseId, oldResourceId)
            try {
                if (this.lessonData.hoursTaken === 0 && this.lessonData.minutesTaken === 0) {
                    // Si alguno de los valores no es un número rechaza la operación
                    this.$vs.notification({
                        title: 'Ops..',
                        text: 'Debe ingresar una duración mayor a 0',
                        color: 'danger',
                        position: 'top-right',
                    })
                    return
                }
                const timeTaken = parseInt(this.lessonData.hoursTaken) * 60 + parseInt(this.lessonData.minutesTaken)
                if (timeTaken === 0) {
                    this.$vs.notification({
                        title: 'Ops..',
                        text: 'Debe ingresar una duración mayor a 0',
                        color: 'danger',
                        position: 'top-right',
                    })
                    return
                } else {
                    const payload = {
                        data: {
                            topic: this.lessonData.topic,
                            description: this.lessonData.description,
                            module: this.moduleId,
                            resources: newResourseId,
                            timeTaken,
                        },
                        id: this.lessonId,
                    }

                    await this.$store.dispatch('lesson/updateLesson', payload)
                    this.$vs.notification({
                        color: 'success',
                        title: 'Éxito',
                        text: 'Lección Actualizada',
                        position: 'top-right',
                    })
                    this.$router.push({
                        path: `/gestion/mis-cursos/${this.courseId}/modulos/${this.moduleId}/lecciones`,
                    })
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
        goToEditHomework(idLeccion) {
            this.$router.push({
                path: `/gestion/mis-cursos/${this.courseId}/modulos/${this.moduleId}/lecciones/${idLeccion}/tareas`,
            })
        },
    },
}
</script>

<style>
.toggle-checkbox:checked {
    @apply: right-0 border-green-400;
    right: 0;
    border-color: #68d391;
}

.toggle-checkbox:checked + .toggle-label {
    @apply: bg-green-400;
    background-color: #68d391;
}

.hover-trigger .hover-target {
    display: none;
}

.hover-trigger:hover .hover-target {
    display: block;
}

.ck-editor .ck-editor__main .ck-content {
    min-height: 250px;
}

.lessonsEditor--container .tooltip-box {
    right: -60px !important;
}
</style>
