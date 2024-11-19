(function ($) {
    "use strict";

    // Spinner
    let spinner = function () {
        setTimeout(function () {
            if ($("#spinner").length > 0) {
                $("#spinner").removeClass("show");
            }
        }, 1);
    };
    spinner();

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $(".back-to-top").fadeIn("slow");
        } else {
            $(".back-to-top").fadeOut("slow");
        }
    });
    $(".back-to-top").click(function () {
        $("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
        return false;
    });

    // Sidebar Toggler
    $(".sidebar-toggler").click(function () {
        $(".sidebar, .content").toggleClass("open");
        return false;
    });

    // Calendar
    $("#calendar").datetimepicker({
        inline: true,
        format: "L",
    });
})(jQuery);

// POPUPS
document.addEventListener("DOMContentLoaded", function () {
    // Function to open a popup
    function openPopup(popupId) {
        let popup = document.getElementById(popupId);
        if (popup) {
            popup.style.display = "block";
            document.body.classList.add("no-scroll");
        }
    }

    // Attach event listeners to open popup buttons
    let openPopupButtons = document.querySelectorAll(".openPopupBtn");
    openPopupButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            let popupId = btn.getAttribute("data-popup-target");
            openPopup(popupId);
        });
    });

    // Attach event listeners to close buttons in each popup
    let closeButtons = document.querySelectorAll(".popup .close");
    closeButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            btn.closest(".popup").style.display = "none";
            document.body.classList.remove("no-scroll");
        });
    });

    // Close popup when clicking outside of it
    window.addEventListener("click", function (event) {
        if (event.target.classList.contains("popup")) {
            event.target.style.display = "none";
            document.body.classList.remove("no-scroll");
        }
    });

    // Close popup when pressing the Escape key
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            document.querySelectorAll(".popup").forEach(function (popup) {
                popup.style.display = "none";
                document.body.classList.remove("no-scroll");
            });
        }
    });
});

// Doctor Greeting
document.addEventListener("DOMContentLoaded", function () {
    var greetingText = document.getElementById("doctorGreeting");
    var now = new Date();
    var hour = now.getHours();

    if (hour < 12) {
        greetingText.innerText = "Good morning";
    } else if (hour < 18) {
        greetingText.innerText = "Good afternoon";
    } else {
        greetingText.innerText = "Good evening";
    }
});

// EDIT INFO
document.addEventListener("DOMContentLoaded", function () {
    function setupEditToggle(editButtonId, popupSelector) {
        let editButton = document.getElementById(editButtonId);
        let popup = document.querySelector(popupSelector);
        let inputs = popup.querySelectorAll("input, select, textarea");

        let isEditable = false;

        function makeFieldsEditable(editable) {
            inputs.forEach(function (input) {
                input.disabled = !editable;
            });
            isEditable = editable;
        }

        // Initially, make fields not editable
        makeFieldsEditable(false);

        editButton.addEventListener("click", function () {
            makeFieldsEditable(!isEditable);
            document.getElementById("editPatientInfoBtn").style.display = "none";
            document.getElementById("updatePatientProfile").style.display =
                "inline-block";
        });
    }

    // Setup for Patient Info Edit Button
    setupEditToggle("editPatientInfoBtn", "#patientInfoPopup");
    setupEditToggle("editDoctorInfoBtn", "#doctorInfoPopup form");

    // Additional setups for other forms can be added in a similar way
});

// Image Preview
function previewImage() {
    var input = document.getElementById("imageInput");
    var preview = document.getElementById("preview");

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";
        };

        reader.readAsDataURL(input.files[0]);
    }
}

// Welcome Back Message (Based on Session Cookie)
function getCookie(cookieName) {
    var name = cookieName + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(";");
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// Toggle Show Password
document
    .getElementById("toggle-password")
    .addEventListener("change", function () {
        var passwordInput = document.getElementById("floatingPassword");
        if (this.checked) {
            passwordInput.type = "text";
        } else {
            passwordInput.type = "password";
        }
    });

// Password Strength Check
function checkPasswordStrength() {
    var password = document.getElementById("floatingPassword").value;
    var allRequirementsMet = true;

    // Check each requirement
    allRequirementsMet &= password.length >= 8;
    document
        .getElementById("min-length")
        .classList.toggle("met", password.length >= 8);

    allRequirementsMet &= /[a-z]/.test(password);
    document
        .getElementById("lowercase")
        .classList.toggle("met", /[a-z]/.test(password));

    allRequirementsMet &= /[A-Z]/.test(password);
    document
        .getElementById("uppercase")
        .classList.toggle("met", /[A-Z]/.test(password));

    allRequirementsMet &= /[0-9]/.test(password);
    document
        .getElementById("number")
        .classList.toggle("met", /[0-9]/.test(password));

    allRequirementsMet &= /[\W_]/.test(password);
    document
        .getElementById("special-char")
        .classList.toggle("met", /[\W_]/.test(password));

    // Enable or disable the sign-in button
    document.getElementById("signupButton").disabled = !allRequirementsMet;
}

document
    .getElementById("floatingPassword")
    .addEventListener("input", checkPasswordStrength);