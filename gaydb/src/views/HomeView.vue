<template>
  <h1 class="nadpis">This is homepage</h1>
  <div id="home_kontejner">
    <div id="test_api">
      <h1>Beckend srandy:</h1>
      <button id="activator" v-on:click="requestData">get data</button>
      <p> Message: {{ this.api_msg }} </p>
    </div>
    <div id="test_server">
      <h1>Server srandy</h1>
      <input class="text_input" v-model="input_data" form="text" placeholder="pošlete zprávu serveru" />
      <button id="activator" v-on:click="smth_with_server">send msg to server</button>
      <p>Server response: {{ this.server_response }}</p>
    </div>
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

#test_server {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 70%;
  margin-top: 25px;
  padding: 10px;
  font-size: 2em;
  padding: 10px;
}

#home_kontejner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
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
      api_msg: "",
      server_response: "",
      input_data: "",
    }
  },
  mounted() {

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
    },
    smth_with_server() {
      const ws = new WebSocket("ws://localhost:8080");
      ws.addEventListener("open", () => {
        console.log("we are connected");
      });

      ws.addEventListener("message", (e) => {
        this.server_response = e;
      });
    }
    
  }
}
</script>
