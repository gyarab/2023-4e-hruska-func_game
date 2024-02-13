<template>
  <h1 class="nadpis">This is homepage</h1>
  <div id="test_api">
    <button id="activator" v-on:click="requestData">get data</button>
    <p> Message: {{ this.msg }} </p>
  </div>
</template>
<style scoped>
#test_api {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  font-size: 2em;
}

#activator {
  padding: 5px;
}
</style>

<script>
import axios from "axios";

export default {
  data() {
    return {
      msg: "",
    }
  },

  methods: {
    async requestData() {
      try {
        const response = await axios.get('http://127.0.0.1:5173/');
        console.log(response)
        this.msg = response.data.message;
      } catch (error) {
        console.error('Error fetching data:', error);
        this.msg = 'Error fetching data';
      }
    }
  }
}
</script>
