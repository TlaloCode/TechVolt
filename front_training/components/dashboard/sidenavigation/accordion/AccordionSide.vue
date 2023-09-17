<template>
    <div>
        <div role="button" class="flex justify-start my-2 py-6 px-4 text-black text-sm" @click="toggle">
            <slot name="item" />
            <span class="ml-auto">
                <AngleDownIcon v-show="isActive" />
                <AngleRightIcon v-show="!isActive" />
            </span>
        </div>
        <div
            id="accordion"
            ref="accordionRef"
            :style="[isActive ? { height: computedHeight } : {}]"
            class="-mt-5 overflow-hidden text-gray-600 transition-height ease duration-300"
        >
            <slot name="panel" />
        </div>
    </div>
</template>

<script>
import AngleDownIcon from './AngleDownIcon.vue'
import AngleRightIcon from './AngleRightIcon.vue'

export default {
    name: 'AccordionSide',
    components: { AngleRightIcon, AngleDownIcon },
    data() {
        return {
            isActive: true,
            computedHeight: '0',
        }
    },
    mounted() {
        this.initHeight()
    },
    methods: {
        toggle() {
            this.isActive = !this.isActive
        },
        initHeight() {
            this.$refs.accordionRef.style.height = 'auto'

            this.computedHeight = getComputedStyle(this.$refs.accordionRef).height
            this.$refs.accordionRef.style.height = '0'
        },
    },
}
</script>

<style scoped>
#accordion {
    height: 0;
    overflow: hidden;
    transition: 300ms;
}
</style>
