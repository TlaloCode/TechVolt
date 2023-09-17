<template>
    <div class="pl-5">
        <NuxtLink :to="to">
            <span class="inline-flex items-center justify-start my-1 p-3 text-black">
                <span
                    :class="
                        $route.path === to
                            ? 'font-normal mx-4 text-sm text-blue-600'
                            : 'font-light mx-4 text-sm text-gray-900'
                    "
                >
                    {{ title }}
                </span>
            </span>
        </NuxtLink>
    </div>
</template>

<script>
export default {
    name: 'SidenavItem',
    props: {
        to: {
            type: String,
            default: '',
        },
        title: {
            type: String,
            default: '',
        },
    },
}
</script>
