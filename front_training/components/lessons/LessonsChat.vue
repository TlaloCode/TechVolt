<template>
    <div class="w-full flex flex-col space-y-5 text-gray-700 overflow-auto">
        <div class="p-5 space-x-4 flex flex-row">
            <ChatIcon />
            <strong class="mt-1 object-left font-sans text-3xl"> Comentarios </strong>
        </div>

        <div class="py-2 px-5 w-full">
            <textarea
                v-model="homeworkContent.note"
                placeholder="Comentario"
                class="w-full py-2 px-5 rounded-md bg-gray-50 px-4 ring-2 ring-gray-200"
            />
        </div>
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
                        <div class="flex flex-auto max-h-48 w-1/5 mx-auto -mt-10 text-center cursor-pointer">
                            <img
                                class="has-mask h-36 object-center cursor-pointer"
                                src="https://img.freepik.com/free-vector/image-upload-concept-landing-page_52683-27130.jpg?size=338&ext=jpg"
                                alt="freepik image"
                            />
                        </div>
                        <p class="cursor-pointer text-gray-500 text-center">
                            <span class="text-sm-center object-center" /><br />Selecciona un archivo de tu equipo
                        </p>
                    </div>
                    <input type="file" class="hidden" @change="loadDocument($event)" />
                </div>
            </label>
        </div>
        <p class="text-sm text-gray-300">
            <span>Tipos permitidos: doc, pdf, tipos de imagenes</span>
        </p>
        <div class="px-4 py-2 font-semibold">Archivos a subir</div>
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
        <div class="py-2 px-5 w-full flex flex-row justify-between items-center">
            <button
                class="text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                data-bs-toggle="tooltip"
                title="Enviar mensaje"
                @click="levantaAdvertencia = true"
            >
                Enviar
            </button>
        </div>

        <div v-if="chatMode" class="h-15 max-h-full w-11/12 flex flex-col-reverse ml-5 bg-stone-200 rounded-md">
            <template v-for="(mensaje, index) in msgHistorial">
                <!--Student deliver homework-->
                <div :key="index" class="flex flex-row-reverse py-1 space-x-1 mr-2">
                    <img
                        v-if="!mensaje.createdBy.picture"
                        :src="require('@/assets/images/user-avatar.png')"
                        class="object-none box-border h-10 w-10 rounded-full mt-2"
                    />
                    <img
                        v-if="mensaje.createdBy.picture"
                        :src="
                            mensaje.createdBy.picture.includes('https://')
                                ? mensaje.createdBy.picture
                                : 'http://localhost:8000' + mensaje.createdBy.picture
                        "
                        class="object-none box-border h-10 w-10 rounded-full mt-2"
                    />
                    <div class="w-10/12 rounded-md bg-white px-2 flex flex-col flex-wrap text-right">
                        <span class="text-xs font-mono">
                            {{ mensaje.createdBy.name + ' ' + mensaje.createdBy.lastName }}
                        </span>
                        <span class="mr-10 font-sans">
                            {{ mensaje.note }}
                        </span>
                        <div v-if="fileresource != null">
                            <span class="mr-10 font-sans">
                                {{ fileresource }}
                            </span>
                            <a target="blank" :href="url">📁</a>
                        </div>
                    </div>
                </div>
            </template>
        </div>
        <div v-else class="w-full rounded-md shadow px-2 flex flex-row flex-wrap justify-end items-center space-x-2">
            <template v-if="msgHistorial !== null">
                <div class="flex flex-col bg-white p-2 rounded-md text-right">
                    <span class="text-xs font-mono">{{ msgHistorial.createdBy }}</span>
                    <span>{{ msgHistorial.note }}</span>
                    <span class="text-xs text-blue-500">{{ fileresource }}</span>
                </div>
                <img
                    v-if="!msgHistorial.userPicture"
                    :src="require('@/assets/images/user-avatar.png')"
                    class="object-none box-border h-10 w-10 rounded-full mt-2"
                />
                <img
                    v-if="msgHistorial.userPicture"
                    :src="
                        msgHistorial.userPicture.includes('https://')
                            ? msgHistorial.userPicture
                            : 'http://localhost:8000' + msgHistorial.userPicture
                    "
                    class="object-none box-border h-10 w-10 rounded-full mt-2"
                />
            </template>
        </div>
        <ModalAdvertencia v-if="levantaAdvertencia" @cierraModal="levantaAdvertencia = false" @guardaTarea="sendTo()">
            Al enviar la tarea no podrás editarla en el futuro
        </ModalAdvertencia>
    </div>
