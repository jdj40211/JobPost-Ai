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



const dateElement = document.getElementById('current-date');
const today = new Date();
const options = { year: 'numeric', month: 'long', day: 'numeric' };
dateElement.textContent = today.toLocaleDateString('en-US', options);