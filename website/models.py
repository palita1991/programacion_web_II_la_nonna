import re
from django.db import models
from django.contrib.auth.models import User

class SolicitudContacto(models.Model):
    CATEGORIA_COMERCIAL = 'Consulta Comercial'
    CATEGORIA_TECNICA = 'Consulta Técnica'
    CATEGORIA_RRHH = 'Consulta de RRHH'
    CATEGORIA_GENERAL = 'Consulta General'

    CATEGORIAS_CHOICES = [
        (CATEGORIA_COMERCIAL, 'Consulta Comercial'),
        (CATEGORIA_TECNICA, 'Consulta Técnica'),
        (CATEGORIA_RRHH, 'Consulta de RRHH'),
        (CATEGORIA_GENERAL, 'Consulta General'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.EmailField(verbose_name="Email")
    mensaje = models.TextField(verbose_name="Consulta")
    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIAS_CHOICES,
        default=CATEGORIA_GENERAL,
        verbose_name="Categoría",
    )
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de envío")
    leida = models.BooleanField(default=False, verbose_name="Leída")

    class Meta:
        verbose_name = "Solicitud de contacto"
        verbose_name_plural = "Solicitudes de contacto"
        ordering = ['-fecha_envio']

    def clasificacion_mensaje(self):
        texto = self.mensaje.lower()

        patron_comercial = r'\b(precios?|costos?|tarifas?|compras?)\b'
        patron_tecnica = r'\b(soportes?|error(?:es)?|problemas?|ayudas?)\b'
        patron_rrhh = r'\b(trabajos?|cvs?|empleos?|linkedin)\b'

        if re.search(patron_comercial, texto):
            return self.CATEGORIA_COMERCIAL
        elif re.search(patron_tecnica, texto):
            return self.CATEGORIA_TECNICA
        elif re.search(patron_rrhh, texto):
            return self.CATEGORIA_RRHH
        else:
            return self.CATEGORIA_GENERAL

    def save(self, *args, **kwargs):
        self.categoria = self.clasificacion_mensaje()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.email}) - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"

class UsuarioPermitido(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email permitido")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de alta")

    class Meta:
        verbose_name = "Usuario permitido"
        verbose_name_plural = "Usuarios permitidos"
        ordering = ['email']

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class CodigoValidacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codigos_validacion')
    codigo = models.CharField(max_length=6, verbose_name="Código de validación")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de emisión")
    usado = models.BooleanField(default=False, verbose_name="Usado")

    class Meta:
        verbose_name = "Código de validación"
        verbose_name_plural = "Códigos de validación"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.email} - {self.codigo} ({'Usado' if self.usado else 'Activo'})"