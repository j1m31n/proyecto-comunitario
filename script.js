document.addEventListener("DOMContentLoaded", function () {
    cargarProyectosAuto();
});

async function cargarProyectosAuto() {
    try {
        const respuesta = await fetch("proyectos.json?cache_bypass=" + new Date().getTime());
        const proyectos = await respuesta.json();

        const categorias = ["finanzas", "tecnologia", "autoayuda", "recursos"];
        categorias.forEach(cat => {
            const el = document.getElementById(cat);
            if (el) el.innerHTML = "";
        });

        if (!proyectos || proyectos.length === 0) {
            document.getElementById("finanzas").innerHTML = "<p style='text-align:center;'>Buscando y clasificando nuevos proyectos...</p>";
            return;
        }

        proyectos.forEach(item => {
            const contenedor = document.getElementById(item.categoria);
            if (contenedor) {
                contenedor.innerHTML += crearTarjetaHTML(item);
            }
        });

    } catch (error) {
        console.error("Error al cargar datos dinámicos:", error);
    }
}

function crearTarjetaHTML(item) {
    let icono = "fa-file-alt";
    if (item.categoria === "finanzas") icono = "fa-file-invoice-dollar";
    if (item.categoria === "tecnologia") icono = "fa-robot";
    if (item.categoria === "autoayuda") icono = "fa-book-reader";
    if (item.categoria === "recursos") icono = "fa-folder-open";

    let accion = "";
    if (item.tipo === "pago") {
        accion = `
            <div class="blurred-text">${item.bloqueado}</div>
            <div class="unlock-box">
                <button class="btn btn-unlock" onclick="desbloquear('${item.link}')">
                    <i class="fas fa-lock-open"></i> Desbloquear por $${item.precio}
                </button>
            </div>
        `;
    } else {
        accion = `
            <div style="text-align: center; margin-top: 1.5rem;">
                <button class="btn btn-ad" onclick="desbloquear('${item.link}')">
                    <i class="fas fa-play-circle"></i> Ver Anuncio para Desbloquear
                </button>
            </div>
        `;
    }

    return `
        <section class="card">
            <h2><i class="fas ${icono}" style="color:var(--secondary-color);"></i> ${item.titulo}</h2>
            <p>${item.descripcion}</p>
            ${accion}
        </section>
    `;
}

function openCategory(evt, categoryName) {
    const tabContents = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove("active-content");
    }

    const tabBtns = document.getElementsByClassName("tab-btn");
    for (let i = 0; i < tabBtns.length; i++) {
        tabBtns[i].classList.remove("active");
    }

    document.getElementById(categoryName).classList.add("active-content");
    evt.currentTarget.classList.add("active");
}

function desbloquear(link) {
    alert("Redirigiendo a la fuente del proyecto...");
    window.open(link, '_blank');
}
