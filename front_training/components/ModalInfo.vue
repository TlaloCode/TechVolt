<template>
    <div class="modal-mask">
        <div class="modal-wrapper">
            <div class="modal-container h-full overflow-auto">
                <slot name="content">
                    <p>Contenido a remplazar</p>
                </slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {}
</script>

<style scoped>
.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    transition: opacity 0.3s ease;
}
.modal-wrapper {
    display: table-cell;
    vertical-align: middle;
}
.modal-container {
    width: 800px;
    background-color: rgb(255, 255, 255);
    margin: 0px auto;
    padding-bottom: 40px;
    border-radius: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
}
</style>
>
