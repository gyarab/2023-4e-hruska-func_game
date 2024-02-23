const WebSocket = require("ws");
const wss = new WebSocket.Server({port: 8080});

console.log("[STARTING] the server has started...")

wss.on("connection", ws => {
    console.log("New client connected");

    ws.on("message", message => {
        console.log("in a message method");
        console.log(`received message from client: ${message}`);
        try{
            const data = parseInt(message);
            const response = data * 2;
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