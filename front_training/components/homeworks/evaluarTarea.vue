<!--listaTareas muestra la tabla con las tareas destinadas al <profesor-->
<!--evaluarTareas muestra el modal para actualizar la calificación de cada tarea individual-->
<template>
    <div class="fixed top-0 left-0 right-0 bottom-0 flex justify-items-center modal-mask">
        <div
            class="fixed top-10 left-1/3 right-0 bottom-0 flex-col justify-center bg-white text-gray-700 shadow w-2/6 h-5/6 overflow-auto"
        >
            <div class="px-10 py-8 flex flex-row justify-between">
                <h2 class="font-sans text-3xl">
                    <b>{{ dataTarea.tarea }}</b>
                </h2>
                <button
                    class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                    @click="cierraEvaluacion"
                >
                    Regresar
                </button>
            </div>
            <div class="px-10 py-5 flex flex-col space-y-5 font-sans">
                <div class="space-y-1 flex flex-col">
                    <span class="text-lg"><b>Alumno: </b></span>
                    <span class="ml-10">{{ dataTarea.alumno }}</span>
                </div>
                <div class="space-y-1 flex flex-col">
                    <span class="text-lg"><b>Fecha de entrega: </b></span>
                    <span class="ml-10">{{ dataTarea.fechaEntrega }}</span>
                </div>
            </div>
            <div class="px-10 py-5 flex flex-col space-y-2">
                <span class="font-sans text-lg"><b>Archivo de tarea:</b></span>
                <button
                    class="cursor-pointer hover:bg-gray-200 px-4 py-3 bg-gray-100 rounded-md text-black outline-none focus:ring-4 shadow-lg transform active:scale-x-75 transition-transform mx-5 flex"
                    @click="openResource(dataTarea.resources)"
                >
                    <div class="">
                        <div class="whitespace-normal overflow-hidden">
                            <div class="">{{ dataTarea.resources.split('/').slice(-1).toString() }}</div>
                        </div>
                    </div>
                </button>
            </div>
            <div class="py-5 px-10 w-full flex flex-col space-y-5">
                <span class="font-sans text-lg"><b>Comentario del profesor</b></span>
                <textarea
                    v-if="dataTarea.idRevision === null"
                    v-model="comentario"
                    placeholder="Introduzca un comentario"
                    class="w-full py-2 px-5 rounded-md bg-gray-50 px-4 ring-2 ring-gray-200"
                />
                <textarea
                    v-else
                    v-model="comentarioActualizado"
                    :placeholder="dataTarea.idRevision.review"
                    class="w-full py-2 px-5 rounded-md bg-gray-50 px-4 ring-2 ring-gray-200"
                />
            </div>
            <div class="px-10 py-5 flex flex-row justify-between">
                <div class="flex flex-row space-x-3 items-center">
                    <span class="font-sans text-lg"><b>Calificación: </b></span>
                    <template v-if="dataTarea.idRevision === null">
                        <input
                            v-model="evaluacion"
                            placeholder="10"
                            class="w-9 px-2 rounded-md bg-gray-50 ring-2 ring-gray-200"
                        />
                    </template>
                    <template v-else>
                        <input
                            v-model="evaluacionActualizada"
                            :placeholder="dataTarea.idRevision.qualification"
                            class="w-9 px-2 rounded-md bg-gray-50 ring-2 ring-gray-200"
                        />
                    </template>
                    <span>/10</span>
                </div>
                <button
                    class="text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                    @click="guardarCalificacion"
                >
                    <span v-if="dataTarea.idRevision === null">Evaluar</span>
                    <span v-else>Actualizar evaluación</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { getErrorDetails } from '@/assets/utils/utils'

export default {
    name: 'EvaluarTarea',
    props: {
        dataTarea: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            comentario: null,
            comentarioActualizado: null,
            evaluacion: null,
            evaluacionActualizada: null,
            muestraCalificacion: true,
            calificacion: 0,
        }
    },
    mounted() {
        this.muestraCalificacion = this.dataTarea.calificacion === 'pendiente'
    },
    methods: {
        cierraEvaluacion() {
            this.$emit('cierreEvaluacion')
        },
        openResource(url) {
            window.open(
                url,
                '_blank' // <- This is what makes it open in a new window.
            )
        },
        guardarCalificacion() {
            if (this.dataTarea.idRevision === null) {
                this.generaCalificacion()
            } else {
                this.actualizaCalificacion()
            }
        },
        async generaCalificacion() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const payload = {
                    homeworkLessonDelivery: this.dataTarea.id,
                    qualification: this.evaluacion,
                    review: this.comentario,
                }
                await this.$store.dispatch('homework-review/createHomeworkReview', payload)
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
            this.cierraEvaluacion()
        },
        async actualizaCalificacion() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const payload = {
                    homeworkLessonDelivery: this.dataTarea.id,
                    id: this.dataTarea.idRevision.id,
                    qualification: this.evaluacionActualizada,
                    review: this.comentarioActualizado,
                }
                await this.$store.dispatch('homework-review/editHomeworkReview', payload)
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
            this.cierraEvaluacion()
        },
    },
}
</script>

<style scoped>
.modal-mask {
    z-index: 9998;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity 0.3s ease;
}
</style>
