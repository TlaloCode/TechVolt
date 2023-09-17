<template>
    <div>
        <AccordionSide>
            <template #item> <DocumentIcon /> <span class="pl-3">Cursos</span> </template>
            <template #panel>
                <SidenavItem title="Explorar cursos" to="/cursos" />
                <SidenavItem title="Cursos en progreso" to="/cursos-en-progreso" />
            </template>
        </AccordionSide>

        <AccordionSide>
            <template #item> <StaticsIcon /> <span class="pl-3">Gestión</span> </template>
            <template #panel>
                <SidenavItem title="Mis cursos" to="/gestion/mis-cursos" />
                <SidenavItem title="Agregar Curso" to="/gestion/mis-cursos/nuevo" />
                <SidenavItem title="Calendario" to="/gestion/mis-clases" />
                <SidenavItem title="Revisión de tareas" to="/gestion/tareas/calificar" />
            </template>
        </AccordionSide>

        <AccordionSide v-if="activeUserInfo.role === 'ADMIN'">
            <template #item> <StaticsIcon /> <span class="pl-3">Administración</span> </template>
            <template #panel>
                <SidenavItem title="Categorías de cursos" to="/administracion/catalogos/categorias" />
                <SidenavItem title="Invitar Usuarios" to="/administracion/invitaciones" />
            </template>
        </AccordionSide>
    </div>
</template>

<script>
/* ICONS */
import AccordionSide from './accordion/AccordionSide.vue'
import SidenavItem from './Item.vue'
import StaticsIcon from '@/components/icons/Statistics.vue'
import DocumentIcon from '@/components/icons/Documents.vue'

export default {
    name: 'SidenavItems',
    components: {
        AccordionSide,
        SidenavItem,
        DocumentIcon,
        StaticsIcon,
    },
    computed: {
        activeUserInfo() {
            return this.$store.state.auth.appActiveUser
        },
    },
}
</script>
