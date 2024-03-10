<template>
    <div class="kontejner">
      <h1>Můj účet</h1>
      <p>token_type: {{ token_type }}</p>
      <p>token: {{ token }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        token: "",
        token_type: "",
      };
    },
    mounted() {
      this.get_token_from_storage();
    },
    methods: {
      get_token_from_storage() {
        // Retrieve token details from localStorage
        this.token_type = localStorage.getItem("token_type") || "";
        this.token = localStorage.getItem("token") || "";
      },
    },
  };
  </script>

<style>
p {
    max-width: 800px;
    word-wrap: break-word;
}
</style>