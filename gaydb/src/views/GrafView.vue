<script>

export default {
    data() {
        return {
            function_input: "",
            canvas: "",
            ctx: "",
            textInput: '',
            selectedOption: '',
            ws: null,
        }
    },
    mounted() {
        const gameId = localStorage.getItem("gameId")
        if (gameId === null){
            console.log("no gameID")
            this.$router.push("/home");
        }

        this.ws = new WebSocket("ws://localhost:8000/graf")

        this.canvas = document.getElementById("graf");
        this.canvasL = document.getElementById("levej_graf");
        this.canvasR = document.getElementById("pravej_graf");
        this.ctx = this.canvas.getContext("2d");
        this.ctxL = this.canvasL.getContext("2d");
        this.ctxR = this.canvasR.getContext("2d");
        this.draw_left_and_right_canvas(this.ctxL, this.ctxR)
        this.draw_axes_and_field(this.ctx);
    }, 
    methods: {
        //FIXME animace po překročení canvas borderu, vytvořit logiku pro trefování protivníka
        sendMessage() {
            const gameId = localStorage.getItem("gameId")
            this.ws.send(JSON.stringify({"gameId": gameId, "func": this.function_input}))
            console.log(`[SENDING] data: {"gameId": ${gameId}, "func": ${this.function_input}`)
        },        
        draw_graph(e) {
            //e.preventDefault();
            let w = this.canvas.width;
            let h = this.canvas.height;
            this.ctx.strokeStyle = "red";
            this.ctx.lineWidth = 3;

            this.ctx.beginPath(); //kreslení grafu
            for (let i = 0; i < w; i += .1) {
                let y = eval(this.calculate_y(i, this.function_input))
                let [x1, y1] = this.konvertor(i, y)
                if (this.collided(y)){
                    this.ctx.stroke();
                    if (y > this.canvas.height){
                        this.draw_collision(this.ctx, x1, 0);
                    }else if(y < -this.canvas.height/2){
                        this.draw_collision(this.ctx, i, this.canvas.height);
                    }
                    break;
                }
                let [grafX, grafY] = this.konvertor(i*(w/12)/1.04, y*(h/8)/1.04) //1.04 - dont judge me
                this.ctx.lineTo(grafX, grafY);
                this.ctx.moveTo(grafX, grafY);
            }

            this.ctx.stroke();
            console.log("graph done");
        },
        draw_axes_and_field(ctx) {
            //vars
            let h = this.canvas.height; let w = this.canvas.width;
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
        },
        konvertor(x, y) { //graph cords
            let y2 = (-y + this.canvas.height / 2);  
            let x2 = (x);// + this.canvas.width / 2);
            if(this.get_lowering_gradient(this.selectedOption) == -2){
                y2 -= this.canvas.height/4
            }else if (this.get_lowering_gradient(this.selectedOption) == -1){
                y2 += this.canvas.height/4
            }
            return [x2, y2];
        },
        calculate_y(x, func) { //FIXME;
            const replaced = func.replaceAll('x', x);
            return replaced;
            //https://mathjs.org/docs/reference/functions.html
        },
        get_lowering_gradient(s){
            //mid default
            if (s == "top") return -2 //start +h/4, +w/4
            else if(s == "mid") return 0
            else return -1 //start -h/4, -w/4 //bottom
        },
        clean_canvas(ctx){
            //ctx.clearRect(0,0,ctx.width, ctx.height)
            ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.draw_axes_and_field(ctx)
        },
        draw_left_and_right_canvas(ctxL, ctxR){
            //left canvas rect / lines
            let h = this.canvasL.height; let w = this.canvasL.width;
            let ctxs = [ctxL, ctxR]
            for (let x = 0; x < 2; x++){
                if(!x){ //nebudu to prohazovat
                    ctxs[x].fillStyle = `#D3C4E3`; //levej canvas
                    ctxs[x].strokeStyle = "red";
                }else{
                    ctxs[x].fillStyle = `#8F95D3`; //pravej canvas
                    ctxs[x].strokeStyle = "blue";
                }

                ctxs[x].fillRect(0, 0, 1000, 1500);
                ctxs[x].lineWidth = 5;
                for (let i = 1; i < 4; i++){
                    ctxs[x].beginPath();
                    ctxs[x].moveTo(0, i*h/4);
                    ctxs[x].lineTo(w, i*h/4);
                    ctxs[x].stroke();   
                }
            }
        },
        collided(y){
            if (y > this.canvas.height || y < -this.canvas.height/2){
                return true;
            }
            return false
        },
        draw_collision(ctx, x, y){
            ctx.beginPath();
            ctx.strokeStyle = "red"
            ctx.fillStyle = "red"
            console.log(x,y)
            ctx.arc(x, y, 40, 0, 2 * Math.PI);
            ctx.fill()
            ctx.stroke();
            console.log("collision made")
        },
        send_message() {
            this.ws.onmessage = function(){
                var message = this.function_input;
                console.log(message)
                this.ws.send(message)
            }
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
                <legend>Insert func and choose startig point:</legend>
                    <div id="singles">
                        <label>
                            <input type="radio" v-model="selectedOption" value="top"><br>
                            Top
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" v-model="selectedOption" value="mid">
                            mid
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" v-model="selectedOption" value="bottom">
                            Bottom
                        </label>
                    </div>
                    <button v-on:click="draw_graph()" class="btn" type="button">submit</button>
                    <button v-on:click="sendMessage()" class="btn" type="button">send message</button>
                </fieldset>
            </div>
        </form>
        <button class="btn" v-on:click="clean_canvas(this.ctx)">Clean canvas</button>
            

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