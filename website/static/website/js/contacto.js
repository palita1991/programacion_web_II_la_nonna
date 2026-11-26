document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');

    if (form) {
        form.addEventListener('submit', function(event) {
            let isValid = true;

            const nombre = document.getElementById('id_nombre');
            const email = document.getElementById('id_email');
            const mensaje = document.getElementById('id_mensaje');

            // Se borran errores anteriores
            document.querySelectorAll('.js-error').forEach(e => e.remove());

            // Cartel de error
            const showError = (input, message) => {
                isValid = false;
                const errorDiv = document.createElement('div');
                errorDiv.className = 'mt-1 small js-error fw-bold';
                errorDiv.innerText = message;
                errorDiv.style.color = 'var(--bordo)';
                input.parentNode.appendChild(errorDiv);
                input.style.borderColor = 'var(--bordo)';
            };

            // Validación Nombre
            if (nombre.value.trim().length === 0) {
                showError(nombre, 'Por favor ingrese un nombre válido');
            } else {
                nombre.style.borderColor = 'var(--verde-oliva)';
            }

            // Validación Email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email.value.trim())) {
                showError(email, 'Por favor ingrese un email válido.');
            } else { 
                email.style.borderColor = 'var(--verde-oliva)'; 
            }

            // Validación Mensaje
            if (mensaje.value.trim().length === 0) {
                showError(mensaje, 'Por favor ingrese una consulta válida.');
            } else {
                mensaje.style.borderColor = 'var(--verde-oliva)';
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }
});