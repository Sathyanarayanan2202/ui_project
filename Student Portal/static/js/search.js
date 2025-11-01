document.addEventListener("DOMContentLoaded", () => {
  // Selecting elements
  let userTypeSelect = document.getElementById("usertype");
  let userList = document.getElementById("user-list");
  let detailsContainer = document.getElementById("details");

  // When user type (Student/Teacher) is changed
  userTypeSelect.addEventListener("change", () => {
    let userType = userTypeSelect.value;
    if (!userType) return;

    // Fetch list of users from Flask
    fetch(`/get_users/${userType}`)
      .then(response => response.json())
      .then(users => {
        // Clear old list and details
        userList.innerHTML = "";
        detailsContainer.innerHTML = "";

        // Create clickable list items for each user
        users.forEach(user => {
          let li = document.createElement("li");
          li.textContent = `${user.Name} (${user.RegNo})`;
          li.classList.add("user-item");

          // On click → show user details
          li.addEventListener("click", () => showDetails(user.RegNo));
          userList.appendChild(li);
        });
      });
  });

  // Function to fetch and display user details (like an application form)
  function showDetails(regno) {
    fetch(`/get_user_details/${regno}`)
      .then(response => response.json())
      .then(data => {
        if (!data.RegNo) {
          detailsContainer.innerHTML = "<p>No data found.</p>";
          return;
        }

        // Display non-editable data in application form style
        detailsContainer.innerHTML = `
          <div class="application-form">
            <h3>Application Form</h3>
            <p><strong>Reg No:</strong> ${data.RegNo}</p>
            <p><strong>User Type:</strong> ${data.UserType}</p>
            <p><strong>Name:</strong> ${data.Name}</p>
            <p><strong>Email:</strong> ${data.Email}</p>
            <p><strong>Phone:</strong> ${data.Phone}</p>
            <p><strong>Address:</strong> ${data.Address}</p>
            <p><strong>Date of Birth:</strong> ${data.DOB}</p>
          </div>
        `;
      });
  }
});
