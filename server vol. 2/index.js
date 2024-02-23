const WebSocket = require("ws");
const wss = new WebSocket.Server({port: 8080});

console.log("[STARTING] the server has started...")

wss.on("connection", ws => {
    console.log("[Beckend] New client connected");
    
    ws.on("message", message => {
        try{
            console.log(`[Beckend] displaying message: ${message}`)
            const data = parseInt(message);
            const response = data * 2;
            console.log(`[Beckend] sending data: ${JSON.stringify(response)}`)
            ws.send(JSON.stringify(response));
            //const input = JSON.parse(data);
            //console.log(input)
            //let num = parseInt(data.message);
            //ws.send(num*2);
        } catch(err) {
            ws.send("not a num")
        }
    });

    ws.on("close", () => {
        console.log("Client has disconnected");
    });
});