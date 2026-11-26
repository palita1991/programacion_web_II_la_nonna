from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),

    path('panel/', views.panel_solicitudes, name='panel_solicitudes'),
    path('panel/nueva/', views.crear_solicitud, name='crear_solicitud'),
    path('panel/editar/<int:pk>/', views.editar_solicitud, name='editar_solicitud'),
    path('panel/eliminar/<int:pk>/', views.eliminar_solicitud, name='eliminar_solicitud'),
]
