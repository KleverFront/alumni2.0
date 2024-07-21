from django.db.models.signals import post_delete, pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import os



@receiver(post_delete, sender="aplicacion.Graduado")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Graduado
    # Eliminar archivos asociados al eliminar el objeto Graduado
    if instance.fotografia and os.path.isfile(instance.fotografia.path):
        os.remove(instance.fotografia.path)
    if instance.curriculum and os.path.isfile(instance.curriculum.path):
        os.remove(instance.curriculum.path)


### PARA ARCHIVOS EN CASO DE EDICION ####

def delete_file(instance,sender,name_attribute):
    if instance and hasattr(instance, name_attribute):
        old_instance = sender.objects.filter(pk=instance.pk).first()
        if old_instance and getattr(old_instance, name_attribute) and os.path.isfile(getattr(old_instance, name_attribute).path):
            if getattr(instance, name_attribute) != getattr(old_instance, name_attribute):
                os.remove(getattr(old_instance, name_attribute).path)

@receiver(pre_save, sender="aplicacion.Capacitacion")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Capacitacion
    delete_file(instance,sender,"portada")


@receiver(pre_save, sender="aplicacion.Emprendimiento")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Emprendimiento
    delete_file(instance,sender,"portada")


@receiver(pre_save, sender="aplicacion.Empleo")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Empleo
    delete_file(instance,sender,"portada")


@receiver(pre_save, sender="aplicacion.Empleo")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Graduado
    delete_file(instance,sender,"portada")

@receiver(pre_save, sender="aplicacion.Administrador")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Administrador
    delete_file(instance,sender,"imagen")


@receiver(pre_save, sender="aplicacion.Graduado")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Graduado
    delete_file(instance,sender,"fotografia")
    delete_file(instance,sender,"curriculum")

@receiver(pre_save, sender="aplicacion.Configuraciones")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Configuraciones
    delete_file(instance,sender,"image_home")
    delete_file(instance,sender,"image_mision")
    delete_file(instance,sender,"image_vision")
    delete_file(instance,sender,"teacher_in_charge_image")
    delete_file(instance,sender,"favicon")
    delete_file(instance,sender,"favicon")
    delete_file(instance,sender,"image_nav")
    delete_file(instance,sender,"image_login")

@receiver(pre_delete, sender="aplicacion.Configuraciones")
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    from .models import Configuraciones
    delete_file(instance,sender,"image_home")
    delete_file(instance,sender,"image_mision")
    delete_file(instance,sender,"image_vision")
    delete_file(instance,sender,"teacher_in_charge_image")
    delete_file(instance,sender,"favicon")
    delete_file(instance,sender,"favicon")
    delete_file(instance,sender,"image_nav")
    delete_file(instance,sender,"image_login")
    
    

