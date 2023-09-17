<template>
    <div class="bg-gray-100">
        <div class="container mx-auto my-5 p-5">
            <ValidationObserver ref="observer" v-slot="{ invalid }" tag="div" class="min-h-full flex justify-center">
                <!-- Left Side -->
                <div class="w-full md:w-3/12 md:mx-2">
                    <!-- Profile Card -->
                    <div class="bg-white p-3 border-t-4 border-green-400">
                        <div class="image overflow-hidden">
                            <div class="gap-32 md:gap-56 w-full flex justify-center p-2">
                                <img
                                    :src="userPersonalData.picture"
                                    alt="PersonalImage"
                                    srcset=""
                                    class="prev-image rounded-sm position-relative image-perfil"
                                />
                            </div>
                            <div v-if="edit === true" class="flex py-3">
                                <label class="cursor-pointer mx-auto">
                                    <span
                                        class="focus:outline-none text-white text-sm-center py-2 px-4 rounded-full bg-green-400 hover:bg-green-500 hover:shadow-lg"
                                    >
                                        Editar Imagen
                                    </span>
                                    <input
                                        type="file"
                                        class="hidden button"
                                        accept="image/*"
                                        @change="oneFileChanged($event)"
                                    />
                                </label>
                            </div>
                        </div>
                        <h1 class="text-gray-900 font-bold text-xl leading-8 my-1 text-center">
                            {{ completeName }}
                        </h1>
                    </div>
                    <!-- End of profile card -->
                    <div class="my-4" />
                </div>
                <!-- Right Side -->
                <div v-if="edit === false" class="w-full md:w-9/12 mx-2">
                    <!-- Profile tab -->
                    <!-- About Section -->
                    <div class="bg-white p-3 shadow-sm rounded-sm">
                        <div class="flex items-center space-x-2 font-semibold text-gray-900 leading-8 mb-8">
                            <span class="text-green-500">
                                <svg
                                    class="h-8"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                                    />
                                </svg>
                            </span>
                            <span class="tracking-wide text-3xl">Información</span>
                        </div>
                        <div class="text-gray-700">
                            <div class="container">
                                <div class="row">
                                    <div class="col-12">
                                        <div class="px-4 py-2 font-semibold text-lg">Nombre</div>
                                    </div>
                                    <div class="col-12">
                                        <div class="px-6 py-2 text-base">
                                            {{ userPersonalData.name }}
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-12">
                                        <div class="px-4 py-2 font-semibold text-lg">Apellido (Paterno)</div>
                                    </div>
                                    <div class="col-12">
                                        <div class="px-6 py-2 text-base">
                                            {{ userPersonalData.lastName }}
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-12">
                                        <div class="px-4 py-2 font-semibold text-lg">Apellido (Materno)</div>
                                    </div>
                                    <div class="col-12">
                                        <div class="px-6 py-2 text-base">
                                            {{ userPersonalData.secondLastName }}
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-12">
                                        <div class="px-4 py-2 font-semibold text-lg">Teléfono</div>
                                    </div>
                                    <div class="col-12">
                                        <div class="px-6 py-2 text-base">
                                            {{ userPersonalData.phone }}
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-12">
                                        <div class="px-4 py-2 font-semibold text-lg">Email</div>
                                    </div>
                                    <div class="col-12">
                                        <div class="px-6 py-2">
                                            <a
                                                class="text-blue-800 text-base"
                                                :href="`mailto:${userPersonalData.email}`"
                                            />
                                            {{ userPersonalData.email }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <button
                            v-if="sameProfile === true"
                            class="block w-full text-white text-sm font-semibold rounded-lg bg-green-400 hover:bg-green-500 focus:outline-none focus:shadow-outline focus:bg-gray-100 hover:shadow-xs p-3 my-4"
                            @click="edit = true"
                        >
                            Editar
                        </button>
                    </div>
                </div>
                <!-- BEGIN EDIT section -->
                <div v-if="edit === true" class="bg-white p-3 shadow-sm rounded-sm">
                    <div class="flex items-center space-x-2 font-semibold text-gray-900 leading-8">
                        <span class="text-green-500">
                            <svg
                                class="h-5"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                                />
                            </svg>
                        </span>
                        <span class="tracking-wide text-3xl">Editar Información</span>
                    </div>
                    <br /><br />
                    <div class="text-gray-700">
                        <div class="grid md:grid-cols-1 text-sm">
                            <div class="grid grid-cols-2">
                                <div class="px-4 py-2 font-semibold text-lg">Nombre</div>
                                <br />
                                <ValidationProvider
                                    v-slot="{ errors }"
                                    name="Nombres"
                                    rules="required|max:120|alpha_spaces|min:4"
                                >
                                    <input
                                        v-model="userPersonalData.name"
                                        label-placeholder="Nombre(s)"
                                        class="w-80 mx-6 py-2 rounded-md bg-gray-50 px-4 ring-2 ring-gray-200 text-base"
                                    />
                                    <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </div>
                            <div class="grid grid-cols-2">
                                <div class="px-4 py-2 font-semibold text-lg">Apellido Paterno</div>
                                <br />
                                <ValidationProvider
                                    v-slot="{ errors }"
                                    name="Apellido Paterno"
                                    rules="required|max:45|alpha_spaces"
                                >
                                    <input
                                        v-model="userPersonalData.lastName"
                                        label-placeholder="Apellido Paterno"
                                        class="w-80 mx-6 py-2 rounded-md bg-gray-50 px-4 ring-2 ring-gray-200 text-base"
                                    />
                                    <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </div>
                            <div class="grid grid-cols-2">
                                <div class="px-4 py-2 font-semibold text-lg">Apellido Materno</div>
                                <br />
                                <ValidationProvider
                                    v-slot="{ errors }"
                                    name="Apellido Materno"
                                    rules="max:45|alpha_spaces"
                                >
                                    <input
                                        v-model="userPersonalData.secondLastName"
                                        label-placeholder="Apellido Materno"
                                        class="w-80 mx-6 py-2 rounded-md bg-gray-50 px-4 ring-2 ring-gray-200 text-base"
                                    />
                                    <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </div>
                            <div class="grid grid-cols-2">
                                <div class="px-4 py-2 font-semibold text-lg">Teléfono</div>
                                <br />
                                <ValidationProvider
                                    v-slot="{ errors }"
                                    name="phoneNumber"
                                    rules="required|min:10|max:10|numeric"
                                >
                                    <input
                                        id="phoneNumber"
                                        v-model="userPersonalData.phone"
                                        class="w-80 mx-6 py-2 rounded-md bg-gray-50 px-4 ring-2 ring-gray-200 text-base"
                                        type="tel"
                                        name="phoneNumber"
                                        placeholder="Número celular *"
                                    />
                                    <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </div>
                            <div class="grid grid-cols-2">
                                <div class="px-4 py-2 font-semibold text-lg">Email</div>
                                <br />
                                <ValidationProvider v-slot="{ errors }" name="Email" rules="required|email|max:254">
                                    <input
                                        v-model="userPersonalData.email"
                                        label-placeholder="Nombre(s)"
                                        class="w-80 mx-6 py-2 rounded-md bg-gray-50 px-4 ring-2 ring-gray-200 text-base"
                                    />
                                    <span class="block text-red-700 text-xs mt-1 ml-1 h-5">{{ errors[0] }}</span>
                                </ValidationProvider>
                            </div>
                        </div>
                        <button
                            :disabled="invalid"
                            class="block w-full text-white text-sm font-semibold rounded-lg bg-green-400 hover:bg-green-500 focus:outline-none focus:shadow-outline focus:bg-gray-100 hover:shadow-xs p-3 my-4"
                            :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                            @click="updatePersonalData"
                        >
                            Guardar
                        </button>
                    </div>
                    <!-- END Edit Seccion -->

                    <div class="my-4" />

                    <!-- CURSOS Visibles si eres profe -->
                    <div v-if="activeUserInfo.role === 'teacher'" class="bg-white p-3 shadow-sm rounded-sm">
                        <div class="grid grid-cols-2">
                            <div>
                                <div class="flex items-center space-x-2 font-semibold text-gray-900 leading-8 mb-3">
                                    <span class="text-green-500">
                                        <UserIcon />
                                    </span>
                                    <span class="tracking-wide">Cursos Disponibles</span>
                                </div>
                                <ul class="list-inside space-y-2">
                                    <li>
                                        <div class="text-teal-600">Owner at Her Company Inc.</div>
                                        <div class="text-gray-500 text-xs">March 2020 - Now</div>
                                    </li>
                                    <li>
                                        <div class="text-teal-600">Owner at Her Company Inc.</div>
                                        <div class="text-gray-500 text-xs">March 2020 - Now</div>
                                    </li>
                                    <li>
                                        <div class="text-teal-600">Owner at Her Company Inc.</div>
                                        <div class="text-gray-500 text-xs">March 2020 - Now</div>
                                    </li>
                                    <li>
                                        <div class="text-teal-600">Owner at Her Company Inc.</div>
                                        <div class="text-gray-500 text-xs">March 2020 - Now</div>
                                    </li>
                                </ul>
                            </div>
                            <div>
                                <div class="flex items-center space-x-2 font-semibold text-gray-900 leading-8 mb-3">
                                    <span class="text-green-500">
                                        <svg
                                            class="h-5"
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
                                    <span class="tracking-wide">Cursos</span>
                                </div>
                                <ul class="list-inside space-y-2">
                                    <li>
                                        <div class="text-teal-600">Masters Degree in Oxford</div>
                                        <div class="text-gray-500 text-xs">March 2020 - Now</div>
                                    </li>
                                    <li>
                                        <div class="text-teal-600">Bachelors Degreen in LPU</div>
                                        <div class="text-gray-500 text-xs">March 2020 - Now</div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <!-- End of Experience and education grid -->
                    </div>
                    <!-- End of profile tab -->
                </div>
            </ValidationObserver>
        </div>
    </div>
</template>
<script>
import { getErrorDetails } from '@/assets/utils/utils'
import UserIcon from '@/components/icons/User.vue'

export default {
    components: {
        UserIcon,
    },
    data() {
        return {
            imagen: {
                src: '',
                type: 'image/jpg',
            },
            imageLoaded: '',
            isUserActive: '',
            activeUserInfo: {},
            sameProfile: '',
            username: '',
            picture: '',
            edit: false,
            userPersonalData: {
                lastName: '',
                secondLastName: '',
                name: '',
                email: '',
                picture: '/images/1.png',
                description: '',
                contact: '',
                phone: '',
            },
        }
    },
    computed: {
        completeName() {
            return (
                this.userPersonalData.name +
                ' ' +
                this.userPersonalData.lastName +
                ' ' +
                this.userPersonalData.secondLastName
            )
        },
    },
    async created() {
        if (!this.$route.query.id) {
            const payload = {}
            this.activeUserInfo = await this.$store.dispatch('user/fetchUserMe', payload)
            this.sameProfile = true
        } else {
            const id = this.$route.query.id
            this.$store.dispatch('user/fetchUser', id).then((data) => {
                this.activeUserInfo = data
            })
            this.sameProfile = false
        }

        this.setInitialData()
    },
    mounted() {
        // Inicializa listener para input de imagen de perfil
        // this.setPictureFileInputEventListener()
    },
    methods: {
        /**
         *  Simula un clic para cargar la iamgen de perfil de usuario
         */
        updatePhoto() {
            document.getElementById('pictureFile').click()
        },
        /**
         * Configura los campos iniciales del componente
         */
        setInitialData() {
            // Campos de sólo lectura
            this.username = this.activeUserInfo.username
            if (this.activeUserInfo.isActive) {
                this.isUserActive = this.activeUserInfo.isActive
                this.isUserActive = 'Activo'
            } else {
                this.isUserActive = 'Inactivo'
            }
            // this.picture = this.activeUserInfo.userprofile.picture
            // this.email = this.activeUserInfo.email
            this.userPersonalData.email = this.activeUserInfo.email

            if (this.activeUserInfo.picture !== null) {
                this.userPersonalData.picture = this.activeUserInfo.picture
            }
            this.imageLoaded = true
            // Campos editables
            this.userPersonalData.name = this.activeUserInfo.name
            this.userPersonalData.email = this.activeUserInfo.email
            this.userPersonalData.lastName = this.activeUserInfo.lastName
            this.userPersonalData.secondLastName = this.activeUserInfo.secondLastName
            this.userPersonalData.phone = this.activeUserInfo.phoneNumber
            this.userPersonalData.contact = this.activeUserInfo.contact
        },
        /**
         * Actualiza datos basicos del usuario
         */
        async updatePersonalData() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            try {
                this.edit = false
                const formData = new FormData()

                formData.append('name', this.userPersonalData.name)
                formData.append('lastName', this.userPersonalData.lastName)
                formData.append('secondLastName', this.userPersonalData.secondLastName)
                formData.append('phoneNumber', this.userPersonalData.phone)
                formData.append('contact', this.userPersonalData.contact)
                formData.append('description', this.userPersonalData.description)
                formData.append('user', this.userPersonalData.user)
                formData.append('email', this.userPersonalData.email)

                const payload = {
                    data: formData,
                    id: this.activeUserInfo.id,
                }
                await this.$store.dispatch('user/updateUser', payload)
                this.$vs.notification({
                    color: 'success',
                    title: 'Éxito',
                    text: 'Información actualizada',
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
         * Método para cargar la imagen de perfil
         */
        async oneFileChanged(event) {
            // Carga imagen del usuario
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            const { files } = event.target
            if (files && files[0]) {
                if (this.imagen.src) {
                    URL.revokeObjectURL(this.imagen.src)
                    this.imagen.src = ''
                }
                const blob = URL.createObjectURL(files[0])
                this.imagen = {
                    src: blob,
                    type: files[0].type,
                }
                this.imageLoaded = true
                this.userPersonalData.picture = this.imagen.src

                const form = new FormData()
                form.append('picture', files[0])
                form.append('user', this.activeUserInfo.id)
                const payload = {
                    data: form,
                    id: this.activeUserInfo.id,
                }

                try {
                    await this.$store.dispatch('user/updatePictureUser', payload)
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
        /**
         * Listener para el input file de imagen de perfil
         */
        setPictureFileInputEventListener() {
            const pictureFile = this.$refs.pictureFile
            const self = this
            pictureFile.addEventListener('change', function () {
                self.fileChosenName = this.files[0].name
            })
        },
    },
}
</script>
<style></style>
