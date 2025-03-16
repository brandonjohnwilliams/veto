// Pull variables from oTree

let radioX = js_vars.round_type;
let selectedX = js_vars.selectedX;
let from = Number(js_vars.fromM);
let to = Number(js_vars.toM)

// Function to hide or show radio buttons based on the value of `from`

const choices = document.querySelectorAll('.choices-container .choice');

function toggleRadioButtons() {
    choices.forEach(function(choice) {
        const value = parseInt(choice.getAttribute('data-value'));
        if (value === 0 || value >= from && value <= to) {
            choice.style.visibility = 'visible'; // Show radio button
        } else {
            choice.style.visibility = 'hidden'; // Hide radio button
        }
    });
}

// Initially toggle the radio buttons
toggleRadioButtons();

// Section to dynamically create the table

  // Define your JavaScript dictionary with table values
  var tableData = {
    "M=0": ["$4", "$25", "$20", "$15", "$10", "$5", "$4"],
    "M=1": ["$8", "$30", "$25", "$20", "$15", "$10", "$5"],
    "M=2": ["$12", "$25", "$30", "$25", "$20", "$15", "$10"],
    "M=3": ["$16", "$20", "$25", "$30", "$25", "$20", "$15"],
    "M=4": ["$20", "$15", "$20", "$25", "$30", "$25", "$20"],
    "M=5": ["$24", "$10", "$15", "$20", "$25", "$30", "$25"],
    "M=6": ["$28", "$5", "$10", "$15", "$20", "$25", "$30"],
    "M=7": ["$32", "$4", "$5", "$10", "$15", "$20", "$25"],
    "M=8": ["$36", "$3", "$4", "$5", "$10", "$15", "$20"]
  };

  // Function to update the Your Payoff column based on selectedX
function updateYourPayoffColumn(selectedX) {
    var yourPayoffColumnHeader = document.querySelector("#payoffTable th:nth-child(2)");

    // Check if selectedX is a valid number
    if (typeof selectedX === 'number' && selectedX >= 1 && selectedX <= 6) {
        var yourPayoffColumn = document.getElementById("selectedX");
        yourPayoffColumn.textContent = selectedX;

        // Copy the corresponding Buyer Payoff column
        var buyerPayoffColumnIndex = selectedX + 1; // Buyer Payoff columns start from index 2
        var tableRows = document.querySelectorAll("#tableBody tr");
        tableRows.forEach(function(row, index) {
            var cell = row.children[buyerPayoffColumnIndex].cloneNode(true);
            row.insertBefore(cell, row.children[1]); // Insert before the 2nd cell
        });

        // Show the Your Payoff column and header
        yourPayoffColumnHeader.style.display = '';
        var tableRows = document.querySelectorAll("#tableBody tr");
        tableRows.forEach(function(row, index) {
            row.children[1].style.display = ''; // Show the 2nd cell (Your Payoff column)
        });
    } else {
        // Populate the "Your Payoff" column with all 0 values, this allows for the spacing to remain constant
        var tableRows = document.querySelectorAll("#tableBody tr");
        tableRows.forEach(function(row, index) {
            var cell = document.createElement("td");
            cell.className = "tg-0pky";
            cell.textContent = "$0"; // Populate with 0 value
            row.insertBefore(cell, row.children[1]); // Insert before the 2nd cell
        });

        // Hide the Your Payoff column and header so that the table can be used in all pages
        yourPayoffColumnHeader.style.display = 'none';
        var tableRows = document.querySelectorAll("#tableBody tr");
        tableRows.forEach(function(row, index) {
            row.children[1].style.display = 'none'; // Hide the 2nd cell (Your Payoff column)
        });
    }
}




  // Get the table body element
  var tbody = document.getElementById("tableBody");

  // Loop through the dictionary and populate the table
Object.keys(tableData).forEach(function(key) {
    var row = document.createElement("tr");
    row.setAttribute("data-value", key.replace("M=", "")); // Ensure numeric matching


    var rowData = tableData[key];
    var cellM = document.createElement("td");
    cellM.className = "tg-0pky";
    cellM.textContent = key;
    row.appendChild(cellM);

    rowData.forEach(function(value) {
        var cell = document.createElement("td");
        cell.className = "tg-0pky";
        cell.textContent = value;
        row.appendChild(cell);
    });

    tbody.appendChild(row);
});


  updateYourPayoffColumn(selectedX); // Initial update




