// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {

    let loginForm = document.getElementById("loginForm");
    let registerForm = document.getElementById("registerForm");

    // Utility: show error below an input with accessibility support
    function showError(inputId, message) {
        let input = document.getElementById(inputId);
        let error = input.nextElementSibling;

        // If no error span exists, create one
        if (!error || !error.classList.contains("error-text")) {
            error = document.createElement("div");
            error.className = "error-text";
            error.setAttribute("aria-live", "polite");  // screen reader support
            error.id = inputId + "-error";              // give each error a unique ID
            input.setAttribute("aria-describedby", error.id);
            input.parentNode.insertBefore(error, input.nextSibling);
        }

        error.textContent = message;
    }

    // Utility: clear error for a specific input
    function clearError(inputId) {
        let input = document.getElementById(inputId);
        let error = input.nextElementSibling;

        if (error && error.classList.contains("error-text")) {
            error.textContent = "";
        }
    }

    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            let valid = true;

            let email = document.getElementById("loginEmail").value.trim();
            let password = document.getElementById("loginPassword").value.trim();

            // Improved email regex (allows long TLDs, subdomains)
            let emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

            // Clear previous errors
            clearError("loginEmail");
            clearError("loginPassword");

            // Email validation
            if (!email) {
                showError("loginEmail", "Email is required.");
                valid = false;
            } else if (!emailPattern.test(email)) {
                showError("loginEmail", "Enter a valid email address.");
                valid = false;
            }

            // Password validation
            if (!password) {
                showError("loginPassword", "Password is required.");
                valid = false;
            } else if (password.length < 6) {
                showError("loginPassword", "Password must be at least 6 characters long.");
                valid = false;
            }

            if (!valid) e.preventDefault();
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", (e) => {
            let valid = true;

            let username = document.getElementById("username").value.trim();
            let email = document.getElementById("email").value.trim();
            let password = document.getElementById("password").value.trim();
            let confirmPassword = document.getElementById("confirmPassword").value.trim();

            let emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

            // Clear previous errors
            ["username", "email", "password", "confirmPassword"].forEach(clearError);

            // Username validation
            if (!username) {
                showError("username", "Username is required.");
                valid = false;
            }

            // Email validation
            if (!email) {
                showError("email", "Email is required.");
                valid = false;
            } else if (!emailPattern.test(email)) {
                showError("email", "Enter a valid email address.");
                valid = false;
            }

            // Password validation
            if (!password) {
                showError("password", "Password is required.");
                valid = false;
            } else if (password.length < 6) {
                showError("password", "Password must be at least 6 characters long.");
                valid = false;
            }

            // Confirm password validation
            if (!confirmPassword) {
                showError("confirmPassword", "Please confirm your password.");
                valid = false;
            } else if (password !== confirmPassword) {
                showError("confirmPassword", "Passwords do not match.");
                valid = false;
            }

            if (!valid) e.preventDefault();
        });
    }

});
