from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
class GraduadoResource(resources.ModelResource):
    class Meta:
        model = Graduado

class GraduadoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = GraduadoResource

class AdministradorResource(resources.ModelResource):
    class Meta:
        model = Administrador

class AdministradorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = AdministradorResource
    
class CapacitacionResource(resources.ModelResource):
    class Meta:
        model = Capacitacion

class CapacitacionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = CapacitacionResource
    
class EmpleoResource(resources.ModelResource):
    class Meta:
        model = Empleo

class EmpleoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = EmpleoResource

class EmprendimientoResource(resources.ModelResource):
    class Meta:
        model = Emprendimiento

class EmprendimientoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = EmprendimientoResource    
    
class UserResource(resources.ModelResource):
    class Meta:
        model = User
class UserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = UserResource    
    

admin.site.register(Graduado, GraduadoAdmin)
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(Capacitacion, CapacitacionAdmin)
admin.site.register(Empleo, EmpleoAdmin)
admin.site.register(Emprendimiento, EmprendimientoAdmin)



