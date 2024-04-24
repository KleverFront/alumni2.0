const mobileScreen = window.matchMedia("(max-width: 990px )");
var diccTget = {
    'administradores': [1,2,3,4],
    'graduados': [5],
    'capacitaciones': [3,5],
    'empleos': [1,2,3],
    'emprendimientos': [1,3,4],
    'estadistica': [3],
    'diable-ordered-estadistica':[2,5,6,7],
    'width-colum-target':[7],
};
var espanol;
$.getJSON(rutaJsonEspanol, function(data) {
    espanol = data;
    

}).fail(function(jqxhr, textStatus, error) {
    console.error("Error al cargar el JSON:", textStatus, error);
});

function ajustes_de_tablas (columnDisableOrdered,scroll, ultimaCol) {
    const dataTableAjustes = {
        "scrollX": scroll,
        "scrollY": false,
        destroy: true,
        columnDefs: [
            { className: "center-table", targets: [0,1,2]},
            { orderable: false, targets: columnDisableOrdered},
            { width: "10%", targets: [ultimaCol]},
        ],
        language: espanol,
        dom: 'Bfrtilp',
            buttons: [
                'copyHtml5',
                'excelHtml5',
                'csvHtml5',
                'pdfHtml5'
            ],
    }

    return dataTableAjustes
}

$(document).ready(function () {

    $(".dashboard-nav-dropdown-toggle").click(function () {
        $(this).closest(".dashboard-nav-dropdown")
            .toggleClass("show")
            .find(".dashboard-nav-dropdown")
            .removeClass("show");
        $(this).parent()
            .siblings()
            .removeClass("show");

    });

  

    $(document).ready(function () {
        $('#admin').DataTable(ajustes_de_tablas(diccTget['administradores'],false, 4));
    });

    $(document).ready(function () {
        $('#capacitaciones').DataTable(ajustes_de_tablas(diccTget['capacitaciones'],false,5 ));
    });
    $(document).ready(function () {
        $('#empleos').DataTable(ajustes_de_tablas(diccTget['empleos'],false,3 ));
    });
    $(document).ready(function () {
        $('#emprendimientos').DataTable(ajustes_de_tablas(diccTget['emprendimientos'],false,4));
    });
    $(document).ready(function () {
        $('#graduadopre').DataTable(ajustes_de_tablas(diccTget['graduados'],true,5));
    });
 
});






document.getElementById('logout-link').addEventListener('click', function (event) {
    event.preventDefault();
    const logoutUrl = this.getAttribute('data-logout-url');

    Swal.fire({
        icon: 'warning',
        title: '¿Estás seguro?',
        text: '¿Quieres cerrar la sesión?',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: "No, cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = logoutUrl;
        }
    });
});

