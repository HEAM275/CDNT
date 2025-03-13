var accionesPorEstado = {
    'Archivado': ['Documento', 'Expediente'],
    'Cumplida': ['Documento', 'Expediente', 'Archivar'],
    'Espera': ['Documento', 'Observación', 'Cumplida', 'Revisar Resumen'],
    'Confección': ['Documento', 'Editar', 'Eliminar'],
    'Incumplido': ['Documento', 'Observación', 'Reasignar', 'Prorrogar', 'Cumplida', 'Reenviar Correo'],
    'Proceso': ['Documento', 'Observación', 'Reasignar', 'Prorrogar', 'Cumplida', 'Reenviar Correo']
};

function ejecutarAccion(accion, id, tipo) {
    let baseUrl = tipo === 'acuerdo' ? '/Acuerdos' : '/Indicaciones';
    switch (accion) {
        case 'Documento':
            alert("Función Documento ejecutada.");
            window.location.href = '/pagina_en_blanco/';
            break;
        case 'Expediente':
            alert("Función Expediente ejecutada.");
            break;
        case 'Archivar':
            window.location.href = `${baseUrl}/archivar/${id}/`;
            break;
        case 'Observación':
            alert("Función Observación ejecutada.");
            break;
        case 'Cumplida':
            window.location.href = `${baseUrl}/cumplir/${id}/`;
            break;
        case 'Revisar Resumen':
            alert("Función Revisar Resumen ejecutada.");
            break;
        case 'Editar':
            window.location.href = `${baseUrl}/editar/${id}/`;
            break;
        case 'Eliminar':
            window.location.href = `${baseUrl}/eliminar/${id}/`;
            break;
        case 'Reasignar':
            alert("Función Reasignar ejecutada.");
            break;
        case 'Prorrogar':
            alert("Función Prorrogar ejecutada.");
            break;
        case 'Reenviar Correo':
            alert("Función Reenviar Correo ejecutada.");
            break;
        default:
            alert("Acción no definida.");
            break;
    }
}

var acuerdoSeleccionadoId = null;

function seleccionarAcuerdo(row, tipo) {
    // Eliminar la clase 'selected-row' de cualquier fila previamente seleccionada
    var filas = document.querySelectorAll('.selected-row');
    filas.forEach(function (fila) {
        fila.classList.remove('selected-row');
    });
    // Añadir la clase 'selected-row' a la fila seleccionada
    row.classList.add('selected-row');
    acuerdoSeleccionadoId = row.dataset.id;
    var estado = row.dataset.estado;
    mostrarAcciones(estado, acuerdoSeleccionadoId, tipo);  // Pasa el acuerdo_id y el tipo a mostrarAcciones
}

function obtenerIdAcuerdo() {
    return acuerdoSeleccionadoId;
}

function mostrarAcciones(estado, id, tipo) {
    var acciones = accionesPorEstado[estado] || [];
    var accionesContainer = document.getElementById('acciones');
    accionesContainer.innerHTML = '';
    acciones.forEach(function (accion) {
        var accionElement = document.createElement('button');
        accionElement.textContent = accion;
        accionElement.onclick = function () { ejecutarAccion(accion, id, tipo); };
        accionesContainer.appendChild(accionElement);
    });
}
