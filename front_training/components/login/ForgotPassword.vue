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
                        <h4 class="pt-16 mb-4 text-2xl font-black">Recuperar tu contraseña</h4>
                    </div>
                    <br />
                    <p class="font-normal mx-2 text-sm text-gray-600">
                        Favor de introducir su email para recuperar la contraseña.
                    </p>
                    <div class="flex items-center border-2 py-2 px-3 rounded-2xl mb-4">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5 text-gray-400"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
                            />
                        </svg>
                        <input
                            id="email"
                            v-model="email"
                            class="w-96 pl-2 outline-none border-none"
                            type="email"
                            name="email"
                            placeholder="Email"
                        />
                    </div>
                    <button
                        class="block w-full bg-indigo-600 mt-2 py-2 rounded-2xl text-white font-semibold mb-2"
                        @keyup.enter="recoverPasswordByEmail"
                        @click="recoverPasswordByEmail"
                    >
                        Recuperar contraseña
                    </button>
                </div>
                <router-link
                    :to="{
                        name: 'auth-login',
                    }"
                    class="font-normal mx-4 text-sm text-blue-600 cursor-pointer"
                >
                    Iniciar Sesión
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import { getErrorDetails } from '@/assets/utils/utils'

export default {
    components: {},
    data() {
        return {
            email: '',
            error: null,
        }
    },
    methods: {
        recoverPasswordByEmail() {
            const payload = { email: this.email }
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            this.$store
                .dispatch('auth/recoverPasswordByEmail', payload)
                .then(() => {
                    this.$vs.notification({
                        title: 'Email enviado.',
                        text: 'Por favor, revisa tu correo para recuperar tu cuenta.',
                        color: 'success',
                        position: 'bottom-center',
                    })
                    this.$nuxt.$router.replace({ path: '/auth/login' })
                })
                .catch((err) => {
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
                })
                .finally(() => {
                    loading.close()
                })
        },
    },
}
</script>
