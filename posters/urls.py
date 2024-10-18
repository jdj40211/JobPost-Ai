from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'confirmacion/<str:job_file_name>/<str:job_description>/<str:template_image_name>/<str:poster_url>/',
        views.confirmacion,
        name='confirmacion'
    ),
    path('image-selection/', views.image_selection, name='image_selection'),

]
