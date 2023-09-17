<template>
    <div class="h-screen flex">
        <div class="flex w-1/2 bg-gradient-to-tr from-blue-800 to-purple-700 i justify-around items-center">
            <div>
                <h1 class="text-white font-bold text-4xl font-sans">FYG Training</h1>
                <p class="text-white mt-1">La mejor forma de crecer y aprender</p>
            </div>
        </div>
        <div class="flex w-1/2 justify-center items-center bg-white">
            <div class="bg-white">
                <h1 class="text-gray-800 font-bold text-2xl mb-1">¡Hola!</h1>
                <p class="text-sm font-normal text-gray-600 mb-7">Bienvenido</p>
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
                        v-model="user.username"
                        class="w-96 pl-2 outline-none border-none"
                        type="email"
                        name="email"
                        placeholder="Email"
                        @keyup.enter="loginJWT"
                    />
                </div>
                <div class="flex items-center border-2 py-2 px-3 rounded-2xl mb-4">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5 text-gray-400"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                            clip-rule="evenodd"
                        />
                    </svg>
                    <input
                        id="password"
                        v-model="user.password"
                        class="w-96 pl-2 outline-none border-none"
                        type="password"
                        name="password"
                        placeholder="Password"
                        @keyup.enter="loginJWT"
                    />
                </div>
                <button
                    class="block w-full bg-indigo-600 mt-4 py-2 rounded-2xl text-white font-semibold mb-2"
                    @click="loginJWT"
                >
                    Iniciar Sesión
                </button>
                <router-link
                    :to="{
                        name: 'olvide-contrasenia',
                    }"
                    class="font-normal mx-4 text-sm text-blue-600 cursor-pointer"
                >
                    Recuperar contraseña
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import { getUrlVars, getErrorDetails } from '@/assets/utils/utils'

export default {
    name: 'AuthLogin',
    components: {},
    data() {
        return {
            user: {
                username: '',
                password: '',
            },
            error: null,
        }
    },
    mounted() {
        const token = getUrlVars('token').token
        if (token !== undefined) {
            this.userActivation({ token })
                .then((res) => {
                    this.$vs.notification({
                        color: 'success',
                        title: 'Cuenta activada',
                        text: res.message,
                        position: 'top-right',
                    })
                })
                .catch((error) => {
                    let res = ''
                    if (error.response) {
                        res = getErrorDetails(error.response.data.errors)
                    } else {
                        res = error.message
                    }
                    this.$vs.notification({
                        title: 'Ops..',
                        text: `${res}`,
                        color: 'danger',
                        position: 'top-right',
                    })
                })
        }
        if (localStorage.getItem('accessToken')) {
            this.$router.push('/')
        }
    },
    methods: {
        userActivation(payload) {
            return this.$store.dispatch('auth/userActivation', payload)
        },
        checkLogin() {
            // If user is already logged in notify
            if (localStorage.getItem('accessToken')) {
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
        async loginJWT() {
            if (!this.checkLogin()) return
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                await this.$store.dispatch('auth/loginJWT', this.user)
                await this.$store.dispatch('user/fetchUserMe')
                this.$nuxt.$router.replace({ path: '/cursos' }).catch()
            } catch (error) {
                let res = ''
                if (error.response) {
                    res = getErrorDetails(error.response.data.errors)
                }
                this.$vs.notification({
                    title: 'Error',
                    text: `${res}`,
                    icon: '<i class="bx bx-error-alt"></i>',
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
