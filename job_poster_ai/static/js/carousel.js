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