// This function updates the 'from' input based on user input
function controlFromSlider(fromSlider, toSlider) {
    // Extract 'from' and 'to' values from sliders
    const [from, to] = getParsed(fromSlider, toSlider);
    // Fill the control slider with appropriate colors
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
    // Update 'from' input
    if (from > to) {
        fromSlider.value = to;

        // Component to control visibility of table rows
        var rows = document.getElementById("payoffTable").rows;
        for (var i = 1; i <= rows.length - 1; i++) {
            if (i === to+3 || i===1 || i === 2) {
                rows[i].classList.remove("hidden-text");
            } else {
                rows[i].classList.add("hidden-text");
            }
        }

        console.log("From:", fromSlider.value, "To:", to);

    } else {
        fromSlider.value = from;

        // Component to control visibility of table rows
        var rows = document.getElementById("payoffTable").rows;
        for (var i = 1; i <= rows.length - 1; i++) {
            if (i >= from+2 && i <= to+2 || i===1 || i === 2) {
                rows[i].classList.remove("hidden-text");
            } else {
                rows[i].classList.add("hidden-text");
            }
        }

    }
    updateTableOpacity(from,to)
}

// This function updates the 'to' slider based on user input
function controlToSlider(fromSlider, toSlider) {
    // Extract 'from' and 'to' values from sliders
    const [from, to] = getParsed(fromSlider, toSlider);
    // Fill the control slider with appropriate colors
    fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
    // Make 'to' slider accessible
    setToggleAccessible(toSlider);
    // Update 'to' slider and input
    if (from <= to) {
        toSlider.value = to;

        // Component to control visibility of table rows
        var rows = document.getElementById("payoffTable").rows;
        for (var i = 1; i <= rows.length - 1; i++) {
            if (i >= from+2 && i <= to+2 || i===1 || i === 2) {
                rows[i].classList.remove("hidden-text");
            } else {
                rows[i].classList.add("hidden-text");
            }
        }

    } else {
        toSlider.value = from;
    }
    updateTableOpacity(from,to)
}

// This function parses values from input fields
function getParsed(currentFrom, currentTo) {
    const from = parseInt(currentFrom.value, 10);
    const to = parseInt(currentTo.value, 10);
    return [from, to];
}

// This function fills the control slider with appropriate colors
function fillSlider(from, to, sliderColor, rangeColor, controlSlider) {
    // Check if inputs exist and have valid properties
    if (!from || !to || !controlSlider || isNaN(from.value) || isNaN(to.value)) {
        return; // Exit the function early
    }

    const rangeDistance = to.max - to.min;
    const fromPosition = from.value - to.min;
    const toPosition = to.value - to.min;

    controlSlider.style.background = `linear-gradient(
      to right,
      ${sliderColor} 0%,
      ${sliderColor} ${(fromPosition / rangeDistance) * 100}%,
      ${rangeColor} ${((fromPosition / rangeDistance) * 100)}%,
      ${rangeColor} ${(toPosition / rangeDistance) * 100}%,
      ${sliderColor} ${(toPosition / rangeDistance) * 100}%,
      ${sliderColor} 100%)`;
}


// This function sets the accessibility of the 'to' slider
function setToggleAccessible(currentTarget) {
    if (!currentTarget) {
        return; // Exit the function early
    }
    const toSlider = document.querySelector('#toSlider');
    if (Number(currentTarget.value) <= 0) {
        toSlider.style.zIndex = 2;
    } else {
        toSlider.style.zIndex = 0;
    }
}


const fromSlider = document.getElementById('fromSlider');
const toSlider = document.querySelector('#toSlider');

const fromValueDisplay = document.getElementById('fromValue');
const toValueDisplay = document.getElementById('toValue');

// Update the displayed values when sliders are moved
if (fromSlider && toSlider && fromValueDisplay && toValueDisplay) {
    fromSlider.addEventListener('input', function() {
        fromValueDisplay.textContent = "Min: " + this.value;
    });

    toSlider.addEventListener('input', function() {
        toValueDisplay.textContent = "Max: " + this.value;
    });
}


// Initialize slider colors and accessibility
fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);
setToggleAccessible(toSlider);

// Event listeners for input changes
// Check if the sliders exist before adding event listeners
if (typeof fromSlider !== "undefined" && fromSlider) {
    fromSlider.oninput = () => controlFromSlider(fromSlider, toSlider);
} else {
}

