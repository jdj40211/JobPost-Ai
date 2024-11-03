const carousel = document.querySelector('.carousel');
let scrollPosition = 0;

window.addEventListener('wheel', (event) => {
    // Ajusta la cantidad de desplazamiento (puedes modificar el valor para aumentar o reducir la sensibilidad)
    const scrollAmount = 30;

    if (event.deltaY > 0) {
        // Scroll hacia abajo, mueve el carrusel a la izquierda
        scrollPosition -= scrollAmount;
    } else {
        // Scroll hacia arriba, mueve el carrusel a la derecha
        scrollPosition += scrollAmount;
    }

    // Limita el scroll para evitar que se salga de los elementos
    scrollPosition = Math.min(scrollPosition, 0);
    scrollPosition = Math.max(scrollPosition, -carousel.scrollWidth + carousel.offsetWidth);

    carousel.style.transform = `translateX(${scrollPosition}px)`;
});
