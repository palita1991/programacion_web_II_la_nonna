from django.contrib import admin
from .models import SolicitudContacto, UsuarioPermitido, CodigoValidacion


@admin.register(SolicitudContacto)
class SolicitudContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'categoria', 'fecha_envio', 'leida')
    list_editable = ('leida',)
    list_filter = ('categoria', 'leida', 'fecha_envio')
    search_fields = ('nombre', 'email', 'mensaje')
    readonly_fields = ('categoria', 'fecha_envio')

@admin.register(UsuarioPermitido)
class UsuarioPermitidoAdmin(admin.ModelAdmin):
    list_display = ('email', 'fecha_creacion')
    search_fields = ('email',)

@admin.register(CodigoValidacion)
class CodigoValidacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'codigo', 'usado', 'fecha_creacion')
    list_filter = ('usado', 'fecha_creacion')
    search_fields = ('usuario__email', 'codigo')
    readonly_fields = ('fecha_creacion',)