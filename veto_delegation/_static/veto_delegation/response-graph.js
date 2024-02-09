const canvasPayoff = document.getElementById("payoffCanvas");
const response = document.getElementById('response')
let resp = 0

// pulls the variables from init.py

const vetoerBias =  js_vars.vetoer_bias;
const minSlider = js_vars.lower_interval;
const maxSlider = js_vars.upper_interval;


// Real time acceptance for response

function updateDescription(input) {
    let response = parseInt(input.value);
    let p2payoff = 25 - Math.abs(parseInt(input.value) - vetoerBias);
    description.innerText = `Accept ${response} `;
    payoff.innerText = `for a payoff of ${p2payoff}.`
}


response.addEventListener('input', function() {
    resp = parseInt(response.value);
    drawPayoffs(vetoerBias,minSlider,maxSlider,resp);
});


// Places cross lines
const yticksPayoff = [
    {  y: 5, yTxt:"$5" },
    {  y: 10, yTxt:"$10" },
    {  y: 15 , yTxt:"$15"},
    {  y: 20 , yTxt:"$20"},
    {  y: 25 , yTxt:"$25"},
    {  y: 30 , yTxt:"$30"}
];

const axisTextSize = "14px Arial";

function xyTranslate(x,y,setts){
    // Function to translate the (x,y) coordinates to a scaled coordinate system
    const bw = setts['bw'];
    const chb = setts['ch']-2*bw;
    const cwb = setts['cw']-2*bw;
    const originY= bw + chb;
    const xMin = setts['xMin'];
    const xIncrement = cwb / (setts['xMax']-setts['xMin']);
    const yMin = setts['yMin'];
    const yIncrement = chb / (setts['yMax']-setts['yMin']);
    return {cx: setts['bw'] + (x-xMin) * xIncrement , cy: originY - (y-yMin) * yIncrement};
};

function drawLine(ctx,x1,y1,x2,y2,graphsettings){
    // Function to draw a line between two points
    const pt0=xyTranslate(x1,y1,graphsettings);
    const pt1=xyTranslate(x2,y2,graphsettings);
    ctx.beginPath();
    ctx.moveTo(pt0.cx, pt0.cy);
    ctx.lineTo(pt1.cx, pt1.cy);
    ctx.stroke();
};

function drawPoint(ctx,x1,y1,r,graphsettings){
    // Function to draw an (x,y) point
    const pt0=xyTranslate(x1,y1,graphsettings);
    ctx.beginPath();
    ctx.arc(pt0.cx, pt0.cy, r, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
};

function drawTicks(ctx,yTicks,gs,xOff){
    // Function to draw an (x,y) point
    yTicks.forEach(tick => {
        // Draw ytick
        ctx.setLineDash([1, 3]);
        ctx.strokeStyle = "gray,d";
        drawLine(ctx,gs["xMin"],tick.y,gs["xMax"],tick.y,gs);
        ctx.fillStyle = "black";
        ctx.font = axisTextSize;
        ctx.textAlign = "right" ;
        const txtLoc1=xyTranslate(gs["xMin"],tick.y,gs);
        const txtLoc2=xyTranslate(gs["xMax"],tick.y,gs);
        ctx.fillText(tick.yTxt, txtLoc1.cx-xOff/2, txtLoc1.cy);
        ctx.textAlign = "left" ;
        ctx.fillText(tick.yTxt, txtLoc2.cx+xOff/2, txtLoc2.cy);
    });
};


// DRAW THE PAYOFF GRAPH
function drawPayoffs(theta,minC,maxC,selection){

    const ctx = canvasPayoff.getContext("2d");
    const gs= {'ch':canvasPayoff.height,'cw':canvasPayoff.width,'bw':60,'xMin':0,'xMax':25,'yMin':0,'yMax':30 };
    const xTextoffset = 30;

        // Clear the canvas before drawing
    ctx.clearRect(0, 0, canvasPayoff.width, canvasPayoff.height);


    ctx.strokeStyle = "black";
    ctx.strokeStyle = "black";
    drawLine(ctx,0,0,25,0,gs);
    // Draw the yTicks
    ctx.setLineDash([1, 3]);
    ctx.strokeStyle = "gray,d";
    drawTicks(ctx,yticksPayoff,gs,xTextoffset);

    for (let xi = 0; xi < 26; xi++) {
        const ptLoc=xyTranslate(xi,0,gs);
        ctx.fillStyle = "black";
        ctx.font = axisTextSize;
        ctx.textAlign = "center" ;
        ctx.fillText(xi, ptLoc.cx, ptLoc.cy+xTextoffset)
    };
    // Remove dashing
    ctx.setLineDash([]);
    // Plot each point for the showPlot layer
    for (let xi = 0; xi < 26; xi++) {
        const payoffP= 30-Math.abs(25-xi);
        let alpha = xi === selection ? 1 : 0.3;
        ctx.strokeStyle = "gray";
        ctx.fillStyle = "blue";
        ctx.globalAlpha = alpha;
        if(xi===0 || ( xi >= minC && xi<=maxC)){
            drawLine(ctx,xi,0,xi,payoffP, gs);
            drawPoint(ctx,xi,payoffP,7, gs);
        };
    };
    for (let xi = 0; xi < 26; xi++) {
        const payoffP= 25-Math.abs(theta-xi);
        let alpha = xi === selection ? 1 : 0.3
        ctx.strokeStyle = "gray";
        ctx.fillStyle = "red";
        ctx.globalAlpha = alpha;
        if(xi==0 || ( xi >= minC && xi<=maxC)){
        drawLine(ctx,xi,0,xi,payoffP, gs);
        drawPoint(ctx,xi,payoffP,5, gs);
        };
    };
};



drawPayoffs(vetoerBias,minSlider, maxSlider,resp);

// confirms choice before advancing

        function checkSubmit() {
            confirm(`Confirm your selection: Accept offer of ${resp}.`)
            form.submit();
        }
        function checkReject() {
            confirm(`Confirm your selection: Reject the offer.`)
            form.submit();
        }


