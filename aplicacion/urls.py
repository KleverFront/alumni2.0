from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

urlpatterns =[

    path('estadistica',estadistica, name ='estadistica'),
    
    ##############   REGISTRO DEL FORMULARIO POR PARTE DEL GRADUADO #########
    path('registro/graduado',registro_graduado, name ='registro'),

    ###############  VISTAS DEL LADO DEL CLIENTE ######################

    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('alumni',index, name ='index'),
    path('perfil/usuario',perfil_graduado, name ='perfil'),
    path('ingresar',login_base, name ='ingresar'),
    path('formulario',previus_formulario, name ='formulario'),
    path('empleos',empleos, name ='empleos'),
    path('emprendimientos',emprendimientos, name ='emprendimientos'),
    path('capacitaciones',capacitaciones, name = 'capacitaciones'),
    path('filemanager/', filemanager, name='filemanager'),
    path('editar/encuesta',editar_graduado, name ='editarEncuesta'),

    ############## TABLAS DE ADMINISTRACION PARA EL ADMIN #################
    path('administrador/administradores',admin_administradores, name = 'adminAdministradores'),
    path('administrador/graduadospre',admin_graduadospre, name = 'adminGraduadospre'),
    path('administrador/emprendimientos',admin_emprendimientos, name = 'adminEmprendimientos'),
    path('administrador/capacitaciones',admin_capacitaciones, name = 'adminCapacitaciones'),
    path('administrador/empleos',admin_empleos, name = 'adminEmpleos'),
    path('administrador/configuraciones',config, name = 'adminConfig'),


    ##########  REGISTROS EN EL ADMINISTRADOR ###############
    path('registro/pregraduado',reg_pregraduado, name ='regPregraduado'),
    path('registro/administrador',reg_administrador, name ='regAdministrador'),
    path('registro/capacitacion',reg_capacitacion, name = 'regCapacitacion'),
    path('registro/empleo',reg_empleo, name = 'regEmpleo'),
    path('registro/emprendimiento',reg_emprendimiento, name = 'regEmprendimiento'),
    path('registro/configuracion',reg_config, name = 'regConfiguracion'),
    path('administrador/graduadospre/registro-carrera/<int:id>/',registro_carrera, name = 'regCarrera'),
    path('administrador/graduadospre/change/password/graduado/<int:id>/',cambiar_password_graduado, name = 'change_pass_graduado'),
    path('administrador/graduadospre/change/password/admin/<int:id>/',cambiar_password_administrador, name = 'change_pass_admin'),
    
 
    ############   EDITAR ######################
    path('editar/pregraduado/<int:id>/', editar_pregraduado, name='editarPregraduado'),
    path('editar/administrador/<id>/' ,editar_administrador, name='editarAdministrador'),
    path('editar/empleo/<id>/' ,editar_empleo, name='editarEmpleo'),
    path('editar/capacitacion/<id>/' ,editar_capacitacion, name='editarCapacitacion'),
    path('editar/emprendimiento/<id>/' ,editar_emprendimiento, name='editarEmprendimiento'),
    path('administrador/graduadospre/editar/carrera/<int:id>/',editar_carrera, name = 'editarCarrera'),
    path('editar/configuracion/<id>/' ,editar_config, name='editarConfiguracion'),

    ##########  ELIMINAR   ###########################

    path('eliminar/pregraduado/<id>/' ,eliminar_pregraduado, name='eliminarPregraduado'),
    path('eliminar/administrador/<id>/' ,eliminar_administrador, name='eliminarAdministrador'),
    path('eliminar/capacitacion/<id>/' ,eliminar_capacitacion, name='eliminarCapacitacion'),
    path('eliminar/empleo/<id>/' ,eliminar_empleo, name='eliminarEmpleo'),
    path('eliminar/emprendimiento/<id>/' ,eliminar_emprendimiento, name='eliminarEmprendimiento'),
    path('administrador/graduadospre/eliminar/carrera/<id>/' ,eliminar_carrera, name='eliminarCarrera'),
    path('eliminar/configuracion/<id>/' ,eliminar_config, name='eliminarConfiguracion'),


    ##########  VISTAS DE CAMBIO DE OLVIDE MI CONTRASEÑA   ###########################
    path('reset/password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/password/send/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/password/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    ##########  VISTAS DE CAMBIO DE CONTRASEÑA GRADUADO   ###########################
    path('change/password/', login_required(CustomPasswordChangeView.as_view()), name='profile_password_change'),
    path('change/password/done/', login_required(CustomPasswordChangeDoneView.as_view()), name='cambio_password_exitoso'),
    path('', intro, name='intro'),

]
