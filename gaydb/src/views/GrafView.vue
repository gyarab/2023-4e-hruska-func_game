<template>
  <h1 class="nadpis">This is a Graf page</h1>
  <form class="funcInput">
    <div>
      <input type="text" id="textus" v-model="draw_graph">
      <input type="submit" id="buttonus">
    </div>
  </form>
  <div class="grafDiv">
    <canvas class="graf" ref="graf"></canvas>
  </div>
</template>

<script>
  export default {
    mounted(){
      const canvas = document.querySelector(".graf");
      const width = (canvas.width = window.innerWidth / 3);
      const height = (canvas.height = window.innerHeight / 3);
      const ctx = canvas.getContext("2d");
    },
    methods: {
      async draw_graph(func){
        ctx.beginPath();
        ctx.moveTo(-500, 0);
        for (let i = -500; i < 500; i += 5){
          ctx.lineTo(i, eval(i, func))
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