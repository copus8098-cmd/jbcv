const form = document.getElementById("cvForm");
const iframe = document.getElementById("previewFrame");

let timeout = null;

function updatePreview() {
    const formData = new FormData(form);

    fetch("/cv/preview", {
        method: "POST",
        body: formData
    })
    .then(res => res.text())
    .then(html => {
        iframe.srcdoc = html;
    });
}

// تأخير بسيط (debounce)
form.addEventListener("input", () => {
    clearTimeout(timeout);
    timeout = setTimeout(updatePreview, 400);
});

// أول تحميل
updatePreview();
function addExperience() {
    const container = document.getElementById("experienceList");

    const div = document.createElement("div");
    div.className = "block";

    div.innerHTML = `
        <input type="text" name="experience_title[]" placeholder="Job Title">
        <input type="text" name="experience_company[]" placeholder="Company">
        <textarea name="experience_desc[]" placeholder="Description"></textarea>
        <button type="button" onclick="this.parentElement.remove()">Remove</button>
        <hr>
    `;

    container.appendChild(div);
}
function addEducation() {
    const container = document.getElementById("educationList");

    const div = document.createElement("div");
    div.className = "block";

    div.innerHTML = `
        <input type="text" name="education_degree[]" placeholder="Degree">
        <input type="text" name="education_school[]" placeholder="School">
        <input type="text" name="education_year[]" placeholder="Year">
        <button type="button" onclick="this.parentElement.remove()">Remove</button>
        <hr>
    `;

    container.appendChild(div);
}
function addProject() {
    const container = document.getElementById("projectList");

    const div = document.createElement("div");
    div.className = "block";

    div.innerHTML = `
        <input type="text" name="project_name[]" placeholder="Project Name">
        <textarea name="project_desc[]" placeholder="Description"></textarea>
        <button type="button" onclick="this.parentElement.remove()">Remove</button>
        <hr>
    `;

    container.appendChild(div);
}
function exportPDF() {
    const form = document.getElementById("cvForm");
    const formData = new FormData(form);

    fetch("/cv/export-pdf", {
        method: "POST",
        body: formData
    })
    .then(res => res.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "cv.pdf";
        a.click();
    });
}
function saveCV() {
    const form = document.getElementById("cvForm");
    const formData = new FormData(form);

    fetch("/cv/save", {
        method: "POST",
        body: formData
    })
    .then(res => res.redirected ? window.location = res.url : null);
}




