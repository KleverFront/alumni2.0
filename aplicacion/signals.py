from django.db.models.signals import post_delete
from django.dispatch import receiver
import os



@receiver(post_delete, sender='aplicacion.Graduado')
def eliminar_archivos_relacionados(sender, instance, **kwargs):
    # Eliminar archivos asociados al eliminar el objeto Graduado
    from .models import Graduado
    if instance.fotografia and os.path.isfile(instance.fotografia.path):
        os.remove(instance.fotografia.path)
    if instance.curriculum and os.path.isfile(instance.curriculum.path):
        os.remove(instance.curriculum.path)

