// define what sided dice we are using

const xRange = 6;

// then automatically update the following
let pointsx;
let yRange;
let yticksProb;

// updates the value next to the slider
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

// prevents min and max from crossing each other and automatically updates opposite bound
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
if (xRange === 20) {

    yRange = .15;
    yticksProb = [
        {  y: 0.05, yTxt:"5%" },
        {  y: 0.10, yTxt:"10%" },
        {  y: 0.15 , yTxt:"15%"}
    ];

pointsx = {
  1: [
  { x: 1, y: 0.14262, yCDF: "0%", yADJ: "85.7%", yPT: "14.26%" },
  { x: 2, y: 0.12837, yCDF: "14.3%", yADJ: "72.9%", yPT: "12.84%" },
  { x: 3, y: 0.11488, yCDF: "38.6%", yADJ: "61.4%", yPT: "11.49%" },
  { x: 4, y: 0.10212, yCDF: "48.8%", yADJ: "51.2%", yPT: "10.21%" },
  { x: 5, y: 0.09012, yCDF: "57.8%", yADJ: "42.2%", yPT: "9.01%" },
  { x: 6, y: 0.07887, yCDF: "65.7%", yADJ: "34.3%", yPT: "7.89%" },
  { x: 7, y: 0.06838, yCDF: "72.5%", yADJ: "27.5%", yPT: "6.84%" },
  { x: 8, y: 0.05862, yCDF: "78.4%", yADJ: "21.6%", yPT: "5.86%" },
  { x: 9, y: 0.04962, yCDF: "83.4%", yADJ: "16.6%", yPT: "4.96%" },
  { x: 10, y: 0.04138, yCDF: "87.5%", yADJ: "12.5%", yPT: "4.14%" },
  { x: 11, y: 0.03388, yCDF: "90.9%", yADJ: "9.1%", yPT: "3.39%" },
  { x: 12, y: 0.02712, yCDF: "93.6%", yADJ: "6.4%", yPT: "2.71%" },
  { x: 13, y: 0.02112, yCDF: "95.7%", yADJ: "4.3%", yPT: "2.11%" },
  { x: 14, y: 0.01588, yCDF: "97.3%", yADJ: "2.7%", yPT: "1.59%" },
  { x: 15, y: 0.01137, yCDF: "98.4%", yADJ: "1.6%", yPT: "1.14%" },
  { x: 16, y: 0.00762, yCDF: "99.2%", yADJ: "0.8%", yPT: "0.76%" },
  { x: 17, y: 0.00462, yCDF: "99.7%", yADJ: "0.3%", yPT: "0.46%" },
  { x: 18, y: 0.00237, yCDF: "99.9%", yADJ: "0.1%", yPT: "0.24%" },
  { x: 19, y: 0.00088, yCDF: "99.9%", yADJ: "0.1%", yPT: "0.09%" },
  { x: 20, y: 0.00012, yCDF: "100.%", yADJ: "0%", yPT: "0.01%" }
],
  2: [
  { x: 1, y: 0.00725, yCDF: "0.7%", yADJ: "99.3%", yPT: "0.73%" },
  { x: 2, y: 0.02075, yCDF: "2.8%", yADJ: "97.2%", yPT: "2.08%" },
  { x: 3, y: 0.03275, yCDF: "6.1%", yADJ: "93.9%", yPT: "3.28%" },
  { x: 4, y: 0.04325, yCDF: "10.4%", yADJ: "89.6%", yPT: "4.33%" },
  { x: 5, y: 0.05225, yCDF: "15.6%", yADJ: "84.4%", yPT: "5.23%" },
  { x: 6, y: 0.05975, yCDF: "21.6%", yADJ: "78.4%", yPT: "5.98%" },
  { x: 7, y: 0.06575, yCDF: "28.2%", yADJ: "71.8%", yPT: "6.58%" },
  { x: 8, y: 0.07025, yCDF: "35.2%", yADJ: "64.8%", yPT: "7.03%" },
  { x: 9, y: 0.07325, yCDF: "42.5%", yADJ: "57.5%", yPT: "7.32%" },
  { x: 10, y: 0.07475, yCDF: "50%", yADJ: "50%", yPT: "7.47%" },
  { x: 11, y: 0.07475, yCDF: "57.5%", yADJ: "42.5%", yPT: "7.47%" },
  { x: 12, y: 0.07325, yCDF: "64.8%", yADJ: "35.2%", yPT: "7.32%" },
  { x: 13, y: 0.07025, yCDF: "71.8%", yADJ: "28.2%", yPT: "7.03%" },
  { x: 14, y: 0.06575, yCDF: "78.4%", yADJ: "21.6%", yPT: "6.58%" },
  { x: 15, y: 0.05975, yCDF: "84.4%", yADJ: "15.6%", yPT: "5.98%" },
  { x: 16, y: 0.05225, yCDF: "89.6%", yADJ: "10.4%", yPT: "5.23%" },
  { x: 17, y: 0.04325, yCDF: "93.9%", yADJ: "6.1%", yPT: "4.33%" },
  { x: 18, y: 0.03275, yCDF: "97.2%", yADJ: "2.8%", yPT: "3.28%" },
  { x: 19, y: 0.02075, yCDF: "99.3%", yADJ: "0.7%", yPT: "2.08%" },
  { x: 20, y: 0.00725, yCDF: "100.%", yADJ: "0%", yPT: "0.73%" }
],
  3: [
  { x: 1, y: 0.00012, yCDF: "0%", yADJ: "100%", yPT: "0.01%" },
  { x: 2, y: 0.00088, yCDF: "0.1%", yADJ: "99.9%", yPT: "0.09%" },
  { x: 3, y: 0.00237, yCDF: "0.3%", yADJ: "99.7%", yPT: "0.24%" },
  { x: 4, y: 0.00462, yCDF: "0.8%", yADJ: "99.2%", yPT: "0.46%" },
  { x: 5, y: 0.00762, yCDF: "1.6%", yADJ: "98.4%", yPT: "0.76%" },
  { x: 6, y: 0.01137, yCDF: "2.7%", yADJ: "97.3%", yPT: "1.14%" },
  { x: 7, y: 0.01588, yCDF: "4.3%", yADJ: "95.7%", yPT: "1.59%" },
  { x: 8, y: 0.02112, yCDF: "6.4%", yADJ: "93.6%", yPT: "2.11%" },
  { x: 9, y: 0.02712, yCDF: "9.1%", yADJ: "90.9%", yPT: "2.71%" },
  { x: 10, y: 0.03388, yCDF: "12.5%", yADJ: "87.5%", yPT: "3.39%" },
  { x: 11, y: 0.04138, yCDF: "16.6%", yADJ: "83.4%", yPT: "4.14%" },
  { x: 12, y: 0.04962, yCDF: "21.6%", yADJ: "78.4%", yPT: "4.96%" },
  { x: 13, y: 0.05862, yCDF: "27.5%", yADJ: "72.5%", yPT: "5.86%" },
  { x: 14, y: 0.06838, yCDF: "34.3%", yADJ: "65.7%", yPT: "6.84%" },
  { x: 15, y: 0.07887, yCDF: "42.2%", yADJ: "57.8%", yPT: "7.89%" },
  { x: 16, y: 0.09012, yCDF: "51.2%", yADJ: "48.8%", yPT: "9.01%" },
  { x: 17, y: 0.10212, yCDF: "61.4%", yADJ: "38.6%", yPT: "10.21%" },
  { x: 18, y: 0.11488, yCDF: "72.9%", yADJ: "27.1%", yPT: "11.49%" },
  { x: 19, y: 0.12837, yCDF: "85.7%", yADJ: "14.3%", yPT: "12.84%" },
  { x: 20, y: 0.14262, yCDF: "100%", yADJ: "0%", yPT: "14.26%" }
],

}} else if (xRange === 10) {

    yRange = .30;

    yticksProb = [
        {  y: 0.10, yTxt:"10%" },
        {  y: 0.20, yTxt:"20%" },
        {  y: 0.30 , yTxt:"30%"}
    ];

    pointsx = {
      1: [{ x: 1, y: 0.271, yCDF: "0.00%", yADJ: "72.90%", yPT: "27.10%"} ,{ x: 2, y: 0.217, yCDF: "21.10%", yADJ: "51.10%", yPT: "21.70%"} ,{ x: 3, y: 0.169, yCDF: "48.80%", yADJ: "34.30%", yPT: "16.90%"} ,{ x: 4, y: 0.127, yCDF: "65.90%", yADJ: "23.00%", yPT: "12.70%"} ,{ x: 5, y: 0.091, yCDF: "76.20%", yADJ: "18.70%", yPT: "9.10%"} ,{ x: 6, y: 0.061, yCDF: "84.10%", yADJ: "9.80%", yPT: "6.10%"} ,{ x: 7, y: 0.037, yCDF: "90.00%", yADJ: "10.00%", yPT: "3.70%"} ,{ x: 8, y: 0.019, yCDF: "95.30%", yADJ: "3.80%", yPT: "1.90%"} ,{ x: 9, y: 0.007, yCDF: "98.20%", yADJ: "1.80%", yPT: "0.70%"} ,{ x: 10, y: 0.001, yCDF: "99.90%", yADJ: "0.00%", yPT: "0.10%"} ],
      2: [{ x: 1, y: 0.028, yCDF: "0.00%", yADJ: "97.20%", yPT: "2.80%"} ,{ x: 2, y: 0.076, yCDF: "5.20%", yADJ: "87.20%", yPT: "7.60%"} ,{ x: 3, y: 0.112, yCDF: "10.80%", yADJ: "77.00%", yPT: "11.20%"} ,{ x: 4, y: 0.136, yCDF: "22.40%", yADJ: "64.40%", yPT: "13.60%"} ,{ x: 5, y: 0.148, yCDF: "36.40%", yADJ: "49.60%", yPT: "14.80%"} ,{ x: 6, y: 0.148, yCDF: "49.20%", yADJ: "36.80%", yPT: "14.80%"} ,{ x: 7, y: 0.136, yCDF: "64.00%", yADJ: "22.00%", yPT: "13.60%"} ,{ x: 8, y: 0.112, yCDF: "76.40%", yADJ: "12.60%", yPT: "11.20%"} ,{ x: 9, y: 0.076, yCDF: "87.60%", yADJ: "4.60%", yPT: "7.60%"} ,{ x: 10, y: 0.028, yCDF: "97.20%", yADJ: "0.00%", yPT: "2.80%"} ],
      3: [{ x: 1, y: 0.001, yCDF: "0.00%", yADJ: "99.90%", yPT: "0.10%"} ,{ x: 2, y: 0.007, yCDF: "0.70%", yADJ: "98.20%", yPT: "0.70%"} ,{ x: 3, y: 0.019, yCDF: "2.00%", yADJ: "96.10%", yPT: "1.90%"} ,{ x: 4, y: 0.037, yCDF: "5.70%", yADJ: "93.30%", yPT: "3.70%"} ,{ x: 5, y: 0.061, yCDF: "9.40%", yADJ: "90.50%", yPT: "6.10%"} ,{ x: 6, y: 0.091, yCDF: "15.50%", yADJ: "83.50%", yPT: "9.10%"} ,{ x: 7, y: 0.127, yCDF: "22.60%", yADJ: "76.40%", yPT: "12.70%"} ,{ x: 8, y: 0.169, yCDF: "35.30%", yADJ: "63.70%", yPT: "16.90%"} ,{ x: 9, y: 0.217, yCDF: "53.80%", yADJ: "24.20%", yPT: "21.70%"} ,{ x: 10, y: 0.271, yCDF: "78.20%", yADJ: "21.80%", yPT: "27.10%"} ]
}} else if (xRange === 6) {

    yRange = .46;

    yticksProb = [
        {  y: 0.15, yTxt:"15%" },
        {  y: 0.30, yTxt:"30%" },
        {  y: 0.45 , yTxt:"45%"}
    ];

    pointsx = {
        1: [{ x: 1, y: 0.4213, yCDF: "0%", yPT: "42.13%", yADJ: "57.87%" }, { x: 2, y: 0.28241, yCDF: "42.16%", yPT: "28.24%", yADJ: "29.6%" }, { x: 3, y: 0.1713, yCDF: "70.37%", yPT: "17.13%", yADJ: "12.5%" }, { x: 4, y: 0.08796, yCDF: "87.5%", yPT: "8.8%", yADJ: "3.7%" }, { x: 5, y: 0.03241, yCDF: "96.26%", yPT: "3.24%", yADJ: "0.5%" }, { x: 6, y: 0.00463, yCDF: "99.54%", yPT: "0.46%", yADJ: "0.0%" }],
        2: [{ x: 1, y: 0.07407, yCDF: "0%", yPT: "7.41%", yADJ: "92.59%" }, { x: 2, y: 0.18519, yCDF: "7.38%", yPT: "18.52%", yADJ: "74.1%" }, { x: 3, y: 0.24074, yCDF: "25.93%", yPT: "24.07%", yADJ: "50.0%" }, { x: 4, y: 0.24074, yCDF: "50.03%", yPT: "24.07%", yADJ: "25.9%" }, { x: 5, y: 0.18519, yCDF: "74.08%", yPT: "18.52%", yADJ: "7.4%" }, { x: 6, y: 0.07407, yCDF: "92.59%", yPT: "7.41%", yADJ: "0.0%" }],
        3: [{ x: 1, y: 0.00463, yCDF: "0%", yPT: "0.46%", yADJ: "99.54%" }, { x: 2, y: 0.03241, yCDF: "0.46%", yPT: "3.24%", yADJ: "96.3%" }, { x: 3, y: 0.08796, yCDF: "3.7%", yPT: "8.8%", yADJ: "87.5%" }, { x: 4, y: 0.1713, yCDF: "12.47%", yPT: "17.13%", yADJ: "70.4%" }, { x: 5, y: 0.28241, yCDF: "29.66%", yPT: "28.24%", yADJ: "42.1%" }, { x: 6, y: 0.4213, yCDF: "57.87%", yPT: "42.13%", yADJ: "0.0%" }]};
};


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

