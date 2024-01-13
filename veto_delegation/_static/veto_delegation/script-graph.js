// this just updates the value next to the slider
let minDesc = document.getElementById('minDesc');

function updateMinSlider(input) {
    let minSlider = parseInt(input.value)
    minDesc.innerText = `${minSlider}`
}
let maxDesc = document.getElementById('maxDesc');

function updateMaxSlider(input) {
    let maxSlider = parseInt(input.value)
    maxDesc.innerText = `${maxSlider}`
}

// this prevents min and max from crossing each other and automatically updates opposite bound
let minSlider = document.getElementById('minSlider');
let maxSlider = document.getElementById('maxSlider');

minSlider.addEventListener('input', function() {
    const value = parseInt(this.value)
    minDesc.textContent = value;
    if (value > parseInt(maxSlider.value)) {
        maxSlider.value = value;
        maxDesc.textContent = value
    }
    drawProbs(radioX.value,pointsx,yticksProb,sliderTheta.value);
    drawPayoffs(sliderTheta.value,minSlider.value,maxSlider.value);
});

maxSlider.addEventListener('input', function() {
    const value = parseInt(this.value)
    maxDesc.textContent = value;
    if (value < parseInt(minSlider.value)) {
        minSlider.value = value;
        minDesc.textContent = value
    }
    drawProbs(radioX.value,pointsx,yticksProb,sliderTheta.value);
    drawPayoffs(sliderTheta.value,minSlider.value,maxSlider.value);
});

// These are the probabilities for each Ideal point
const pointsx = {1:[{ x: 1, y: 0.14262} ,{ x: 2, y: 0.12837} ,{ x: 3, y: 0.11488} ,{ x: 4, y: 0.10212} ,{ x: 5, y: 0.09012} , { x: 6, y: 0.07887} ,{ x: 7, y: 0.06838} ,{ x: 8, y: 0.05862} ,{ x: 9, y: 0.04962} ,{ x: 10, y: 0.04138} , { x: 11, y: 0.03388} ,{ x: 12, y: 0.02712} ,{ x: 13, y: 0.02112} ,{ x: 14, y: 0.01588} ,{ x: 15, y: 0.01137} ,{ x: 16, y: 0.00762} ,{ x: 17, y: 0.00462} ,{ x: 18, y: 0.00237} ,{ x: 19, y: 0.00088} ,{ x: 20, y: 0.00012} ], 2:[ { x: 1, y: 0.00725} ,{ x: 2, y: 0.02075} ,{ x: 3, y: 0.03275} ,{ x: 4, y: 0.04325} ,{ x: 5, y: 0.05225} ,{ x: 6, y: 0.05975} ,{ x: 7, y: 0.06575} ,{ x: 8, y: 0.07025} ,{ x: 9, y: 0.07325} ,{ x: 10, y: 0.07475} ,{ x: 11, y: 0.07475} ,{ x: 12, y: 0.07325} ,{ x: 13, y: 0.07025} ,{ x: 14, y: 0.06575} ,{ x: 15, y: 0.05975} ,{ x: 16, y: 0.05225} ,{ x: 17, y: 0.04325} ,{ x: 18, y: 0.03275} ,{ x: 19, y: 0.02075} ,{ x: 20, y: 0.00725} ], 3:[{ x: 1, y: 0.00012} ,{ x: 2, y: 0.00088} ,{ x: 3, y: 0.00237} ,{ x: 4, y: 0.00462} ,{ x: 5, y: 0.00762} ,{ x: 6, y: 0.01137} ,{ x: 7, y: 0.01588} ,{ x: 8, y: 0.02112} ,{ x: 9, y: 0.02712} ,{ x: 10, y: 0.03388} ,{ x: 11, y: 0.04138} ,{ x: 12, y: 0.04962} ,{ x: 13, y: 0.05862} ,{ x: 14, y: 0.06838} ,{ x: 15, y: 0.07887} ,{ x: 16, y: 0.09012} ,{ x: 17, y: 0.10212} ,{ x: 18, y: 0.11488} ,{ x: 19, y: 0.12837} ,{ x: 20, y: 0.14262} ]};

// Places cross lines
const yticksProb = [
    {  y: 0.05, yTxt:"5%" },
    {  y: 0.10, yTxt:"10%" },
    {  y: 0.15 , yTxt:"15%"}
];

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
var showPlotIn = 3;
const radioX = document.getElementById("dist");

radioX.selectedIndex = 0;

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


