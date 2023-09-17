<template>
    <div>
        <AddAndEditHomework :type="TYPE_VIEW.EDIT" />
    </div>
</template>

<script>
import AddAndEditHomework from '@/components/homeworks/CreateEditHomework.vue'
import mixins from '@/mixins/globals'

export default {
    components: { AddAndEditHomework },
    mixins: [mixins],
    layout: 'base',
}
</script>
