from django.db import models

class SolicitudContacto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.EmailField(verbose_name="Email")
    mensaje = models.TextField(verbose_name="Consulta")
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de envío")
    leida = models.BooleanField(default=False, verbose_name="Leída")

    class Meta:
        verbose_name = "Solicitud de contacto"
        verbose_name_plural = "Solicitudes de contacto"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.nombre} ({self.email}) - {self.fecha_envio.strftime('%d/%m/%Y %H:%M')}"