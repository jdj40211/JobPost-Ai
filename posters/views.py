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
from django.http import JsonResponse
import os
import google.generativeai as genai
import re
import uuid
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('paginaPrompt')  # Cambia esto por tu vista de redirección después de iniciar sesión
        else:
            # Maneja el error de login fallido
            return render(request, 'login.html', {
                'error': 'Credenciales inválidas',
                'show_register': True  # Indica que se debe mostrar el botón de registro
            })
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de inicio de sesión
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# Configura tu clave API de Gemini
genai.configure(api_key='AIzaSyDVjet7JX0216nprw9KRWozDzckWeUoOgE')

def generar_imagen_vyro(descripcion, api_token):
    url = 'https://api.vyro.ai/v1/imagine/api/generations'

    headers = {
        'Authorization': f'Bearer {api_token}'
    }

    payload = {
        'prompt': (None, descripcion),
        'style_id': (None, '29'),
        'aspect_ratio': (None, '1:1')
    }

    response = requests.post(url, headers=headers, files=payload)

    if response.status_code == 200:
        # Generar un nombre de archivo único usando UUID
        unique_id = uuid.uuid4().hex
        file_name = f'image_{unique_id}.jpg'
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

def crear_poster(request):
    # Obtener la imagen seleccionada de la sesión
    selected_poster_url = request.session.get('selected_poster_url')

    job_context = request.session.get('job_context')
    # Bloque de texto con el contexto del empleo (job_context)
    extraer_datos_empleo(request, job_context)

    # Extraer el título y la descripción del trabajo del bloque de texto
    job_title = request.session.get('job_title', 'Título no disponible')
    job_description = request.session.get('job_description', 'Descripción no disponible')
    contact_info = "contacto@empresa.com"
    
    # Información de contacto (esto puede ser dinámico también)
    contact_info = "contacto@empresa.com"

    if selected_poster_url:
        context = {
            'poster_url': selected_poster_url,
            'job_title': job_title,
            'job_description': job_description,
            'contact_info': contact_info
        }
        return render(request, 'nueva_plantilla.html', context)
    else:
        return HttpResponse("No se ha seleccionado ninguna imagen.")




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
            job_context = get_summaryDescription(file_text)
            request.session['job_context'] = job_context

        # Subir la imagen de la plantilla
        if 'template_image' in request.FILES:
            template_image = request.FILES['template_image']
            fs = FileSystemStorage()
            template_image_name = fs.save(template_image.name, template_image)

        # Llamada a la IA para generar las 3 imágenes del puesto
        imagen_ia_url = generar_imagen_vyro(f'Generate a hyperrealistic image of a {job_description}', 'vk-YhGqtkpc2KuFM4F0Byh4D0HhpFQN3gQ2LZoBPnP6mcVP2SgV')
        print(imagen_ia_url)
        imagen_ia_url2 = generar_imagen_vyro(f'Generate a hyperrealistic image of a {job_description}', 'vk-YhGqtkpc2KuFM4F0Byh4D0HhpFQN3gQ2LZoBPnP6mcVP2SgV')
        print(imagen_ia_url2)
        imagen_ia_url3 = generar_imagen_vyro(f'Generate a hyperrealistic image of a {job_description}', 'vk-YhGqtkpc2KuFM4F0Byh4D0HhpFQN3gQ2LZoBPnP6mcVP2SgV')
        print(imagen_ia_url3)
        if not all([imagen_ia_url, imagen_ia_url2, imagen_ia_url3]):
            return HttpResponse("Error generando las imágenes", status=500)

        # Redirigir a la página de confirmación con los argumentos necesarios
        return redirect(reverse('confirmacion', kwargs={
            'job_file_name': quote(job_file_name, encoding='utf-8'),
            'job_description': quote(job_description, encoding='utf-8'),
            'template_image_name': quote(template_image_name, encoding='utf-8'),
            'poster_url1': quote(os.path.basename(imagen_ia_url), encoding='utf-8'),
            'poster_url2': quote(os.path.basename(imagen_ia_url2), encoding='utf-8'),
            'poster_url3': quote(os.path.basename(imagen_ia_url3), encoding='utf-8')
        }))

    return render(request, 'paginaPrompt.html')

# Vista para confirmar y generar el póster
def confirmacion(request, job_file_name, job_description, template_image_name, poster_url1, poster_url2, poster_url3):
    context = {
        'job_file_name': unquote(job_file_name),
        'job_description': unquote(job_description),
        'template_image_name': unquote(template_image_name),
        'poster_url1': unquote(poster_url1),
        'poster_url2': unquote(poster_url2),
        'poster_url3': unquote(poster_url3),
    }
    return render(request, 'confirmacion.html', context)

