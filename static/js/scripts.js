// scripts.js

// Function to update the table with localStorage data
function updateTable() {
    const tableBody = document.getElementById('localStorageTableBody');
    tableBody.innerHTML = ''; // Clear existing rows
    const tempData = JSON.parse(localStorage.getItem('tempData')) || [];

    tempData.forEach((data) => {
        // Create a new row for each item in localStorage
        const newRow = document.createElement('tr');
        newRow.innerHTML = `<td>${data.item}</td><td>${data.units}</td><td>${data.price}</td><td>${data.date}</td>`;
        tableBody.appendChild(newRow);
    });
}

function tempSend() {
    const item = document.getElementById('itemInput').value.trim();
    const units = document.getElementById('unitsInput').value.trim();
    const price = document.getElementById('priceInput').value.trim();
    const date = document.getElementById('dateInput').value.trim();

    // Validate inputs
    if (!item || !units || !price || !date) {
        showAlert("All fields must be filled.", "danger");
        return; // Exit if any field is empty
    }

    // Get existing data from localStorage, or initialize an empty array
    const tempData = JSON.parse(localStorage.getItem('tempData')) || [];
    tempData.push({ item, units, price, date }); // Add new data
    localStorage.setItem('tempData', JSON.stringify(tempData)); // Store updated data

    showAlert("Data stored in localStorage.", "success");
    updateTable(); // Update the table to reflect new data

    // Clear the input fields after storing data
    document.getElementById('itemInput').value = '';
    document.getElementById('unitsInput').value = '';
    document.getElementById('priceInput').value = '';
}

function dbSend() {
    const tempData = JSON.parse(localStorage.getItem('tempData')) || [];
    if (tempData.length === 0) {
        showAlert("No data in localStorage to send.", "danger");
        return;
    }

    fetch('/send_to_db', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: tempData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            showAlert("Data stored in the database successfully.", "success");
            localStorage.removeItem('tempData'); // Clear localStorage
            updateTable(); // Update the table to reflect data removal
        } else {
            showAlert("Error: " + data.message, "danger");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showAlert("An error occurred: " + error.message, "danger");
    });
}

function showAlert(message, type) {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type} alert-dismissible fade show`;
    alertBox.role = 'alert';
    alertBox.innerHTML = message + 
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
        '<span aria-hidden="true">&times;</span></button>';
    document.getElementById('alertContainer').appendChild(alertBox);
    setTimeout(() => {
        $(alertBox).alert('close');
    }, 3000); // Auto-close after 3 seconds
}

// Initial call to update the table on page load
document.addEventListener('DOMContentLoaded', (event) => {
    updateTable();
});

function clearLocalStorageAndRefresh() {
    localStorage.clear();
    location.reload();
}
