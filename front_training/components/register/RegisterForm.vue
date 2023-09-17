<template>
    <div class="h-screen flex">
        <div class="flex w-1/2 bg-gradient-to-tr from-blue-800 to-purple-700 i justify-around items-center">
            <div>
                <img src="@/assets/images/pages/not-authorized.png" alt="registrar" />
            </div>
        </div>
        <div class="flex w-1/2 justify-left px-20 py-20 bg-white">
            <div class="w-full">
                <div class="flex flex-col bg-white">
                    <div class="flex border-none">
                        <h4 class="pt-16 mb-4 text-2xl font-black">Registrarse</h4>
                    </div>
                    <ValidationObserver v-slot="{ invalid }">
                        <ValidationProvider v-slot="{ errors }" name="Email" rules="required|email">
                            <div class="flex border-2 py-2 w-full rounded-2xl mb-4">
                                <input
                                    id="email"
                                    v-model="email"
                                    class="pl-2 outline-none border-none w-full"
                                    type="email"
                                    name="email"
                                    placeholder="Email"
                                    disabled
                                />
                            </div>
                            <span class="block text-red-700 text-sm mt-1 ml-1 h-1">{{ errors[0] }}</span>
                        </ValidationProvider>
                        <ValidationProvider v-slot="{ errors }" name="Nombre" rules="required|min:2">
                            <div class="flex border-2 py-2 w-full rounded-2xl mb-4">
                                <input
                                    id="nombre"
                                    v-model="name"
                                    class="pl-2 outline-none border-none w-full"
                                    type="text"
                                    name="nombre"
                                    placeholder="Nombre(s) *"
                                />
                            </div>
                            <span class="block text-red-700 text-sm mb-2">{{ errors[0] }}</span>
                        </ValidationProvider>
                        <ValidationProvider v-slot="{ errors }" name="Apellido paterno" rules="required|min:2">
                            <div class="flex border-2 py-2 w-full rounded-2xl mb-4">
                                <input
                                    id="Apellidopaterno"
                                    v-model="lastName"
                                    class="pl-2 outline-none border-none w-full"
                                    type="text"
                                    name="Apellidopaterno"
                                    placeholder="Apellido paterno *"
                                />
                            </div>
                            <span class="block text-red-700 text-sm mb-2">{{ errors[0] }}</span>
                        </ValidationProvider>
                        <ValidationProvider v-slot="{ errors }" name="Apellido materno" rules="min:2">
                            <div class="flex border-2 py-2 w-full rounded-2xl mb-4">
                                <input
                                    id="Apellidomaterno"
                                    v-model="secondLastName"
                                    class="pl-2 outline-none border-none w-full"
                                    type="text"
                                    name="Apellidomaterno"
                                    placeholder="Apellido materno"
                                />
                            </div>
                            <span class="block text-red-700 text-sm mb-2">{{ errors[0] }}</span>
                        </ValidationProvider>
                        <ValidationProvider
                            v-slot="{ errors }"
                            name="Número de teléfono"
                            rules="required|min:10|max:10|numeric"
                        >
                            <div class="flex border-2 py-2 w-full rounded-2xl mb-4">
                                <input
                                    id="phoneNumber"
                                    v-model="phoneNumber"
                                    class="pl-2 outline-none border-none w-full"
                                    type="tel"
                                    name="phoneNumber"
                                    placeholder="Número celular *"
                                />
                            </div>
                            <span class="block text-red-700 text-sm mb-2">{{ errors[0] }}</span>
                        </ValidationProvider>
                        <ValidationProvider v-slot="{ errors }" name="Contraseña" rules="required|min:8|max:32">
                            <div class="flex border-2 py-2 w-full rounded-2xl mb-4">
                                <input
                                    id="password"
                                    v-model="password"
                                    autocomplete="off"
                                    class="pl-2 outline-none border-none w-full"
                                    type="password"
                                    name="password"
                                    placeholder="Contraseña *"
                                />
                            </div>
                            <span class="block text-red-700 text-sm mb-2">{{ errors[0] }}</span>
                        </ValidationProvider>
                        <ValidationProvider v-slot="{ errors }" name="Confirmar contraseña" rules="required">
                            <div class="flex border-2 py-2 w-full rounded-2xl mb-4">
                                <input
                                    id="passwordn"
                                    v-model="passwordConfirmation"
                                    autocomplete="off"
                                    class="pl-2 outline-none border-none w-full"
                                    type="password"
                                    name="passwordn"
                                    placeholder="Confirmar contraseña *"
                                />
                            </div>
                            <span class="block text-red-700 text-sm mb-2">{{ errors[0] }}</span>
                        </ValidationProvider>
                        <div class="lg:ml-40 ml-10 space-x-8">
                            <button
                                class="flex items-center bg-indigo-600 text-md border-black-300 border text-white font-semibold px-10 py-2 rounded-full boton"
                                :invalid="invalid"
                                :disabled="invalid"
                                :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                @click="registerUserJWt"
                            >
                                Registrarme
                            </button>
                        </div>
                    </ValidationObserver>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import jwtDecode from 'jwt-decode'
import { getUrlVars, getErrorDetails } from '@/assets/utils/utils'

export default {
    data() {
        return {
            name: '',
            lastName: '',
            email: '',
            password: '',
            passwordConfirmation: '',
            phoneNumber: '',
            secondLastName: '',
            role: '',
            token: '',
            isTermsConditionAccepted: false,
        }
    },
    created() {
        // Valida si una cuenta requiere ser activada
        const tokenUrl = getUrlVars('token').token
        this.token = tokenUrl
        if (tokenUrl !== undefined) {
            const decoded = jwtDecode(tokenUrl)
            this.email = decoded.email
            this.role = decoded.role
        } else {
            this.$nuxt.$router.replace({ path: '/auth/login' })
        }
    },
    methods: {
        checkLogin() {
            // If user is already logged in notify
            if (this.$store.state.auth.isUserLoggedIn) {
                // Close animation if passed as payload

                this.$vs.notification({
                    title: 'Login Attempt',
                    text: 'Ya tienes una sesión activa!',
                    iconPack: 'feather',
                    icon: '<i class="bx bx-error-alt"></i>',
                    color: 'warning',
                })

                return false
            }
            return true
        },
        /**
         * Creación de clientes nuevos
         */
        async registerUserJWt() {
            if (!this.checkLogin()) return
            const payload = {
                userDetails: {
                    name: this.name,
                    lastName: this.lastName,
                    secondLastName: this.secondLastName,
                    email: this.email,
                    password: this.password,
                    passwordConfirmation: this.passwordConfirmation,
                    phoneNumber: this.phoneNumber,
                    role: this.role,
                    token: this.token,
                },
            }

            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })

            await this.$store
                .dispatch('auth/registerUserJWT', { payload })
                .then(() => {
                    this.$vs.notification({
                        title: 'Usuario creado.',
                        time: 8000,
                        text: 'Por favor, revisa tu correo para activar tu cuenta.',
                        color: 'primary',
                        position: 'bottom-center',
                    })
                    this.$nuxt.$router.replace({ path: '/auth/login' })
                })
                .catch((error) => {
                    let res = ''
                    if (error.response) {
                        res = getErrorDetails(error.response.data.errors)
                    } else {
                        res = error.message
                    }
                    this.$vs.notification({
                        color: 'danger',
                        title: 'Ocurrió un problema al crear tu cuenta',
                        time: 8000,
                        text: `${res}`,
                        position: 'top-right',
                    })
                })
                .finally(() => {
                    loading.close()
                })
        },
    },
}
</script>
