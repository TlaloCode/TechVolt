<template>
    <div>
        <span>Entrega de Tareas:</span>
        <div class="px-4 py-2 font-semibold">
            <span>Entrega de Tareas:</span>
        </div>
        <LessonsChat />
    </div>
</template>
<script>
import LessonsChat from '~/components/lessons/LessonsChat.vue'

export default {
    name: 'ChatComponent',
    components: {
        LessonsChat,
    },
}
</script>
