from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q

class MiAuthBackend(BaseBackend):
    def authenticate(self, request, cedula=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Verifica si el campo cedula está presente y no es None
        if cedula is not None:
            # Validar si la entrada es un correo electrónico
            is_email = "@" in cedula

            try:
                if is_email:
                    user = UserModel.objects.get(email=cedula)
                else:
                    user = UserModel.objects.get(cedula=cedula)
            except UserModel.DoesNotExist:
                return None  # No existe el usuario

            # Verificar la contraseña
            if user.check_password(password):
                return user  # Autenticación exitosa
            else:
                return None  # Contraseña incorrecta

        return None  # cedula es None, retorna None

    def get_user(self, user_id):
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None