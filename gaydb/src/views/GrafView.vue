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
            const scaleX = 1;
            const scaleY = 1;
            this.ctx.scale(scaleX, scaleY);
            this.ctx.strokeStyle = "red";
            this.ctx.lineWidth = 3;
            this.ctx.beginPath(); //kreslení grafu
            for (let i = -w/2; i < w/2; i += .1) {
                let y = eval(this.calculate_y(i, this.function_input)) // / 1
                let [grafX, grafY] = this.konvertor(i*(w/12), y*(w/12)/1.04) //1.04 - dont judge me
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
            //main axis
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.strokeStyle = "white";
            ctx.moveTo(xmin, y0); ctx.lineTo(w, y0);  // X axis
            ctx.moveTo(x0, 0); ctx.lineTo(x0, h);  // Y axis
            ctx.stroke();
            //small axis
            ctx.lineWidth = 1;
            ctx.beginPath();
            for (let i = 0; i < w; i += w/12){
                ctx.moveTo(i, 0); ctx.lineTo(i, h);
            }
            for (let i = 0; i < h; i += h/8){
                ctx.moveTo(0, i); ctx.lineTo(w, i);
            }
            ctx.stroke();

            ctxL.fillStyle = `#D3C4E3`; //levej červenej //#d67cdb //`#DCABDF`
            ctxL.fillRect(0, 0, 1000, 1500);

            ctxR.fillStyle = `#8F95D3`; //pravej modrej
            ctxR.fillRect(0, 0, 1000, 1500);
            console.log("debuuuuuuuuuuuuuug")
            console.log((w/13)/(h/9));


            console.log('axes and battlefield done');
        },
        konvertor(x, y) { //graph cords
            let y2 = (-y + this.canvas.height / 2) / 1;  
            let x2 = (x + this.canvas.width / 2) / 1;
            return [x2, y2];
        },
        calculate_y(x, func) { //FIXME;
            const replaced = func.replaceAll('x', x);
            return replaced;
            //https://mathjs.org/docs/reference/functions.html
        }
    }
}
</script>
<template>
    <div class="kontejner">
        <form class="func_input">
            <input type="text" v-model="function_input" placeholder="Insert function" class="text_input">
            <button v-on:click="draw_graph()" class="btn" type="button">submit</button>
        </form>

        <div class="graf_div">
            <canvas id="levej_graf" width="1000" height="1500"></canvas>
            <canvas id="graf" ref="graf" width="1250" height="800"></canvas>
            <canvas id="pravej_graf" width="1000" height="1500"></canvas>
        </div>
    </div>
</template>
<style>
.kontejner {
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
    width: 80%;
    border: solid 5px var(--graf-border)
}
#pravej_graf, #levej_graf {
    width: 15%;
}
#graf {
    width: 70%;
}
::placeholder {
    color: var(--seda);
}
</style>