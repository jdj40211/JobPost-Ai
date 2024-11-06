// ver_post.js

// Función para mostrar la previsualización según la red social seleccionada
function showPreview(platform) {
    const previewContainer = document.getElementById('preview-container');
    let content = '';

    switch (platform) {
        case 'instagram':
            content = `
                <!-- Contenido de la previsualización de Instagram -->
                <h2>Previsualización de Instagram</h2>
                <div class="instagram-preview">
                    <!-- Aquí insertas tu plantilla de Instagram -->
                    <div class="border rounded shadow p-3">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fa-brands fa-instagram me-2"></i>
                                <div>
                                    <strong>Instagram</strong><br>
                                    <span>Magneto</span>
                                </div>
                            </div>
                            <i class="fa-solid fa-ellipsis-vertical"></i>
                        </div>
                        <div class="poster-dynamic-content">
                            {{ poster_html|safe }}
                        </div>
                        <div class="d-flex justify-content-between align-items-center mt-3">
                            <div>
                                <i class="fa-regular fa-heart me-3"></i>
                                <i class="fa-regular fa-comment me-3"></i>
                                <i class="fa-regular fa-paper-plane"></i>
                            </div>
                            <i class="fa-regular fa-bookmark"></i>
                        </div>
                        <div class="mt-3">
                            <p>Liked by <strong>Magneto</strong>, <strong>HTML5</strong>, <strong>Web</strong> and
                                <strong>100,000 others</strong>
                            </p>
                            <p>{{ job_description }}</p>
                        </div>
                    </div>
                </div>
                <!-- Botón para publicar en Instagram -->
                <div class="text-center mt-4">
                    <button class="btn btn-primary mx-2" onclick="publicarEnInstagram()">Publicar en Instagram</button>
                </div>
            `;
            break;
        case 'facebook':
            content = `
                <!-- Contenido de la previsualización de Facebook -->
                <h2>Previsualización de Facebook</h2>
                <div class="facebook-preview">
                    <!-- Aquí insertas tu plantilla de Facebook -->
                    <div class="border rounded shadow p-3">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <div class="d-flex align-items-center">
                                <img src="{% static 'images/author-pic.jpg' %}" class="rounded-circle me-2" width="40"
                                    height="40">
                                <div>
                                    <strong><a href="#">Magneto</a></strong><br>
                                    <small id="current-date"></small>
                                </div>
                            </div>
                            <i class="fa-solid fa-ellipsis-vertical"></i>
                        </div>
                        <div class="poster-dynamic-content">
                            {{ poster_html|safe }}
                        </div>
                        <div class="mt-3">
                            <p class="mb-1">{{ job_description }}</p>
                        </div>
                        <div class="d-flex justify-content-between mt-3">
                            <span class="text-muted"><a href="#">193K</a> reactions</span>
                            <span class="text-muted"><a href="#">50K Comments</a> · <a href="#">5.4K Shares</a></span>
                        </div>
                        <div class="d-flex justify-content-around mt-2">
                            <button class="btn btn-light w-100 me-2"><i class="fa-regular fa-thumbs-up"></i>
                                Like</button>
                            <button class="btn btn-light w-100 me-2"><i class="fa-regular fa-comment"></i>
                                Comment</button>
                            <button class="btn btn-light w-100"><i class="fa-solid fa-share"></i> Share</button>
                        </div>
                    </div>
                </div>
                <!-- Botón para publicar en Facebook -->
                <div class="text-center mt-4">
                    <button class="btn btn-primary mx-2" onclick="publicarEnFacebook()">Publicar en Facebook</button>
                </div>
            `;
            break;
        case 'whatsapp':
            content = `
                <!-- Contenido de la previsualización de WhatsApp -->
                <h2>Previsualización de WhatsApp</h2>
                <p>Así se vería tu post en WhatsApp.</p>
                <!-- Agrega el contenido que desees -->
            `;
            break;
        case 'gmail':
            content = `
                <!-- Contenido de la previsualización de Gmail -->
                <h2>Previsualización de Gmail</h2>
                <p>Así se vería tu post en un correo de Gmail.</p>
                <!-- Agrega el contenido que desees -->
            `;
            break;
        default:
            content = `<p>Selecciona una red social para ver la previsualización.</p>`;
    }

    // Actualizamos el contenido del contenedor de previsualización
    previewContainer.innerHTML = content;

    // Si la plataforma es Facebook, actualizar la fecha
    if (platform === 'facebook') {
        // Esperar a que el contenido se haya insertado en el DOM
        const dateElement = document.getElementById('current-date');
        if (dateElement) {
            const today = new Date();
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            dateElement.textContent = today.toLocaleDateString('es-ES', options);
        }
    }
}

// Función para publicar en Instagram
function publicarEnInstagram() {
    const imageUrl = "{{ image_url }}";
    const caption = "{{ job_description }}";

    fetch("{% url 'publicar_poster_instagram' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({
            image_url: imageUrl,
            caption: caption
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("El post se ha publicado exitosamente en Instagram.");
            } else {
                alert("Error al publicar el post: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error al publicar en Instagram:", error);
            alert("Ocurrió un error al intentar publicar en Instagram.");
        });
}

// Función para publicar en Facebook (puedes implementar esta función según tus necesidades)
function publicarEnFacebook() {
    const imageUrl = "{{ image_url }}";
    const caption = "{{ job_description }}";

    fetch("{% url 'publicar_poster_facebook' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({
            image_url: imageUrl,
            caption: caption
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("El post se ha publicado exitosamente en Facebook.");
            } else {
                alert("Error al publicar el post: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error al publicar en Facebook:", error);
            alert("Ocurrió un error al intentar publicar en Facebook.");
        });
}

// Establecer la fecha actual si está presente el elemento con id 'current-date'
document.addEventListener('DOMContentLoaded', function () {
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        const today = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = today.toLocaleDateString('es-ES', options);
    }
});
