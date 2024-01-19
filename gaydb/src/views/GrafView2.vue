<script>

export default {
    data() {
        return {
            function_input: "",
            canvas: "",
            ctx: ""
        }
    },
    mounted() {
        //const canvas = document.getElementById("graf");
        this.canvas = document.getElementById("graf");
        this.ctx = this.canvas.getContext("2d");
        this.draw_axes(this.ctx, this.canvas.height, this.canvas.width);
    },             //FIXME vytvořit překážky - metoda
    methods: {
        //FIXME animace po překročení canvas borderu, vytvořit logiku pro trefování protivníka
        draw_graph() {
            console.log("function: " + this.function_input)
            let w = this.canvas.width;
            let h = this.canvas.height;
            this.ctx.strokeStyle = "red";
            this.ctx.lineWidth = 3;
            this.ctx.beginPath(); //kreslení grafu
            var y;
            for (let i = -w/2; i < w/2; i += 1) {
                y = eval(this.calculate_y(i, this.function_input))
                let [grafX, grafY] = this.konvertor(i, y)
                console.log(grafX, grafY)
                this.ctx.lineTo(grafX, grafY);
                this.ctx.moveTo(grafX, grafY);
            }
            this.ctx.stroke();
            console.log("graph done");
        },
        draw_axes(ctx, h, w) {
            let x0 = w / 2;
            let y0 = h / 2;  //varibles
            let xmin = 0;
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.strokeStyle = "white";
            ctx.moveTo(xmin, y0); ctx.lineTo(w, y0);  // X axis
            ctx.moveTo(x0, 0); ctx.lineTo(x0, h);  // Y axis
            ctx.stroke();
            console.log('axes done')
        },
        konvertor(x, y) { //graph cords
            let y2 = -y + this.canvas.height / 2;
            let x2 = x + this.canvas.width / 2;
            return [x2, y2];
        },
        calculate_y(x, func) { //FIXME;
            const replaced = func.replaceAll('x', x);
            return replaced;
        }
    }
}
</script>
<template>
    <div id="kontejner">
        <form class="funcInput">
            <input type="text" v-model="function_input" placeholder="Function" id="text_input">
            <button @click="draw_graph()" id="buttonus" type="button">submit</button>
        </form>

        <div class="grafDiv">
            <canvas id="levejGraf" width="1000" height="1500"></canvas>
            <canvas id="graf" ref="graf" width="2500" height="1600"></canvas>
            <canvas id="pravejGraf" width="1000" height="1500"></canvas>
        </div>
    </div>
</template>
<style>
#kontejner {
    display: flex;
    flex-direction: column;
    gap: 5em;
    width: 100%;
    align-items: center;
}

.funcInput {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1em;
}

.grafDiv {
    display: flex;
}

#levejGraf,
#pravejGraf {
    width: 15%;
}


#graf {
    border: solid 1px red;
    width: 70%;
}

#buttonus {
    width: 5em;
    height: 2em;
}

#text_input {
    height: 2em;
}
</style>