from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),

    path('registro/', views.registro_usuario, name='registro'),
    path('validar-cuenta/', views.validar_cuenta, name='validar_cuenta'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),

    path('panel/', views.panel_solicitudes, name='panel_solicitudes'),
    path('panel/nueva/', views.crear_solicitud, name='crear_solicitud'),
    path('panel/editar/<int:pk>/', views.editar_solicitud, name='editar_solicitud'),
    path('panel/eliminar/<int:pk>/', views.eliminar_solicitud, name='eliminar_solicitud'),

    path('api/consultas/', views.ConsultasAPIView.as_view(), name='api_consultas')
]
