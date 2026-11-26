import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .models import SolicitudContacto, UsuarioPermitido, CodigoValidacion
from .forms import (
    ContactoForm,
    SolicitudPanelForm,
    RegistroForm,
    ValidarCuentaForm,
    LoginEmailForm,
)

import requests
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SolicitudContactoSerializer, RecetaExternaSerializer

def inicio(request):
    return render(request, 'website/inicio.html')

API_RECETAS_PASTA_URL = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=Pasta'

def obtener_recetas_pasta_drf(limite=6):
    try:
        respuesta = requests.get(API_RECETAS_PASTA_URL, timeout=5)
        respuesta.raise_for_status()
        datos = respuesta.json().get('meals') or []
    except (requests.RequestException, ValueError):
        return [], True

    serializer = RecetaExternaSerializer(data=datos[:limite], many=True)
    if serializer.is_valid():
        return serializer.data, False

    return [], True

def productos(request):
    recetas_api, error_api = obtener_recetas_pasta_drf(limite=6)
    return render(request, 'website/productos.html', {
        'recetas_api': recetas_api,
        'error_api': error_api,
    })


def sobre_nosotros(request):
    return render(request, 'website/sobre_nosotros.html')

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
@login_required
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
@login_required
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
@login_required
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
@login_required
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

# =========================================
# AUTENTICACIÓN Y SESIONES
# =========================================

def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('panel_solicitudes')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            nombre_completo = form.cleaned_data['nombre_apellido']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # 1. Verificar si el correo está en la tabla de usuarios permitidos
            esta_permitido = UsuarioPermitido.objects.filter(email__iexact=email).exists()

            if not esta_permitido:
                messages.error(
                    request,
                    'Acceso restringido. No está autorizado a utilizar este sistema.'
                )
                return redirect('registro')

            # 2. Verificar si ya existe una cuenta activa con ese correo
            usuario_existente = User.objects.filter(email__iexact=email).first()
            if usuario_existente and usuario_existente.is_active:
                messages.warning(
                    request,
                    'Este correo ya se encuentra registrado y validado. Iniciá sesión con tu contraseña.'
                )
                return redirect('iniciar_sesion')

            # Separar nombre y apellido para que user.get_full_name() lo devuelva completo
            partes = nombre_completo.split(' ', 1)
            first_name = partes[0]
            last_name = partes[1] if len(partes) > 1 else ''

            if usuario_existente:
                # Si se registró antes pero nunca validó, actualizamos datos y emitimos nuevo código
                usuario = usuario_existente
                usuario.first_name = first_name
                usuario.last_name = last_name
                usuario.set_password(password)
                usuario.is_active = False
                usuario.save()
                CodigoValidacion.objects.filter(usuario=usuario, usado=False).update(usado=True)
            else:
                usuario = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=False,
                )

            # 3. Generar código seguro de 6 dígitos y enlace de validación
            codigo = str(secrets.randbelow(900000) + 100000)
            CodigoValidacion.objects.create(usuario=usuario, codigo=codigo)

            enlace_validacion = f"{request.build_absolute_uri(reverse('validar_cuenta'))}?email={email}"

            asunto = 'Validación de cuenta - Panel La Nonna'
            cuerpo = (
                f"Hola {nombre_completo},\n\n"
                "Recibimos tu solicitud de registro para acceder al Panel de Administración de La Nonna.\n\n"
                f"Tu código de validación es: {codigo}\n\n"
                "Para habilitar tu cuenta, ingresá al siguiente enlace e introducí tu correo y el código:\n"
                f"{enlace_validacion}\n\n"
                "Saludos,\n"
                "La Nonna - Pastas Artesanales"
            )

            try:
                send_mail(
                    subject=asunto,
                    message=cuerpo,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Le llegará un correo para validar su cuenta')
            except Exception as e:
                messages.warning(
                    request,
                    f'Tu registro se creó, pero hubo un error al enviar el correo de validación: {e}'
                )

            return redirect(f"{reverse('validar_cuenta')}?email={email}")
    else:
        form = RegistroForm()

    return render(request, 'website/registro.html', {'form': form})


def validar_cuenta(request):
    if request.user.is_authenticated:
        return redirect('panel_solicitudes')

    if request.method == 'POST':
        form = ValidarCuentaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            codigo_ingresado = form.cleaned_data['codigo']

            usuario = User.objects.filter(email__iexact=email).first()

            if not usuario:
                messages.error(request, 'El correo o el código de validación son incorrectos.')
                return render(request, 'website/validar_cuenta.html', {'form': form})

            if usuario.is_active:
                messages.info(request, 'Esta cuenta ya fue validada anteriormente. Podés iniciar sesión.')
                return redirect('iniciar_sesion')

            registro_codigo = CodigoValidacion.objects.filter(
                usuario=usuario,
                codigo=codigo_ingresado,
                usado=False,
            ).first()

            if registro_codigo:
                usuario.is_active = True
                usuario.save()
                registro_codigo.usado = True
                registro_codigo.save()

                messages.success(
                    request,
                    '¡Cuenta validada correctamente! Ya podés iniciar sesión con tu correo y contraseña.'
                )
                return redirect('iniciar_sesion')
            else:
                messages.error(request, 'El código de validación es incorrecto o ya fue utilizado.')
    else:
        email_inicial = request.GET.get('email', '')
        form = ValidarCuentaForm(initial={'email': email_inicial})

    return render(request, 'website/validar_cuenta.html', {'form': form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('panel_solicitudes')

    next_url = request.GET.get('next') or request.POST.get('next', '')

    if request.method == 'POST':
        form = LoginEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            usuario_existente = User.objects.filter(email__iexact=email).first()

            if usuario_existente:
                # Si la contraseña coincide pero todavía no validó el código, avisamos con claridad
                if not usuario_existente.is_active and usuario_existente.check_password(password):
                    messages.warning(
                        request,
                        'Tu cuenta todavía no fue validada. Ingresá el código que te enviamos por correo.'
                    )
                    return redirect(f"{reverse('validar_cuenta')}?email={email}")

                user = authenticate(
                    request,
                    username=usuario_existente.username,
                    password=password,
                )

                if user is not None:
                    login(request, user)
                    nombre_mostrar = user.get_full_name() or user.email
                    messages.success(request, f'¡Bienvenido/a, {nombre_mostrar}!')

                    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                    return redirect('panel_solicitudes')

            messages.error(request, 'Email o contraseña incorrectos.')
    else:
        form = LoginEmailForm()

    return render(request, 'website/iniciar_sesion.html', {
        'form': form,
        'next': next_url,
    })


def cerrar_sesion(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Cerraste sesión correctamente.')
    return redirect('inicio')

class ConsultasAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        solicitudes = SolicitudContacto.objects.all()
        serializer = SolicitudContactoSerializer(solicitudes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)