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
            }
            else if(nav.classList.contains("show") && action=="remove"){
                nav.classList.remove('show');
                // Cambia el icono del botón
                toggle.classList.remove('bx-x');
                // Añade o quita padding al cuerpo
                bodypd.classList.remove('body-pd');
                // Añade o quita padding al encabezado
                headerpd.classList.remove('body-pd');
            }
        }

    }


    const toggleNavbar = (action) => {
        setTimeout(() => {
            showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header',action);
        }, 200);

    };

    // Event listener para el contenedor padre de los elementos que pueden abrir el menú
    const container = document.getElementById("nav-bar");
    let menuOpen = false;
    document.getElementById("header-toggle").addEventListener('click', function (event) {
        if(document.getElementById("nav-bar").classList.contains("show")){
            toggleNavbar("remove");
            menuOpen=false;
            localStorage.setItem('menuOpen', false);
        }else{
            toggleNavbar("add");
            menuOpen=true;
            localStorage.setItem('menuOpen', true);
        }

    });

    if(localStorage.getItem('menuOpen')==='true'){
        toggleNavbar("add");
        menuOpen=true;
    }


    // Event listener para mouseover en el contenedor padre
    container.addEventListener('mouseenter', function() {
        if(!menuOpen){
            toggleNavbar("add");
        }
    });

    container.addEventListener('mouseleave', function() {
        if(!menuOpen){
            toggleNavbar("remove");
        }

    });




    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')
    linkColor.forEach(l => l.addEventListener('click', colorLink))

    function colorLink() {
        if (linkColor) {
            linkColor.forEach(l => l.classList.remove('active'))
            this.classList.add('active')
        }
    }

    if(document.getElementById('logout-link')){
        document.getElementById('logout-link').addEventListener('click', function (event) {
            event.preventDefault();
            const url = this.getAttribute('data-url');
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
                    window.location.href = url
                }
            });
        });
    }

});