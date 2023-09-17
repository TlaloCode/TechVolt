<template>
    <div id="lateralCalendario" class="h-11/12 w-1/3 flex justify-center shadow overflow-auto">
        <!--Detalles curso-->
        <template v-if="infoClase.pantallaInicio && !infoClase.agendaClase">
            <div class="ml-7 basis-9/12 w-10/12 flex flex-col space-y-10 justify-center">
                <h1 class="text-center text-2xl">
                    <b>Haz click sobre una clase agendada para revisar su información</b>
                </h1>
                <ClickIcon class="h-14 w-14 ml-24" />
            </div>
        </template>
        <!--Pantalla de inicio-->
        <template v-else-if="!infoClase.pantallaInicio && infoClase.agendaClase && listaCursos.length === 0">
            <div class="ml-7 basis-9/12 w-10/12 flex flex-col space-y-10 justify-center">
                <h1 class="text-center text-2xl">
                    <b>Todavía no haz registrado cursos para impartir ¡Inicia tu primer curso ahora!</b>
                </h1>
                <ClickIcon class="h-14 w-14 ml-24" />
            </div>
        </template>
        <template v-else-if="!infoClase.pantallaInicio">
            <!--Pantalla datos de clase-->
            <div class="basis-full w-full flex flex-col justify-center self-start">
                <div class="ml-8 w-10/12 mt-3 flex flex-row justify-between">
                    <div class="space-x-2 flex flex-row">
                        <BookIcon />
                        <h2 v-if="!editarLeccion && !infoClase.agendaClase" class="mt-1 font-sans">
                            <!--text-3xl-->
                            <b>Detalles del curso</b>
                        </h2>
                        <h2 v-else-if="editarLeccion && !infoClase.agendaClase" class="mt-1 font-sans">
                            <!--text-3xl-->
                            <b>Editar lección</b>
                        </h2>
                        <h2 v-else class="mt-1 font-sans">
                            <!--text-3xl-->
                            <b>¡Agenda una clase!</b>
                        </h2>
                    </div>
                    <div v-if="editarLeccion || infoClase.agendaClase" @click="cierreEdicion()">
                        <div class="ml-14 mt-1 hover:bg-red-700 rounded-full cursor-pointer">
                            <XInCircle />
                        </div>
                    </div>
                </div>

                <div class="ml-8 w-10/12 flex flex-col">
                    <ValidationObserver v-slot="{ invalid }" tag="div">
                        <div class="space-y-2 mt-5">
                            <p
                                class="text-base font-bold"
                                :class="{ 'font-normal': editarLeccion || infoClase.agendaClase }"
                            >
                                Curso
                            </p>
                            <template v-if="!editarLeccion && !infoClase.agendaClase">
                                <span class="ml-5 text-justify text-sm">{{ cursoMostrado }}</span>
                            </template>

                            <template v-else>
                                <ValidationProvider v-slot="{ errors }" name="de Curso" rules="required" tag="div">
                                    <select
                                        v-model="cursoSeleccionado"
                                        class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                        @change="cargaModulos(0)"
                                    >
                                        <option disabled :value="null">Seleccione una categoria</option>
                                        <option
                                            v-for="(choice0, index) in listaCursos"
                                            :key="index"
                                            :value="choice0.id"
                                        >
                                            {{ choice0.name }}
                                        </option>
                                    </select>
                                    <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </template>
                        </div>

                        <div class="space-y-2 mt-3">
                            <p
                                class="text-base font-bold"
                                :class="{ 'font-normal': editarLeccion || infoClase.agendaClase }"
                            >
                                Módulo
                            </p>
                            <template v-if="!editarLeccion && !infoClase.agendaClase">
                                <span class="ml-5 text-justify text-sm">{{ moduloPanel }}</span>
                            </template>
                            <template v-else>
                                <select
                                    v-model="moduloSeleccionado"
                                    :disabled="esCurso"
                                    class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                    @change="cargaLecciones(0)"
                                >
                                    <option disabled :value="null">Seleccione una categoria</option>
                                    <option
                                        v-for="(choice1, index1) in listaModulos"
                                        :key="index1"
                                        name="Modulo"
                                        :value="choice1.id"
                                    >
                                        {{ choice1.topic }}
                                    </option>
                                </select>
                                <label for="Modulo" class="mb-3 italic text-xs font-thin text-gray-400">
                                    Campo opcional
                                </label>
                            </template>
                        </div>

                        <div class="space-y-2 mt-3">
                            <!--abre campo -->
                            <p
                                class="text-base font-bold"
                                :class="{ 'font-normal': editarLeccion || infoClase.agendaClase }"
                            >
                                Lección
                            </p>
                            <template v-if="!editarLeccion && !infoClase.agendaClase">
                                <span class="ml-5 text-justify text-sm">{{ leccionPanel }}</span>
                            </template>
                            <template v-else>
                                <select
                                    v-model="leccionSeleccionado"
                                    :disabled="esModulo"
                                    class="border border-gray-300 placeholder-gray-500 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                    placeholder="Seleccione una categoria"
                                >
                                    <option disabled :value="null">Seleccione una categoria</option>
                                    <option
                                        v-for="(choice2, index2) in listaLecciones"
                                        :key="index2"
                                        name="Leccion"
                                        :value="choice2.id"
                                    >
                                        {{ choice2.topic }}
                                    </option>
                                </select>
                                <label for="Leccion" class="mb-3 italic text-xs font-thin text-gray-400">
                                    Campo opcional
                                </label>
                            </template>
                        </div>
                        <!--Cierra campo -->

                        <div class="space-y-2 mt-3">
                            <!--abre campo-->
                            <p
                                class="text-base font-bold"
                                :class="{
                                    'font-normal': editarLeccion || infoClase.agendaClase,
                                }"
                            >
                                Descripción
                            </p>
                            <template v-if="!editarLeccion && !infoClase.agendaClase">
                                <span class="ml-5 text-justify text-sm overflow-auto">{{ infoClase.descripcion }}</span>
                            </template>
                            <template v-else>
                                <div
                                    class="text-justify text-sm overflow-auto border border-slate-200 rounded-md flex justify-center"
                                >
                                    <textarea
                                        v-model="claseDescripcion"
                                        class="w-full m-1 text-base px-2 placeholder-gray-500"
                                        placeholder="Temas a tratar en la clase"
                                    />
                                </div>
                            </template>
                        </div>
                        <!--Cierra campo-->

                        <div class="space-y-2 mt-3">
                            <div v-if="!editarLeccion && !infoClase.agendaClase" class="w-full">
                                <p class="text-base font-bold">Ingresa a tu clase</p>
                                <a
                                    :href="infoClase.dirEnlace"
                                    class="ml-5 text-justify text-sm text-sky-500 text-ellipsis overflow-hidden"
                                >
                                    <p class="text-ellipsis overflow-hidden">{{ infoClase.dirEnlace }}</p>
                                </a>
                            </div>
                            <div v-else>
                                <p class="text-base font-normal">Ingresa la URL a tu clase</p>
                                <ValidationProvider
                                    v-slot="{ errors }"
                                    name="de URL"
                                    tag="div"
                                    :rules="{
                                        required: true,
                                        regex: /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/,
                                    }"
                                >
                                    <div class="flex flex-col">
                                        <input
                                            v-model="dirEnlace"
                                            class="shadow placeholder-gray-500 px-3 rounded-md w-full border border-slate-200 h-10 mt-2"
                                            placeholder="Dirección de enlace"
                                        />
                                        <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                    </div>
                                </ValidationProvider>
                            </div>
                        </div>

                        <div class="space-y-1 mt-3 flex flex-col">
                            <p
                                class="text-base font-bold"
                                :class="{ 'font-normal': editarLeccion || infoClase.agendaClase }"
                            >
                                Horario
                            </p>
                            <div v-if="!editarLeccion && !infoClase.agendaClase" class="flex flex-col">
                                <span class="ml-5 text-center text-sm">{{ infoClase.fecha }}</span>
                                <span class="ml-5 text-center text-sm">{{ infoClase.horario }}</span>
                            </div>
                            <div v-else class="mt-2">
                                <div class="space-y-1">
                                    <span class="text-sm">Fecha de programación</span>
                                    <ValidationProvider v-slot="{ errors }" rules="required" tag="div">
                                        <v-date-picker
                                            v-model="claseFecha"
                                            class="inline-block h-full w-full"
                                            :min-date="new Date()"
                                        >
                                            <template #default="{ inputValue, togglePopover, inputEvents }">
                                                <div class="flex items-center space-x-5 w-full">
                                                    <button
                                                        class="border border-blue-200 hover:bg-blue-200 rounded-md"
                                                        @click="togglePopover()"
                                                    >
                                                        <Calendar />
                                                    </button>
                                                    <input
                                                        :value="inputValue"
                                                        class="bg-white p-2 ml-2 h-10 w-full text-gray-700 appearance-none border rounded focus:outline-none focus:border-blue-500"
                                                        readonly
                                                        v-on="inputEvents"
                                                    />
                                                </div>
                                            </template>
                                        </v-date-picker>
                                        <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                    </ValidationProvider>
                                </div>
                                <div class="space-y-1">
                                    <span class="text-sm">Inicio de la clase</span>
                                    <ValidationProvider v-slot="{ errors }" rules="required" tag="div">
                                        <div class="w-full justify-center">
                                            <label for="inicio" class="mb-3 block text-base font-medium text-[#07074D]">
                                                {{ etiquetaFecha }}
                                            </label>
                                            <v-date-picker v-model="claseInicio" name="inicio" mode="time" />
                                            <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{
                                                errors[0]
                                            }}</span>
                                        </div>
                                    </ValidationProvider>
                                </div>
                                <div class="space-y-1">
                                    <span class="text-sm">Término de la clase</span>
                                    <ValidationProvider v-slot="{ errors }" rules="required" tag="div">
                                        <div class="w-full justify-center">
                                            <label
                                                for="termino"
                                                class="mb-3 block text-base font-medium text-[#07074D]"
                                            >
                                                {{ etiquetaFecha }}
                                            </label>
                                            <v-date-picker
                                                ref="claseFin"
                                                v-model="claseFin"
                                                name="termino"
                                                mode="time"
                                            />
                                            <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{
                                                errors[0]
                                            }}</span>
                                        </div>
                                    </ValidationProvider>
                                </div>
                            </div>
                        </div>
                        <div v-if="infoClase.createdBy === activeUserInfo.id" class="mt-5 w-full justify-right">
                            <div
                                v-if="infoClase.idCheck && !editarLeccion && !infoClase.agendaClase"
                                class="w-100 text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-green-500 dark:hover:bg-green-600 dark:focus:ring-green-600 cursor-pointer"
                                @click="entraLeccion()"
                            >
                                <p>Editar</p>
                            </div>
                            <div
                                v-if="infoClase.idCheck && !editarLeccion && !infoClase.agendaClase"
                                class="w-100 text-red-600 hover:text-white hover:bg-red-600 focus:outline-none focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:hover:bg-red-600 dark:focus:ring-red-600 cursor-pointer"
                                @click="eliminarLeccion()"
                            >
                                <p>Borrar</p>
                            </div>
                        </div>
                        <div class="mt-5 w-full justify-right">
                            <div v-if="editarLeccion || infoClase.agendaClase">
                                <button
                                    class="w-full text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-green-500 dark:hover:bg-green-600 dark:focus:ring-green-600 cursor-pointer"
                                    :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                    type="button"
                                    :disabled="invalid"
                                    @click="guardaClase()"
                                >
                                    <p>Guardar</p>
                                </button>
                            </div>
                        </div>
                    </ValidationObserver>
                </div>
            </div>
        </template>
        <!--Pantalla datos de clase-->
    </div>
