<template>
    <div class="kontejner">
      <h1 class="nadpis">Můj účet</h1>
      <div id="items">
        <table>
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
      <div class="fake-kontejner">
        <p class="pod-nadpis">Chceš si zahrát online?</p>
        <a id="wanna-play" v-bind:href="'/play'">TADY</a>
      </div>
      <button v-on:click="logout" class="log-out">odhlásit se</button>
    </div>s
</template>

<script>
import axios from 'axios' 

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
    this.prihlasen = false
    if (this.get_token_from_storage()){
      this.prihlasen = true
    }
    this.getMyInfo();
  },
  methods: {
    get_token_from_storage() {
      // Retrieve token details from localStorage
      this.token = localStorage.getItem("token") || "";
    },
    logout(){
      localStorage.removeItem("token")
      this.prihlasen = false
      this.$router.push('/prihlaseni');
    },
    async getMyInfo(){
      try{
        console.log("in get my info")
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
th, td {
  padding-top: 5px;
  padding-left: 15px;
  font-size: 1.2em;
  color: var(--bila-soft);
}

.header {
  padding: 10px;
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
}

#items {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 0.5em;
  padding: 10px;
  background-color: var(--login-form-bg);
  border-radius: 25px;
  width: 65%;
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