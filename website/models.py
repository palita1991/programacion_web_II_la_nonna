from django.db import models


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

        palabras_comercial = ('precio', 'costo', 'tarifa', 'compra')
        palabras_tecnica = ('soporte', 'error', 'problema', 'ayuda')
        palabras_rrhh = ('trabajo', 'cv', 'empleo', 'linkedin')

        if any(palabra in texto for palabra in palabras_comercial):
            return self.CATEGORIA_COMERCIAL
        elif any(palabra in texto for palabra in palabras_tecnica):
            return self.CATEGORIA_TECNICA
        elif any(palabra in texto for palabra in palabras_rrhh):
            return self.CATEGORIA_RRHH
        else:
            return self.CATEGORIA_GENERAL

    def save(self, *args, **kwargs):
        self.categoria = self.clasificacion_mensaje()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.email}) - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"