</template>

<script>
import { ValidationProvider } from 'vee-validate'
import { getErrorDetails } from '@/assets/utils/utils'
import BookIcon from '@/components/icons/Book.vue'
import ClickIcon from '@/components/icons/ClickIcon.vue'
import XInCircle from '@/components/icons/XInCircle.vue'
import Calendar from '@/components/icons/Calendar.vue'

export default {
    name: 'CalendarSidePan',

    components: {
        BookIcon,
        ClickIcon,
        XInCircle,
        ValidationProvider,
        Calendar,
    },

    props: {
        infoClase: {
            type: Object,
            required: true,
        },
    },

    data() {
        return {
            editarLeccion: false,
            estadoAnt: 0,
            iniState: true,
            esCurso: true,
            esModulo: true,
            listaLecciones: [],
            listaModulos: [],
            listaCursos: [],
            cursoMostradoVar: '',
            moduloPanel: '',
            leccionPanel: '',
            cursoSeleccionado: null,
            moduloSeleccionado: null,
            leccionSeleccionado: null,
            claseDescripcion: '',
            claseFecha: '',
            claseInicio: '',
            claseFin: '',
            dirEnlace: '',
            isSameUser: false,
        }
    },
    computed: {
        etiquetaFecha() {
            return this.claseFecha.toLocaleString('es-ES', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
            })
        },
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
        cursoMostrado() {
            this.cargaCursoMostrado(this.infoClase.curso)
            if (this.infoClase.modulo !== null) {
                this.cargaModulos(1)
            } else {
                this.setNoDefinido(true)
            }
            if (this.infoClase.leccion !== null) {
                this.cargaLecciones(1)
            } else {
                this.setNoDefinido(false)
            }
            return this.cursoMostradoVar
        },
    },
    mounted() {
        this.cargaCursos()
    },
    methods: {
        colocaFechas() {
            console.log(this.claseFecha)
        },
        eliminarLeccion() {
            this.borraClase()
            this.$emit('BorradoClase')
        },
        setNoDefinido(selector) {
            if (selector) {
                this.moduloPanel = 'Módulo no definido'
            } else {
                this.leccionPanel = 'Lección no definida'
            }
        },
        resetFormulario() {
            this.cursoSeleccionado = null
            this.moduloSeleccionado = null
            this.leccionSeleccionado = null
            this.claseFecha = ''
            this.claseInicio = ''
            this.claseFin = ''
            this.claseDescripcion = ''
            this.dirEnlace = ''
        },
        cierreEdicion() {
            if (this.infoClase.agendaClase && this.editarLeccion) {
                this.estadoAnt = 1
            } else if (this.infoClase.agendaClase && !this.editarLeccion && this.estadoAnt === 0) {
                this.estadoAnt = 0
            } else {
                this.estadoAnt = 3
            }
            this.editarLeccion = false
            this.$emit('cambiaAgendaClase')

            if (this.estadoAnt === 0) {
                this.iniState = true
                this.$emit('cambiaPaginaInicio')
            } else {
                this.iniState = false
            }
            this.resetFormulario()
        },

        guardaClase() {
            let moduloId = null
            let leccionId = null
            if (this.moduloSeleccionado !== null) {
                moduloId = this.moduloSeleccionado
            }
            if (this.leccionSeleccionado !== null) {
                leccionId = this.leccionSeleccionado
            }
            const dataClase = {
                course: this.cursoSeleccionado,
                module: moduloId,
                lesson: leccionId,
                description: this.claseDescripcion,
                url: this.dirEnlace,
                start_date: new Date(
                    this.claseFecha.getFullYear(),
                    this.claseFecha.getMonth(),
                    this.claseFecha.getDate(),
                    this.claseInicio.getHours(),
                    this.claseInicio.getMinutes()
                ),
                end_date: new Date(
                    this.claseFecha.getFullYear(),
                    this.claseFecha.getMonth(),
                    this.claseFecha.getDate(),
                    this.claseFin.getHours(),
                    this.claseFin.getMinutes()
                ),
            }
            if (this.editarLeccion) {
                this.editaClase(dataClase)
            } else {
                this.agendaClase(dataClase)
            }
        },

        async entraLeccion() {
            this.editarLeccion = true
            this.estadoAnt = 3
            this.iniState = false
            this.$emit('editando')
            this.claseDescripcion = this.infoClase.descripcion
            this.dirEnlace = this.infoClase.dirEnlace
            this.cursoSeleccionado = this.listaCursos.filter((t) => t.name === this.cursoMostrado)[0].id
            await this.cargaModulos(0)
            if (this.moduloPanel !== 'Módulo no definido') {
                this.moduloSeleccionado = this.listaModulos.filter((t) => t.topic === this.moduloPanel)[0].id
                await this.cargaLecciones(0)
            } else {
                this.moduloSeleccionado = null
            }
            if (this.leccionPanel !== 'Lección no definida') {
                this.leccionSeleccionado = this.listaLecciones.filter((t) => t.topic === this.leccionPanel)[0].id
            } else {
                this.leccionSeleccionado = null
            }
        },
        async agendaClase(infoCarga) {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                await this.$store.dispatch('course-schedules/createScheduleClass', infoCarga)
                this.cierreEdicion()
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Clase agendada exitosamente',
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

        async editaClase(infoCarga) {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const payload = infoCarga
                payload.id = this.infoClase.id
                await this.$store.dispatch('course-schedules/editScheduleClass', payload)
                this.cierreEdicion()
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Clase editada exitosamente',
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
        async borraClase() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const payload = this.infoClase.id
                await this.$store.dispatch('course-schedules/deleteScheduleClass', payload)
                this.cierreEdicion()
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Clase editada exitosamente',
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
        async cargaCursos() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const params = `?created_by=${this.activeUserInfo.id}`
                const respuestaLista = await this.$store.dispatch('course/getCourseList', params)
                this.listaCursos = respuestaLista.results
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
        async cargaCursoMostrado(idCurso) {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const dataReturned = await this.$store.dispatch('course/getCourse', idCurso)
                this.cursoMostradoVar = dataReturned.name
            } catch (err) {
                console.error(err)
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
        async cargaModulos(mode) {
            let selector = ''
            if (mode !== 0) {
                selector = this.infoClase.curso
            } else {
                this.esCurso = false
                selector = this.cursoSeleccionado
            }
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const respuestaModulos = await this.$store.dispatch('course/getModules', selector)
                if (mode === 0) {
                    this.listaModulos = respuestaModulos.results
                } else {
                    const recibePanel = respuestaModulos.results.filter((modulo) => modulo.id === this.infoClase.modulo)
                    this.moduloPanel = recibePanel[0].topic
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

        async cargaLecciones(mode) {
            let selector = ''
            if (mode !== 0) {
                selector = this.infoClase.modulo
            } else if (mode === 0) {
                this.esModulo = false
                selector = this.moduloSeleccionado
            }
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const respuestaLecciones = await this.$store.dispatch('lesson/getLessons', selector)
                if (mode === 0) {
                    this.listaLecciones = respuestaLecciones.results
                } else {
                    const recibeLeccion = respuestaLecciones.results.filter(
                        (leccion) => leccion.id === this.infoClase.leccion
                    )
                    this.leccionPanel = recibeLeccion[0].topic
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
    },
}
</script>

<style lang="scss">
#lateralCalendario .vc-container {
    width: calc(100% - 2px) !important;
    align-items: center !important;
}
#lateralCalendario .vc-time-picker {
    width: 300px !important;
    height: 45px !important;
    justify-items: center !important;
}
#lateralCalendario .vc-date-time {
    width: calc(95% - 5px) !important;
    justify-items: center;
}
#lateralCalendario .vc-time {
    display: flex !important;
    align-items: flex-end !important;
}
#lateralCalendario .vc-select {
    padding-left: 15px !important;
    padding-right: 15px !important;
}
#lateralCalendario .vc-select-arrow {
    right: 10px !important;
}
#lateralCalendario .vc-date {
    visibility: hidden !important;
    position: absolute !important;
}
</style>
