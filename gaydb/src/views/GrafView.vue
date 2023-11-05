<template>
  <h1 class="nadpis">This is a Graf page</h1>
  <div class="funcInput">
    <input type="text" v-model="function_input" placeholder="Function" id="text_input">
    <button @click="draw_graph()" id="buttonus">submit</button>
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
    },             //FIXME vytvořit překážky - metoda
    methods: { 
      //FIXME animace po překročení canvas borderu, vytvořit logiku pro trefování protivníka
      draw_graph(){ //FIXME rozdělit do metod: calculate_y(var x), udělat global ctx / funkce vyjde z postavy hráče
        //middle var of canvas and starting point of func
        let ctx = this.ctx; let w =  this.canvas.width; let h = this.canvas.height;
        let y0 = h / 2; var x0 = w / 2;
        let xmin = 0; let xmax = w;
        let ymin = 0; let ymax = h;
        ctx.strokeStyle = "red";
        ctx.lineWidth = 0.7;
        ctx.beginPath();
        ctx.moveTo(xmin, y0 - this.calculate_y(0,this.function_input));
        ctx.moveTo(xmin,y0);
        var y;
        for (let i = xmin + 1; i < xmax; i++){ //drawing graph, FIXME - collisions with objects
          y = this.calculate_y(i,this.function_input);
          if (y > ymax || y < ymin){
            ctx.stroke()            
            return;
          }
          //console.log(y0 - y)
          ctx.lineTo(i, y0 - y);
          ctx.moveTo(i, y0 - y);
        }
        ctx.stroke();
        console.log("graph done")
      },
      draw_axes(ctx,h,w){
        //axes.scale = 10 //10 px from x to another 
        let x0 = w / 2; 
        let y0 = h / 2;  //varibles
        let xmin = 0; 
        ctx.beginPath();
        ctx.lineWidth = .05;
        ctx.strokeStyle = "white";
        ctx.moveTo(xmin,y0); ctx.lineTo(w,y0);  // X axis
        ctx.moveTo(x0,0); ctx.lineTo(x0,h);  // Y axis
        ctx.stroke();
        console.log('axes done')
      },
      calculate_y(x, func){ //FIXME
        if (func.length == 0) return;
        console.log(eval((func).replace('x',x)))
        return eval((func).replace('x',x))
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