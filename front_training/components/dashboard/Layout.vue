<template>
    <DashboardProvider>
        <div class="bg-gray-100 h-screen overflow-hidden relative">
            <div class="content h-screen overflow-hidden relative lg:rounded-2xl">
                <div class="flex items-start">
                    <OverlayDash />
                    <SideNavigation mobile-position="right" />
                    <div class="flex flex-col h-screen pl-0 w-full lg:space-y-4 lg:w-99">
                        <TopNavigation />
                        <main class="h-screen overflow-auto pb-36 pt-8 px-2 md:pb-8 md:pt-4 md:px-8 lg:pt-0">
                            <slot />
                        </main>
                    </div>
                </div>
            </div>
        </div>
    </DashboardProvider>
</template>

<script>
import TopNavigation from './topnavigation/Index.vue'
import SideNavigation from './sidenavigation/Index.vue'
import DashboardProvider from './provider/Provider.vue'
import OverlayDash from './provider/OverlayDash.vue'

export default {
    name: 'DashboardLayout',
    components: { DashboardProvider, SideNavigation, TopNavigation, OverlayDash },
}
</script>
