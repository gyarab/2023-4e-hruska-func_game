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
      funkce: String,
      barva: String,
      jmeno: String
    },
    mounted(){
      Chart.defaults.elements.line.cubicInterpolationMode = 'monotone';
      Chart.defaults.plugins.legend.display = false
      const grafus = new Chart(this.$refs.graf, {
        type: "line",
        data: {
          datasets: [{
            label: 'First dataset',
            data: [319, 17, 241, 21, 376, 446, 11, 60, 40, 221, 315, 278, 56, 366, 34, 245, 402, 75, 379, 367]
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
      async calculate_x(x) {
        console.log(this.funkce)
        var y = x //based on a x and function it returns the value 
        return y
      },
      
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