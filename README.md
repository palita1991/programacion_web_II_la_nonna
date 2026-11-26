# La Nonna — Pastas Artesanales

Sitio web institucional y sistema de gestión interna desarrollado en **Django** con persistencia en **PostgreSQL**, panel CRUD con clasificación automática de consultas, autenticación con control de usuarios autorizados y APIs.

## Sitio Desplegado (Render)

* **URL pública:** [https://la-nonna.onrender.com](https://la-nonna.onrender.com/)
* **API propia de consultas (JSON):** [https://la-nonna.onrender.com/api/consultas/](https://la-nonna.onrender.com/api/consultas/)

---

## Funcionalidades Principales

* **Sitio:** Secciones de Inicio, Productos, Sobre Nosotros y Contacto.
* **Formulario de contacto** Validación cliente y servidor, persistencia en PostgreSQL y envío de correo de confirmación al cliente con los datos cargados y la categoría asignada en el asunto.
* **Panel interno CRUD y clasificación automática (`/panel/`):** Alta, edición, eliminación y listado de solicitudes, con tarjetas de resumen estadístico y categorización automática por palabras clave (`Consulta Comercial`, `Consulta Técnica`, `Consulta de RRHH` y `Consulta General`).
* **Autenticación y sesiones en español:** Registro restringido a correos cargados en la tabla `UsuarioPermitido` (precargada vía migración de datos con `annavillegas@live.com.ar`), validación de cuenta mediante código de 6 dígitos enviado por correo electrónico, inicio de sesión con email y contraseña, visualización del nombre del usuario activo en el header y cierre de sesión.

---

## APIs Implementadas

### 1. API Externa Consumida
* **Servicio:** TheMealDB (API pública y gratuita de recetas gastronómicas)
* **URL consumida:** `https://www.themealdb.com/api/json/v1/1/filter.php?c=Pasta`
* **Implementación:** Consumida desde el backend con `requests` y validada/serializada mediante `RecetaExternaSerializer`. Los platos de pasta obtenidos se renderizan en la sección **Productos** (`/productos/`) como parte de los platos internacionales.

### 2. API Propia
* **Endpoint:** `GET /api/consultas/`
* **Formato de respuesta:** JSON (`application/json`)
* **Implementación:** `ConsultasAPIView` (`APIView`) y `SolicitudContactoSerializer` (`ModelSerializer`) de DRF. Devuelve todas las solicitudes registradas en PostgreSQL junto con su categoría asignada, fecha de envío y estado.

---

## Tecnologías Utilizadas

* Python 3 & Django
* Django REST Framework (DRF) & Requests
* PostgreSQL (`psycopg2` / `dj-database-url`)
* Bootstrap 5 & Bootstrap Icons
* Gunicorn & WhiteNoise (despliegue en Render)
* `python-dotenv` (gestión de variables de entorno)

---

## Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/palita1991/programacion_web_II_la_nonna.git
   ```

2. **Crear y activar el entorno virtual:**

3. **Instalar dependencias:**
   ```bash
   python -m pip install -r requirements.txt
   ```
   
4. **Configurar variables de entorno:**
   Copiar `.env.example` a `.env` en la raíz del proyecto y completar los datos de PostgreSQL local y las credenciales SMTP para envío de correos.

5. **Ejecutar migraciones:**
   Asegurarse de tener creada la base de datos configurada en `DB_NAME` y ejecutar:
   ```bash
   python manage.py migrate
   ```
   *(Las migraciones incluyen la carga automática del correo autorizado `annavillegas@live.com.ar` en la tabla `UsuarioPermitido`).*

6. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   Acceder desde el navegador en `http://127.0.0.1:8000/`.
