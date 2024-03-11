var currentTab = 0;
document.addEventListener("DOMContentLoaded", function (event) {


    showTab(currentTab);

});

function showTab(n) {
    var x = document.getElementsByClassName("tab_");
    x[n].style.display = "block";
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = '<i class="bx bx-right-arrow-circle"></i>';
    } else {
        document.getElementById("nextBtn").innerHTML = '<i class="bx bx-right-arrow-circle"></i>';
    }
    fixStepIndicator(n)
}

function nextPrev(n) {
    var x = document.getElementsByClassName("tab_");
    if (n == 1 && !validateForm()) return false;
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    if (currentTab >= x.length) {

        document.getElementById("nextprevious").style.display = "none";
        document.getElementById("all-steps").style.display = "none";
        document.getElementById("register").style.display = "none";
        document.getElementById("txt-required").style.display = "none";
        document.getElementById("text-message").style.display = "block";




    }
    showTab(currentTab);
}

function validateForm() {
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab_");
    y = x[currentTab].querySelectorAll("input, select, textarea");
    for (i = 0; i < y.length; i++) {
        // Verifica si el campo está deshabilitado
        if (!y[i].disabled && y[i].hasAttribute("required")) {
            if (y[i].type === "radio") {
                var radioGroup = document.getElementsByName(y[i].name);
                if (![...radioGroup].some(radio => radio.checked)) {
                    valid = false;
                    // Aquí agregamos la clase "invalid" al botón de opción no seleccionado
                    radioGroup.forEach(radio => {
                        if (!radio.checked) {
                            radio.classList.add("invalid");
                        }
                    });
                }else{
                    radioGroup.forEach(radio => {
                        radio.classList.remove("invalid");
                    });
                }
            } else {
                if (y[i].value.trim() === "") {
                    if (!y[i].classList.contains("invalid")) {
                        y[i].classList.add("invalid");
                    }
                    valid = false;
                    
                } else {
                    // Si el campo no está vacío, quita la clase "invalid" (si está presente)
                    y[i].classList.remove("invalid");
                }
            }
        }
        
    }
    if (valid) {
        var step = document.getElementsByClassName("step")[currentTab];
        if (!step.classList.contains("finish")) {
            step.classList.add("finish");
        }
    }else{
        // Mostrar mensaje de error con SweetAlert2
        Swal.fire({
            icon: 'error',
            title: '<strong>Error de validación</strong>',
            text: 'Por favor, completa todos los campos obligatorios.',
        });
    }
    return valid;
}


function fixStepIndicator(n) {
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
}
var myLink = document.querySelector('a[href="#"]');
myLink.addEventListener('click', function (e) {
    e.preventDefault();
});