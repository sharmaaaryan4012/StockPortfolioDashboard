let timeoutSeconds = Math.floor(sessionTimeoutMs / 1000);

function updateTimer() {
    const minutes = Math.floor(timeoutSeconds / 60);
    const seconds = timeoutSeconds % 60;
    const timerElement = document.getElementById('timeout-timer');
    if (timerElement) {
        timerElement.textContent = `Timeout: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    if (timeoutSeconds > 0) {
        timeoutSeconds--;
    } else {
        clearInterval(timerInterval);
        alert("Your session has expired. You will be logged out.");
        window.location.href = "/logout"; // Redirect to logout
    }
}

const timerInterval = setInterval(updateTimer, 1000);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.update-ltp').forEach(button => {
        button.addEventListener('click', () => {
            alert('Update LTP clicked!');
        });
    });

    document.querySelectorAll('.square-off').forEach(button => {
        button.addEventListener('click', () => {
            alert('Square-off clicked!');
        });
    });
});

function sortTable(columnIndex, isNumeric = false) {
    const table = document.querySelector(".data-table tbody");
    const rows = Array.from(table.rows);

    const sortedRows = rows.sort((a, b) => {
        const cellA = a.cells[columnIndex].innerText.trim();
        const cellB = b.cells[columnIndex].innerText.trim();

        if (isNumeric) {
            const numA = parseFloat(cellA.replace(/[+%]/g, ""));
            const numB = parseFloat(cellB.replace(/[+%]/g, ""));
            return numA - numB;
        } else {
            return cellA.localeCompare(cellB);
        }
    });

    table.innerHTML = "";
    sortedRows.forEach(row => table.appendChild(row));
}

let originalTableRows = [];

// Store original table rows on page load
document.addEventListener('DOMContentLoaded', () => {
    const table = document.querySelector(".data-table tbody");
    if (table) {
        originalTableRows = Array.from(table.rows).map(row => row.cloneNode(true));
    }
});

// Reset table to its original order
function resetTable() {
    const table = document.querySelector(".data-table tbody");
    if (table && originalTableRows.length > 0) {
        table.innerHTML = ""; // Clear current rows
        originalTableRows.forEach(row => table.appendChild(row)); // Restore original rows
    }
}
