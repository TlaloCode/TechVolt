<template>
    <div class="bg-white p-8 rounded-md w-full">
        <div class="flex items-center justify-between pb-6">
            <div>
                <h2 class="text-gray-600 font-semibold text-2xl">Usuarios</h2>
            </div>
            <div class="flex items-center justify-between">
                <!--        <div class='flex bg-gray-50 items-center p-2 rounded-md'>-->
                <!--          <svg xmlns='http://www.w3.org/2000/svg' class='h-5 w-5 text-gray-400' viewBox='0 0 20 20' fill='currentColor'>-->
                <!--            <path-->
                <!--              fill-rule='evenodd'-->
                <!--              d='M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z'-->
                <!--              clip-rule='evenodd'-->
                <!--            />-->
                <!--          </svg>-->
                <!--          <input id='' class='bg-gray-50 outline-none ml-1 block ' type='text' name='' placeholder='search...'>-->
                <!--        </div>-->
                <div class="lg:ml-40 ml-10 space-x-8">
                    <button
                        class="text-green-600 hover:text-white border border-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mb-2 dark:border-green-400 dark:text-green-400 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-700"
                        @click="openModal"
                    >
                        Invitar Usuario
                    </button>
                </div>
            </div>
        </div>
        <div>
            <div>
                <vue-good-table
                    :columns="columns"
                    :rows="rowsUser"
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
                />
            </div>
            <div class="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4 overflow-x-auto">
                <div class="inline-block min-w-full shadow rounded-lg overflow-hidden">
                    <div v-if="showModal">
                        <ModalInfo>
                            <template #content>
                                <div class="flex flex-col px-4 sm:px-6 md:px-8 lg:px-10 py-8 rounded-3xl">
                                    <div
                                        class="flex w-1/12 h-auto justify-center cursor-pointer"
                                        @click="showModal = false"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            width="24"
                                            height="24"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="#000000"
                                            stroke-width="2"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            class="feather feather-x"
                                        >
                                            <line x1="18" y1="6" x2="6" y2="18" />
                                            <line x1="6" y1="6" x2="18" y2="18" />
                                        </svg>
                                    </div>
                                    <div class="font-medium self-center text-xl sm:text-3xl text-gray-800">
                                        Invitacion de usuario
                                    </div>
                                    <div class="mt-4 self-center text-xl sm:text-md text-gray-800">
                                        Escribe el correo del usuario
                                    </div>
                                    <div class="mt-10">
                                        <div class="flex flex-col mb-5">
                                            <label for="email" class="mb-1 text-md tracking-wide text-gray-600">
                                                Email:
                                            </label>
                                            <div class="relative">
                                                <div
                                                    class="inline-flex items-center justify-center absolute left-0 top-0 h-full w-10 text-gray-400"
                                                >
                                                    <i class="fas fa-at text-blue-500" />
                                                </div>
                                                <input
                                                    id="email"
                                                    v-model="userInfo.email"
                                                    type="email"
                                                    name="email"
                                                    class="text-sm placeholder-gray-500 pl-10 pr-4 rounded-2xl border border-gray-400 w-full py-2 focus:outline-none focus:border-blue-400"
                                                    placeholder="Ingresar correo"
                                                    @keyup.enter="sendInvitation"
                                                />
                                            </div>
                                        </div>
                                        <div>
                                            <label class="mb-1 text-md tracking-wide text-gray-600"> Rol: </label>
                                            <div
                                                class="inline-flex items-center justify-center absolute left-0 top-0 h-full w-10 text-gray-400"
                                            >
                                                <i class="fas fa-at text-blue-500"></i>
                                            </div>
                                            <select
                                                v-if="activeUserInfo.role === 'ADMIN'"
                                                v-model="userInfo.role"
                                                placeholder="Rol"
                                                class="text-sm placeholder-gray-500 pl-10 pr-4 mb-5 rounded-2xl border border-gray-400 w-full py-2 focus:outline-none focus:border-blue-400"
                                            >
                                                <option value="ADMIN">Administrador</option>
                                                <option selected value="USER">Usuario</option>
                                            </select>
                                        </div>
                                        <div class="flex w-full">
                                            <button
                                                class="flex mt-2 items-center justify-center focus:outline-none text-white text-sm sm:text-base bg-blue-500 hover:bg-blue-600 rounded-2xl py-2 w-full transition duration-150 ease-in"
                                                @click="sendInvitation"
                                            >
                                                <span class="mr-2 uppercase">Enviar</span>
                                                <span>
                                                    <svg
                                                        class="h-6 w-6"
                                                        fill="none"
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        stroke-width="2"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor"
                                                    >
                                                        <path
                                                            d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z"
                                                        />
                                                    </svg>
                                                </span>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </ModalInfo>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { getErrorDetails } from '@/assets/utils/utils'
import ModalInfo from '@/components/ModalInfo'

export default {
    components: {
        ModalInfo,
    },
    data() {
        return {
            rowsUser: [],
            userInfo: {
                role: '',
                email: '',
            },
            userEmail: '',
            columns: [
                {
                    label: 'Nombre',
                    field: 'user.getFullName',
                },
                {
                    label: 'Email',
                    field: 'email',
                },
                {
                    label: 'Estatus',
                    field: 'isRegistered',
                },
                {
                    label: 'Invitaciones enviadas',
                    field: 'count',
                },
                {
                    label: 'Fecha invitación',
                    field: 'sendAt',
                },
                {
                    label: 'Fecha de Creación',
                    field: 'createdAt',
                },
                {
                    label: 'Rol',
                    field: 'role',
                },
            ],
            showModal: false,
        }
    },
    computed: {
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
    },
    mounted() {
        this.getUsersTable()
        this.initModalForm()
    },
    methods: {
        async getUsersTable() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                const getUserInvitationsResult = await this.$store.dispatch('user/getUserInvitations')
                this.rowsUser = getUserInvitationsResult.results.map((item) => {
                    item.isRegistered = item.isRegistered === true ? 'Registrado' : 'Pendiente'
                    item.role = item.role === 'USER' ? 'Usuario' : 'Administrador'
                    return item
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
        initModalForm() {
            this.userInfo.email = ''
            this.userInfo.role = 'USER'
        },
        openModal() {
            this.showModal = true
        },
        // Método para envíar invitacion del usuario
        async sendInvitation() {
            const loading = this.$vs.loading({
                scale: 0.95,
                type: 'circles',
                color: '#16a34a',
            })
            try {
                this.showModal = false
                this.dataModules = await this.$store.dispatch('user/sendInvitation', this.userInfo)
                this.$vs.notification({
                    color: 'success',
                    title: 'Email enviado',
                    text: 'Invitación enviada',
                    position: 'top-right',
                })
                this.getUsersTable()
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
                this.initModalForm()
            }
        },
    },
}
</script>
