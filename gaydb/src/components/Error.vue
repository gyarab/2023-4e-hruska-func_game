<script>
export default {
    return:{
        props: {
            errors: ["error"]
        }
    }
}
</script>

<template>
    <div id="error_kontejner">

        <p v-for="error in errors">{{ error }}</p>
    </div>
</template>

<style>
#error_kontejner {
    display: flex;
    background-color: var(--login-form-bg);
    flex-direction: column;
    align-items: center;
    font-size: 15px;
    color: white;
    align-self: flex-end;
}
</style>