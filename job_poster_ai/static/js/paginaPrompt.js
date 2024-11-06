// Espera a que el DOM esté cargado
document.addEventListener("DOMContentLoaded", function () {
    // Obtén el formulario y la pantalla de carga
    var form = document.querySelector("form");
    var loadingScreen = document.getElementById("loading-screen");

    // Agrega un evento al enviar el formulario
    form.addEventListener("submit", function () {
        // Muestra la pantalla de carga
        loadingScreen.classList.remove("d-none");
    });
});

// Oculta la pantalla de carga cuando la página haya terminado de cargar
window.onload = function () {
    var loadingScreen = document.getElementById("loading-screen");
    loadingScreen.classList.add("d-none");
};
