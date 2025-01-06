document.addEventListener("DOMContentLoaded", function () {
    const deleteForms = document.querySelectorAll(".delete-patient-form");

    deleteForms.forEach(form => {
        form.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent form submission

            if (!confirm("Are you sure you want to delete this patient?")) {
                return; // Stop if user cancels
            }

            try {
                const response = await fetch(form.action, {
                    method: "POST"
                });

                if (response.ok) {
                    alert("Patient deleted successfully!");
                    window.location.reload(); // Refresh page after deletion
                } else {
                    alert("An error occurred while deleting the patient.");
                }
            } catch (error) {
                console.error("Error deleting patient:", error);
                alert("Failed to delete patient.");
            }
        });
    });
});