/**
 * Function to translate the (x, y) coordinates to a scaled coordinate system.
 * @param {number} x - The x-coordinate to be translated.
 * @param {number} y - The y-coordinate to be translated.
 * @param {object} setts - The settings object containing graph parameters, usually defined by gs.
 * @returns {object} - An object with translated coordinates (cx, cy).
 */
function xyTranslate(x, y, setts) {
    // Extracting graph settings from the setts object
    const bw = setts['bw'];                 // Border width
    const chb = setts['ch'] - 2 * bw;       // Canvas height excluding borders
    const cwb = setts['cw'] - 2 * bw;       // Canvas width excluding borders
    const originY = bw + chb;               // Origin y-coordinate

    // Extracting x-axis settings
    const xMin = setts['xMin'];            // Minimum x-value
    const xIncrement = cwb / (setts['xMax'] - xMin); // Increment for each x-unit

    // Extracting y-axis settings
    const yMin = setts['yMin'];            // Minimum y-value
    const yIncrement = chb / (setts['yMax'] - yMin); // Increment for each y-unit

    // Calculating translated coordinates
    const translatedX = setts['bw'] + (x - xMin) * xIncrement;
    const translatedY = originY - (y - yMin) * yIncrement;

    // Returning an object with translated coordinates
    return { cx: translatedX, cy: translatedY };
}

