document.addEventListener("DOMContentLoaded", () => {
  // Selecting elements
  let userTypeSelect = document.getElementById('usertype');
  let userList = document.getElementById('userList');
  let userDetails = document.getElementById('userDetails');

  userTypeSelect.addEventListener('change', async function () {
    let userType = this.value;
    userList.innerHTML = "";
    userDetails.classList.remove('visible');
    userDetails.classList.add('hidden');

    if (!userType) {
      userList.innerHTML = "<p>Please select a user type.</p>";
      return;
    }

    try {
      let response = await fetch(`/get_users/${userType}`);
      let users = await response.json();

      if (users.length === 0) {
        userList.innerHTML = "<p>No users found.</p>";
        return;
      }

      users.forEach(u => {
        let div = document.createElement('div');
        div.classList.add('user-item');
        div.textContent = `${u.RegNo} — ${u.Name}`;
        div.addEventListener('click', () => loadUserDetails(u.RegNo));
        userList.appendChild(div);
      });

    } catch (err) {
      console.error(err);
      userList.innerHTML = "<p>Error fetching users.</p>";
    }
  });

  async function loadUserDetails(regno) {
    try {
      let response = await fetch(`/get_user_details/${regno}`);
      let data = await response.json();

      if (!data.RegNo) {
        alert("User not found.");
        return;
      }

      document.getElementById('regno').value = data.RegNo;
      document.getElementById('type').value = data.UserType;
      document.getElementById('name').value = data.Name;
      document.getElementById('email').value = data.Email;
      document.getElementById('phone').value = data.Phone;
      document.getElementById('address').value = data.Address;
      document.getElementById('dob').value = data.DOB;

      userDetails.classList.remove('hidden');
      setTimeout(() => userDetails.classList.add('visible'), 50);

    } catch (err) {
      console.error(err);
      alert("Failed to load user details.");
    }
  }
});
