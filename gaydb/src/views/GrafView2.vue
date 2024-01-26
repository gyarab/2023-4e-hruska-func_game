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
        this.canvas = document.getElementById("graf");
        this.canvasL = document.getElementById("levej_graf");
        this.canvasR = document.getElementById("pravej_graf");
        this.ctxL = this.canvasL.getContext("2d");
        this.ctxR = this.canvasR.getContext("2d");
        this.ctx = this.canvas.getContext("2d");
        this.draw_axes_and_field(this.ctx, this.ctxL, this.ctxR, this.canvas.height, this.canvas.width);
    },             //FIXME vytvořit překážky - metoda
    methods: {
        //FIXME animace po překročení canvas borderu, vytvořit logiku pro trefování protivníka
        draw_graph(e) {
            //e.preventDefault();
            console.log("function: " + this.function_input)
            let w = this.canvas.width;
            let h = this.canvas.height;
            this.ctx.strokeStyle = "red";
            this.ctx.lineWidth = 3;
            this.ctx.beginPath(); //kreslení grafu
            for (let i = -w / 2; i < w / 2; i += .1) {
                let y = eval(this.calculate_y(i, this.function_input))
                let [grafX, grafY] = this.konvertor(i * 10, y * 10)
                this.ctx.lineTo(grafX, grafY);
                this.ctx.moveTo(grafX, grafY);
            }
            this.ctx.stroke();
            console.log("graph done");
        },
        draw_axes_and_field(ctx, ctxL, ctxR, h, w) {
            let x0 = w / 2;
            let y0 = h / 2;  //varibles
            let xmin = 0;

            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.strokeStyle = "white";
            ctx.moveTo(xmin, y0); ctx.lineTo(w, y0);  // X axis
            ctx.moveTo(x0, 0); ctx.lineTo(x0, h);  // Y axis
            ctx.stroke();

            ctxL.fillStyle = `#DCABDF`; //levej červenej
            ctxL.fillRect(0, 0, 1000, 1500);

            ctxR.fillStyle = `#8295D9`; //pravej modrej
            ctxR.fillRect(0, 0, 1000, 1500);

            console.log('axes and battlefield done');
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
        <form class="func_input">
            <input type="text" v-model="function_input" placeholder="Insert function" id="text_input">
            <button @click="draw_graph()" id="buttonus" type="button">submit</button>
        </form>

        <div class="graf_div">
            <canvas id="levej_graf" width="1000" height="1500"></canvas>
            <canvas id="graf" ref="graf" width="1250" height="800"></canvas>
            <canvas id="pravej_graf" width="1000" height="1500"></canvas>
        </div>
    </div>
</template>
<style>
#kontejner {
    display: flex;
    flex-direction: column;
    gap: 2em;
    align-items: center;
    height: 85vh;
    width: 100%;
    padding: 20px;
}

.func_input {
    display: flex;
    flex-direction: row;
    gap: 2em;
}

.graf_div {
    display: flex;
    flex-direction: row;
    width: 100%;
}

#levej_graf {
    width: 15%;
    border-left: solid 5px var(--graf-border);
    border-top: solid 5px var(--graf-border);
    border-bottom: solid 5px var(--graf-border);
}

#pravej_graf {
    width: 15%;
    border-right: solid 5px var(--graf-border);
    border-top: solid 5px var(--graf-border);
    border-bottom: solid 5px var(--graf-border);
}

#graf {
    border-top: solid 5px var(--graf-border);
    border-bottom: solid 5px var(--graf-border);
    width: 70%;
}

#buttonus {
    color: white;
    width: 5em;
    height: 2em;
    border-radius: 5px;
    background-color: var(--func-input-bg);
    border-style: solid;
    border: none;
    cursor: pointer;
    outline: none;
}

#buttonus:hover {
    background-color: var(--btn-hover);
}

#text_input {
    color: white;   
    width: auto;
    height: 2em;
    text-align: left;
    padding-left: 10px;
    border-radius: 5px;
    border: none;
    background-color: var(--func-input-bg);
    outline: none;
}

::placeholder {
    color: var(--seda);
}

</style>