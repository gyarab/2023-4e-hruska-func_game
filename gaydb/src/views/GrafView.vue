<script>

export default {
    data() {
        return {
            username: '', //příchozí jméno od serveru
            canvas: '',
            ctx: '',
            selectedOption: '',
            function_input: '',
            ws: null, //websocket
            circles: null, //překážky
            canvas_circles: [[0,0,0],[0,0,0],[0,0,0]], //circles souřadnice přepočítané na canvas pixely
            gameData: null, //data z local storage
            flip: null, //jeden z hráčů permanentně flipuje canvas
            targets_num: 0, //pokud trefím, tak se číslo nyvýší
            gameLogic: {
                myscore: 0, 
                hisscore: 0,
                ready: null, //jsem ready na hru
                gameready: null, //oba hráči jsou ready na hru
                myname: null, //myname ve hře
                hisname: null, //jeho jméno ve hře
                myturn: null, //jsem na řadě
            }
        }
    },
    mounted() {
        //game logic data

        this.gameData = JSON.parse(localStorage.getItem("game"))
        //const gameStatus = this.gameData["message"]
        const gameId = this.gameData["data"] //mé gameId
        const whoFirst = this.gameData["who first"]
        if (whoFirst == "not you"){ //nezačínáš, tak flipuješ
            this.flip = true
            this.gameLogic.myturn = false
        }else{
            this.flip = false
            this.gameLogic.myturn = true
        }
        const myName = this.gameData["nickname"]
        this.gameLogic.myname = myName
        this.circles = this.gameData["circles"]

        if (gameId === null){
            this.$router.push("/ucet"); //back to the lobby
        }

        this.ws = new WebSocket("ws://localhost:8000/graf")
        //in game logic
        this.ws.onmessage = (event) =>{ //jde o data, která přišla socketem
            //print(event.data)
            if (event.data == "ready to play"){
                this.gameLogic.gameready = true
            } else {
                let a = JSON.parse(event.data)
                console.log(`[RECEIVED DATA] ${a}`)
                let game_id = a["gameId"]
                let func = a["func"]
                let selected = a["selected"] 
                this.selectedOption = selected
                this.username = a["username"]

                if (selected && (gameId == game_id)){
                    if (this.username != myName){ 
                        this.gameLogic.hisname = this.username
                        //console.log("this.username != myName",this.username, this.gameLogic.myname, this.gameLogic.hisname)
                        //console.log("[DEBUGINGAME] not equal names")
                        let color = "blue"
                        this.clean_canvas()
                        this.draw_circles()
                        this.flip_my_turn()
                        this.draw_graph(func, selected, color)
                    }
                    else if(this.username == myName){ 
                        //console.log("this.username == myName",this.username, this.gameLogic.myname, this.gameLogic.hisname)
                        //console.log("[DEBUGINGAME] equal names")
                        let color = "red"
                        this.clean_canvas()
                        this.draw_circles()
                        this.draw_graph(func, selected, color)
                        this.flip_my_turn()
                    }
                } else {
                    console.log("error")
                }
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
            if (!this.gameLogic.myturn || !this.function_input || !this.selectedOption){
                console.log(`[PROBLEM] worng input data`)
            }
            if (this.selectedOption && this.function_input) {
                const gameId = this.gameData["data"]
                const myName = this.gameData["nickname"]
                this.ws.send(JSON.stringify({"username": myName, "gameId": gameId, "func": this.function_input, "selected": this.selectedOption}))
                console.log(`[SENDING] data: {"username": ${myName},"gameId": ${gameId}, "func": ${this.function_input}, "selected": ${this.selectedOption}}`)
            } else {
                console.log("problém")
            }
        },        
        draw_graph(func, selected, color) {
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
            let naboural = false
            for (let i = 0; i < w; i += 0.1) {
                let y = eval(this.calculate_y(i, func))
                let [grafX, grafY] = this.konvertor(i * (w / 12), y * (h / 8), selected);
                /*
                if (this.collided(y)){
                    console.log(`[Y COLLIDED] x: ${i}, y: ${y}`)
                    this.ctx.stroke();
                    break;
                }
                */
                console.log("koule")
                if (this.circle_collision(grafX, grafY, color=='blue')){ // i,y --> logic-asi, //grafx, grafy --> canvasove
                    console.log(`[CIRCLE COLLIDED] in x: ${grafX}, y: ${grafY}`)
                    naboural = true
                    break;
                } 
                this.ctx.lineTo(grafX, grafY);
                this.ctx.moveTo(grafX, grafY); 

            }

            this.ctx.stroke();

            if (!naboural && this.hit_target(func)){
                this.targets_num += 1 //score
                this.draw_left_and_right_canvas(this.ctxL, this.ctxR)
            }
            
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
        draw_circles(){
            let magic_num = this.canvas.height/8 //jde o velikost jedné kostičky
            this.ctx.strokeStyle = "black"
            for (let i = 0; i < 3; i++){
                this.ctx.beginPath()
                this.ctx.arc(this.canvas.width / 2 + this.circles[i][0] * magic_num, this.canvas.height / 2 + this.circles[i][1] * magic_num, this.circles[i][2]  * magic_num, 0, 2 * Math.PI);
                //canvas pixels 
                this.ctx.fill();
            }
            if (this.canvas_circles[0][2] == 0) {
                this.canvas_circles = this.transfer_circle_cords(this.circles)
                console.log(this.canvas_circles)
            }
        },
        transfer_circle_cords(circles){
            let magic_num = this.canvas.height/8 //jde o velikost jedné kostičky
            let readyfregys = [[0,0,0],[0,0,0],[0,0,0]]
            for (let i = 0; i < 3; i++){
                readyfregys[i][0] = this.canvas.width / 2 + circles[i][0] * magic_num
                readyfregys[i][1] = this.canvas.height / 2 + circles[i][1] * magic_num
                readyfregys[i][2] = circles[i][2]  * magic_num
                //canvas pixels 
            }
            return readyfregys
        },
        
        circle_collision(x, y, flip_it) {
            let circs = this.canvas_circles
            if (flip_it){
                circs = this.transfer_circle_cords(this.flip_circles(this.circles))
            } 

            let magic_num = this.canvas.height / 8
            
            if (x < 2*magic_num || x > 10*magic_num){
                return false
            }
            
            for (let i = 0; i < 3; i++) {
                if (Math.sqrt(Math.pow(x - circs[i][0], 2) + Math.pow(y - circs[i][1], 2)) < circs[i][2]) {
                    return true;
                }
            }
            return false;
        },
        hit_target(func){
            let target_bottom = null;
            let target_top = null;
            if (this.gameData["targets"][this.targets_num] == 1){
                target_bottom = 2
                target_top = 4
            } else if (this.gameData["targets"][this.targets_num] == 2) {
                target_bottom = 0
                target_top = 2
            } else if (this.gameData["targets"][this.targets_num] == 3) {
                target_bottom = -2
                target_top = 0
            } else if (this.gameData["targets"][this.targets_num] == 4) {
                target_bottom = -4
                target_top = -2
            }
            let y = eval(this.calculate_y(12, func))
            if (this.gameData["nickname"] != this.username){
                if(this.selectedOption == "top"){ //top
                    y += 2
                }else if (this.selectedOption == "bottom"){ //low
                    y -= 2
                }
                let m = target_top
                target_top = -target_bottom
                target_bottom = -m
            } else {
                if(this.selectedOption == "top"){ //top
                    y += 2
                }else if (this.selectedOption == "bottom"){ //low
                    y -= 2
                }
            }
            if (y > target_bottom && y < target_top){
                console.log(`[DEBUG NAMES] myname: ${this.gameLogic.myname} hreceived name: ${this.gameLogic.hisname}`)
                if (this.gameLogic.hisname == null){
                    //console.log("[SCORE] MYscore++")
                    this.gameLogic.myscore += 1
                } else if (this.gameLogic.myname == this.username){
                    this.gameLogic.myscore += 1
                    //console.log("[SCORE] MYscore++")
                } else if (this.gameLogic.myname != this.gameLogic.hisname) {
                    this.gameLogic.hisscore += 1 
                    //console.log("[SCORE] HISscore++")
                }
                return true
            }
            return false
        },
        check_win(){
            if (this.gameLogic.myscore == 2 || this.gameLogic.hisscore == 2){
                if (this.gameLogic.myscore > this.gameLogic.hisscore){
                    this.we_won(localStorage.getItem("username"))
                    
                } else {
                    this.we_lose(localStorage.getItem("username"))
                }
                console.log(`[ENDE SCHLUSS]`)
                localStorage.removeItem("game")
                localStorage.removeItem("nickname")

                this.$router.push("/ucet");
            }
        },
        ready_to_play(){
            this.ws.send(JSON.stringify({"message": "ready fregy", "gameId": this.gameData["data"]}))
            this.gameLogic.ready = true
        },
        we_lose(user){
            this.ws.send(JSON.stringify({"message": "welose", "gameId": this.gameData["data"], "user": user}))
            this.ws.close()
        },
        we_won(user){
            this.ws.send(JSON.stringify({"message": "wewon", "gameId": this.gameData["data"], "user": user}))
            this.ws.close()
        },
        flip_my_turn(){
            this.gameLogic.myturn = !this.gameLogic.myturn
        },
        flip_circles(circs){
            return [[circs[0][0], circs[0][1], circs[0][2]],[-circs[1][0], circs[1][1], circs[1][2]],[-circs[2][0],circs[2][1],circs[2][2]]]
        },
    }
}
</script>
<template>
    <div class="kontejner">
        <form class="func_input">
            <div class="radio_kontejner">
            <fieldset v-if="this.gameLogic.gameready" id="radios">
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
                    <button v-on:click="sendMessage()" :disabled="!this.gameLogic.myturn" 
                    v-bind:class="{'disabled-button': !this.gameLogic.myturn, 'btn': this.gameLogic.myturn}" type="button">shoot</button>
                </fieldset>
            </div>
        </form>
        <div v-if="this.gameLogic.ready" class="scoreboard">
            <div>
                <h2>Moje statistiky:</h2>
                <br>
                {{ this.gameLogic.myname }}
                {{ this.gameLogic.myscore }}
            </div>
            <div>
                <h2>Status hry</h2>
                
                {{ this.gameLogic.myturn }}
            </div>
            <div>
                <h2>Statistiky soupeře:</h2>
                <br>
                {{ this.gameLogic.hisname }}
                {{ this.gameLogic.hisscore }}
            </div>
        </div>
        <div v-else>
            <h1>Čekání na protihráče...</h1>
            <button v-on:click="ready_to_play()" class="btn">READY</button>
        </div>
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
.opponents_turn{
    border: red solid 2px
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