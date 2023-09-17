<template>
    <div class="py-8 md:container md:mx-auto bg-white text-gray-700 shadow">
        <div class="w-11/12 bg-white flex flex-col space-y-5 justify-items-center">
            <div class="w-full flex flex-row space-x-10 justify-between">
                <!--Encabezado-->
                <div class="ml-16 flex flex-row space-x-1">
                    <CalendarIcon />
                    <h2 class="mt-1 font-sans text-3xl">
                        <!--text-3xl-->
                        <b>Calendario de clases</b>
                    </h2>
                </div>
                <div v-if="!pantallaLateral.agendaClase && !estadoEdicion" class="basis-1/3">
                    <button
                        class="ml-24 flex flex-row text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                        @click="agendarClase()"
                    >
                        <PlusCircleIcon class="mt-1" />
                        <span class="mt-2 px-2">Agenda una nueva clase</span>
                    </button>
                </div>
            </div>
            <!--Fin encabezado-->

            <div class="flex flex-row w-max-full justify-center space-x-10">
                <div class="w-7/12 text-center section">
                    <v-calendar
                        class="custom-calendar max-w-full"
                        :masks="masks"
                        :attributes="attributesC"
                        disable-page-swipe
                        is-expanded
                        title-position="left"
                    >
                        <template #day-content="{ day, attributes }">
                            <div class="h-24 border-2 border-gray-100 flex flex-col h-full z-10 overflow-hidden">
                                <span class="day-label text-sm text-gray-700">{{ day.day }}</span>
                                <div class="flex-grow overflow-y-auto overflow-x-auto">
                                    <div
                                        v-for="attr in attributes"
                                        :key="attr.key"
                                        class="text-xs leading-tight rounded-md p-1 mt-0 mb-1 hover:z-20 hover:drop-shadow-lg translation-colors ease-in-out duration-300 cursor-pointer"
                                        :class="
                                            attr.customData.createdBy === activeUserInfo.id
                                                ? 'bg-red-400 hover:bg-red-800'
                                                : 'bg-blue-400 hover:bg-blue-800'
                                        "
                                        @click="detallesClase(attr)"
                                    >
                                        <p>
                                            {{
                                                new Date(attr.customData.startDate).toLocaleString('en-US', {
                                                    hour: 'numeric',
                                                    minute: 'numeric',
                                                    hour12: true,
                                                })
                                            }}
                                            -
                                            {{
                                                new Date(attr.customData.endDate).toLocaleString('en-US', {
                                                    hour: 'numeric',
                                                    minute: 'numeric',
                                                    hour12: true,
                                                })
                                            }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </v-calendar>
                    <!--Calendario-->
                </div>
                <CalendarSidePan
                    :info-clase="pantallaLateral"
                    @cambiaAgendaClase="recargaCalendario()"
                    @cambiaPaginaInicio="pantallaLateral.pantallaInicio = true"
                    @BorradoClase="recargaBorrado()"
                    @editando="editarClase()"
                />
            </div>
        </div>
    </div>
</template>

<script>
import CalendarSidePan from './CalendarSidePan.vue'
import { getErrorDetails } from '@/assets/utils/utils'
import CalendarIcon from '@/components/icons/Calendar.vue'
import PlusCircleIcon from '@/components/icons/PlusCircleIcon.vue'

export default {
    components: {
        CalendarIcon,
        PlusCircleIcon,
        CalendarSidePan,
    },

    data() {
        return {
            masks: {
                weekdays: 'WWW',
            },
            arregloClases: [],
            usuarioData: null,
            estadoEdicion: false,
            revisionAgenda: false,
            pantallaLateral: {
                dirEnlace: '',
                id: null,
                pantallaInicio: true,
                agendaClase: false,
                ceroCursos: false,
                curso: '',
                idCheck: false,
                modulo: '',
                leccion: '',
                descripcion: '',
                fecha: '',
                horario: '',
                createdBy: '',
            },
        }
    },

    computed: {
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
        attributesC() {
            return this.arregloClases
        },
    },

    mounted() {
        this.loadClases()
    },

    methods: {
        detallesClase(data) {
            if (this.pantallaLateral.agendaClase || this.estadoEdicion) {
                const res = 'Cierra la pantalla de edición antes de explorar las clases agendadas'
                this.$vs.notification({
                    title: 'Ops..',
                    text: `${res}`,
                    color: 'danger',
                    position: 'top-right',
                })
            } else {
                const fechaInicio = new Date(data.customData.startDate)
                const fechaFinal = new Date(data.customData.endDate)
                this.pantallaLateral.pantallaInicio = false
                this.revisionAgenda = true
                this.pantallaLateral.curso = data.customData.course
                this.pantallaLateral.modulo = data.customData.module
                this.pantallaLateral.leccion = data.customData.lesson
                this.pantallaLateral.descripcion = data.customData.description
                this.pantallaLateral.fecha = fechaInicio.toLocaleString('es-ES', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                })
                this.pantallaLateral.horario =
                    fechaInicio.toLocaleString('en-US', {
                        hour: 'numeric',
                        minute: 'numeric',
                        hour12: true,
                    }) +
                    '-' +
                    fechaFinal.toLocaleString('en-US', {
                        hour: 'numeric',
                        minute: 'numeric',
                        hour12: true,
                    })
                this.pantallaLateral.dirEnlace = data.customData.url
                this.pantallaLateral.idCheck = true
                this.pantallaLateral.id = data.customData.id
                this.pantallaLateral.createdBy = data.customData.createdBy
            }
        },
        agendarClase() {
            this.pantallaLateral.pantallaInicio = false
            this.pantallaLateral.agendaClase = true
            this.revisionAgenda = false
        },
        editarClase() {
            this.revisionAgenda = false
            this.estadoEdicion = true
        },
        recargaBorrado() {
            this.pantallaLateral.pantallaInicio = true
            this.estadoEdicion = false
            this.loadClases()
        },
        recargaCalendario() {
            this.pantallaLateral.agendaClase = false
            this.estadoEdicion = false
            this.loadClases()
        },
        async loadClases() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                this.arregloClases = []
                const { teacher, student } = await this.$store.dispatch('course-schedules/getScheduleClass')
                const arregloGeneral = teacher
                Array.prototype.push.apply(arregloGeneral, student)
                const arregloCalendario = arregloGeneral.sort((a, b) =>
                    a.startDate === b.startDate ? 0 : a.startDate > b.startDate ? 1 : -1
                )
                this.arregloClases = arregloCalendario.map((t) => ({
                    key: `arregloCalendario.findIndex( (item) => item.id === ${t.id})`,
                    dates: t.endDate,
                    customData: t,
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
    },
}
</script>
