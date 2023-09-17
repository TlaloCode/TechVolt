<template>
    <CreateEditCategory :type="TYPE_VIEW.CREATE" />
</template>

<script>
import CreateEditCategory from '@/components/categories/CreateEditCategory'
import mixins from '@/mixins/globals'

export default {
    name: 'Index',
    components: { CreateEditCategory },
    mixins: [mixins],
    layout: 'base',
}
</script>

<style scoped></style>
