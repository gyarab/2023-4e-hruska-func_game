<template>
  <h1 class="nadpis">This is a Graf page</h1>
  <div class="grafDiv">
    <canvas class="graf" ref="graf"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
  export default {
    name: "Graf",
    props: {
      funkce: Array,
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
</style>