function drawProbs(showPlot,points,yticks,redPoint){
    // Function to draw the probability graph
    const ctx = canvasProb.getContext("2d");
    const gs={'ch':canvasProb.height,'cw':canvasProb.width,'bw':60,'xMin':1,'xMax':20,'yMin':0,'yMax':0.16 };
    const xTextoffset = 30;
    ctx.strokeStyle = "black";
    drawLine(ctx,1,0,20,0,gs);
    // Draw the yTicks
    drawTicks(ctx,yticks,gs,xTextoffset);
    // For each point label the axis
    points[showPlot].forEach(point => {
        const ptLoc=xyTranslate(point.x,0,gs);
        ctx.fillStyle = "black";
        ctx.font = axisTextSize;
        ctx.textAlign = "center" ;
        ctx.fillText(point.x, ptLoc.cx, ptLoc.cy+xTextoffset)
    });
    // Remove dashing
    ctx.setLineDash([]);
    // Plot each point for the showPlot layer
    points[showPlot].forEach(point => {
        pt=xyTranslate(point.x,point.y,gs);
        ctx.save();
        // Draw circle for the point
        if (point.x == redPoint){ // If the highlighted point
            ctx.strokeStyle = "black";
            ctx.shadowColor = "gray";
            ctx.fillStyle = "red";
            ctx.shadowOffsetX = 5;
            ctx.shadowOffsetY = 5;
            ctx.shadowBlur = 4;

            }
        else{ //otherwise no special styling
            ctx.strokeStyle = "gray";
            ctx.fillStyle = "blue";
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 0;
            ctx.shadowBlur = 0;
        };

        // Draw stem line
        drawLine(ctx,point.x,0,point.x,point.y,gs);
        drawPoint(ctx,point.x,point.y,7,gs)
        ctx.restore(); // restore settings
    }); //End of function def
};

// DRAW THE PAYOFF GRAPH
function drawPayoffs(theta,minC,maxC){
    const ctx = canvasPayoff.getContext("2d");
    const gs= {'ch':canvasPayoff.height,'cw':canvasPayoff.width,'bw':60,'xMin':0,'xMax':25,'yMin':0,'yMax':30 };
    const xTextoffset = 30;
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
        let alpha = 1;
                if(xi!=0 && xi < minC || xi > maxC) {
            alpha = 0.1;
        }
        ctx.strokeStyle = "gray";
        ctx.fillStyle = "blue";
        ctx.globalAlpha = alpha;
        // if(xi==0 || ( xi >= minC && xi<=maxC)){   this would restore the old way to have values not mapped
        drawLine(ctx,xi,0,xi,payoffP, gs);
        drawPoint(ctx,xi,payoffP,7, gs);
        // };
    };
    for (let xi = 0; xi < 26; xi++) {
        const payoffP= 25-Math.abs(theta-xi);
                let alpha = 1;
                if(xi!=0 && xi < minC || xi > maxC) {
            alpha = 0.1;
        }
        ctx.strokeStyle = "gray";
        ctx.fillStyle = "red";
        ctx.globalAlpha = alpha;
        // if(xi==0 || ( xi >= minC && xi<=maxC)){
        drawLine(ctx,xi,0,xi,payoffP, gs);
        drawPoint(ctx,xi,payoffP,5, gs);
        // };
    };
};

const sliderTheta = document.getElementById("thetaRange");
var outputTheta = document.getElementById("thetaOut");

const canvasProb = document.getElementById("probCanvas");
const canvasPayoff = document.getElementById("payoffCanvas");


outputTheta.innerHTML = sliderTheta.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
sliderTheta.oninput = function() {
    canvasProb.getContext("2d").clearRect(0, 0, canvasProb.width, canvasProb.height);
    canvasPayoff.getContext("2d").clearRect(0, 0, canvasPayoff.width, canvasPayoff.height);
    outputTheta.innerHTML = this.value;
    drawProbs(radioX.value,pointsx,yticksProb,sliderTheta.value);
    drawPayoffs(sliderTheta.value,minSlider.value,maxSlider.value);
};

radioX.oninput = function() {
    canvasProb.getContext("2d").clearRect(0, 0, canvasProb.width, canvasProb.height);
    canvasPayoff.getContext("2d").clearRect(0, 0, canvasPayoff.width, canvasPayoff.height);
    drawProbs(radioX.value,pointsx,yticksProb,sliderTheta.value);
    drawPayoffs(sliderTheta.value,minSlider.value,maxSlider.value);
};

minSlider.oninput = function() {
    canvasProb.getContext("2d").clearRect(0, 0, canvasProb.width, canvasProb.height);
    canvasPayoff.getContext("2d").clearRect(0, 0, canvasPayoff.width, canvasPayoff.height);
    drawProbs(radioX.value,pointsx,yticksProb,sliderTheta.value);
    drawPayoffs(sliderTheta.value,minSlider.value,maxSlider.value);
};

maxSlider.oninput = function() {
    canvasProb.getContext("2d").clearRect(0, 0, canvasProb.width, canvasProb.height);
    canvasPayoff.getContext("2d").clearRect(0, 0, canvasPayoff.width, canvasPayoff.height);
    drawProbs(radioX.value,pointsx,yticksProb,sliderTheta.value);
    drawPayoffs(sliderTheta.value,minSlider.value,maxSlider.value);
};


//Initial call
drawProbs(1,pointsx,yticksProb,0);
drawPayoffs(0,minSlider.value, maxSlider.value);