</template>

<script>
import ModalAdvertencia from '../ModalAdvertencia.vue'
import ChatIcon from '@/components/icons/ChatIcon.vue'
import { getErrorDetails } from '@/assets/utils/utils'

export default {
    components: { ModalAdvertencia, ChatIcon },
    props: {
        homeworkId: {
            type: Number,
            default: 0,
        },
        chatMode: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            levantaAdvertencia: false,
            fileresource: '',
            url: '',
            files: [],
            homeworkContent: {
                note: '',
                noteType: 'Entrega tarea',
                adjuntedFile: '',
                homeworkLesson: '',
            },
            esEstudiante: false,
            value1: '',
            estatusTarea: 'No recibida',
            usuario: 'Alumno',
            usuario2: 'Profesor',
            califTarea: 0,
            attachFile: false,
            comentUsuario: true,
            comentUsuario2: true,
            msgHistorial: null,
            califBlock: true,
            mostrarInfo: true,
            estatusTareaFinal: 'No entregado',
            infoTarea: {
                dataUsuario: {
                    nombre: 'usuario',
                    apellidoPaterno: '1',
                    apellidoMaterno: '',
                    email: '',
                    id: '',
                    esActivo: true,
                    rol: null,
                    nombreUsuario: '',
                },
                archivoAdjunto: null,
                fechaAtencion: null,
                entregaAceptada: false,
                id: null,
                esActive: false,
                esCerrado: false,
                curso: null,
                nombreCurso: null,
                remitente: null,
                horaEmision: null,
                titulo: null,
                usuarioRemit: null,
                usuarioRemitData: {
                    id: null,
                    esActivo: null,
                    esMaestro: false,
                    curso: null,
                    usuario: null,
                },
            },
        }
    },
    computed: {
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
    },
    created() {
        this.getHomeworkData()
    },
    methods: {
        async getHomeworkData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const dataHomework = await this.$store.dispatch('homework/getDeliveryInfo', this.homeworkId)
                if (dataHomework.length > 0) {
                    const tareaFiltrado = dataHomework.filter((item) => item.createdBy.id === this.activeUserInfo.id)
                    if (tareaFiltrado.length > 0) {
                        const baseURL = process.env.NODE_ENV !== 'production' ? 'http://localhost:8000/' : ''
                        this.url = baseURL + tareaFiltrado[0].resource
                        this.fileresource = this.url.split('/').slice(-1).toString()
                        this.msgHistorial = tareaFiltrado.map((t) => ({
                            createdBy: t.createdBy.getFullName,
                            userPicture: t.createdBy.picture,
                            note: t.note,
                        }))[0]
                        console.log(this.msgHistorial)
                    }
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
        async sendTo() {
            if (!this.chatMode) {
                await this.sendHomework()
            }
        },
        async sendHomework() {
            this.levantaAdvertencia = false
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const formData = new FormData()
                formData.append('homeworkLesson', this.homeworkId)
                formData.append('note', this.homeworkContent.note)
                formData.append('note_type', this.homeworkContent.noteType)
                if (this.homeworkContent.adjuntedFile !== '') {
                    formData.append('resource', this.homeworkContent.adjuntedFile)
                }
                const payload = {
                    data: formData,
                }
                await this.$store.dispatch('homework/deliverHomework', payload)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Tarea entregada',
                    position: 'top-right',
                })
                this.$router.go(0)
                await this.getHomeworkData()
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
         * Método para agregar recursos a la lección
         * @param event
         * @returns {Promise<void>}
         */
        loadDocument(e) {
            const droppedFiles = e.target.files[0]
            if (!droppedFiles) return
            this.files = [droppedFiles]
            this.homeworkContent.adjuntedFile = droppedFiles
        },
        /**
         * Permite eliminar un recurso
         * @param file
         */
        removeFile(file) {
            this.files = this.files.filter((f) => {
                return f !== file
            })
        },
    },
}
</script>

<style></style>
