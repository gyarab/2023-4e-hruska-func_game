<template>
  <h1 class="nadpis">This is homepage</h1>
  <div id="home_kontejner">
    <div id="test_server">
      <h1>Server srandy</h1>
      <input class="text_input" id="text_server" v-model="input_data" form="text" placeholder="pošlete zprávu serveru" />
      <button id="activator" v-on:click="sendMessage">send msg to server</button>
      <p v-for="s in server_response">Server response: {{ s }}</p>
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
      server_response: [],
      input_data: "",
      ws: null,
    }
  },
  mounted() {
    this.ws = new WebSocket("ws://127.0.0.1:8000/"); 
    this.ws.onmessage = (event) => {
      let a = JSON.parse(event.data)
      console.log(a.data)
      this.server_response = a.data
      console.log(this.print_msgs(this.server_response))
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
    }
  }
}
</script>
