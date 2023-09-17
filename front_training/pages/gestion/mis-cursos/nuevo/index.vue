<template>
    <div>
        <AgregarCursos :type="TYPE_VIEW.CREATE" />
    </div>
</template>

<script>
import AgregarCursos from '@/components/courses/CreateEditCourse.vue'
import mixins from '@/mixins/globals'

export default {
    components: { AgregarCursos },
    mixins: [mixins],
    layout: 'base',
}
</script>
