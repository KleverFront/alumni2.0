from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import *
from .forms import *
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from django.contrib.auth.forms import PasswordChangeForm




#################### INDEX ##############################


def intro(request):

    return render(request,'vistas_generales/intro_alumni.html' )



def index(request):
    user = request.user
    if user.is_authenticated:
        if user.is_graduado:

            return render(request,'vistas_generales\\index.html' )
        elif user.is_staff:
            return render(request,'vistas_generales\\index.html' )
        else:
            return redirect('formulario')
    else:
        return render(request,'vistas_generales\\index.html' ) 
    



#################### ADMINISTRADOR ##############################


     

@login_required(login_url='ingresar')
def admin_capacitaciones (request):
    if request.user.is_staff:
        capacitacion = Capacitacion.objects.all()
        contexto = {
            'capacitacion': capacitacion,
        }
        return render(request, 'vistas_administrador\\gestion_capacitaciones\\admin_capacitaciones.html',contexto)
    else:
        return redirect('index')


@login_required(login_url='ingresar')
def admin_emprendimientos (request):
    if request.user.is_staff:
        emprendimiento = Emprendimiento.objects.all()
        contexto = {
            'emprendimiento': emprendimiento
        }
        return render(request, 'vistas_administrador\\gestion_emprendimientos\\admin_emprendimientos.html',contexto)
    else:
        return redirect('index')


@login_required(login_url='ingresar')
def admin_empleos (request):
    if request.user.is_staff:
        empleo = Empleo.objects.all()
        contexto = {
            'empleo': empleo,
        }
        return render(request, 'vistas_administrador\\gestion_empleos\\admin_empleos.html',contexto) 
    else:
        return redirect('index')



@login_required(login_url='ingresar')
def admin_administradores (request):
    if request.user.is_staff:
        admin= Administrador.objects.all()
        contexto = {
            'admin':admin,
        }
        return render(request, 'vistas_administrador\\gestion_administrador\\admin_administradores.html',contexto) 
    else:
        return redirect('index')



@login_required(login_url='ingresar')
def admin_graduadospre (request):
    if request.user.is_staff:
        pregraduado = GraduadoPre.objects.all()
        for graduado_pre in pregraduado:
            graduado_pre.relaciones_filtradas = CarreraGraduado.objects.filter(graduado=graduado_pre)
        contexto = {
            'pregraduado': pregraduado,
        }
        return render(request, 'vistas_administrador\\gestion_graduados\\admin_graduadospre.html',contexto)
    else:
        return redirect('index')




## dato: la palabra "login" ya esta reservada
def login_base (request):
    login_form = AuthenticationBaseForm(request.POST or None)

    if request.method == 'POST' and 'login_admin' in request.POST:
        if login_form.is_valid():
            cedula = login_form.cleaned_data['cedula']
            password = login_form.cleaned_data['password']
            
            # Autenticar usando el backend personalizado
            user = authenticate(request=request, cedula=cedula, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, '¡Bievenido! :)')
                if user.is_staff:
                    return redirect('estadistica')
                else:
                    if user.is_graduado:
                        messages.success(request, '¡Disfrute de secciones como Capacitaciones o Bolsa Empleo! :)')
                        return redirect('index')
                    else:
                        return redirect('formulario')     
            else:
                alert_message = "Cédula o contraseña incorrecta"
                return render(request, 'vistas_generales\\login.html', {'login_form': login_form, 'alert_message': alert_message})
        else:
            messages.error(request, 'Formulario no válido. Verifique los campos.')
    return render(request, 'vistas_generales\\login.html', {'login_form': login_form})


@login_required(login_url='ingresar')
def reg_administrador(request):
    if request.user.is_staff:
         # Este código manejará tanto GET como POST
        if request.method == 'POST':
            form = AdministradorCreationForm(request.POST, request.FILES)
            if form.is_valid():
                administrador = form.save()
                return redirect('adminAdministradores')
            else:
                # Si el formulario no es válido, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")

                error_message = '<br>'.join(error_messages)
                script = f"""
                <script>
                    Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});
                </script>
                """

                return render(request, 'vistas_administrador\\gestion_administrador\\reg_administrador.html', {'form': form, 'script': script})
        else:
            form = AdministradorCreationForm()

        # Puedes personalizar el contexto según tus necesidades
        context = {
            'form': form,
            'titulo_pagina': 'Agregar Administrador',  # Por ejemplo, puedes agregar un título personalizado
        }

        return render(request, 'vistas_administrador\\gestion_administrador\\reg_administrador.html', context)
    else:
        return redirect('index')
    
    