function drawLine(ctx,x1,y1,x2,y2,graphsettings){
    // Function to draw a line between two points
    const pt0=xyTranslate(x1,y1,graphsettings);
    const pt1=xyTranslate(x2,y2,graphsettings);
    ctx.beginPath();
    ctx.moveTo(pt0.cx, pt0.cy);
    ctx.lineTo(pt1.cx, pt1.cy);
    ctx.stroke();
};

// Function to draw left arrow
function drawLArrow(ctx, x1, y1, x2, y2, arrowText, xOff, graphsettings) {
    // Translate coordinates to canvas space
    const pt0 = xyTranslate(x1, y1, graphsettings);
    const pt1 = xyTranslate(x2, y2, graphsettings);

    // Calculate arrowhead properties
    var headlen = 10; // length of head in pixels
    var dx = pt1.cx - pt0.cx;
    var dy = pt1.cy - pt0.cy;
    var angle = Math.atan2(dy, dx);
    var atPT = x1 + 1;

    // Save the current context settings
    ctx.save();

    // Draw the arrow lines
    ctx.moveTo(pt0.cx, pt0.cy);
    ctx.lineTo(pt1.cx, pt1.cy);
    ctx.lineTo(pt1.cx - headlen * Math.cos(angle - Math.PI / 6), pt1.cy - headlen * Math.sin(angle - Math.PI / 6));
    ctx.moveTo(pt1.cx, pt1.cy);
    ctx.lineTo(pt1.cx - headlen * Math.cos(angle + Math.PI / 6), pt1.cy - headlen * Math.sin(angle + Math.PI / 6));
    ctx.moveTo(pt0.cx - headlen * Math.sin(angle), pt0.cy - headlen * Math.cos(angle));
    ctx.lineTo(pt0.cx + headlen * Math.sin(angle), pt0.cy + headlen * Math.cos(angle));

    // Stroke the lines
    ctx.stroke();

    // Set text properties and position
    ctx.fillStyle = "black";
    ctx.font = axisTextSize;
    ctx.textAlign = "left";
    ctx.fillText("Probability below " + atPT + " is " + arrowText, (pt1.cx + pt0.cx) / 2, (pt1.cy + pt0.cy) / 2 - xOff);

    // Restore the previous context settings
    ctx.restore();
}

