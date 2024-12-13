document.addEventListener("DOMContentLoaded", function () {
    const updatePasswordForm = document.getElementById("updatePasswordForm");
    const newPasswordInput = document.getElementById("newPassword");
    const confirmPasswordInput = document.getElementById("confirmPassword");
    const passwordError = document.getElementById("passwordError");

    // Real-time password validation
    function validatePasswords() {
        const newPassword = newPasswordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();

        if (newPassword === "" || confirmPassword === "") {
            passwordError.textContent = ""; // Clear error when fields are empty
            passwordError.style.display = "none";
            return;
        }

        if (newPassword !== confirmPassword) {
            passwordError.textContent = "Passwords do not match.";
            passwordError.style.color = "red";
            passwordError.style.display = "block";
        } else {
            passwordError.textContent = "Passwords match.";
            passwordError.style.color = "green";
            passwordError.style.display = "block";
        }
    }

    // Add event listeners for real-time validation
    newPasswordInput.addEventListener("input", validatePasswords);
    confirmPasswordInput.addEventListener("input", validatePasswords);

    // Form submission logic
    updatePasswordForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(updatePasswordForm);

        const newPassword = formData.get("new_password").trim();
        const confirmPassword = formData.get("confirm_password").trim();

        // Final check if passwords match before submission
        if (newPassword !== confirmPassword) {
            passwordError.textContent = "Passwords do not match.";
            passwordError.style.color = "red";
            passwordError.style.display = "block";
            return; // Do not proceed if passwords don't match
        }

        try {
            const response = await fetch(updatePasswordForm.action, {
                method: updatePasswordForm.method,
                body: formData,
            });
        
            if (response.ok) {
                alert("Password updated successfully!"); // Show success alert
                window.location.reload(); // Reload the page on success
            } else if (response.status === 400) {
                const data = await response.json();
                if (data.error) {
                    alert(data.error); // Show alert for incorrect old password
                } else {
                    alert("An unknown error occurred.");
                }
            } else {
                alert("An unexpected error occurred. Please try again.");
            }
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("Failed to update password. Please try again later.");
        }        
    });
});
