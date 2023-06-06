window.addEventListener("load", () =>{
    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext("2d")

    //resizing
    canvas.height = (2*window.innerHeight)/3;
    canvas.width = (3*window.innerWidth)/4;

    //axis x, y
    console.log(canvas.height, canvas.width);
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(canvas.width - canvas.width, canvas.height/2);
    ctx.lineTo(canvas.width, canvas.height/2);
    ctx.moveTo(canvas.width/2, canvas.height);
    ctx.lineTo(canvas.width/2, canvas.height - canvas.height)
    ctx.stroke();
    ctx.beginPath();
    ctx.fillStyle = "red";
    ctx.font = "30px Arial";
})
/* //responsive resizing
window.addEventListener("resize", () =>{

})
*/







    //ctx.fillText("-10", 3, canvas.height/2 + canvas.height/20);
    //ctx.fillText("10", canvas.width - canvas.width/35, canvas.height/2 + canvas.height/20);

    /*
    //graphics
    ctx.strokeStyle = "green";
    ctx.lineWidth = 5;
    ctx.strokeRect(100, 100, 50, 50);
    ctx.strokeStyle = "blue";
    ctx.strokeRect(200, 100, 50, 50);
    
    //lines
    ctx.strokeStyle = "red"
    ctx.beginPath();
    ctx.moveTo(100, 100);
    ctx.lineTo(250, 150);
    ctx.lineTo(300, 150);
    ctx.lineTo(300, 250);
    ctx.lineTo(100, 100);
    ctx.stroke();
    ctx.beginPath()
    

    //vars
    let painting = false;

    function startPosition(e){
        painting = true;
        draw(e);
    }

    function finishedPosition(){
        painting = false;
        ctx.beginPath();
    }

    function draw(e){
        if (!painting) return;
        ctx.lineWwidth = 5;
        ctx.lineCap = "round";
        ctx.lineTo(e.clientX, e.clientY);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.clientX, e.clientY);
    }

    //events
    canvas.addEventListener("mousedown", startPosition);
    canvas.addEventListener("mouseup", finishedPosition);
    canvas.addEventListener("mousemove", draw);
    */
