<!--listaTareas muestra la tabla con las tareas destinadas al <profesor-->
<!--evaluarTareas muestra el modal para actualizar la calificación de cada tarea individual-->
<template>
    <div class="lg:container lg:max-auto flex flex-col justify-center bg-white text-gray-700 shadow">
        <div class="px-10 py-12 flex flex-row space-x-5">
            <span class="text-green-500"><GridPlusIcon /></span>
            <h2 class="font-sans text-3xl"><b>Revisión de tareas</b></h2>
        </div>
        <div class="px-10 py-5 flex justify-center w-full">
            <vue-good-table
                class="w-full"
                :columns="columnas"
                :rows="tareasNoFiltro"
                max-height="65vh"
                :pagination-options="{
                    enabled: true,
                    mode: 'records',
                    perPage: 10,
                    position: 'top',
                    perPageDropdown: [20, 30, 40, 50, 60, 70, 80, 90, 100],
                    dropdownAllowAll: false,
                    setCurrentPage: 1,
                    nextLabel: 'Siguiente',
                    prevLabel: 'Anterior',
                    rowsPerPageLabel: 'Registros por Página',
                    ofLabel: 'of',
                    pageLabel: 'page', // for 'pages' mode
                    allLabel: 'All',
                }"
                @on-row-click="llamaEvaluacion"
            >
            </vue-good-table>
        </div>
        <div v-if="evaluandoTarea">
            <EvaluarTarea :data-tarea="evaluacionData" @cierreEvaluacion="cierraEvaluacion()" />
        </div>
    </div>
</template>

<script>
import EvaluarTarea from './evaluarTarea.vue'
import { getErrorDetails } from '@/assets/utils/utils'
import GridPlusIcon from '@/components/icons/GridPlus.vue'
export default {
    components: { GridPlusIcon, EvaluarTarea },
    data() {
        return {
            evaluandoTarea: false,
            tareaPendiente: true,
            tareaCalificada: null,
            evaluacionData: null,
            tareasNoFiltro: [],
            dataRevision: null,
            columnas: [
                {
                    label: 'Revisión',
                    field: 'revision',
                    filterOptions: {
                        enabled: true,
                        filterValue: 'Pendiente',
                        filterDropdownItems: ['Pendiente', 'Revisado'],
                    },
                },
                {
                    label: 'Alumno',
                    field: 'alumno',
                    filterOptions: {
                        enabled: true,
                        filterValue: null,
                        filterDropdownItems: [],
                    },
                },
                {
                    label: 'Curso',
                    field: 'curso',
                    filterOptions: {
                        enabled: true,
                        filterValue: null,
                        filterDropdownItems: [],
                    },
                },
                {
                    label: 'Módulo',
                    field: 'modulo',
                },
                {
                    label: 'Tarea',
                    field: 'tarea',
                },
                {
                    label: 'Fecha de entrega',
                    field: 'fechaEntrega',
                },
            ],
        }
    },
    computed: {
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
    },
    mounted() {
        this.cargaTareas()
    },
    methods: {
        cierraEvaluacion() {
            this.evaluandoTarea = false
            this.cargaTareas()
        },
        llamaEvaluacion(params) {
            this.evaluandoTarea = true
            this.evaluacionData = params.row
        },
        filtroNombre(data, filterString) {
            return data === filterString
        },
        async cargaTareas() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                const paqueteTareas = await this.$store.dispatch('homework-review/getHomeworkReviewList')
                const arregloNoFiltro = paqueteTareas.results.map((item) => ({
                    id: item.id,
                    tarea: item.homeworkLesson.title,
                    modulo: item.moduleTopic,
                    curso: item.courseName,
                    alumno: item.createdBy.getFullName,
                    createdBy: item.homeworkLesson.createdBy,
                    fechaEntrega: new Date(item.createdAt).toLocaleString('es-ES', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                    }),
                    revision: item.homeworkLessonReview === null ? 'Pendiente' : 'Revisado',
                    idRevision: item.homeworkLessonReview,
                    resources: item.resource,
                }))
                const unique = (value, index, self) => {
                    return self.indexOf(value) === index
                }
                const noUniqueCursos = arregloNoFiltro.map((item) => item.curso)
                const noUniqueAlumnos = arregloNoFiltro.map((item) => item.alumno)
                this.columnas[2].filterOptions.filterDropdownItems = noUniqueCursos.filter(unique)
                this.columnas[1].filterOptions.filterDropdownItems = noUniqueAlumnos.filter(unique)
                this.tareasNoFiltro = arregloNoFiltro.filter((item) => item.createdBy === this.activeUserInfo.id)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Lista de Tareas actualizada',
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
    },
}
</script>
