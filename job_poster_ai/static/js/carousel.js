<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", function () {
    const carousel = $('#carouselExampleSlidesOnly');
    
    // Opcional: iniciar el carrusel automáticamente
    carousel.carousel({
        interval: 3000, // Cambia cada 3 segundos
        ride: 'carousel' // Hace que comience automáticamente
    });
    
    // Opcional: pausar el carrusel al pasar el mouse encima
    carousel.on('mouseenter', function () {
        carousel.carousel('pause');
    });
    
    // Opcional: reanudar el carrusel cuando el mouse sale
    carousel.on('mouseleave', function () {
        carousel.carousel('cycle');
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const logosTrack = document.querySelector(".logo-carousel-track");
    const clone = logosTrack.cloneNode(true);
    document.querySelector(".logo-carousel").appendChild(clone);
});

=======
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
>>>>>>> d64d59ffeb4f3dc492bbc7ad27aafdaffc3d04d3