if (typeof toSlider !== "undefined" && toSlider) {
    toSlider.oninput = () => controlToSlider(fromSlider, toSlider);
} else {
}


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
    ctx.textAlign = "center";
    if (x1 == 1) {
        ctx.fillText("Probability below " + atPT + " is " + arrowText, (pt1.cx + pt0.cx) / 2 +50, (pt1.cy + pt0.cy) / 2 - xOff);
    } else {
        ctx.fillText("Probability below " + atPT + " is " + arrowText, (pt1.cx + pt0.cx) / 2, (pt1.cy + pt0.cy) / 2 - xOff);
    }
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
    ctx.lineTo(pt1.cx +12, pt1.cy);
    ctx.lineTo(pt1.cx + headlen * Math.cos(angle - Math.PI / 6) +12, pt1.cy + headlen * Math.sin(angle - Math.PI / 6));
    ctx.moveTo(pt1.cx+12, pt1.cy);
    ctx.lineTo(pt1.cx + headlen * Math.cos(angle + Math.PI / 6) +12, pt1.cy + headlen * Math.sin(angle + Math.PI / 6));
    ctx.moveTo(pt0.cx - headlen * Math.sin(angle), pt0.cy - headlen * Math.cos(angle));
    ctx.lineTo(pt0.cx + headlen * Math.sin(angle), pt0.cy + headlen * Math.cos(angle));

    // Stroke the lines
    ctx.stroke();

    // Set text properties and position
    ctx.fillStyle = "black";
    ctx.font = axisTextSize;
    ctx.textAlign = "left";
    if (x1 == 6) {
        ctx.fillText("Probability above " + atPT + " is " + arrowText, (pt1.cx + pt0.cx) / 2 - 150 , (pt1.cy + pt0.cy) / 2 - xOff);
    } else {
        ctx.fillText("Probability above " + atPT + " is " + arrowText, (pt1.cx + pt0.cx) / 2 - 100, (pt1.cy + pt0.cy) / 2 - xOff);
    }
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

function drawProbs(showPlot, points, yticks, redPoint) {
    // Exit if canvasProb is not available
    if (typeof canvasProb === "undefined" || !canvasProb) return;

    // Get the canvas context and exit if not available
    const ctx = canvasProb.getContext("2d");
    if (!ctx) return;

    // Exit if points or the requested showPlot layer is missing
    if (!points || !points[showPlot]) return;

    // Define graph settings
    const gs = {
        'ch': canvasProb.height,    // Called from HTML
        'cw': canvasProb.width,     // Called from HTML
        'bw': 60,                   // Bar width
        'xMin': 1,                  // X-axis minimum value
        'xMax': xRange,             // X-axis maximum value
        'yMin': 0,                  // Y-axis minimum value
        'yMax': yRange              // Y-axis maximum value
    };

    // Offset for x-axis labels
    const xTextoffset = 30;

    // Set the stroke style for the context
    ctx.strokeStyle = "black";

    // Draw the base line of the graph
    drawLine(ctx, 1, 0, xRange, 0, gs);

    // Draw the yTicks
    drawTicks(ctx, yticks, gs, xTextoffset);

    // Label the x-axis for each point in the current layer
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
        const pt = xyTranslate(point.x, point.y, gs);
        ctx.save();

        // If this is the highlighted point, apply special styling and draw arrows
        if (point.x == redPoint) {
            let yArrow = yRange + 0.01;
            if (redPoint == 1) {
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            } else if (redPoint == 6) {
                drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
            } else {
                drawLArrow(ctx, parseInt(redPoint) - 1, yArrow, 0.9, yArrow, point.yCDF, xTextoffset, gs);
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            }

            ctx.strokeStyle = "black";
            ctx.shadowColor = "gray";
            ctx.fillStyle = "red";
            ctx.shadowOffsetX = 5;
            ctx.shadowOffsetY = 5;
            ctx.shadowBlur = 4;

            ctx.font = axisTextSize;
            ctx.textAlign = "center";
            ctx.fillText(point.yPT, pt.cx + 10, pt.cy - 15);
        } else { // For non-highlighted points
            ctx.strokeStyle = "gray";
            ctx.fillStyle = "blue";
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 0;
            ctx.shadowBlur = 0;
        }

        // Draw the stem line and the point
        drawLine(ctx, point.x, 0, point.x, point.y, gs);
        drawPoint(ctx, point.x, point.y, 7, gs);
        ctx.restore();
    });
}



const sliderTheta = document.getElementById("thetaRange");
var outputTheta = document.getElementById("thetaOut");

const canvasProb = document.getElementById("probCanvas");

// Check if elements exist before setting the value
if (typeof outputTheta !== "undefined" && outputTheta && typeof sliderTheta !== "undefined" && sliderTheta) {
    outputTheta.innerHTML = sliderTheta.value; // Display the default slider value
} else {
}

