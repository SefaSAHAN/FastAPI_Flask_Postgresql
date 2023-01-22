const baseUrl = "http://localhost:8000"; // Replace this with the correct URL of your server

// Function to display an alert message
function displayAlert(message, type) {
  const alertMessage = document.getElementById("alert-message");
  alertMessage.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

// Function to clear the input fields
function clearInputFields() {
  document.getElementById("input-id").value = "";
  document.getElementById("input-value").value = "";
  document.getElementById("update-id").value = "";
  document.getElementById("update-value").value = "";
  document.getElementById("search-id").value = "";
  document.getElementById("delete-id").value = "";
}


// Function to create an input
async function addInput() {
  const inputId = document.getElementById("input-id").value;
  const inputValue = document.getElementById("input-value").value;
  
  if (!inputId || !inputValue) {
    displayAlert("Please enter both ID and value", "danger");
    return;
  }

  if (!Number.isInteger(parseInt(inputId)) ) {
    displayAlert("Input ID should be an integer", "danger");
    return;
  }a
  
  try {
    const response = await fetch(`${baseUrl}/inputs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        id: inputId,
        input: inputValue
      })
    });
    if (response.status === 400) {
      displayAlert("There is already an input with this ID. Please use a different ID.", "danger");
    }
    else if (!response.ok) {
      const error = await response.json();
      displayAlert(error.message, "danger");
    } else {
      const data = await response.json();
      if (data.message) {
        displayAlert(data.message, "success");
        clearInputFields();
        getInputs();
      }
    }
  } catch (err) {
    displayAlert("An error occurred", "danger");
  }
}


  

// Function to get all inputs
async function getInputs() {
  try {
    const response = await fetch(`${baseUrl}/`);
    const data = await response.json();
    if (data.inputs) {
      const inputList = document.getElementById("input-list");
      inputList.innerHTML = "";
      data.inputs.forEach((input) => {
        inputList.innerHTML += `
          <tr>
            <td>${input[0]}</td>
            <td>${input[1]}</td>
            <td>${input[2]}</td>
          </tr>
        `;
      });
    } else {
      displayAlert("An error occurred", "danger");
    }
  } catch (err) {
    console.error(err);
    displayAlert("An error occurred", "danger");
  }
}


// Function to search for an input
async function searchInput() {
  const inputValue = document.getElementById("search-id").value;
  
  if (!inputValue) {
    displayAlert("Please enter an input to search", "danger");
    return;
  }
  
  try {
    const response = await fetch(`${baseUrl}/inputs/${inputValue}`);
    if (!response.ok) {
        if(response.status === 400) {
            displayAlert("No input found with this name", "danger");
        } else {
            const error = await response.json();
            displayAlert(error.message, "danger");
        }
    } else {
        const data = await response.json();
        renderInputs(data);
    }
  } catch (err) {
    console.log(err);
    displayAlert("An error occurred", "danger");
  }
}

  
function renderInputs(data) {
  const inputList = document.getElementById("input-list");
      inputList.innerHTML = "";
      data.inputs.forEach((input) => {
        inputList.innerHTML += `
          <tr>
            <td>${input[0]}</td>
            <td>${input[1]}</td>
            <td>${input[2]}</td>
          </tr>
        `;
      });
}




// Function to update an input
async function updateInput() {
  const inputId = document.getElementById("update-id").value;
  const inputValue = document.getElementById("update-value").value;
  
  if (!inputId || !inputValue) {
    displayAlert("Please enter both ID and value", "danger");
    return;
  }

  if (!Number.isInteger(parseInt(inputId)) ) {
    displayAlert("Input ID should be an integer", "danger");
    return;
  }

  try {
    const response = await fetch(`${baseUrl}/inputs/${inputId}`, {
      method: "PUT",
      body: JSON.stringify({ id: inputId, input: inputValue }),
      headers: { "Content-Type": "application/json" }
    });
    if (!response.ok) {
      if (response.status === 400) {
          displayAlert("No input found with this ID", "danger");
      } else {
          const error = await response.json();
          displayAlert(error.message, "danger");
      }
    } else {
      const data = await response.json();
      if (data.message) {
        displayAlert(data.message, "success");
        clearInputFields();
        getInputs();
      }
    }
  } catch (err) {
    displayAlert("An error occurred", "danger");
  }
}


// Function to delete an input
async function deleteInput() {
  const inputId = document.getElementById("delete-id").value;
  
  if (!inputId) {
    displayAlert("Please enter an ID", "danger");
    return;
  }

  if (!Number.isInteger(parseInt(inputId)) ) {
      displayAlert("Input ID should be an integer", "danger");
      return;
  }

  try {
      const response = await fetch(`${baseUrl}/inputs/${inputId}`, {
        method: "DELETE",
      });
      if (!response.ok) {
          if (response.status === 400) {
              displayAlert("No input found with this ID", "danger");
              return;
          }
      }
      const data = await response.json();
      if (data.message) {
        displayAlert(data.message, "success");
        clearInputFields();
        getInputs();
      }
  } catch (err) {
    displayAlert("An error occurred", "danger");
  }
}


  
  

// Add event listeners to the forms
document.getElementById("create-form").addEventListener("submit", (event) => {
    event.preventDefault();
  addInput();
});
document.getElementById("update-form").addEventListener("submit", (event) => {
  event.preventDefault();
  updateInput();
});
document.getElementById("search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  searchInput();
});
document.getElementById("delete-form").addEventListener("submit", (event) => {
  event.preventDefault();
  deleteInput();
});

// Get the inputs when the page loads
getInputs();


