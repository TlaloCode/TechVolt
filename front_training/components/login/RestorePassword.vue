<template>
    <div class="h-screen flex">
        <div class="flex w-1/2 bg-gradient-to-tr from-blue-800 to-purple-700 i justify-around items-center">
            <div>
                <img src="@/assets/images/pages/forgot-password.png" alt="registrar" class="mx-auto" />
            </div>
        </div>
        <div class="flex w-1/2 justify-left px-20 py-20 bg-white">
            <div class="w-full">
                <div class="flex flex-col bg-white">
                    <div class="flex border-none">
                        <h4 class="pt-16 mb-4 text-2xl font-black">Recuperar contraseña</h4>
                    </div>
                    <ValidationObserver ref="observerInformation" v-slot="{ invalid }" tag="div">
                        <ValidationProvider v-slot="{ errors }" name="Contraseña" rules="required|min:8|max:32">
                            <div class="flex border-2 py-2 w-full rounded-2xl mb-4">
                                <input
                                    id="password"
                                    v-model="userPassword.password"
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
                                    v-model="userPassword.passwordConfirmation"
                                    autocomplete="off"
                                    class="pl-2 outline-none border-none w-full"
                                    type="password"
                                    name="passwordn"
                                    placeholder="Confirmar contraseña *"
                                />
                            </div>
                            <span class="block text-red-700 text-sm mb-2">{{ errors[0] }}</span>
                        </ValidationProvider>
                        <div class="lg:ml-31 ml-7 space-x-8">
                            <button
                                class="flex items-center bg-indigo-600 text-md border-black-300 border text-white font-semibold px-10 py-3 rounded-full boton"
                                :disabled="invalid"
                                :class="{ 'opacity-25 cursor-not-allowed': invalid }"
                                @click="recoveryPassword"
                            >
                                Cambiar contraseña
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
import { getUrlVars } from '@/assets/utils/utils'

export default {
    name: 'RestorePassword',
    components: {},
    data() {
        return {
            userPassword: {
                password: '',
                passwordConfirmation: '',
                token: '',
            },
        }
    },
    created() {
        const tokenUrl = getUrlVars('token').token
        this.userPassword.token = tokenUrl
        if (tokenUrl !== undefined) {
            const decoded = jwtDecode(tokenUrl)
            const date = Math.floor(Date.now() / 1000)
            if (date >= decoded.exp) {
                this.$vs.notification({
                    color: 'danger',
                    title: 'Url caducada',
                    text: `Favor de solicitar otro correo`,
                    position: 'top-right',
                })
            }
        } else {
            this.$nuxt.$router.replace({ path: '/auth/login' })
        }
    },
    methods: {
        recoveryPassword() {
            const payload = this.userPassword
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            this.$store
                .dispatch('auth/recoverPasswordJwt', payload)
                .then(() => {
                    this.$vs.notification({
                        title: 'Contraseña actualizada.',
                        text: 'Ahora puedes iniciar sesión.',
                        color: 'primary',
                        position: 'bottom-center',
                    })
                    this.$nuxt.$router.replace({ path: '/auth/login' })
                })
                .catch((error) => {
                    const res = error.message
                    this.$vs.notification({
                        color: 'danger',
                        title: 'Ocurrió un problema al recuperar tu cuenta',
                        text: res,
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
