from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactoForm

def inicio(request):
    return render(request, 'website/inicio.html')

def productos(request):
    return render(request, 'website/productos.html')

def sobre_nosotros(request):
    return render(request, 'website/sobre_nosotros.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactoForm


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)

        # 1. Todo el proceso de envío DEBE estar dentro del form.is_valid()
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']

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

                messages.success(request,'¡Gracias! Hemos recibido tu mensaje')
                return redirect('contacto')

            except Exception as e:
                # Si falla el servidor de correos, avisa al usuario en pantalla
                messages.error(request, f'Hubo un problema al enviar el correo de confirmación: {e}')

    else:
        form = ContactoForm()

    return render(request, 'website/contacto.html', {'form': form})