// Function to draw right arrow
function drawRArrow(ctx, x1, y1, x2, y2, arrowText, xOff, graphsettings) {
    // Translate coordinates to canvas space
    const pt0 = xyTranslate(x1, y1, graphsettings);
    const pt1 = xyTranslate(x2, y2, graphsettings);

    // Calculate arrowhead properties
    var headlen = 10; // length of head in pixels
    var dx = pt1.cx - pt0.cx;
    var dy = pt1.cy - pt0.cy;
    var angle = Math.atan2(dy, dx) + Math.PI; // Add Math.PI to reverse the angle
    var atPT = x1 - 1;

    // Save the current context settings
    ctx.save();

    // Draw the arrow lines
    ctx.moveTo(pt0.cx, pt0.cy);
    ctx.lineTo(pt1.cx, pt1.cy);
    ctx.lineTo(pt1.cx + headlen * Math.cos(angle - Math.PI / 6), pt1.cy + headlen * Math.sin(angle - Math.PI / 6));
    ctx.moveTo(pt1.cx, pt1.cy);
    ctx.lineTo(pt1.cx + headlen * Math.cos(angle + Math.PI / 6), pt1.cy + headlen * Math.sin(angle + Math.PI / 6));
    ctx.moveTo(pt0.cx - headlen * Math.sin(angle), pt0.cy - headlen * Math.cos(angle));
    ctx.lineTo(pt0.cx + headlen * Math.sin(angle), pt0.cy + headlen * Math.cos(angle));

    // Stroke the lines
    ctx.stroke();

    // Set text properties and position
    ctx.fillStyle = "black";
    ctx.font = axisTextSize;
    ctx.textAlign = "center";
    ctx.fillText("Probability above " + atPT + " is " + arrowText, (pt1.cx + pt0.cx) / 2, (pt1.cy + pt0.cy) / 2 - xOff);

    // Restore the previous context settings
    ctx.restore();
}

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

