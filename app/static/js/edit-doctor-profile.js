document.addEventListener("DOMContentLoaded", () => {
    const editButton = document.getElementById("editProfileBtn");
    const saveButton = document.getElementById("saveChangesBtn");
    const formFields = document.querySelectorAll("input:not([type='password']), select");

    // Function to toggle form field states
    function toggleFields(editable) {
        formFields.forEach(field => {
            field.disabled = !editable;
        });
    }

    // Initially disable all fields
    toggleFields(false);

    // Handle Edit button click
    editButton.addEventListener("click", () => {
        toggleFields(true);
        editButton.style.display = "none";
        saveButton.style.display = "inline-block";
    });
});