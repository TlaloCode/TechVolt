<template>
    <div class="py-8 max-w-full bg-white text-gray-700 shadow">
        <div class="max-w-screen-xl mx-auto">
            <div class="w-full">
                <div class="flex container md:px-8">
                    <span class="mt-4 text-green-500 flex-none">
                        <CapIcon />
                    </span>
                    <h2 class="md:px-5 flex items-center text-3xl flex-auto">
                        <span>{{ titleForm }}</span>
                    </h2>
                    <div class="flex flex-initial justify-end">
                        <button
                            class="w-40 text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
                            @click="$router.go(-1)"
                        >
                            Regresar
                        </button>
                    </div>
                    <div v-if="type === 'edit'" class="flex flex-initial justify-end">
                        <NuxtLink
                            :to="`/gestion/mis-cursos/${courseId}/modulos`"
                            class="w-40 text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                        >
                            Editar módulos
                        </NuxtLink>
                    </div>
                </div>
            </div>
        </div>
        <ValidationObserver v-slot="{ invalid: invalidCourseFrom }" tag="div">
            <div class="max-w-screen-xl mx-auto flex items-center justify-center px-10 py-5">
                <div class="mx-auto w-full">
                    <div>
                        <div class="w-full md:w-4/12 md:mx-1">
                            <div class="mb-3 w-96">
                                <label class="mb-3 block text-base font-medium text-[#07074D]"> Nombre </label>
                                <ValidationProvider v-slot="{ errors }" name="Nombre" rules="required|min:4|max:50">
                                    <input
                                        v-model="courseContent.name"
                                        name="name"
                                        class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-4 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                    />
                                    <span class="block text-red-700 text-sm mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </div>
                            <div class="mb-3 w-96">
                                <div class="gap-x-16 mb-4 md:flex justify-between">
                                    <div class="w-full mb-4 md:mr-2 md:mb-0">
                                        <label class="mb-3 block text-base font-medium text-[#07074D]">
                                            Categoría
                                        </label>
                                        <ValidationProvider
                                            v-slot="{ errors }"
                                            name="Categoría del curso"
                                            rules="required|max:120"
                                        >
                                            <select
                                                v-model="courseContent.categories"
                                                class="border cursor-pointer border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 mb-5"
                                            >
                                                <option disabled value="">Seleccione una categoria:</option>
                                                <option
                                                    v-for="(choice, index) in categoriesList"
                                                    :key="index"
                                                    :value="choice.id"
                                                >
                                                    {{ choice.name }}
                                                </option>
                                            </select>
                                            <span class="block text-red-700 text-xs mt-1 ml-1">{{ errors[0] }}</span>
                                        </ValidationProvider>
                                    </div>
                                    <div class="w-full md:ml-2" hidden>
                                        <label class="mb-3 block text-base font-medium text-[#07074D]">
                                            Tipo de Curso
                                        </label>
                                        <ValidationProvider
                                            v-slot="{ errors }"
                                            name="Tipo de curso"
                                            rules="required|max:120"
                                        >
                                            <div>
                                                <select
                                                    v-model="courseContent.courseType"
                                                    class="border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                                                >
                                                    <option disabled value="">Seleccione un Tipo de Curso</option>
                                                    <option value="public">Público</option>
                                                    <option value="private">Requiere invitación</option>
                                                </select>
                                            </div>
                                            <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{
                                                errors[0]
                                            }}</span>
                                        </ValidationProvider>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="mb-3 block text-base font-medium text-[#07074D]"> Descripción </label>
                                    <ValidationProvider
                                        v-slot="{ errors }"
                                        name="Descripción"
                                        rules="required|max:120|min:4"
                                    >
                                        <textarea
                                            v-model="courseContent.description"
                                            rows="4"
                                            placeholder="En este Curso veremos..."
                                            class="w-full resize-none rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                                        />
                                        <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                    </ValidationProvider>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="w-full md:w-8/12 md:mx-2 mb-24">
                    <div class="justify-center items-center justify-center">
                        <div class="w-4/6">
                            <div class="bg-white">
                                <div class="image overflow-hidden">
                                    <div class="gap-32 md:gap-16 w-full flex justify-center pt-10">
                                        <img
                                            :src="imagen.src"
                                            alt="Anonimo"
                                            srcset=""
                                            class="prev-image rounded-sm position-relative image-perfil"
                                        />
                                    </div>
                                    <div class="flex justify-center items-center py-3">
                                        <label class="cursor-pointer">
                                            <span
                                                class="flex items-center text-white text-md border-black-300 border bg-black px-10 py-2 rounded-full"
                                            >
                                                Añadir Imagen
                                            </span>
                                            <ValidationProvider v-slot="{ errors }" name="Imagen" rules="required">
                                                <input
                                                    type="file"
                                                    class="hidden"
                                                    accept="image/*"
                                                    @change="oneFileChanged($event)"
                                                />
                                                <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{
                                                    errors[0]
                                                }}</span>
                                            </ValidationProvider>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="justify-end px-8">
                <div class="flex max-w-screen-xl mx-auto items-center justify-end space-x-2 mb-1 mt-4 mt-8">
                    <button
                        :disabled="invalidCourseFrom"
                        class="text-white bg-green-500 hover:bg-green-600 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:bg-green-500 dark:hover:bg-green-600 dark:focus:ring-green-600"
                        :class="{ 'opacity-25 cursor-not-allowed': invalidCourseFrom }"
                        @click="onClickSubmit"
                        v-text="type === TYPE_VIEW.CREATE ? 'Guardar nuevo curso' : 'Guardar cambios'"
                    />
                </div>
            </div>
        </ValidationObserver>
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
            updateButton: true,
            butonValid: false,
            moduleId: '',
            number: '',
            nombre: [],
            descripcion: [],
            imagen: {
                src: '/images/aviv.webp',
                type: 'image/jpg',
            },
            imageLoaded: false,
            categoriesList: [],
            courseContent: {
                courseImage: '',
                image: null,
                name: '',
                categories: '',
                type: '',
                courseType: 'public',
                description: '',
                modules: [],
            },
            dataReturned: {},
        }
    },
    computed: {
        titleForm() {
            return this.type === TYPE_VIEW.CREATE ? 'Crear nuevo curso' : 'Editar curso'
        },
        courseId() {
            return this.$route.params.idCurso
        },
    },
    mounted() {
        this.loadDataCategories()
    },
    created() {
        this.setComponentInfo()
    },
    methods: {
        setComponentInfo() {
            if (this.type === TYPE_VIEW.EDIT) {
                this.setInitialData()
            }
        },
        async setInitialData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                this.dataReturned = await this.$store.dispatch('course/getCourse', this.courseId)
                this.courseContent.name = this.dataReturned.name
                this.courseContent.categories = this.dataReturned.categories[0]
                this.courseContent.description = this.dataReturned.description
                this.courseContent.courseType = this.dataReturned.courseType
                if (this.dataReturned.courseImage) {
                    this.imagen.src = this.dataReturned.courseImage.image
                }
                this.imageLoaded = true
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
        onClickSubmit() {
            if (this.type === TYPE_VIEW.CREATE) {
                this.saveCourseAndModules()
            } else {
                this.editContentCourse()
            }
        },
        async loadDataCategories() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                this.categoriesList = await this.$store.dispatch('categories/getCategories')
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
        async editContentCourse() {
            const aux = JSON.stringify(this.courseContent)
            const JsonAux = JSON.parse(aux)
            JsonAux.categories = [this.courseContent.categories]
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                const payload = {
                    data: JsonAux,
                    id: this.courseId,
                }
                await this.$store.dispatch('course/updateCourse', payload)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Curso Actualizado',
                    position: 'top-right',
                })
                this.$router.go(-1)
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
        async oneFileChanged(event) {
            // Carga imagen del usuario
            const { files } = event.target
            if (files && files[0]) {
                if (this.imagen.src) {
                    URL.revokeObjectURL(this.imagen.src)
                    this.imagen.src = ''
                }
                const blob = URL.createObjectURL(files[0])
                // const reader = new FileReader()
                this.imagen = {
                    src: blob,
                    type: files[0].type,
                }
                this.imageLoaded = true
                const form = new FormData()
                form.append('image', files[0])
                const payload = {
                    data: form,
                }
                const loading = this.$vs.loading({
                    scale: 0.95,
                    type: 'circles',
                    color: '#16a34a',
                })

                try {
                    const imageLoaded = await this.$store.dispatch('course/uploadImage', payload)
                    this.courseContent.image = imageLoaded.id
                    this.$vs.notification({
                        color: 'success',
                        title: 'Éxito',
                        text: 'Imagen Actualizada',
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
        async saveCourseAndModules() {
            const aux = JSON.stringify(this.courseContent)
            const jsonAux = JSON.parse(aux)
            jsonAux.categories = [this.courseContent.categories]
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                if (this.imagen.src === '/images/aviv.webp') {
                    this.$vs.notification({
                        color: 'danger',
                        title: 'Error en Imagen',
                        text: 'Campo Imagen Obligatorio',
                        position: 'top-right',
                    })
                } else {
                    const data = await this.$store.dispatch('course/createCourse', jsonAux)
                    this.moduleId = data
                    this.$router.push({ path: `/gestion/mis-cursos/${data.id}/modulos` })
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
