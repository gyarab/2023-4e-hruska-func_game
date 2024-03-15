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
      <input class="text_input" id="text_server" v-model="input_data" form="text" placeholder="pošlete zprávu serveru" />
      <button id="activator" v-on:click="sendMsg">send msg to server</button>
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
let socket = new WebSocket("ws://localhost:8080");

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
    async requestData() { //test api
      try {
        const response = await axios.get('/');
        console.log(`[response] ${response}`)
        this.api_msg = response.data.message;
      } catch (error) {
        console.error('Error fetching data:', error);
        this.api_msg = 'Error fetching data';
      }
    },
    connectToServer() { //test server
      socket.onopen = function(e) {
        socket.send("Connection to the server from vue")
      }
      socket.onclose = function(event) {
        if (event.wasClean) {
          console.log(`[Frontend] clean conn close, code= ${event.code}`)
        } else {
          console.log(`[Frontend] conn died`)
        }
      }

      socket.onerror = function(error) {
        console.log(`[Frontend] error: ${error}`)
      }
      socket.addEventListener("mesasge", (message) => {
        console.log(`[Frontend] displaying data from server ${message.data}`)
        this.server_response = message.data;
      });

    },
    sendMsg() { //test server
      this.connectToServer();
      
      const msg = {
        type: "message",
        text: document.getElementById("text_server").value,
      }
      console.log(`[Frontend] displaying sended data: ${msg.text}`)
      socket.send(msg.text);

      socket.onmessage = (event) => {
        this.server_response = event.data
      }
    }
    
  }
}
</script>