// Function to draw the probability graph
function drawProbs(showPlot, points, yticks, redPoint) {
    // Get the canvas context
    const ctx = canvasProb.getContext("2d");

    // Define graph settings
    const gs = {
        'ch': canvasProb.height,    // called from HTML
        'cw': canvasProb.width,     // called from HTML
        'bw': 60,         // Bar width
        'xMin': 1,        // X-axis minimum value
        'xMax': xRange,       // X-axis maximum value
        'yMin': 0,        // Y-axis minimum value
        'yMax': yRange      // Y-axis maximum value
    };

    // Offset for x-axis labels
    const xTextoffset = 30;

    // Set the stroke style for the context
    ctx.strokeStyle = "black";

    // Draw the base line of the graph
    drawLine(ctx, 1, 0, xRange, 0, gs);

    // Draw the yTicks
    drawTicks(ctx, yticks, gs, xTextoffset);

    // For each point label the axis
    points[showPlot].forEach(point => {
        const ptLoc = xyTranslate(point.x, 0, gs);
        ctx.fillStyle = "black";
        ctx.font = axisTextSize;
        ctx.textAlign = "center";
        ctx.fillText(point.x, ptLoc.cx, ptLoc.cy + xTextoffset);
    });

    // Remove dashing
    ctx.setLineDash([]);

    // Plot each point for the showPlot layer
    points[showPlot].forEach(point => {
        pt = xyTranslate(point.x, point.y, gs);
        ctx.save();

        // Draw circle for the point
        if (point.x == redPoint) { // If the highlighted point

            // Draw arrows for the highlighted point
            let yArrow = yRange + .01;
            drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
            drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);

            // Apply special styling for the highlighted point
            ctx.strokeStyle = "black";
            ctx.shadowColor = "gray";
            ctx.fillStyle = "red";
            ctx.shadowOffsetX = 5;
            ctx.shadowOffsetY = 5;
            ctx.shadowBlur = 4;

            // Add text above the circle for the point labeled by point.yPT
            ctx.font = axisTextSize;
            ctx.textAlign = "center";
            ctx.fillText(point.yPT, pt.cx + 10, pt.cy - 15); // Adjust the offset as needed

        } else { // Otherwise, no special styling
            ctx.strokeStyle = "gray";
            ctx.fillStyle = "blue";
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 0;
            ctx.shadowBlur = 0;
        };

        // Draw stem line
        drawLine(ctx, point.x, 0, point.x, point.y, gs);
        // Draw points
        drawPoint(ctx, point.x, point.y, 7, gs);
        ctx.restore(); // Restore settings
    });
    // End of function def
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

