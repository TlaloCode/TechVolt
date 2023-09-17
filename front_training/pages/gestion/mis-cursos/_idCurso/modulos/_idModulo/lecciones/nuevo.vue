<template>
    <CreateEditLessonContent :type="TYPE_VIEW.CREATE" />
</template>
<script>
import CreateEditLessonContent from '@/components/lessons/CreateEditLessonContent.vue'
import mixins from '@/mixins/globals'

export default {
    components: {
        CreateEditLessonContent,
    },
    mixins: [mixins],
    layout: 'base',
}
</script>
