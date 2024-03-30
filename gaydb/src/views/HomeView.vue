<template>
  <div id="home_kontejner">
    <h1 class="nadpis">This is prematch lobby</h1>
    <div id="test_server">
      <h1>Enter Lobby</h1>
      <input class="text_input" style="width: 50%" v-model="username_input" form="text" placeholder="zadejte nickname" />
      <button id="activator" v-on:click="sendMessage">PLAY ONLINE</button>
      <li v-if="server_response">Server response: {{ server_response }}</li>
    </div>
  </div>
</template>
<style scoped>

#test_server {
  display: flex;
  background-color: var(--login-form-bg);
  flex-direction: column;
  align-items: center;
  width: 60%;
  border-radius: 20px;
  gap: 0.5em;
  margin-top: 25px;
  padding: 10px;
  font-size: 2em;
}

#home_kontejner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  gap: 2em;
  padding: 20px;
}

#activator {
  padding: 5px;
  background-color: var(--func-input-bg);
  border-radius: 5px;
  border-style: none;
  color: white;
  padding: 12px;
  margin: 5px;
}
</style>

<script>
export default {
  data() {
    return {
      server_response: "",
      username_input: "",
      ws: null,
    }
  },
  mounted() {
    localStorage.removeItem("gameId")
    this.ws = new WebSocket("ws://localhost:8000/play"); 

    this.ws.onmessage = (event) => {
      let a = JSON.parse(event.data)
      console.log("[in home]", a)
      const gameStatus = a["message"];
      const gameId = a["data"];
      const whoFirst = a["who first"]
      const myName = a["nickname"]
      if (gameStatus == "new lobby" || gameStatus == "connected"){ //vytvořil nové game lobby
        localStorage.setItem("game", JSON.stringify({"game status": gameStatus, "gameId": gameId, "who first": whoFirst, "username": myName}))
        console.log("[WRITE] into localstorage: ", gameStatus, gameId, whoFirst, myName)
        this.$router.push('/graf');

      }else if (a["message"] == "chyba"){
        //něco se posralo idk co, ale teď je to wrong input - neposílám gameId / 1 / -1
        this.server_response = `${a["message"]} ${a["data"]}`
      }
    }
  },
  methods: {
    sendMessage(event) {
      this.ws.send(JSON.stringify({"message": "1", "username": this.username_input})) //chce hrát / přidat se do Q
      console.log(`[SENDING] username: ${this.username_input}`)
      event.preventDefault()
    },
  }
}
</script>
