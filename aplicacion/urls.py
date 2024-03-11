from django.urls import path, include
from .views import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static


urlpatterns =[

    path('estadistica',estadistica, name ='estadistica'),
    
    ##############   REGISTRO DEL FORMULARIO POR PARTE DEL GRADUADO #########
    path('registro-graduado',registro_graduado, name ='registro'),

    ###############  VISTAS DEL LADO DEL CLIENTE ######################
    path('intro', intro, name='intro'),
    path('alumni',index, name ='index'),
    path('perfil-usuario',perfil_graduado, name ='perfil'),
    path('ingresar',login_base, name ='ingresar'),
    path('formulario',previus_formulario, name ='formulario'),
    path('empleos',empleos, name ='empleos'),
    path('emprendimientos',emprendimientos, name ='emprendimientos'),
    path('capacitaciones',capacitaciones, name = 'capacitaciones'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('filemanager/', filemanager, name='filemanager'),
    path('editar-encuesta',editar_graduado, name ='editarEncuesta'),

    ############## TABLAS DE ADMINISTRACION PARA EL ADMIN #################
    path('admin-administradores',admin_administradores, name = 'adminAdministradores'),
    path('admin-graduadospre',admin_graduadospre, name = 'adminGraduadospre'),
    path('admin_emprendimientos',admin_emprendimientos, name = 'adminEmprendimientos'),
    path('admin_capacitaciones',admin_capacitaciones, name = 'adminCapacitaciones'),
    path('admin_empleos',admin_empleos, name = 'adminEmpleos'),


    ##########  REGISTROS EN EL ADMINISTRADOR ###############
    path('registro-pregraduado',reg_pregraduado, name ='regPregraduado'),
    path('registro-administrador',reg_administrador, name ='regAdministrador'),
    path('registro-capacitacion',reg_capacitacion, name = 'regCapacitacion'),
    path('registro-empleo',reg_empleo, name = 'regEmpleo'),
    path('registro-emprendimiento',reg_emprendimiento, name = 'regEmprendimiento'),
    path('admin-graduadospre/registro-carrera/<int:id>/',registro_carrera, name = 'regCarrera'),
    
 
    ############   EDITAR ######################
    path('editar-pregraduado/<int:id>/', editar_pregraduado, name='editarPregraduado'),
    path('editar-administrador/<id>/' ,editar_administrador, name='editarAdministrador'),
    path('editar-empleo/<id>/' ,editar_empleo, name='editarEmpleo'),
    path('editar-capacitacion/<id>/' ,editar_capacitacion, name='editarCapacitacion'),
    path('editar-emprendimiento/<id>/' ,editar_emprendimiento, name='editarEmprendimiento'),
    path('admin-graduadospre/editar-carrera/<int:id>/',editar_carrera, name = 'editarCarrera'),

    ##########  ELIMINAR   ###########################

    path('eliminar-pregraduado/<id>/' ,eliminar_pregraduado, name='eliminarPregraduado'),
    path('eliminar-administrador/<id>/' ,eliminar_administrador, name='eliminarAdministrador'),
    path('eliminar-capacitacion/<id>/' ,eliminar_capacitacion, name='eliminarCapacitacion'),
    path('eliminar-empleo/<id>/' ,eliminar_empleo, name='eliminarEmpleo'),
    path('eliminar-emprendimiento/<id>/' ,eliminar_emprendimiento, name='eliminarEmprendimiento'),
    path('admin-graduadospre/eliminar-carrera/<id>/' ,eliminar_carrera, name='eliminarCarrera'),


    ##########  VISTAS DE CAMBIO DE OLVIDE MI CONTRASEÑA   ###########################
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password-reset.html"), name='password_reset'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password-confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),

    ##########  VISTAS DE CAMBIO DE CONTRASEÑA GRADUADO   ###########################
    path('change_password/', login_required(CustomPasswordChangeView.as_view()), name='profile_password_change'),
    path('change_password_done/', login_required(auth_views.PasswordChangeDoneView.as_view(template_name="cambio_contraseña_completado.html")), name='cambio_password_exitoso'),
 
]
