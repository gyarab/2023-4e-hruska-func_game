<script>

export default {
    data() {
        return {
            function_input: "",
            canvas: "",
            ctx: "",
            textInput: '',
            selectedOption: ''
        }
    },
    mounted() {
        this.canvas = document.getElementById("graf");
        this.canvasL = document.getElementById("levej_graf");
        this.canvasR = document.getElementById("pravej_graf");
        this.ctx = this.canvas.getContext("2d");
        this.ctxL = this.canvasL.getContext("2d");
        this.ctxR = this.canvasR.getContext("2d");
        this.draw_axes_and_field(this.ctx, this.ctxL, this.ctxR);
    },             //FIXME vytvořit překážky - metoda
    methods: {
        //FIXME animace po překročení canvas borderu, vytvořit logiku pro trefování protivníka
        draw_graph(e) {
            //e.preventDefault();
            const lower_it_man = this.get_lowering_gradient(this.selectedOption)
            let w = this.canvas.width;
            let h = this.canvas.height;
            //const scaleX = 1;
            //const scaleY = 1;
            //this.ctx.scale(scaleX, scaleY);
            this.ctx.strokeStyle = "red";
            this.ctx.lineWidth = 3;

            this.ctx.beginPath(); //kreslení grafu
            for (let i = -w/2; i < w/2; i += .1) {
                let y = eval(this.calculate_y(i, this.function_input))
                let [grafX, grafY] = this.konvertor(i*(w/12)/1.04 + w*lower_it_man, y*(h/8)/1.04 + h*lower_it_man) //1.04 - dont judge me
                this.ctx.lineTo(grafX, grafY);
                this.ctx.moveTo(grafX, grafY);
            }

            this.ctx.stroke();
            console.log("graph done");
        },
        draw_axes_and_field(ctx, ctxL, ctxR) {
            //vars
            let h = this.canvas.height; let w = this.canvas.width;
            let hL = this.canvasL.height; let wL = this.canvasL.width;
            let hR = this.canvasR.height; let wR = this.canvasR.width
            let x0 = w / 2;
            let y0 = h / 2;
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
            //left canvas rect / lines
            ctxL.fillStyle = `#D3C4E3`; //levej červenej //#d67cdb //`#DCABDF`
            ctxL.fillRect(0, 0, 1000, 1500);
            ctxL.lineWidth = 5;
            ctxL.strokeStyle = "red";
            for (let i = 1; i < 4; i++){
                ctxL.beginPath();
                ctxL.moveTo(0, i*hL/4);
                ctxL.lineTo(wL, i*hL/4);
                ctxL.stroke();   
            }
            //right canvas rect / lines
            ctxR.fillStyle = `#8F95D3`; //pravej modrej
            ctxR.fillRect(0, 0, 1000, 1500);
            ctxR.lineWidth = 5;
            ctxR.strokeStyle = "blue";
            for (let i = 1; i < 4; i++){
                ctxR.beginPath();
                ctxR.moveTo(0, i*hL/4);
                ctxR.lineTo(wL, i*hL/4);
                ctxR.stroke();   
            }

            console.log('[AXES] done...');
        },
        konvertor(x, y) { //graph cords
            let y2 = (-y + this.canvas.height / 2);  
            let x2 = (x + this.canvas.width / 2);
            return [x2, y2];
        },
        calculate_y(x, func) { //FIXME;
            const replaced = func.replaceAll('x', x);
            return replaced;
            //https://mathjs.org/docs/reference/functions.html
        },
        get_lowering_gradient(s){
            if (s == "top") return -2 //start +h/4, +w/4
            else if (s == "bottom") return -1 //start -h/4, -w/4
            else return 0 //start 0*h/2, 0*w/2
        }
    }
}
</script>
<template>
    <div class="kontejner">
        <form class="func_input">
            <div class="radio_kontejner">
            <fieldset id="radios">
                <input type="text" v-model="function_input" placeholder="Insert function" class="text_input">
                <legend>Choose an option:</legend>
                    <div id="singles">
                        <label>
                            <input type="radio" v-model="selectedOption" value="top"><br>
                            Top
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" v-model="selectedOption" value="mid">
                            Mid
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" v-model="selectedOption" value="bottom">
                            Bottom
                        </label>
                    </div>
                    <button v-on:click="draw_graph()" class="btn" type="button">submit</button>
                </fieldset>
            </div>
        </form>
            

        <div class="graf_div">
            <canvas id="levej_graf" width="1000" height="1500"></canvas>
            <canvas id="graf" ref="graf" width="1250" height="800"></canvas>
            <canvas id="pravej_graf" width="1000" height="1500"></canvas>
        </div>
    </div>
</template>
<style>
.radio-kontejner {
    display: flex; 
    justify-content: center;
}

legend {
    font-size: 1.2em;
    color: #fff;
    padding: 3px 6px;
}

input {
    margin: 0.4em;
}

#radios{
    display: flex;
    gap: 0.2em;
    flex-direction: row;
    margin: 5px;
    border: none;
}
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