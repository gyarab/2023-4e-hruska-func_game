<script>

export default {
    data() {
        return {
            username: '',
            canvas: '',
            ctx: '',
            selectedOption: '',
            function_input: '',
            ws: null,
            circles: null,
            gameData: null,
        }
    },
    mounted() {
        /*
        potřebné údaje pro hru:
         -kdo hraje první - Y
         -username obou hráčů - x
         -gameId - Y
         -překážky, {[x,y,r], [x,y,r]} - x
        během hry:
         -username, gameId, func, selectedOption, 
        konec:
         -kdo vyhrál, --> close conns
        */

        //game logic data

        this.gameData = JSON.parse(localStorage.getItem("game"))
        //const gameStatus = this.gameData["message"] //
        const gameId = this.gameData["data"] //mé gameId
        //const whoFirst = this.gameData["who first"]
        const myName = this.gameData["nickname"]
        this.circles = this.gameData["circles"]
        //this.draw_circles()
        //console.log(myName) //moje jméno

        if (gameId === null){
            console.log("[ERROR] no gameID")
            this.$router.push("/ucet");
        }

        this.ws = new WebSocket("ws://localhost:8000/graf")
        //in game logic
        this.ws.onmessage = (event) =>{ //jde o data, která přišla socketem
            let a = JSON.parse(event.data)
            console.log("[in ingame logic] ", a)
            let game_id = a["gameId"]
            let func = a["func"]
            let selected = a["selected"] 
            let username = a["username"]
            console.log("[COMPARING NAMES]",myName, username)
            console.log("[PRINTING VALUES] ", selected, gameId, game_id)	//tady nevím, ale username by měl být ten, co přichází ne můj
            if (selected && gameId == game_id){
                if (username != myName){
                    let color = "blue" 
                    this.clean_canvas()
                    this.draw_circles()
                    this.draw_graph(func, selected, color)
                }
                else if(username == myName){
                    let color = "red"
                    this.clean_canvas()
                    this.draw_circles()
                    this.draw_graph(func, selected, color)
                }
            } else {
                console.log("vykuř prdel")
            }
        }

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
            if (this.selectedOption) {
                console.log(this.gameData)
                const gameId = this.gameData["data"]
                const myName = this.gameData["nickname"]
                this.ws.send(JSON.stringify({"username": myName, "gameId": gameId, "func": this.function_input, "selected": this.selectedOption}))
                console.log(`[SENDING] data: {"username": ${myName},"gameId": ${gameId}, "func": ${this.function_input}, "selected": ${this.selectedOption}}`)
            } else {
                console.log("stále kuř prdel")
            }
        },        
        draw_graph(func, selected, color) {
            //e.preventDefault();
            let w = this.canvas.width;
            let h = this.canvas.height;
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = 3;

            this.ctx.beginPath(); //kreslení grafu
            for (let i = 0; i < w; i += .1) {
                let y = eval(this.calculate_y(i, func))
                let [x1, y1] = this.konvertor(i, y, selected)
                if (this.collided(y)){
                    this.ctx.stroke();
                    if (y > this.canvas.height){
                        this.draw_collision(this.ctx, x1, 0);
                    }else if(y < -this.canvas.height/2){
                        this.draw_collision(this.ctx, i, this.canvas.height);
                    }
                    break;
                }
                let [grafX, grafY] = this.konvertor(i*(w/12)/1, y*(h/8)/1, selected) //1.04 - dont judge me
                this.ctx.lineTo(grafX, grafY);
                this.ctx.moveTo(grafX, grafY);
            }

            this.ctx.stroke();
            console.log("graph done");
        },
        draw_axes_and_field() {
            //vars
            let h = this.canvas.height; let w = this.canvas.width;
            let x0 = w / 2;
            let y0 = h / 2;
            let xmin = 0;
            //main axis
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            this.ctx.strokeStyle = "white";
            this.ctx.moveTo(xmin, y0); this.ctx.lineTo(w, y0);  // X axis
            this.ctx.moveTo(x0, 0); this.ctx.lineTo(x0, h);  // Y axis
            this.ctx.stroke();
            //small axis
            this.ctx.lineWidth = 1;
            this.ctx.beginPath();
            for (let i = 0; i < w; i += w/12){
                this.ctx.moveTo(i, 0); this.ctx.lineTo(i, h);
            }
            for (let i = 0; i < h; i += h/8){
                this.ctx.moveTo(0, i); this.ctx.lineTo(w, i);
            }
            this.ctx.stroke();
            this.draw_circles()
        },
        konvertor(x, y, selected) { //graph cords
            let y2 = (-y + this.canvas.height / 2);  
            let x2 = (x);// + this.canvas.width / 2);
            if(selected == "top"){ //top
                y2 -= this.canvas.height/4
            }else if (selected == "bottom"){ //low
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
            if (s == "top") return -2 //start +h/4, +w/4
            else if(s == "mid") return 0
            else return -1 //start -h/4, -w/4 //bottom
        },
        clean_canvas(){
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.draw_axes_and_field()
            this.draw_circles()
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
            console.log("[WHERE COLLISION] ", x,y)
            ctx.arc(x, y, 40, 0, 2 * Math.PI);
            ctx.fill()
            ctx.stroke();
        },
        draw_circles(){
            let magic_num = this.canvas.height/8 //jde o velikost jedné kostičky
            console.log("[WHERE] in draw circles")
            //console.log(this.circles[x][0], this.circles[x][1], this.circles[x][2])
            this.ctx.strokeStyle = "black"
            for (let x = 0; x < 3; x++){
                this.ctx.beginPath()
                this.ctx.arc(this.canvas.width / 2 + this.circles[x][0] * magic_num, this.canvas.height / 2 + this.circles[x][1] * magic_num, this.circles[x][2]  * magic_num, 0, 2 * Math.PI);
                //v hodnotách, jak by vypadaly na grafu, no canvas pxs
                this.ctx.fill();
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
                <input type="text" v-model="function_input" placeholder="Insert function"
                    v-bind:class="{wrong_input: !selectedOption, text_input: selectedOption}">
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
                    <!--<button v-on:click="draw_graph()" class="btn" type="button">submit</button>-->
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
.wrong_input{
    border: red solid 2px;
}

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