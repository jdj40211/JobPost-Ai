from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import requests
from django.conf import settings
from django.urls import reverse
import os
from urllib.parse import quote, unquote
from docx import Document
import PyPDF2
from openai import OpenAI
import openai
import os
import google.generativeai as genai

# Configura tu clave API de OpenAI
genai.configure(api_key='AIzaSyDVjet7JX0216nprw9KRWozDzckWeUoOgE')

def generar_imagen_vyro(descripcion, api_token):
    url = 'https://api.vyro.ai/v1/imagine/api/generations'

    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    payload = {
        'prompt': (None, descripcion),
        'style_id': (None, '29'),
        'aspect_ratio': (None, '9:16')
    }

    response = requests.post(url, headers=headers, files=payload)

    if response.status_code == 200:
        # Nombre y ruta del archivo a guardar
        file_name = 'image.jpg'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Guardar el contenido de la imagen en el archivo
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # Retornar la URL relativa a la imagen usando MEDIA_URL
        image_url = os.path.join(settings.MEDIA_URL, file_name)
        return image_url
    else:
        print("Error:", response.status_code)
        return None

# Renderiza el home
def home(request):
    return render(request, 'home.html')

# Simulación de la función para crear un póster con Adobe Creative Cloud
def crear_poster_adobe(imagen_ia_url, plantilla_url):
    response = requests.post('https://api.adobe.com/crear-poster', json={
        'imagen_ia_url': imagen_ia_url,
        'plantilla_url': plantilla_url,
    })
    if response.status_code == 200:
        poster_url = response.json().url_poster
        return poster_url
    return None

# Vista principal para crear la propuesta
def paginaPrompt(request):
    if request.method == 'POST':
        job_file_name = 'no-file'
        template_image_name = 'no-image'
        job_description = request.POST.get('job_description', '')

        # Subir el archivo del puesto
        if 'job_file' in request.FILES:
            job_file = request.FILES['job_file']
            fs = FileSystemStorage()
            job_file_name = fs.save(job_file.name, job_file)
            job_file_path = fs.url(job_file_name)

            # Extraer texto del archivo subido
            file_text = extract_text_from_file(job_file)

            # Generar el resumen usando OpenAI
            job_description = get_summary(file_text)
            print("job_description:", job_description)

        # Subir la imagen de la plantilla
        if 'template_image' in request.FILES:
            template_image = request.FILES['template_image']
            fs = FileSystemStorage()
            template_image_name = fs.save(template_image.name, template_image)

        # Llamada a la IA para generar la imagen del puesto
        imagen_ia_url = generar_imagen_vyro(f'Generate a hyperrealistic image of a {job_description}', 'vk-WKFXBDqezTzE0Vp6LWY6fwrlagD3DlpRE6MExVYclqF4e')

        if imagen_ia_url is None:
            return HttpResponse("Error generando la imagen", status=500)

        # Extraer solo el nombre del archivo de la imagen
        poster_filename = os.path.basename(imagen_ia_url)
        print("poster_filename:", quote(poster_filename, encoding='utf-8'))

        # Redirigir a la página de confirmación con los argumentos necesarios
        return redirect(reverse('confirmacion', kwargs={
            'job_file_name': quote(job_file_name, encoding='utf-8'),
            'job_description': quote(job_description, encoding='utf-8'),
            'template_image_name': quote(template_image_name, encoding='utf-8'),
            'poster_url': quote(poster_filename, encoding='utf-8')  # Pasar solo el nombre del archivo
        }))

    return render(request, 'paginaPrompt.html')

# Vista para confirmar y generar el póster
def confirmacion(request, job_file_name, job_description, template_image_name, poster_url):
    context = {
        'job_file_name': unquote(job_file_name),
        'job_description': unquote(job_description),
        'template_image_name': unquote(template_image_name),
        'poster_url': unquote(poster_url),
    }
    return render(request, 'confirmacion.html', context)

def image_selection(request):
    if request.method == 'POST':
        selection = request.POST.get('selection')
        poster_url = request.POST.get('poster_url')

        # Aquí puedes procesar la selección de la imagen
        if selection == 'like':
            return HttpResponse("Imagen seleccionada como 'Me gusta'")
        elif selection == 'dislike':
            return HttpResponse("Imagen seleccionada como 'No me gusta'")
    return redirect('home')

# Función para extraer texto de un archivo PDF o DOCX
def extract_text_from_file(file):
    try:
        if file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
            
            return text.encode('utf-8').decode('utf-8')

        elif file.name.endswith('.docx'):
            doc = Document(file)
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text.encode('utf-8').decode('utf-8')

        else:
            return 'Unsupported file format.'

    except Exception as e:
        return f"An error occurred: {e}"


# Función para generar un resumen usando Gemini
def get_summary(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        # Asegúrate de codificar el texto correctamente en UTF-8
        text = text.encode('utf-8').decode('utf-8')

        # Utiliza la nueva llamada de la API de Gemini para generar el resumen
        response = model.generate_content(f'De que trabajo es la vacante que se menciona en el siguiente texto, solo menciona el nombre de el trabajo traducido al ingles: {text}')
    
        summary = response.text  # O ajusta según la estructura del objeto
        return summary

    except Exception as e:
        return f"Error al generar el resumen: {e}"



