document.addEventListener("DOMContentLoaded", function (event) {

    const showNavbar = (toggleId, navId, bodyId, headerId,action) => {
        const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            headerpd = document.getElementById(headerId);

        // Validate that all variables exist
        if (toggle && nav && bodypd && headerpd) {
            // Muestra u oculta la barra de navegación
            if (!nav.classList.contains("show") && action=="add"){
                nav.classList.add('show');
                // Cambia el icono del botón
                toggle.classList.add('bx-x');
                // Añade o quita padding al cuerpo
                bodypd.classList.add('body-pd');
                // Añade o quita padding al encabezado
                headerpd.classList.add('body-pd');
                console.log("add");
            }
            else if(nav.classList.contains("show") && action=="remove"){
                nav.classList.remove('show');
                // Cambia el icono del botón
                toggle.classList.remove('bx-x');
                // Añade o quita padding al cuerpo
                bodypd.classList.remove('body-pd');
                // Añade o quita padding al encabezado
                headerpd.classList.remove('body-pd');
                console.log("remove");
            }
        }
            
    }


    const toggleNavbar = (action) => {
        setTimeout(() => {
            showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header',action);
          }, 400);
        
    };

    // Event listener para el contenedor padre de los elementos que pueden abrir el menú
    const container = document.getElementById("id_nav_list");
    container.addEventListener('click', function (event) {
        // Verifica si el elemento clickeado es el botón o el menú
        if (event.target.id === 'header-toggle' || event.target.id === 'nav-bar' || event.target.id === 'id_nav_list') {
            toggleNavbar();
        }
    });

    // Event listener para mouseover en el contenedor padre
    container.addEventListener('mouseover', function (event) {
        // Verifica si el mouse está sobre el contenedor padre
        
        
    });




    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')

    function colorLink() {
        if (linkColor) {
            linkColor.forEach(l => l.classList.remove('active'))
            this.classList.add('active')
        }
    }
    linkColor.forEach(l => l.addEventListener('click', colorLink))

});