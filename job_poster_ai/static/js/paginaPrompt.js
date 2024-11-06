// paginaPrompt.js

// Espera a que el DOM esté cargado
document.addEventListener("DOMContentLoaded", function () {
    // Obtener el formulario y la pantalla de carga
    var form = document.querySelector("form");
    var loadingScreen = document.getElementById("loading-screen");

    // Agrega un evento al enviar el formulario
    form.addEventListener("submit", function () {
        // Muestra la pantalla de carga
        loadingScreen.classList.remove("d-none");
    });

    // Obtener el input de archivo y el contenedor de carga
    var fileInput = document.getElementById("job_file");
    var uploadContainer = document.getElementById("upload-container");

    // Agregar un evento al cambiar el input de archivo
    fileInput.addEventListener("change", function () {
        if (fileInput.files && fileInput.files.length > 0) {
            // Si se ha seleccionado un archivo, agregar la clase
            uploadContainer.classList.add("file-selected");
        } else {
            // Si no hay archivos seleccionados, remover la clase
            uploadContainer.classList.remove("file-selected");
        }
    });
});

// Oculta la pantalla de carga cuando la página haya terminado de cargar
window.onload = function () {
    var loadingScreen = document.getElementById("loading-screen");
    loadingScreen.classList.add("d-none");
};
