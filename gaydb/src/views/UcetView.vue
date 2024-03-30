<template>
    <div class="kontejner">
      <h1 class="nadpis">Můj účet</h1>
      <div id="items">
        <table class="custom-table">
          <thead>
            <tr>
              <th class="header">Key<hr></th>
              <th class="header">Value<hr></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(l, d) in this.res" :d="d">
              <td>{{ d }}</td>
              <td>{{ l }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="ucet-kontejner">
        <div class="fake-kontejner">
          <p class="pod-nadpis">Chceš si zahrát online?</p>
          <a id="wanna-play" v-bind:href="'/play'">TADY</a>
        </div>
        <div class="fake-kontejner">
          <p class="pod-nadpis">Procvičovat solo</p>
          <a id="wanna-play" v-bind:href="'/home'">TADY</a>
        </div>
      </div>
      <button v-on:click="logout" class="log-out">odhlásit se</button>
    </div>
</template>

<script>
import axios from 'axios' 
//import { prihlasen } from ''

export default {
  data() {
    return {
      token: "",
      token_type: "",
      res: null,
      prihlasen: null,
    };
    
  },
  mounted() {
    this.getMyInfo();
    this.prihlasen = true
  },
  methods: {
    get_token_from_storage() {
      if (localStorage.getItem("token")){
        return true
      }
      return false
    },
    logout(){
      localStorage.removeItem("token")
      this.prihlasen = false
      this.$router.push('/prihlaseni');
    },
    async getMyInfo(){
      try{
        console.log("[GETTING USER INFO] in get my info")
        let resp = await axios.get('/ucet', {
            headers: {
              Authorization: localStorage.getItem("token")
            }
        })
        this.res = resp.data

      }catch(e){
        //this.$router.push('/prihlaseni');
        console.log(e)
      }
    },
  }
}
</script>

<style>
.custom-table {
  
  width: 100%;
  border-collapse: collapse;
  background-color: var(--login-form-bg);
  border-radius: 10px;
}

.custom-table th,
.custom-table td {
  padding: 8px;
}

.custom-table th {
  background-color: #f2f2f2;
  text-align: left;
}

.custom-table td {
  text-align: left;
}

.custom-table th.header {
  font-weight: bold;
}

.header {
  color: black;
  text-align: center;
}

tr {
  color: var(--bila-soft);
}

.fake-kontejner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.23em;
  height: 25vh;
  border-radius: 25px;
  width: 65%;
  padding: 5px;
  background-color: var(--login-form-bg);
  border: 1px solid white;
}

#items {
  display: flex;
  height: 75vh;
  gap: 0.5em;
  padding: 10px;
  background-color: var(--login-form-bg);
  border-radius: 25px;
  width: 65%;
  border: 1px solid white;
}

#wanna-play{
  flex-direction: column;
  font-size: 2em;
  align-items: center;
  text-decoration: none;
  color: white;
  padding: 7px;
  background-color: var(--func-input-bg);
  border-radius: 10px;
  border: solid 1px white;
}

p {
    max-width: 800px;
    word-wrap: break-word;
}
.log-out {
  padding: 5px;
  background-color: rgb(255, 0, 21);
  color: white;
  font-size: 1.5em;
  border-style: none;
  border-radius: 5px;
}
.log-out:hover {
  background-color: rgb(255, 0, 0);
}
</style>