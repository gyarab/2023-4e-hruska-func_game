<template>
  <h1 class="nadpis">This is a Graf page</h1>
  <div class="funcInput">
    <input type="text" v-model="function_input" placeholder="Function" id="text_input">
    <button @click="my_method" id="buttonus">submit</button>
  </div>
  
  <div class="grafDiv">
    <canvas id="graf" ref="graf"></canvas>
  </div>
</template>

<script>
  export default{
    data(){
      return{
        function_input: ""
      }
    },
    mounted(){

    },
    methods: {
      my_method(){
        const myCanvas = document.getElementById("graf"); //200 x 300 px
        const ctx = myCanvas.getContext("2d");
        ctx.strokeStyle = "red";
        ctx.font = "15px Arial";
        ctx.fillText(this.function_input, 10, 10);
        ctx.lineWidth = 3;
        ctx.rect(0,0,200,300)
        ctx.beginPath();
        ctx.moveTo(0, eval(0, this.function_input));
        for (let i = 0; i < 300; i += 1){
          ctx.lineTo(i, eval(i, this.function_input));
          ctx.moveTo(i, eval(i, this.function_input))
        }  
        console.log(eval(300, this.function_input));
        ctx.stroke();
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
  #graf {
    width: 100% !important;
    height: 100% !important;
    text-align: center;
  }
  .funcInput{
    padding: 0;
    margin: 0;
    display: flex;
    justify-content: center;
    height: auto; 
  }
  #text_input{
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