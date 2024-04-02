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
            flip: null,
            targets_num: 0, //pokud trefím, tak se číslo nyvýší
            myname: null,
        }
    },
    mounted() {
        //game logic data

        this.gameData = JSON.parse(localStorage.getItem("game"))
        //const gameStatus = this.gameData["message"]
        //console.log(this.gameData)
        const gameId = this.gameData["data"] //mé gameId
        const whoFirst = this.gameData["who first"]
        //console.log(`[TARGETS] ${targets}`)
        if (whoFirst == "not you"){ //nezačínáš, tak flipuješ
            this.flip = true
        }else{
            this.flip = false
        }
        const myName = this.gameData["nickname"]
        this.myname = myName
        this.circles = this.gameData["circles"]

        if (gameId === null){
            console.log("[ERROR] no gameID")
            this.$router.push("/ucet");
        }

        this.ws = new WebSocket("ws://localhost:8000/graf")
        //in game logic
        this.ws.onmessage = (event) =>{ //jde o data, která přišla socketem
            let a = JSON.parse(event.data)
            console.log(`[RECEIVED DATA] ${a}`)
            console.log(a)
            let game_id = a["gameId"]
            let func = a["func"]
            let selected = a["selected"] 
            this.selectedOption = selected
            this.username = a["username"]
            let username = this.username
            //console.log(`[PRINTING] my vars: myName: ${myName}, gameId: ${gameId}`)
            //console.log(`[PRINTING] incoming vars: username: ${username}, game_id: ${game_id} selected: ${selected} func: ${func}`)
            if (selected && (gameId == game_id)){
                if (username != myName){ //!=
                    console.log("[DEBUGINGAME] not equal names")
                    let color = "blue"
                    this.clean_canvas()
                    this.draw_graph(func, selected, color)
                    this.draw_circles()
                }
                else if(username == myName){ //==
                    console.log("[DEBUGINGAME] equal names")
                    let color = "red"
                    this.clean_canvas()
                    this.draw_graph(func, selected, color)
                    this.draw_circles()
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
        sendMessage() {
            if (this.selectedOption && this.function_input) {
                const gameId = this.gameData["data"]
                const myName = this.gameData["nickname"]
                this.ws.send(JSON.stringify({"username": myName, "gameId": gameId, "func": this.function_input, "selected": this.selectedOption}))
                console.log(`[SENDING] data: {"username": ${myName},"gameId": ${gameId}, "func": ${this.function_input}, "selected": ${this.selectedOption}}`)
            } else {
                console.log("stále kuř prdel")
            }
        },        
        draw_graph(func, selected, color) {
            //var - video assistant ref
            let w = this.canvas.width;
            let h = this.canvas.height;
            this.ctx.lineWidth = 3;
            this.ctx.strokeStyle = color
            //drawing logic
            //kreslení pro opponenta
            if (color == "blue"){
                this.ctx.translate(this.canvas.width, 0);
                this.ctx.scale(-1,1)
            }
            this.ctx.strokeStyle = color;
            this.ctx.beginPath(); //kreslení grafu
            for (let i = 0; i < w; i += 0.1) {
                let y = eval(this.calculate_y(i, func))
                let [grafX, grafY] = this.konvertor(i * (w / 12), y * (h / 8), selected);
                //console.log(grafX/100, grafY/100)
                if (this.collided(y)){
                    console.log(`[Y COLLIDED] x: ${i}, y: ${y}`)
                    this.ctx.stroke();
                    break;
                }
                if (this.circle_collision(i/10, y)){
                    console.log(`[CIRCLE COLLIDED] idk where`)
                    this.ctx.stroke();
                }
               this.ctx.lineTo(grafX, grafY);
               this.ctx.moveTo(grafX, grafY); 
            }
            if (this.hit_target(func)){
                this.targets_num += 1 //score
                this.draw_left_and_right_canvas(this.ctxL, this.ctxR)
            }
            this.ctx.stroke();
            if (color == "blue"){
                this.ctx.translate(this.canvas.width, 0);
                this.ctx.scale(-1,1)
            }
            this.check_win()
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
            let y2 = (-y + this.canvas.height / 2);  //0,0 --> 0,h/2, 
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
            let ctxs = [ctxL, ctxR]
            let h = this.canvasL.height; let w = this.canvasL.width;

            for (let x = 0; x < 2; x++){
                if(!x){ //nebudu to prohazovat
                    ctxs[x].fillStyle = `#D3C4E3`; //levej canvas
                    ctxs[x].strokeStyle = "red";
                }else{
                    ctxs[x].fillStyle = `#8F95D3`; //pravej canvas
                    ctxs[x].strokeStyle = "blue";
                }
                ctxs[x].fillRect(0, 0, 1000, 1500);
                ctxs[x].lineWidth = 6;
                for (let i = 1; i < 4; i++){
                    ctxs[x].beginPath();
                    ctxs[x].moveTo(0, i*h/4);
                    ctxs[x].lineTo(w, i*h/4);
                    ctxs[x].stroke();   
                }
            }
            ctxs[1].fillStyle = `#87E752`
            ctxs[0].fillStyle = `#87E752`
            ctxs[1].fillRect(0, h / 4 * (this.gameData["targets"][this.targets_num] - 1), w, h / 4)
            ctxs[0].fillRect(0, h / 4 * (4 - (this.gameData["targets"][this.targets_num])), w, h / 4)
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
            ctx.arc(x, y, 40, 0, 2 * Math.PI);
            ctx.fill()
            ctx.stroke();
        },
        draw_circles(){
            let magic_num = this.canvas.height/8 //jde o velikost jedné kostičky
            //console.log(this.circles[x][0], this.circles[x][1], this.circles[x][2])
            this.ctx.strokeStyle = "black"
            for (let x = 0; x < 3; x++){
                this.ctx.beginPath()
                this.ctx.arc(this.canvas.width / 2 + this.circles[x][0] * magic_num, this.canvas.height / 2 + this.circles[x][1] * magic_num, this.circles[x][2]  * magic_num, 0, 2 * Math.PI);
                //v hodnotách, jak by vypadaly na grafu, no canvas pxs
                this.ctx.fill();
            }
        },
        circle_collision(x, y) {
            let magic_num = this.canvas.height / 8
            console.log(x, y)
            if (x < -4 || x > 4|| y > 4 || y < -4){
                return false
            }
            console.log(this.circles[1][0], this.circles[1][1])
            for (let i = 0; i < 3; i++) {
                //console.log(Math.sqrt(Math.pow(x - this.canvas.width / 2 + this.circles[i][0] * magic_num, 2) + Math.pow(y - this.canvas.height / 2 + this.circles[i][1] * magic_num, 2)))
                let distance = Math.sqrt(Math.pow(x - this.circles[i][0], 2) + Math.pow(y - this.circles[i][1], 2));
                console.log(distance)
                if (distance < 1) {
                    return true; 
                }
            }
            return false;
        },
        hit_target(func){
            let target_bottom = null;
            let target_top = null;
            if (this.gameData["targets"][this.targets_num] == 1){
                //console.log(`[TARGET] vrchní`)
                target_bottom = 2
                target_top = 4
            } else if (this.gameData["targets"][this.targets_num] == 2) {
                //console.log(`[TARGET] vrchní - 1`)
                target_bottom = 0
                target_top = 2
            } else if (this.gameData["targets"][this.targets_num] == 3) {
                //console.log(`[TARGET] spodní + 1`)
                target_bottom = -2
                target_top = 0
            } else if (this.gameData["targets"][this.targets_num] == 4) {
                //console.log(`[TARGET] spodní`)
                target_bottom = -4
                target_top = -2
            }
            let y = eval(this.calculate_y(12, func))
            if (this.gameData["nickname"] != this.username){
                console.log("in this.gameData[nickname] != this.username")
                if(this.selectedOption == "top"){ //top
                    y += 2
                }else if (this.selectedOption == "bottom"){ //low
                    y -= 2
                }
                let  m = target_top
                target_top = -target_bottom
                target_bottom = -m
            } else {
                console.log("in } else {")
                if(this.selectedOption == "top"){ //top
                    y += 2
                }else if (this.selectedOption == "bottom"){ //low
                    y -= 2
                }
            }
            console.log(`[DEBUG in hit] y: ${y}, target_bottom: ${target_bottom}, target_top: ${target_top}`)
            if (y > target_bottom && y < target_top){
                console.log(`[well yeah collided] [${12}, ${y}]`)
                return true
            }
            return false
        },
        check_win(){
            console.log("in check win")
            if (this.targets_num == 3){
                console.log("konec")
                this.$router.push("/play");
            }
        }
    }
}
</script>
<template>
    <div class="kontejner">
        <form class="func_input">
            <div class="radio_kontejner">
            <fieldset v-if="username" id="radios">
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
        <div v-if="username" class="scoreboard">
            <div>
                <h2>Moje statistiky:</h2>
                <br>
                {{ this.gameData["nickname"] }}
                {{ this.targets_num }}
            </div>
            <div>
                Statistiky soupeře:
                <br>
                {{ this.username }}
                {{ this.targets_num }}
            </div>
        </div>
        <div v-else><h1>Čekání na protihráče...</h1></div>
        <div class="graf_div">
            <canvas id="levej_graf" width="1000" height="1500"></canvas>
            <canvas id="graf" ref="graf" width="1250" height="800"></canvas>
            <canvas id="pravej_graf" width="1000" height="1500"></canvas>
        </div>
    </div>
</template>
<style>
.scoreboard {
    display: flex;
    justify-content: space-between;
    width: 75%;
}

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