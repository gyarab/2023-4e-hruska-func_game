<template>
  <h1 class="nadpis">This is a Graf page</h1>
  <form class="funcInput">
    <div id="app">
      <input type="text" :value="myInput" placeholder="Function" id="textus" @input="get_value">
      <button @click="submit" id="buttonus">Submit</button>
    </div>
  </form>
  <div class="grafDiv">
    <canvas class="graf" ref="graf"></canvas>
  </div>
</template>

<script>
  export default{
    data(){
      return{
        myInput: ""
      }
    },
    mounted(){
      const canvas = document.querySelector(".graf");
      const width = (canvas.width = window.innerWidth / 3);
      const height = (canvas.height = window.innerHeight / 3);
      const ctx = canvas.getContext("2d");
    },
    methods: {
      submit(){

      },
      get_value(){
        this.myInput = event.target.value
        return this.myInput
      },
      draw_graph(){
        var func = this.get_value()
        console.log(func)
        const ctx = canvas.getContext("2d");
        ctx.beginPath();
        ctx.moveTo(-500, eval(-500, func));
        for (let i = -495; i < 500; i += 5){
          ctx.lineTo(i, eval(i, func));
        }  
        ctx.fill();
      }
    }
  }
</script>
<style>
  .grafDiv{
    display: flex;
    justify-content: center;
    border: solid red 1px;
    width: 80em;
    height: 100%;
    padding-left: 0;
    padding-right: 0;
    margin-top: 30px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 30px;
    display: block;
  }
  .graf {
    width: 100% !important;
    height: 100% !important;
    text-align: center;
  }
  .funcInput{
    padding: 10px;
    margin: 10px;
    display: flex;
    justify-content: center;
    height: auto; 
  }
  #textus{
    border-radius: 10px;
    border: solid 1px white;
    margin: 7px;
    height: 30px;
    background-color: lightgray;
    padding: 5px;
  }
  #buttonus{
    border-radius: 10px;
    border: solid 1px white;
    margin: 7px;
    height: 30px;
    background-color: var(--seda-color);
    font-size: 15px;
    padding: 5px;
    color: black;
    font-weight: bold;
  }
</style>