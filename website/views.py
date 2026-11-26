
def inicio(request):
    return render(request, 'website/inicio.html')


def productos(request):
    return render(request, 'website/productos.html')


def sobre_nosotros(request):
    return render(request, 'website/sobre_nosotros.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .models import SolicitudContacto
from .forms import ContactoForm, SolicitudPanelForm


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)

        # 1. Todo el proceso de envío DEBE estar dentro del form.is_valid()
        if form.is_valid():
            solicitud = form.save()

            nombre = solicitud.nombre
            email = solicitud.email

            # 2. Adaptamos el asunto y mensaje para que sea una confirmación hacia el usuario
            asunto = f"¡Hemos recibido tu consulta, {nombre}! - La Nonna"
            cuerpo_mensaje = (
                f"Hola {nombre},\n\n"
                "Gracias por comunicarte con La Nonna. Te escribimos para confirmarte que "
                "hemos recibido tu mensaje correctamente. Nos pondremos en contacto a la brevedad.\n\n"
                "Saludos cordiales,\n"
                "La Nonna - Pastas Artesanales"
            )

            try:
                send_mail(
                    subject=asunto,
                    message=cuerpo_mensaje,
                    from_email='mpalavecino@proyectoweb.website',
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.success(request, '¡Gracias! Hemos recibido tu mensaje')
                return redirect('contacto')

            except Exception as e:
                # Si falla el servidor de correos, avisa al usuario en pantalla
                messages.error(request, f'Hubo un problema al enviar el correo de confirmación: {e}')

            return redirect('contacto')

    else:
        form = ContactoForm()

    return render(request, 'website/contacto.html', {'form': form})


# LECTURA - PANEL INTERIOR
def panel_solicitudes(request):
    solicitudes = SolicitudContacto.objects.all()

    resumen = {
        'total': solicitudes.count(),
        'comercial': solicitudes.filter(categoria=SolicitudContacto.CATEGORIA_COMERCIAL).count(),
        'tecnica': solicitudes.filter(categoria=SolicitudContacto.CATEGORIA_TECNICA).count(),
        'rrhh': solicitudes.filter(categoria=SolicitudContacto.CATEGORIA_RRHH).count(),
        'general': solicitudes.filter(categoria=SolicitudContacto.CATEGORIA_GENERAL).count(),
    }

    return render(request, 'website/panel_solicitudes.html', {
        'solicitudes': solicitudes,
        'resumen': resumen,
    })

# CREACIÓN - PANEL INTERIOR
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudPanelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud creada y clasificada correctamente.')
            return redirect('panel_solicitudes')
    else:
        form = SolicitudPanelForm()

    return render(request, 'website/panel_form.html', {
        'form': form,
        'titulo': 'Nueva Solicitud',
        'texto_boton': 'Guardar Solicitud',
    })

# ACTUALIZACIÓN - PANEL INTERNO
def editar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudContacto, pk=pk)

    if request.method == 'POST':
        form = SolicitudPanelForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            messages.success(request, f'Solicitud de {solicitud.nombre} actualizada correctamente.')
            return redirect('panel_solicitudes')
    else:
        form = SolicitudPanelForm(instance=solicitud)

    return render(request, 'website/panel_form.html', {
        'form': form,
        'solicitud': solicitud,
        'titulo': 'Editar Solicitud',
        'texto_boton': 'Guardar Cambios',
    })

# ELIMINACIÓN - PANEL INTERNO
def eliminar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudContacto, pk=pk)

    if request.method == 'POST':
        nombre = solicitud.nombre
        solicitud.delete()
        messages.success(request, f'La solicitud de {nombre} fue eliminada.')
        return redirect('panel_solicitudes')

    return render(request, 'website/panel_confirmar_eliminar.html', {
        'solicitud': solicitud,
    })
