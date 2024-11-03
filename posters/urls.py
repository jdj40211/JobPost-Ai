from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('paginaPrompt/', views.paginaPrompt, name='paginaPrompt'),
    path(
        'confirmacion/<str:job_file_name>/<str:job_description>/<str:template_image_name>/<str:poster_url1>/<str:poster_url2>/<str:poster_url3>/',
        views.confirmacion,
        name='confirmacion'
    ),
    path('image-selection/', views.image_selection, name='image_selection'),
    path('crear-poster/', views.crear_poster, name='crear_poster'),  
    path('guardar-y-mostrar-post/', views.guardar_y_mostrar_post, name='guardar_y_mostrar_post'),
    path('ver-post-instagram/', views.ver_post_instagram, name='ver_post_instagram'),
    path('publicar_poster_instagram/', views.publicar_poster_instagram, name='publicar_poster_instagram'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)