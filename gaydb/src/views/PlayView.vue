<template>
  <div class="home_kontejner">
    <h1 class="nadpis">Hrát</h1>
    <div id="test_server">
      <h1 style="color: white;">Zadejte svojí přezdívku</h1>
      <input class="text_input" style="width: 50%" v-model="username_input" form="text" placeholder="zadejte přezdívku"/>
      <button id="activator" v-on:click="sendMessage">HRÁT ONLINE</button>
    </div>
  </div>
  <div class="kontejner">
    <div class="items">
        <h2 class="nadpisus" style="margin:0.3em; color: white">Jak hrát</h2>
        <p class="text">
          Cíl hry je velmi jednoduchý, ale na začátek je potřeba pochopit pár základních principů. Pro oba hráče platí, že vždy střílí z levé strany.
          Hráč má na výběr ze tří možností, odkud se začne jeho graf zobrazovat (top, mid, bottom). Pokud není hráč na tahu, tak musí vyčkat na soupeřův tah
          , který se zobrazí v modré barvě.
        </p>
        <img src="../assets/fkce.svg">
        <h2 class="nadpisus" style="margin:0.3em; color: white">Cíl hry</h2>
        <p class="text">
          Hráč má za úkol pomocí předpisu funkce trefit zelený obdélník na pravé straně. Aby to ale neměl tak jednoduché, tak se jeho graf musí vměstnat
          do požadované výšky, kterou graf nemůže překročit, a zároveň obstřelit černé kruhy uprostře hracího pole. První, který dosáhne dvou bodů vyhrává. 
          Hráč má k dispozici konstatní, lineární, kvadratické a exponencíální funkce. Hodně štěstí
        </p>
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
  padding: 10px;
  font-size: 2em;
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
  methods: {
    sendMessage(event) {
      if (this.ws.readyState === WebSocket.OPEN) {
        // Send message over WebSocket
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
          
        } else if (a["message"] === "chyba"){
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
