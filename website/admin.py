from django.contrib import admin
from .models import SolicitudContacto


@admin.register(SolicitudContacto)
class SolicitudContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'categoria', 'fecha_envio', 'leida')
    list_editable = ('leida',)
    list_filter = ('categoria', 'leida', 'fecha_envio')
    search_fields = ('nombre', 'email', 'mensaje')
    readonly_fields = ('categoria', 'fecha_envio')