@login_required(login_url='ingresar')
def editar_administrador (request, id):
    if request.user.is_staff:
        administrador = get_object_or_404(Administrador, id=id)
        if request.method == 'POST':
            form = AdministradorEditForm(request.POST,request.FILES, instance=administrador.base)
            if form.is_valid():
                form.save()
                return redirect('adminAdministradores')
            else:
                # Si el formulario no es válidos, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")
                print(error_messages)
                error_message = '<br>'.join(error_messages)
                script = f"""
                <script>
                    Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});
                </script>
                """

                return render(request, 'vistas_administrador\\gestion_administrador\\editar_administrador.html', {'form': form, 'script': script})
        else:
            form = AdministradorEditForm(instance=administrador.base)

        context = {
            'form': form,
            'titulo_pagina': f'Editar Administrador',
        }

        return render(request, 'vistas_administrador\\gestion_administrador\\editar_administrador.html', context)
    else:
        return redirect('index')
    



	
@login_required(login_url='ingresar')
def eliminar_administrador (request, id):
    if request.user.is_staff:
        admin = get_object_or_404(Administrador, id=id)

        if request.method == 'POST':
            
            if request.user.id == admin.base.id:
                # Desautenticar al usuario
                logout(request)
            admin.delete()
            messages.success(request, 'Administrador eliminado correctamente.')
            return redirect('adminAdministradores')  # Redirige a la página deseada después de eliminar
        # En el caso de 'GET', renderiza la plantilla con los detalles del graduado
        return render(request, 'vistas_administrador\\gestion_administrador\\eliminar_administrador.html', {'admin': admin})  
    else:
        return redirect('index')
    




#################### GRADUADO ##############################
    

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'vistas_graduado\\cambio_contraseña.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('cambio_password_exitoso')


    def form_invalid(self, form):
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{form.fields[field].label}: {error}")
        
        error_message = '<br>'.join(error_messages)
        
        # Usa SweetAlert2 para mostrar la notificación
        script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
        
        return render(
            self.request,
            self.template_name,
            {'form': form, 'script': script}
        )

        

@login_required(login_url='ingresar')
def previus_formulario(request):

    return render(request,'vistas_graduado\\previus_form_graduado.html' )



@login_required(login_url='ingresar')
def perfil_graduado(request):
    user = request.user
    if user.is_staff:
        return redirect('adminAdministradores')
    elif user.is_graduado:
            # Intenta obtener la instancia del modelo Graduado asociada al usuario
        pregraduado = get_object_or_404(GraduadoPre, base=user)
        graduado = get_object_or_404(Graduado,base_pregraduado=pregraduado)

        # Crea un contexto con la información del usuario y del graduado
        contexto = {
            'user': user, 
            'pregraduado': pregraduado,
            'graduado': graduado
        }

        return render(request, 'vistas_graduado\\perfil_usuario.html', contexto)
    else:
        pregraduado = get_object_or_404(GraduadoPre, base=user)
        contexto = {
            'user': user, 
            'pregraduado': pregraduado,
        }
        return render(request, 'vistas_graduado\\perfilusuario.html', contexto)

 

