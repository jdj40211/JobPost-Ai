function submitLike(postNumber) {
    const headContent = document.head.innerHTML;
    const posterContainer = document.getElementById('poster-container-' + postNumber).cloneNode(true);
    const likeDislikeSection = posterContainer.querySelector('.like-dislike');
    if (likeDislikeSection) {
      likeDislikeSection.remove();
    }
    const fullHtml = `
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Póster de Vacante</title>
        ${headContent}
      </head>
      <body>
        ${posterContainer.outerHTML}
      </body>
    </html>`;
    document.getElementById('posterHtml' + postNumber).value = fullHtml;
    document.getElementById('selection' + postNumber).value = 'like';
    document.getElementById('posterHtml' + postNumber).closest('form').submit();
  }