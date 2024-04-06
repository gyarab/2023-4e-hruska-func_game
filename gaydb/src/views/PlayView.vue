<template>
  <div id="home_kontejner">
    <h1 class="nadpis">This is prematch lobby</h1>
    <div id="test_server">
      <h1>Enter Lobby</h1>
      <input class="text_input" style="width: 50%" v-model="username_input" form="text" placeholder="zadejte nickname" />
      <button id="activator" v-on:click="sendMessage">HRÁT ONLINE</button>
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
#activator:hover {
  background-color: var(--btn-hover);
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
    this.clear_localstorage()
    if (!this.ws || this.ws.readyState === WebSocket.CLOSED){
      this.ws = new WebSocket("ws://localhost:8000/play"); 
      this.ws.addEventListener("message", this.my_on_message())
    }
    this.my_on_message()
  },
  /*
  beforeRouteLeave() {
    console.log("in before destroy")
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.close();
    }
  }
  */
  methods: {
    sendMessage(event) {
      if (this.ws.readyState === WebSocket.OPEN) {
        // Send message over WebSocket
        console.log(!this.username_input)
        if (!this.username_input) {
          this.username_input = localStorage.getItem("username")
        }
        this.ws.send(JSON.stringify({"message": "1", "username": this.username_input}));
        console.log(`[SENDING] username: ${this.username_input}`);
      } else {
        console.error("WebSocket connection is not open.");
      }
      event.preventDefault()
    },
    my_on_message() {
    // Handle WebSocket messages
      this.ws.onmessage = (event) => { 
        let a = JSON.parse(event.data);
        console.log("[in home]", a);
        const gameStatus = a["message"];
        const gameId = a["data"]; //just for debug
        const whoFirst = a["who first"]; //just for debug
        const myName = a["nickname"]; //just for debug
        let circles = a["circles"]
        const targets = a["targets"]
        if (whoFirst == "not you"){
          circles = this.flip_circles(circles)
        }
        if (gameStatus === "new lobby" || gameStatus =="connected"){ //vytvořil nové game lobby
          localStorage.setItem("game", JSON.stringify({"message":gameStatus, "data":gameId, "who first":whoFirst, "nickname":myName, "circles":circles, "targets": targets}));
          this.$router.push('/graf');
          /*
        } else if(gameStatus ==="connected"){
          localStorage.setItem("game", JSON.stringify({"message":gameStatus, "data":gameId, "who first":whoFirst, "nickname":myName, "circles":circles, "targets": targets}));
          this.ws.send(JSON.stringify({"message": "ready to play", "gameId": gameId}))
          */
        } else if (a["message"] === "chyba"){
          //něco se posralo idk co, ale teď je to wrong input - neposílám gameId / 1 / -1
          this.server_response = `${a["message"]} ${a["data"]}`;
        }
      }
    },
    flip_circles(circs){
      return [[circs[0][0], circs[0][1], circs[0][2]],[-circs[1][0], circs[1][1], circs[1][2]],[-circs[2][0],circs[2][1],circs[2][2]]]
    },
    clear_localstorage(){
      localStorage.removeItem("game")
    },
  }
}
</script>