// Check if sliderTheta exists before adding event listener
if (typeof sliderTheta !== "undefined" && sliderTheta) {
    sliderTheta.oninput = function() {
        // Ensure canvasProb and its context exist before clearing
        if (typeof canvasProb !== "undefined" && canvasProb) {
            const ctx = canvasProb.getContext("2d");
            if (ctx) ctx.clearRect(0, 0, canvasProb.width, canvasProb.height);
        }

        // Update the output if it exists
        if (typeof outputTheta !== "undefined" && outputTheta) {
            outputTheta.innerHTML = this.value;
        }

        // Ensure drawProbs function exists before calling it
        if (typeof drawProbs === "function") {
            drawProbs(radioX, pointsx, yticksProb, sliderTheta.value);
        }
    };
}


// Function to update the location text based on radioX value
function updateLocationAndDice() {
    let locationElement = document.getElementById("location");
    let diceContainer = document.getElementById("dice-container");

    // Ensure the elements exist before proceeding
    if (!locationElement || !diceContainer) return;

    // Update location text
    let locationText = radioX === 1 ? "lowest" : radioX === 2 ? "middle" : "highest";
    locationElement.textContent = locationText;

    // Update dice order
    let diceHtml = "";

    if (radioX === 1) {
        diceHtml = `
            <span class="die-number-red"></span> ≤ 
            <span class="die-number-white"></span> ≤ 
            <span class="die-number-white"></span>
        `;
    } else if (radioX === 2) {
        diceHtml = `
            <span class="die-number-white"></span> ≤ 
            <span class="die-number-red"></span> ≤ 
            <span class="die-number-white"></span>
        `;
    } else if (radioX === 3) {
        diceHtml = `
            <span class="die-number-white"></span> ≤ 
            <span class="die-number-white"></span> ≤ 
            <span class="die-number-red"></span>
        `;
    }

    diceContainer.innerHTML = diceHtml;
}


// Run the function when the page loads
window.onload = updateLocationAndDice;


document.addEventListener("DOMContentLoaded", function() {
    var thetaRange = document.getElementById("thetaRange");
    var table = document.getElementById("payoffTable");

    // Ensure thetaRange and table exist before adding event listener
    if (thetaRange && table) {
        thetaRange.addEventListener("input", function() {
            var thetaValue = parseInt(thetaRange.value);
            var columnToHighlight = thetaValue + 3; // Adjust column index dynamically

            var rows = table.querySelectorAll("tbody tr"); // Target only body rows
            var headers = table.querySelectorAll("thead th"); // Target header cells

            // Reset all cell borders in the body rows
            rows.forEach(row => {
                row.querySelectorAll("td").forEach(cell => cell.style.border = "");
            });

            // Reset all header borders
            headers.forEach(header => header.style.border = "");

            // Apply borders to the selected column
            rows.forEach((row, rowIndex) => {
                var cells = row.querySelectorAll("td");
                if (cells.length >= columnToHighlight) { // Ensure the row has enough cells
                    var cell = cells[columnToHighlight - 1]; // Adjust for 0-based index
                    if (cell) {
                        if (rowIndex === 0) {
                            cell.style.borderLeft = "2px solid red";
                            cell.style.borderRight = "2px solid red";
                        } else if (rowIndex === rows.length - 1) {
                            cell.style.borderBottom = "2px solid red";
                            cell.style.borderLeft = "2px solid red";
                            cell.style.borderRight = "2px solid red";
                        } else {
                            cell.style.borderLeft = "2px solid red";
                            cell.style.borderRight = "2px solid red";
                        }
                    }
                }
            });

            // Highlight the corresponding header with X= in the text
            const headerToHighlight = Array.from(headers).find(header => header.textContent.trim() === `X=${thetaValue}`);
            if (headerToHighlight) {
                headerToHighlight.style.borderTop = "2px solid red";
                headerToHighlight.style.borderLeft = "2px solid red";
                headerToHighlight.style.borderRight = "2px solid red";
            }
        });
    }
});



//Initial call
drawProbs(radioX,pointsx,yticksProb,0);

function updateTableOpacity(from, to) {
    // Select the table
    var table = document.getElementById('payoffTable');

    // Get all rows in the table
    var rows = table.getElementsByTagName('tr');

    // Adjust row numbers based on "from" and "to"
    var fromADJ = from + 3;
    var toADJ = to + 4;

    // Loop through each row and update opacity
    for (var i = 0; i < rows.length; i++) {
        var rowNumber = i + 1; // Row number starts from 1

        // Rows less than 4 should always have full opacity
        if (rowNumber < 4 || (rowNumber >= fromADJ && rowNumber < toADJ)) {
            rows[i].style.opacity = "1";  // Fully visible
        } else {
            rows[i].style.opacity = "0.15"; // Faded
        }
    }
}



