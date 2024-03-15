<template>
    <div class="kontejner">
      <h1>Můj účet</h1>
      <p>token: {{ token }}</p>
      <div id="items">
        <p name="userinfo" v-for="(l, d) in this.res"><b style="font-size: 1.2em;">{{ d }}:</b> <p>{{ l }}</p></p>
      </div>
      <button v-on:click="logout" class="log-out">odhlásit se</button>
    </div>
</template>
  
<script>
import axios from 'axios'
let prihlasen = false
if (localStorage.getItem("token") != null) {
  prihlasen = true
} 

export default {
  data() {
    return {
      token: "",
      token_type: "",
      res: null
    };
    
  },
  mounted() {
    this.get_token_from_storage();
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
#items {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5em;
}

p {
    max-width: 800px;
    word-wrap: break-word;
}
.log-out {
  padding: 5px;
  background-color: rgb(255, 55, 72);
  color: white;
  font-size: large;
  border-style: none;
  border-radius: 5px;
}
.log-out:hover {
  background-color: rgb(255, 0, 0);

}
</style>