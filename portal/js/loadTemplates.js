async function loadTemplate(elementId, filePath, activePage = null) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) throw new Error(`Failed to load ${filePath}`);
        const htmlContent = await response.text();
        document.getElementById(elementId).innerHTML = htmlContent;

        if (elementId === "header" && activePage) {
            setActiveLink(activePage);
        }
    } catch (error) {
        console.error(error);
    }
}

function setActiveLink(activePage) {
    const navLinks = {
        "/portal/index.html": "homeLink",
        "/portal/my-patients.html": "myPatientsLink",
        "/portal/register-patient.html": "registerPatientLink",
        "/portal/signin.html": "logoutLink"
    };

    const activeLinkId = navLinks[activePage];
    if (activeLinkId) {
        document.getElementById(activeLinkId).classList.add("active");
    }
}

const currentPath = window.location.pathname;
const templateFolder = "loadedTemplates";

(async function () {
    await loadTemplate("header", `${templateFolder}/header.html`, currentPath);
    await loadTemplate("nav", `${templateFolder}/nav.html`);
    await loadTemplate("footer", `${templateFolder}/footer.html`);

    initMain();
})();
