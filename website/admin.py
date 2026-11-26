from django.contrib import admin
from .models import SolicitudContacto

@admin.register(SolicitudContacto)
class SolicitudContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha_envio', 'leida')
    list_filter = ('leida', 'fecha_envio')
    search_fields = ('nombre', 'email', 'mensaje')
    readonly_fields = ('fecha_envio',)