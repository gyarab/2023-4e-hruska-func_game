<template>
  <h1 class="nadpis">This is a Graf page</h1>
  <form class="funcInput">
    <div>
      <input type="text" id="textus" v-bind="funkce">
      <input type="submit" id="buttonus">
    </div>
  </form>
  <div class="grafDiv">
    <canvas class="graf" ref="graf"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
  export default {
    name: "Graf",
    props: {
      graf: Array,
      barva: String,
      jmeno: String,
    },
    mounted(){
      Chart.defaults.elements.line.cubicInterpolationMode = 'monotone';
      Chart.defaults.plugins.legend.display = false
      const grafus = new Chart(this.$refs.graf, {
        type: "line",
        data: {
          datasets: [{
            label: this.jmeno,
            data: this.data
        }],
        labels: [-500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500]
        }, 
        options: {
          scales: {
            y: {
                suggestedMin: -500,
                suggestedMax: 500
            }
          }
        }
      })
    },
    methods: {
      async calculate_x(func_str) {
        //#########################
        //convert_func(func_str)
        //zadá funkci
        //předání dál v podobě str
        //zatím eval
        //  calculate y(single input(x), předpis funkce) //pomocí zásobníku
        //for loop func přímo se strokeline fkcí
        //vykreslení grafu
        //#########################
        var arr = []
        for (let i = -500; i <= 500; i += 5){
          arr.push(eval(i, func_str));
        }
        return arr;
      },
      async draw_graph(){

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