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
updateTableOpacity(from,to)



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
}

// This function parses values from input fields
function getParsed(currentFrom, currentTo) {
    const from = parseInt(currentFrom.value, 10);
    const to = parseInt(currentTo.value, 10);
    return [from, to];
}

// This function fills the control slider with appropriate colors
function fillSlider(from, to, sliderColor, rangeColor, controlSlider) {
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
fromSlider.oninput = () => controlFromSlider(fromSlider, toSlider);
toSlider.oninput = () => controlToSlider(fromSlider, toSlider);

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
            if (redPoint == 1) {
                drawRArrow(ctx, parseInt(redPoint) + 1, yArrow, xRange, yArrow, point.yADJ, xTextoffset, gs);
            } else if (redPoint == 6) {
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


const sliderTheta = document.getElementById("thetaRange");
var outputTheta = document.getElementById("thetaOut");

const canvasProb = document.getElementById("probCanvas");

outputTheta.innerHTML = sliderTheta.value; // Display the default slider value
// Update the current slider value (each time you drag the slider handle)
sliderTheta.oninput = function() {
    canvasProb.getContext("2d").clearRect(0, 0, canvasProb.width, canvasProb.height);
    outputTheta.innerHTML = this.value;
    drawProbs(radioX,pointsx,yticksProb,sliderTheta.value);
};

document.addEventListener("DOMContentLoaded", function() {
        var thetaRange = document.getElementById("thetaRange");
        var table = document.getElementById("payoffTable");

        thetaRange.addEventListener("input", function() {
            var thetaValue = parseInt(thetaRange.value);
            var columnToHighlight = thetaValue + 3; // Adding 2 because indexing starts from 0 and the table starts from the third column

            // Reset previous highlights
            var highlightedCells = document.querySelectorAll(".highlight");
            highlightedCells.forEach(function(cell) {
                cell.classList.remove("highlight");
            });

            // Highlight cells in the selected column
            var cellsToHighlight = document.querySelectorAll("tbody td:nth-child(" + columnToHighlight + ")");
            cellsToHighlight.forEach(function(cell) {
                cell.classList.add("highlight");
            });
        });
    });

//Initial call
drawProbs(radioX,pointsx,yticksProb,0);







function updateTableOpacity(from,to) {
    // Select the table
    var table = document.getElementById('payoffTable'); // Replace 'your_table_id' with the actual ID of your table

    // Get all rows in the table
    var rows = table.getElementsByTagName('tr');

    // Loop through each row
    for (var i = 0; i < rows.length; i++) {
        var fromADJ = from + 2;
        var toADJ = to + 4;
        var rowNumber = i + 1; // Row number starts from 1

        // Check if the row number is greater than the input "from"
        if (rowNumber >= 4 && rowNumber <= fromADJ || rowNumber >= toADJ) {
            // Set opacity to 0.15 for rows greater than "from"
            rows[i].style.opacity = 0.15;
        }
    }
}

        // var columnToHighlight = 4; // Adding 2 because indexing starts from 0 and the table starts from the third column
        //
        // // Reset previous highlights
        // var highlightedCells = document.querySelectorAll(".highlight");
        // highlightedCells.forEach(function(cell) {
        //     cell.classList.remove("highlight");
        // });
        //
        // // Highlight cells in the selected column
        // var cellsToHighlight = document.querySelectorAll("tbody td:nth-child(" + columnToHighlight + ")");
        // cellsToHighlight.forEach(function(cell) {
        //     cell.classList.add("highlight");
        // });