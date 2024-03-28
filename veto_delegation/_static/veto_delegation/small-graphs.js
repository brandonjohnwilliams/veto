
// Probabilities Section

// Define what sided dice we are using
const xRange = 6;

// Preliminaries
const axisTextSize = "14px Arial";

// Points to label

const yRange = .46;

const yticksProb = [
        {  y: 0.15, yTxt:"15%" },
        {  y: 0.30, yTxt:"30%" },
        {  y: 0.45 , yTxt:"45%"}
    ];

const pointsx = {
        1: [{ x: 1, y: 0.4213, yCDF: "0%", yPT: "42.13%", yADJ: "57.87%" }, { x: 2, y: 0.28241, yCDF: "42.16%", yPT: "28.24%", yADJ: "29.6%" }, { x: 3, y: 0.1713, yCDF: "70.37%", yPT: "17.13%", yADJ: "12.5%" }, { x: 4, y: 0.08796, yCDF: "87.5%", yPT: "8.8%", yADJ: "3.7%" }, { x: 5, y: 0.03241, yCDF: "96.26%", yPT: "3.24%", yADJ: "0.5%" }, { x: 6, y: 0.00463, yCDF: "99.54%", yPT: "0.46%", yADJ: "0.0%" }],
        2: [{ x: 1, y: 0.07407, yCDF: "0%", yPT: "7.41%", yADJ: "92.59%" }, { x: 2, y: 0.18519, yCDF: "7.38%", yPT: "18.52%", yADJ: "74.1%" }, { x: 3, y: 0.24074, yCDF: "25.93%", yPT: "24.07%", yADJ: "50.0%" }, { x: 4, y: 0.24074, yCDF: "50.03%", yPT: "24.07%", yADJ: "25.9%" }, { x: 5, y: 0.18519, yCDF: "74.08%", yPT: "18.52%", yADJ: "7.4%" }, { x: 6, y: 0.07407, yCDF: "92.59%", yPT: "7.41%", yADJ: "0.0%" }],
        3: [{ x: 1, y: 0.00463, yCDF: "0%", yPT: "0.46%", yADJ: "99.54%" }, { x: 2, y: 0.03241, yCDF: "0.46%", yPT: "3.24%", yADJ: "96.3%" }, { x: 3, y: 0.08796, yCDF: "3.7%", yPT: "8.8%", yADJ: "87.5%" }, { x: 4, y: 0.1713, yCDF: "12.47%", yPT: "17.13%", yADJ: "70.4%" }, { x: 5, y: 0.28241, yCDF: "29.66%", yPT: "28.24%", yADJ: "42.1%" }, { x: 6, y: 0.4213, yCDF: "57.87%", yPT: "42.13%", yADJ: "0.0%" }]};


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
        // ctx.fillText(tick.yTxt, txtLoc2.cx+xOff/2, txtLoc2.cy);
    });
};

// Function to draw the probability graph
function drawProbs1(showPlot, points, yticks, redPoint) {
    // Get the canvas context
    const ctx = canvasProb1.getContext("2d");

    // Define graph settings
    const gs = {
        'ch': canvasProb1.height,    // called from HTML
        'cw': canvasProb1.width,     // called from HTML
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

    var theta = redPoint;

    // Plot each point for the showPlot layer
    points[showPlot].forEach(point => {
        pt = xyTranslate(point.x, point.y, gs);
        ctx.save();

        // Draw circle for the point
        if (point.x == redPoint) { // If the highlighted point

            // Draw arrows for the highlighted point
            let yArrow = yRange + .01;
            if (theta == 1) {
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            } else if (theta == 6) {
                drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
            } else {
                drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            }


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

function drawProbs2(showPlot, points, yticks, redPoint) {
    // Get the canvas context
    const ctx = canvasProb2.getContext("2d");

    // Define graph settings
    const gs = {
        'ch': canvasProb2.height,    // called from HTML
        'cw': canvasProb2.width,     // called from HTML
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

    var theta = redPoint;

    // Plot each point for the showPlot layer
    points[showPlot].forEach(point => {
        pt = xyTranslate(point.x, point.y, gs);
        ctx.save();

        // Draw circle for the point
        if (point.x == redPoint) { // If the highlighted point

            // Draw arrows for the highlighted point
            let yArrow = yRange + .01;
            if (theta == 1) {
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            } else if (theta == 6) {
                drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
            } else {
                drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            }


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

function drawProbs3(showPlot, points, yticks, redPoint) {
    // Get the canvas context
    const ctx = canvasProb3.getContext("2d");

    // Define graph settings
    const gs = {
        'ch': canvasProb3.height,    // called from HTML
        'cw': canvasProb3.width,     // called from HTML
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

    var theta = redPoint;

    // Plot each point for the showPlot layer
    points[showPlot].forEach(point => {
        pt = xyTranslate(point.x, point.y, gs);
        ctx.save();

        // Draw circle for the point
        if (point.x == redPoint) { // If the highlighted point

            // Draw arrows for the highlighted point
            let yArrow = yRange + .01;
            if (theta == 1) {
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            } else if (theta == 6) {
                drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
            } else {
                drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            }


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

const canvasProb1 = document.getElementById("probCanvas1");
const canvasProb2 = document.getElementById("probCanvas2");
const canvasProb3 = document.getElementById("probCanvas3");

//Initial call
drawProbs1(1,pointsx,yticksProb,0);
drawProbs2(2,pointsx,yticksProb,0);
drawProbs3(3,pointsx,yticksProb,0);