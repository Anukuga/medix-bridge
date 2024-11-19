async function loadTemplate(elementId, filePath, activePage = null) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) throw new Error(`Failed to load ${filePath}`);
        const htmlContent = await response.text();
        document.getElementById(elementId).innerHTML = htmlContent;

        if (elementId === "headerLoadedTemplate" && activePage) {
            setActiveLink(activePage);
        }
    } catch (error) {
        console.error(error);
    }
}

function setActiveLink(activePage) {
    const navLinks = {
        "/dashboard.html": "homeLink",
        "my-patients": "myPatientsLink",
        "register-patient": "registerPatientLink",
        "signin": "logoutLink"
    };

    const activeLinkId = navLinks[activePage];
    if (activeLinkId) {
        document.getElementById(activeLinkId).classList.add("active");
    }
}

function initMain() {
    (function ($) {
        "use strict";

        // Spinner
        const FALLBACK_TIMEOUT = 1500;

        // Fallback timeout to hide spinner if something goes wrong
        let fallbackTimeout = setTimeout(() => {
            let spinnerElement = document.getElementById("spinner");
            if (spinnerElement?.classList.contains("show")) {
                spinnerElement.classList.remove("show");
            }
        }, FALLBACK_TIMEOUT);
        
        // Hide spinner when DOM is fully loaded
        document.addEventListener("DOMContentLoaded", () => {
            let spinnerElement = document.getElementById("spinner");
            if (spinnerElement?.classList.contains("show")) {
                spinnerElement.classList.remove("show");
            }
        
            // Clear the fallback timeout since spinner is handled
            clearTimeout(fallbackTimeout);
        });

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
        const today = new Date();
        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();

        $('#calendar-prev').datetimepicker({
            viewDate: new Date(currentYear, currentMonth - 1, 1),
            format: 'L',
            inline: true,
            useCurrent: false
        });

        $('#calendar-current').datetimepicker({
            format: 'L',
            inline: true
        });

        $('#calendar-next').datetimepicker({
            viewDate: new Date(currentYear, currentMonth + 1, 1),
            format: 'L',
            inline: true,
            useCurrent: false
        });
    })(jQuery);

    // POPUPS
    function openPopup(popupId) {
        let popup = document.getElementById(popupId);
        if (popup) {
            popup.style.display = "block";
            document.body.classList.add("no-scroll");
        }
    }

    let openPopupButtons = document.querySelectorAll(".openPopupBtn");
    openPopupButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            let popupId = btn.getAttribute("data-popup-target");
            openPopup(popupId);
        });
    });

    let closeButtons = document.querySelectorAll(".popup .close");
    closeButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            btn.closest(".popup").style.display = "none";
            document.body.classList.remove("no-scroll");
        });
    });

    window.addEventListener("click", function (event) {
        if (event.target.classList.contains("popup")) {
            event.target.style.display = "none";
            document.body.classList.remove("no-scroll");
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            document.querySelectorAll(".popup").forEach(function (popup) {
                popup.style.display = "none";
                document.body.classList.remove("no-scroll");
            });
        }
    });

    // Doctor Greeting
    var greetingText = document.getElementById("doctorGreeting");
    var now = new Date();
    var hour = now.getHours();

    if (greetingText) {
        if (hour < 12) {
            greetingText.innerText = "Good morning";
        } else if (hour < 18) {
            greetingText.innerText = "Good afternoon";
        } else {
            greetingText.innerText = "Good evening";
        }
    }

    // EDIT INFO
    function setupEditToggle(editButtonId, formSelector) {
        let editButton = document.getElementById(editButtonId);
        let form = document.querySelector(formSelector);
        let inputs = form ? form.querySelectorAll("input, select, textarea") : [];

        let isEditable = false;

        function makeFieldsEditable(editable) {
            inputs.forEach(function (input) {
                input.disabled = !editable;
            });
            isEditable = editable;
        }

        makeFieldsEditable(false);

        if (editButton) {
            editButton.addEventListener("click", function () {
                makeFieldsEditable(!isEditable);
                document.getElementById("editPatientInfoBtn").style.display = "none";
                document.getElementById("updatePatientProfile").style.display = "inline-block";
            });
        }
    }

    setupEditToggle("editPatientInfoBtn", "#patientInfoForm");
    setupEditToggle("editDoctorInfoBtn", "#doctorInfoForm");

    // Image Preview
    function previewImage() {
        var input = document.getElementById("imageInput");
        var preview = document.getElementById("preview");

        if (input && input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                if (preview) {
                    preview.src = e.target.result;
                    preview.style.display = "block";
                }
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
    let togglePasswordCheckbox = document.getElementById("toggle-password");
    let passwordInput = document.getElementById("floatingPassword");

    if (togglePasswordCheckbox && passwordInput) {
        togglePasswordCheckbox.addEventListener("change", function () {
            passwordInput.type = this.checked ? "text" : "password";
        });
    }

    // Password Strength Check
    function checkPasswordStrength() {
        let password = passwordInput ? passwordInput.value : "";
        let allRequirementsMet = true;

        allRequirementsMet &= password.length >= 8;
        document.getElementById("min-length")?.classList.toggle("met", password.length >= 8);

        allRequirementsMet &= /[a-z]/.test(password);
        document.getElementById("lowercase")?.classList.toggle("met", /[a-z]/.test(password));

        allRequirementsMet &= /[A-Z]/.test(password);
        document.getElementById("uppercase")?.classList.toggle("met", /[A-Z]/.test(password));

        allRequirementsMet &= /[0-9]/.test(password);
        document.getElementById("number")?.classList.toggle("met", /[0-9]/.test(password));

        allRequirementsMet &= /[\W_]/.test(password);
        document.getElementById("special-char")?.classList.toggle("met", /[\W_]/.test(password));

        document.getElementById("signupButton").disabled = !allRequirementsMet;
    }

    passwordInput?.addEventListener("input", checkPasswordStrength);
}

(async function initializeApp() {
    const currentPath = window.location.pathname;
    const templateFolder = "/static/loadedTemplates";
    const pagesRequiringTemplates = [
        "/dashboard",
        "/my-patients",
        "/register-patient",
        "/signin"
    ];

    if (pagesRequiringTemplates.includes(currentPath)) {
        await loadTemplate("headerLoadedTemplate", `${templateFolder}/header.html`, currentPath);
        await loadTemplate("navLoadedTemplate", `${templateFolder}/nav.html`);
        await loadTemplate("footerLoadedTemplate", `${templateFolder}/footer.html`);
    }

    initMain();
})();
