<template>
    <header class="h-16 md:h-20 shadow bg-white items-center relative z-10">
        <div class="flex flex-center flex-col h-full justify-center mx-auto relative px-3 text-white z-10">
            <div class="flex items-center pl-1 relative w-full sm:ml-0 sm:pr-2 lg:max-w-68">
                <div class="flex group h-full items-center relative w-12">
                    <button
                        type="button"
                        aria-expanded="false"
                        aria-label="Toggle sidenav"
                        class="text-4xl text-gray-700 focus:outline-none lg:hidden"
                        @click="toggle"
                    >
                        &#8801;
                    </button>
                </div>
                <div
                    class="flex items-center justify-end ml-5 mr-0 p-1 relative text-gray-700 w-full sm:mr-0 sm:right-auto"
                >
                    <nuxt-link to="/cursos" class="icono_play block pr-5 relative tooltip">
                        <span class="tooltip-box">Explorar Cursos</span>
                        <svg
                            class="w-8 h-8"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                            />
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                    </nuxt-link>
                    <div>
                        <button class="block pr-5 relative tooltip" @click="_logout">
                            <span class="tooltip-box">Cerrar Sesión</span>
                            <svg
                                class="icono_logout h-8 w-8"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <path
                                    fill="none"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                                />
                            </svg>
                        </button>
                    </div>
                    <router-link :to="{ name: 'perfil' }">
                        <div class="block relative">
                            <img alt="profile" :src="imagen.src" class="h-10 object-cover rounded-full w-10" />
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </header>
</template>

<script>
import { getErrorDetails } from '@/assets/utils/utils'

export default {
    name: 'TopNavigation',
    inject: ['toggle'],
    data() {
        return {
            imagen: {
                src: '/images/1.png',
                type: 'image/jpg',
            },
        }
    },
    computed: {
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
    },
    async mounted() {
        try {
            await this.$store.dispatch('user/fetchUserMe')
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
        }
        if (this.activeUserInfo.picture !== null) {
            this.imagen.src = this.activeUserInfo.picture
        }
    },
    methods: {
        _logout() {
            this.$store.dispatch('auth/logout')
            location.reload()
        },
    },
}
</script>