def image_selection(request):
    if request.method == 'POST':
        selection = request.POST.get('selection')
        poster_url = request.POST.get('poster_url')

        if selection == 'like':
            # Guardar la imagen seleccionada en la sesión
            request.session['selected_poster_url'] = poster_url

            return redirect('crear_poster')
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
def get_summaryImage(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        
        text = text.encode('utf-8').decode('utf-8')

        # Utiliza la nueva llamada de la API de Gemini para generar el resumen
        response = model.generate_content(f'De que trabajo es la vacante que se menciona en el siguiente texto, solo menciona el nombre de el trabajo traducido al ingles: {text}')
    
        summary = response.text  # O ajusta según la estructura del objeto
        return summary

    except Exception as e:
        return f"Error al generar el resumen: {e}"

def get_summaryDescription(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        
        text = text.encode('utf-8').decode('utf-8')

        # Utiliza la nueva llamada de la API de Gemini para generar el resumen
        response = model.generate_content(f'De el siguiente texto dame los siguientes datos: Salario, Requisitos principales: {text}')
    
        summary = response.text  # O ajusta según la estructura del objeto
        return summary

    except Exception as e:
        return f"Error al generar el resumen: {e}"



def extraer_datos_empleo(request, job_context):
    # Usamos expresiones regulares para capturar datos específicos del contexto
    job_title_match = re.search(r'\*\*Vacante:\*\* (.+)', job_context)
    salary_match = re.search(r'\*\*Salario:\*\* (.+)', job_context)
    requisitos_match = re.search(r'\*\*Requisitos principales:\*\*\n(.+)', job_context, re.DOTALL)

    # Si se encuentran coincidencias, asignamos los valores, de lo contrario usamos un valor predeterminado
    job_title = job_title_match.group(1) if job_title_match else "Sin título"
    salary = salary_match.group(1) if salary_match else "No especificado"
    requisitos = requisitos_match.group(1).strip() if requisitos_match else "No especificado"

    # Remover asteriscos y formatear la descripción
    requisitos_limpios = re.sub(r'\*\*|\*', '', requisitos)

    # Crear una descripción uniendo el salario y los requisitos sin asteriscos
    job_description = f"Salario: {salary}\n\nRequisitos:\n{requisitos_limpios}"

    # Guardar los datos en la sesión
    request.session['job_title'] = job_title
    request.session['job_description'] = job_description

    return job_title, job_description


def guardar_y_mostrar_post(request):
    if request.method == 'POST':
        selection = request.POST.get('selection')
        print(f"Selection value: {selection}")  # Depuración
        poster_html = request.POST.get('poster_html')  # Recibimos el HTML completo

        if selection == 'like':
            # Guardar el HTML del póster en la sesión
            request.session['poster_html'] = poster_html

            # Redirigir a una página que actuará como el post de Instagram
            return redirect('ver_post_instagram')

        elif selection == 'dislike':
            return HttpResponse("Imagen seleccionada como 'No me gusta'")

    return redirect('home')


def ver_post_instagram(request):
    # Obtener el HTML del póster y la descripción del trabajo desde la sesión
    poster_html = request.session.get('poster_html', '')
    job_description = request.session.get('job_description', 'Descripción no disponible')

    # Renderizar la plantilla del post de Instagram con el contenido capturado y la descripción
    return render(request, 'ver_post.html', {
        'poster_html': poster_html,
        'job_description': job_description
    })





#Funciones creación de poster IG
# Función para crear un contenedor de imagen
def crear_contenedor(access_token, instagram_account_id, image_url, caption):
    url = f'https://graph.facebook.com/v15.0/{instagram_account_id}/media'
    params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }
    response = requests.post(url, params=params)
    data = response.json()
    return data.get('id')

# Función para publicar el contenedor
def publicar_contenedor(access_token, instagram_account_id, creation_id):
    url = f'https://graph.facebook.com/v15.0/{instagram_account_id}/media_publish'
    params = {
        'creation_id': creation_id,
        'access_token': access_token
    }
    response = requests.post(url, params=params)
    return response.json()

# Vista para manejar la publicación en Instagram
def publicar_poster_instagram(request):
    if request.method == 'POST':
        data = request.json()
        image_url = data.get("image_url")
        caption = data.get("caption")

        access_token = settings.INSTAGRAM_ACCESS_TOKEN
        instagram_account_id = settings.INSTAGRAM_ACCOUNT_ID

        # Crea y publica el contenedor
        creation_id = crear_contenedor(access_token, instagram_account_id, image_url, caption)
        if creation_id:
            result = publicar_contenedor(access_token, instagram_account_id, creation_id)
            if "id" in result:
                return JsonResponse({"status": "success", "message": "Publicado en Instagram"})
            else:
                return JsonResponse({"status": "error", "message": result.get("error", "Error al publicar")})
        else:
            return JsonResponse({"status": "error", "message": "Error al crear el contenedor"})
    else:
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)