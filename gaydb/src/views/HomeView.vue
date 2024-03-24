<template>
  <h1 class="nadpis">This is homepage</h1>
  <div id="home_kontejner">
    <div id="test_server">
      <h1>Server srandy</h1>
      <input class="text_input" id="text_server" v-model="input_data" form="text" placeholder="pošlete zprávu serveru" />
      <button id="activator" v-on:click="sendMessage">send msg to server</button>
      <li v-if="server_response">Server response: {{ server_response }}</li>
    </div>
  </div>
</template>
<style scoped>

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
export default {
  data() {
    return {
      server_response: "",
      input_data: "",
      ws: null,
    }
  },
  mounted() {
    this.ws = new WebSocket("ws://127.0.0.1:8000/"); 
    this.ws.onmessage = (event) => {
      let a = JSON.parse(event.data)
      if (a["message"] == "gameId"){
        this.server_response = `${a["message"]} ${a["data"]}`
        //poslat na /{gameId}
      }else if (a["message"] == "data"){
        //dostal jsem data a z toho se musí vykreslit graf a tak dále
        this.server_response = `${a["message"]} ${a["data"]}`
      }else if (a["message"] == "connected"){
        //připojil jsem se do probíhající sesh
        this.server_response = `${a["message"]} ${a["data"]}`
      }else if (a["message"] == "chyba"){
        //něco se posralo idk co, ale teď je to wrong input - neposílám gameId / 1 / -1
        this.server_response = `${a["message"]} ${a["data"]}`
      }
    }
  },
  methods: {
    sendMessage(event) {
      this.ws.send(this.input_data)
      console.log(`[SENDING] data: ${this.input_data}`)
      //input.value = ''
      event.preventDefault()
    },
    print_msgs(a){
      let s = ""
      for (let i = 0; i < a.length; i++){
        s += a[i] + ", "
      }
      return s
    },
    joinQue(){
      this.ws.send("-1")
    }
  }
}
</script>