@login_required(login_url='ingresar')
def reg_pregraduado(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = GraduadoPreForm(request.POST)
            if form.is_valid():
                graduado_pre = form.save()

                return redirect('adminGraduadospre')
            else:
                # Si el formulario no es válido, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")
                
                error_message = '<br>'.join(error_messages)
                
                # Usa SweetAlert2 para mostrar la notificación
                script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
                
                return render(request, 'vistas_administrador\\gestion_graduados\\reg_pregraduado.html', {'form': form, 'script': script})
        else:
            form = GraduadoPreForm()

        return render(request, 'vistas_administrador\\gestion_graduados\\reg_pregraduado.html', {'form': form})   
    else:
        return redirect('index')
     



@login_required(login_url='ingresar')
def registro_graduado(request):
    graduado_pre = GraduadoPre.objects.get(base=request.user.id)
    graduado_pre.relaciones_filtradas = CarreraGraduado.objects.filter(graduado=graduado_pre)
    form = GraduadoForm()

    if request.method == 'POST':
        form = GraduadoForm(request.POST,request.FILES)
        if form.is_valid():

            periodos_carreras = request.POST.getlist('periodo_ingreso')

            for nombre_carrera, periodo_carrera in zip(graduado_pre.relaciones_filtradas, periodos_carreras):
                if nombre_carrera:
                    carrera_obj, created = Carrera.objects.get_or_create(nombre=nombre_carrera.carrera.nombre)
                    carrera_final, createded = CarreraGraduado.objects.get_or_create(graduado=graduado_pre, carrera=carrera_obj)
                    carrera_final.periodo_ingreso = periodo_carrera
                    carrera_final.save()
            # Guarda el objeto del modelo con el campo base configurado
            objeto_modelo = form.save(commit=False)
            usuario_base = graduado_pre.base
            usuario_base.is_graduado = True
            usuario_base.save()
            objeto_modelo.base_pregraduado = graduado_pre
            objeto_modelo.save()

            return redirect('index')
        else:
            # Si el formulario no es válido, muestra una notificación de error
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{form.fields[field].label}: {error}")
            
            error_message = '<br>'.join(error_messages)
            
            # Usa SweetAlert2 para mostrar la notificación
            script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
            
            return render(request, 'vistas_graduado\\reg_graduado_formulario.html', {'form':form, 'script': script})  
              
    return render(request, 'vistas_graduado\\reg_graduado_formulario.html', {'form':form,'graduado_pre':graduado_pre})




@login_required(login_url='ingresar')
def editar_graduado(request):

    graduado_pre = GraduadoPre.objects.get(base=request.user.id)
    graduado = get_object_or_404(Graduado,base_pregraduado=graduado_pre)
    graduado_pre.relaciones_filtradas = CarreraGraduado.objects.filter(graduado=graduado_pre)

    if request.method == 'POST':
        form = GraduadoForm(request.POST,request.FILES,instance=graduado)
        if form.is_valid():

            periodos_carreras = request.POST.getlist('periodo_ingreso')

            for nombre_carrera, periodo_carrera in zip(graduado_pre.relaciones_filtradas, periodos_carreras):
                if nombre_carrera:
                    carrera_obj, created = Carrera.objects.get_or_create(nombre=nombre_carrera.carrera.nombre)
                    carrera_final, createded = CarreraGraduado.objects.get_or_create(graduado=graduado_pre, carrera=carrera_obj)
                    carrera_final.periodo_ingreso = periodo_carrera
                    carrera_final.save()
            # Guarda el objeto del modelo con el campo base configurado
            objeto_modelo = form.save(commit=False)
            usuario_base = graduado_pre.base
            usuario_base.is_graduado = True
            usuario_base.save()
            objeto_modelo.base_pregraduado = graduado_pre
            objeto_modelo.save()

            return redirect('index')
        else:
            # Si el formulario no es válido, muestra una notificación de error
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{form.fields[field].label}: {error}")
            
            error_message = '<br>'.join(error_messages)
            
            # Usa SweetAlert2 para mostrar la notificación
            script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
            
            return render(request, 'vistas_graduado\\reg_graduado_formulario.html', {'form':form, 'script': script})  
    else:
        form = GraduadoForm(instance=graduado)
              
    return render(request, 'vistas_graduado\\reg_graduado_formulario.html', {'form':form,'graduado_pre':graduado_pre})



@login_required(login_url='ingresar')
def registro_carrera(request,id):
    if request.user.is_staff:
        graduado_pre = get_object_or_404(GraduadoPre, id=id)

        if request.method == 'POST':
            form = CarreraGraduadoForm(request.POST)
            if form.is_valid():
                carreras_nombres = form.cleaned_data['carreras']
                periodo_graduado = form.cleaned_data['periodo_graduado']

                carrera_obj, created = Carrera.objects.get_or_create(nombre=carreras_nombres)
                CarreraGraduado.objects.create(graduado=graduado_pre, carrera=carrera_obj, periodo_graduado=periodo_graduado)
                
                return redirect('adminGraduadospre')
            else:
                # Si el formulario no es válido, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")
                
                error_message = '<br>'.join(error_messages)
                
                # Usa SweetAlert2 para mostrar la notificación
                script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
                
                return render(request, 'vistas_administrador\\gestion_graduados\\reg_carrera.html', {'form':form, 'script': script})  
        else:
            form = CarreraGraduadoForm()      
        return render(request, 'vistas_administrador\\gestion_graduados\\reg_carrera.html', {'form':form}) 
    else:
        return redirect('index')
     


@login_required(login_url='ingresar')
def editar_carrera(request, id):
    if request.user.is_staff:
        carrera = get_object_or_404(CarreraGraduado, id=id)
        if request.method == 'POST':
            form = CarreraGraduadoForm(request.POST, instance=carrera)
            if form.is_valid():
                carreras_nombres = form.cleaned_data['carreras']
                carrera_, created = Carrera.objects.get_or_create(nombre=carreras_nombres)
                carrera.carrera_id = carrera_
                form.save()
                carrera.save()

                return redirect('adminGraduadospre')
            else:
                # Si el formulario no es válido, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")
                
                error_message = '<br>'.join(error_messages)
                
                # Usa SweetAlert2 para mostrar la notificación
                script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
                
                return render(request, 'vistas_administrador\\gestion_graduados\\reg_carrera.html', {'form':form, 'script': script}) 
                
        else:
            form = CarreraGraduadoForm(instance=carrera)

        contexto = {
            'form': form,
            'carrera': carrera,
        }
        return render(request, 'vistas_administrador\\gestion_graduados\\reg_carrera.html', contexto)
    else:
        return redirect('index')
    



@login_required(login_url='ingresar')
def eliminar_carrera(request, id):
    if request.user.is_staff:
        carrera = get_object_or_404(CarreraGraduado, id=id)
        if request.method == 'POST':
            carrera.delete()
            messages.success(request, 'Carrera eliminada correctamente.')
            return redirect('adminGraduadospre')
        
        return render(request, 'vistas_administrador\\gestion_graduados\\eliminar_carrera.html', {'carrera': carrera})
    else:
        return redirect('index')
    
             

  

@login_required(login_url='ingresar')
def editar_pregraduado(request, id):
    if request.user.is_staff:
        graduado_pre = get_object_or_404(GraduadoPre, id=id)
        form = GraduadoPreEditForm(request.POST or None, instance=graduado_pre.base)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('adminGraduadospre')
            else:
                # Si el formulario no es válido, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")
                
                error_message = '<br>'.join(error_messages)
                
                # Usa SweetAlert2 para mostrar la notificación
                script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
                
                return render(request, 'vistas_administrador\\gestion_graduados\\reg_carrera.html', {'form':form, 'script': script})
        return render(request, 'vistas_administrador\\gestion_graduados\\editar_pregraduado.html', {'form': form, 'graduado_pre': graduado_pre})
    else:
        return redirect('index')
    




@login_required(login_url='ingresar')
def eliminar_pregraduado (request, id):
    if request.user.is_staff:
        graduado = get_object_or_404(GraduadoPre, id=id)

        if request.method == 'POST':
            graduado.delete()
            messages.success(request, 'Graduado eliminado correctamente.')
            return redirect('adminGraduadospre')  # Redirige a la página deseada después de eliminar
        # En el caso de 'GET', renderiza la plantilla con los detalles del graduado
        return render(request, 'vistas_administrador\\gestion_graduados\\eliminar_pregraduado.html', {'graduado': graduado})
    else:
        return redirect('index')
    




#################### EMPRENDIMIENTOS ##############################

 
def emprendimientos(request):
    emprendimientos = Emprendimiento.objects.all().order_by('-fecha')  # Consulta inicial

    # Configura la paginación
    paginator = Paginator(emprendimientos, 4)  # 4 emprendimientos por página
    page = request.GET.get('page')

    try:
        emprendimientos_pagina = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        emprendimientos_pagina = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango, muestra la última página
        emprendimientos_pagina = paginator.page(paginator.num_pages)

    contexto = {
        'emprendimientos': emprendimientos_pagina
    }

    return render(request,'vistas_generales\\emprendimientos.html' , contexto)   


@csrf_exempt
def filemanager(request):
    if request.method == 'POST':
        # Obtén el archivo subido desde la solicitud
        file = request.FILES.get('file')
        # Guarda el archivo en el servidor
        with open('path/to/save/file', 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        # Devuelve la URL del archivo como respuesta
        return JsonResponse({'location': '/path/to/file.ext'})
    else:
        # Redirige a una página de error si la solicitud no es POST
        return redirect('error')


@login_required(login_url='ingresar')
def reg_emprendimiento(request):
    if request.user.is_staff:
        data = { 'form': EmprendimientoForm()}

        if request.method == 'POST':
            form = EmprendimientoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                titulo = form.cleaned_data['titulo']
                messages.success(request,f'Emprendimiento {titulo} creado')            
                return redirect ('adminEmprendimientos')  
            else: 
                # Si el formulario no es válido, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")
                
                error_message = '<br>'.join(error_messages)
                
                # Usa SweetAlert2 para mostrar la notificación
                script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
                return render(request, 'vistas_administrador\\gestion_emprendimientos\\reg_emprendimiento.html', {'form':form, 'script': script})
        else:
            data = { 'form': EmprendimientoForm(files=request.FILES)}    
        return render(request, 'vistas_administrador\\gestion_emprendimientos\\reg_emprendimiento.html', data)  
    else:
        return redirect('index')
    


@login_required(login_url='ingresar')
def editar_emprendimiento (request,id):
    if request.user.is_staff:
        emprendimiento= Emprendimiento.objects.get(id=id)
        if request.method == 'GET':
            form = EmprendimientoForm(instance=emprendimiento)	
        else:
            form = EmprendimientoForm(request.POST,instance=emprendimiento)
            if form.is_valid():
                form.save()
            return redirect('adminEmprendimientos')
        return render(request,'vistas_administrador\\gestion_emprendimientos\\reg_emprendimiento.html', {'form':form})
    else:
        return redirect('index')
	
	
@login_required(login_url='ingresar')
def eliminar_emprendimiento (request,id):
    if request.user.is_staff:
        emprendimiento=Emprendimiento.objects.get(id=id)
        if request.method == 'POST':
            emprendimiento.delete()
            return redirect('adminEmprendimientos')
        return render(request,'vistas_administrador\\gestion_emprendimientos\\eliminar_emprendimiento.html', {'emprendimiento':emprendimiento})
    else:
        return redirect('index')
	



#################### EMPLEOS ##############################


@login_required(login_url='ingresar')
def empleos(request):
    # Obtener todos los empleos sin filtros
    empleos = Empleo.objects.all()

    # Procesar el formulario de filtros
    filtro_form = FiltroEmpleoForm(request.GET)
    if filtro_form.is_valid():
        # Obtener los valores de los campos del formulario
        puesto_buscar = filtro_form.cleaned_data.get('puesto_buscar')
        areas = filtro_form.cleaned_data.get('areas')

        # Aplicar los filtros según los valores proporcionados
        if puesto_buscar:
            empleos = empleos.filter(puesto__icontains=puesto_buscar)
        if areas:
            empleos = empleos.filter(carrera_sugerida=areas)
        # Puedes agregar más campos de filtro según tus necesidades

    contexto = {
        'empleos': empleos,
        'filtro_form': filtro_form,
    }
    return render(request, 'vistas_generales\\empleos.html', contexto)


@login_required(login_url='ingresar')
def reg_empleo(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form= EmpleoForm(request.POST,  request.FILES)
            if form.is_valid():
                form.save()
                puesto = form.cleaned_data['puesto']
                messages.success(request,f'Empleo {puesto} creado')
                return redirect ('adminEmpleos')
            else:
                # Si el formulario no es válido, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")
            
                error_message = '<br>'.join(error_messages)
                
                # Usa SweetAlert2 para mostrar la notificación
                script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
                return render(request, 'vistas_administrador\\gestion_empleos\\reg_empleo.html', {'form':form, 'script': script})
        else:
            data = { 'form': EmpleoForm(files=request.FILES)}        
        return render(request, 'vistas_administrador\\gestion_empleos\\reg_empleo.html', data )  
    else:
        return redirect('index')
    


@login_required(login_url='ingresar')
def editar_empleo(request,id):
    if request.user.is_staff:
        empleo= Empleo.objects.get(id=id)
        if request.method == 'GET':
            form = EmpleoForm(instance=empleo)	
        else:
            form = EmpleoForm(request.POST,instance=empleo)
            if form.is_valid():
                form.save()
            return redirect('adminEmpleos')
        return render(request,'vistas_administrador\\gestion_empleos\\reg_empleo.html', {'form':form})
    else:
        return redirect('index')
	


@login_required(login_url='ingresar')
def eliminar_empleo(request,id):
    if request.user.is_staff:
        empleo= Empleo.objects.get(id=id)
        if request.method == 'POST':
            empleo.delete()
            return redirect('adminEmpleos')
        return render(request,'vistas_administrador\\gestion_empleos\\eliminar_empleo.html', {'empleo':empleo})
    else:
        return redirect('index')
	


#################### CAPACITACIONES ##############################

@login_required(login_url='ingresar')
def capacitaciones(request):
    capacitaciones = Capacitacion.objects.all().order_by('-fecha')

    # Configura la paginación
    paginator = Paginator(capacitaciones, 3)
    page = request.GET.get('page')

    try:
        capacitaciones_pagina = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        capacitaciones_pagina = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango, muestra la última página
        capacitaciones_pagina = paginator.page(paginator.num_pages)

    contexto = {
        'capacitaciones': capacitaciones_pagina
    }

    return render(request, 'vistas_generales\\capacitaciones.html', contexto)



@login_required(login_url='ingresar')
def reg_capacitacion(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CapacitacionForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                titulo = form.cleaned_data['titulo']
                messages.success(request, f'Capacitación {titulo} creada')            
                return redirect('adminCapacitaciones')  
            else: 
                # Si el formulario no es válido, muestra una notificación de error
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{form.fields[field].label}: {error}")
                
                error_message = '<br>'.join(error_messages)
                # Usa SweetAlert2 para mostrar la notificación
                script = f"Swal.fire({{ icon: 'error', title: 'Error en el formulario', html: '{error_message}' }});"
                return render(request, 'vistas_administrador\\gestion_capacitaciones\\reg_capacitacion.html', {'form':form, 'script': script})
        else:
            data = { 'form': CapacitacionForm(files=request.FILES)}     
        return render(request, 'vistas_administrador\\gestion_capacitaciones\\reg_capacitacion.html', data)
    else:
        return redirect('index')
    


@login_required(login_url='ingresar')
def editar_capacitacion(request,id):
    if request.user.is_staff:
        capacitacion= Capacitacion.objects.get(id=id)
        if request.method == 'GET':
            form = CapacitacionForm(instance=capacitacion)	
        else:
            form = CapacitacionForm(request.POST,instance=capacitacion)
            if form.is_valid():
                form.save()
            return redirect('adminCapacitaciones')
        return render(request,'vistas_administrador\\gestion_capacitaciones\\reg_capacitacion.html', {'form':form})
    else:
        return redirect('index')
	


@login_required(login_url='ingresar')
def eliminar_capacitacion (request,id):
    if request.user.is_staff:
        capacitacion= Capacitacion.objects.get(id=id)
        if request.method == 'POST':
            capacitacion.delete()
            return redirect('adminCapacitaciones')
        return render(request,'vistas_administrador\\gestion_capacitaciones\\eliminar_capacitacion.html', {'capacitacion':capacitacion})
    else:
        return redirect('index')




#################### ESTADISTICAS ##############################




@login_required(login_url='ingresar')
def estadistica(request):
    if request.user.is_staff:
        objeto = CarreraGraduado.objects.all()
        contexto = {
            'objeto': objeto,
        }
        return render(request, 'vistas_administrador\\estadistica.html', contexto)
    else:
        return redirect('index')



