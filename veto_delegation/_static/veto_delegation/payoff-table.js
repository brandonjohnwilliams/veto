const selectedX = js_vars.selectedX;

// Define your JavaScript dictionary with table values
var tableData = {
"0 widgets": ["$8", "$26", "$21", "$16", "$13", "$11", "$9"],
"1 widget": ["$12", "$30", "$25", "$20", "$15", "$12", "$10"],
"2 widgets": ["$16", "$25", "$30", "$25", "$20", "$15", "$12"],
"3 widgets": ["$20", "$20", "$25", "$30", "$25", "$20", "$15"],
"4 widgets": ["$24", "$15", "$20", "$25", "$30", "$25", "$20"],
"5 widgets": ["$28", "$12", "$15", "$20", "$25", "$30", "$25"],
"6 widgets": ["$32", "$10", "$12", "$15", "$20", "$25", "$30"],
"7 widgets": ["$36", "$9", "$10", "$12", "$15", "$20", "$25"],
"8 widgets": ["$40", "$8", "$9", "$10", "$12", "$15", "$20"]
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