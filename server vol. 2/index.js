const WebSocket = require("ws");
const wss = new WebSocket.Server({port: 8080});

console.log("[STARTING] the server has started...")

arr = []

wss.on("connection", ws => {
    console.log("[Beckend] New client connected");
    
    ws.on("message", message => {
        try{
            console.log(`[Beckend] displaying message: ${message}`)
            const data = parseInt(message);
            const response = data * 2;
            console.log(`[Beckend] sending data: ${JSON.stringify(response)}`)
            add_item(`${JSON.stringify(response)}`)
            display_arr(get_arr());
            ws.send(JSON.stringify({"message": "ok", "data": get_arr()}));
            
            
        } catch(err) {
            ws.send("not a num")
        }
    });

    ws.on("close", () => {
        console.log("Client has disconnected");
    });
});

function add_item(item){
    a = get_arr();
    a[a.length] = item

}
function get_arr(){
    return arr
}
function display_arr(a){
    let s = ""
    for(let i = 0; i < a.length; i++){
        s += a[i] + ", "
    }
    console.log(s)
}