function shadeColumnsByYPT(radioX) {
    // Get the corresponding pointsx array
    const selectedPoints = pointsx[radioX];
    if (!selectedPoints) return;

    // Loop through columns (1 to 6)
    selectedPoints.forEach(point => {
        const columnIndex = point.x + 3; // Offset for table cells
        const yPTValue = parseFloat(point.yPT) / 100; // Convert yPT to a decimal (e.g., 42.13% -> 0.4213)

        // Select all cells in the column
        const columnCells = document.querySelectorAll(`#payoffTable tr td:nth-child(${columnIndex})`);

        // Select the header based on text content
        const columnHeaders = document.querySelectorAll(`#payoffTable th`);
        let columnHeader = null;
        columnHeaders.forEach(header => {
            if (header.textContent.trim() === `X=${point.x}`) {
                columnHeader = header;
            }
        });

        // Apply background color with opacity for all cells
        columnCells.forEach(cell => {
            cell.style.backgroundColor = `rgba(0, 0, 255, ${yPTValue})`; // Blue with variable opacity
        });

        // Apply to column header
        if (columnHeader) {
            columnHeader.style.backgroundColor = `rgba(0, 0, 255, ${yPTValue})`;
        }
    });
}

// Example usage
shadeColumnsByYPT(js_vars.round_type); // Call with the current round_type value

document.addEventListener("DOMContentLoaded", function () {
    const choices = document.querySelectorAll(".choice");
    const rows = document.querySelectorAll("#tableBody tr");

    choices.forEach(choice => {
        choice.addEventListener("click", function () {

            // Remove 'selected' class from all choices
            choices.forEach(c => c.classList.remove("selected"));

            // Add 'selected' class to the clicked choice
            this.classList.add("selected");

            // Get the selected value
            let selectedValue = this.getAttribute("data-value");

            // Remove highlight from all rows
            rows.forEach(row => row.classList.remove("highlighted-row"));

            // Highlight the corresponding row
            let selectedRow = document.querySelector(`#tableBody tr[data-value="${selectedValue}"]`);

            if (selectedRow) {
                selectedRow.classList.add("highlighted-row");
            } else {
                console.error("No matching row found for data-value:", selectedValue);
            }
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const choices = document.querySelectorAll(".choice");
    const response = document.getElementById("response");

    choices.forEach(choice => {
        choice.addEventListener("click", function () {
            // Remove 'selected' class from all choices
            choices.forEach(c => c.classList.remove("selected"));

            // Add 'selected' class to the clicked choice
            this.classList.add("selected");

            // Get the selected value and update the hidden input field
            let selectedValue = this.getAttribute("data-value");
            response.value = selectedValue;

        });
    });
});


// Hides the back columns on the buyer page

function adjustTableColumns(pageType) {
    const table = document.getElementById("payoffTable");
    if (!table) return; // Exit if table is not found

    const headers = table.querySelectorAll("thead th");
    const rows = table.querySelectorAll("tbody tr");

    if (pageType === "limited") { // Define the condition for hiding columns
        // Hide headers for Buyer Payoff columns
        headers.forEach((header, index) => {
            if (index >= 3) {
                header.style.display = "none";
            }
        });

        // Hide corresponding columns in each row
        rows.forEach(row => {
            row.querySelectorAll("td").forEach((cell, index) => {
                if (index >= 3) {
                    cell.style.display = "none";
                }
            });
        });
    }
}

const response = js_vars.response
if (response === 1) {
    adjustTableColumns("limited"); // Change "limited" dynamically based on the page type
}

updateTableOpacity(1,8)

const single = js_vars.single;

function updateSliders() {
    if (single === 1) {
        // Fully hide fromSlider and remove it from pointer interactions
        fromSlider.disabled = true;
        fromSlider.style.opacity = "0";
        fromSlider.style.pointerEvents = "none";
        fromSlider.style.visibility = "hidden";
        fromSlider.style.width = "0";
        fromSlider.style.height = "0";
        fromSlider.style.position = "absolute";
        fromSlider.style.zIndex = "-1";

        toValueDisplay.style.display = "none"; // Hide max value label

        updateTableOpacity(8, 8);

        // Ensure toSlider moves alone, and fromSlider follows it
        toSlider.oninput = function () {
            const to = parseInt(toSlider.value, 10);
            fromSlider.value = to; // Sync fromSlider with toSlider
            fromValueDisplay.textContent = "Value: " + to;

            // Ensure the slider bar is filled correctly
            fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);

            // Call updateTableOpacity with from = to
            updateTableOpacity(to, to);
        };

    }
}

// Call function on page load
updateSliders();




