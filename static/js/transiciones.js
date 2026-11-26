document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll('.nav-link, .btn');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const destino = this.getAttribute("href");

            // Evitamos animar si el enlace es un ancla (ej: #seccion) o no tiene destino
            if (!destino || destino.startsWith("#") || this.target === "_blank") {
                return;
            }

            // Verifica en página esta, si esta en la misma no hace nada
            if (destino === window.location.pathname) {
                return;
            }

            e.preventDefault();

            // Se le agrega la clase al body
            document.body.classList.add('fade-out-page');

            // 200 milisegundos
            setTimeout(() => {
                window.location.href = destino;
            }, 200);
        });
    });
});