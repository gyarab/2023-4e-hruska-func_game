<template>
  <h1 class="nadpis">This is a Graf page</h1>
  <div class="funcInput">
    <input type="text" v-model="function_input" placeholder="Function" id="text_input">
    <button @click="draw_main" id="buttonus">submit</button>
  </div>
  
  <div class="grafDiv">
    <canvas id="graf" ref="graf"></canvas>
  </div>
</template>

<script>
  export default{
    data(){
      return{
        function_input: "",
        canvas: "",
        ctx: ""
      }
    },
    mounted(){
      //const canvas = document.getElementById("graf");
      this.canvas = document.getElementById("graf");
      this.ctx = this.canvas.getContext("2d");
      this.draw_axes(this.ctx, this.canvas.height, this.canvas.width);
    },
    methods: {
      draw_main(){ //FIXME rozdělit do metod: calculate_y(var x), udělat global ctx / funkce vyjde z postavy hráče
        console.log("draw_main") //FIXME animace po překročení canvas borderu, vytvořit logiku pro trefování protivníka
                    //FIXME vytvořit překážky - metoda
      },
      draw_axes(ctx,h,w){
        var axes = {};
        axes.x0 = .5*w //pixely od x0 do P[0,0]
        axes.y0 = .5*h //piexely od y0 do P[0,0]
        //axes.scale = 10 //10 px from x to another 
        var x0=axes.x0; 
        var y0=axes.y0  //varibles
        var xmin = 0; 
        console.log(xmin, y0);
        console.log(w,y0);
        ctx.beginPath();
        ctx.lineWidth = .05;
        ctx.strokeStyle = "white";
        ctx.moveTo(xmin,y0); ctx.lineTo(w,y0);  // X axis
        ctx.moveTo(x0,0); ctx.lineTo(x0,h);  // Y axis
        console.log("draw_axes")
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