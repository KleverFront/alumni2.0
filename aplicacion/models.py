import os
from datetime import datetime

from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Carrera(models.Model):
    carreras_opciones = [
        ('Tecnología Superior en Procesamiento de Alimentos', 'Tecnología Superior en Procesamiento de Alimentos'),
        ('Tecnología en Agroindustrias', 'Tecnología en Agroindustrias'),
        ('Tecnología en Desarrollo Infantil Integral', 'Tecnología en Desarrollo Infantil Integral'),
        ('Tecnología Superior en Contabilidad', 'Tecnología Superior en Contabilidad'),
        ('Tecnología Superior en Mecánica Automotriz', 'Tecnología Superior en Mecánica Automotriz'),
        ('Tecnología Superior en Electricidad', 'Tecnología Superior en Electricidad'),
        ('Tecnología Superior en Desarrollo de Software', 'Tecnología Superior en Desarrollo de Software'),
        ('Otro', 'Otro'),
    ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(choices = carreras_opciones,max_length=80, unique=True)
    
    def __str__(self):
        return self.id
    

class UsuarioManager(BaseUserManager):
    def create_user(self, cedula, password=None, **extra_fields):
        if not cedula:
            raise ValueError('El campo de cédula debe estar configurado')
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_graduado(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_graduado', True)
        return self.create_user(cedula, password, **extra_fields)

    def create_administrador(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(cedula, password, **extra_fields)
    def create_superuser(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cedula, password, **extra_fields)
    

class UsuarioBase(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField('Cedula', max_length=15, unique=True)
    nombres = models.CharField(max_length=80, default="",null=False)
    apellidos = models.CharField(max_length=80, default="",null=False)
    email = models.EmailField( max_length=100,unique=True, default='',validators=[EmailValidator(message='Introduzca una dirección de correo electrónico válida.')])
    

    # Campos necesarios para AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_graduado = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'cedula'
    

    # Cambios para resolver el conflicto en los nombres de los accesores inversos
    groups = models.ManyToManyField(Group, blank=True, related_name='usuario_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='usuario_user_permissions')

    def __str__(self):
        return self.cedula 

class GraduadoPre(models.Model):
    id = models.AutoField(primary_key=True)
    base = models.OneToOneField(UsuarioBase, on_delete=models.CASCADE,related_name='graduadopre')
    
    carreras = models.ManyToManyField(Carrera , through='CarreraGraduado',blank=True)
    
    # Campos necesarios para AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_graduado = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'cedula'
    

    # Cambios para resolver el conflicto en los nombres de los accesores inversos
    groups = models.ManyToManyField(Group, blank=True, related_name='graduadopre_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='graduadopre_user_permissions')

    def delete(self, using=None, keep_parents=False):
        # Eliminar el UsuarioBase asociado
        if self.base:
            self.base.delete()
        
        # Llama a delete de la clase base para eliminar el preGraduado
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.cedula 


class CarreraGraduado(models.Model):
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    graduado = models.ForeignKey(
        GraduadoPre,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    periodo_graduado = models.CharField(
        max_length = 15,
        null = True,
        blank = True
    )
    periodo_ingreso = models.CharField(
        'Periodo de Ingreso',
        max_length = 15,
        null = True, 
        blank = True, 
        default=''
    )


class Administrador(models.Model):
    id = models.AutoField(primary_key=True)
    base = models.OneToOneField(UsuarioBase, on_delete=models.CASCADE,related_name='administrador')
    imagen = models.ImageField(upload_to = "administrador",null = True)

    # Campos necesarios para AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'cedula'

    groups = models.ManyToManyField(Group, blank=True, related_name='administrador_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='administrador_user_permissions')

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        # Eliminar el UsuarioBase asociado
        if self.base:
            self.base.delete()
        
        # Llama a delete de la clase base para eliminar el Administrador
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.cedula 


   

class Graduado(models.Model):

    campus_opciones = [
        ('Campus Loja', 'Campus Loja'),
        ('Campus Vilcabamba', 'Campus Vilcabamba'),
        ('Realizo cambio de campus', 'Realizo cambio de campus')
    ]
    como_fue_la_formacion_opciones = [
        ('Muy buena', 'Muy buena'),
        ('Bueno', 'Bueno'),
        ('Neutro', 'Neutro'),
        ('Regular', 'Regular'),
        ('Mala', 'Mala'),
        ('Otro', 'Otro'),
    ]
    experiencia_cuantas_horas_opciones = [
        ('2 a 4 horas', '2 a 4 horas'),
        ('4 a 6 horas', '4 a 6 horas'),
        ('6 a 8 horas', '6 a 8 horas'),
        ('8 a 10 horas', '8 a 10 horas'),
        ('10 a 12 horas', '10 a 12 horas')
    ]
    grado_importacia_opciones = [
        ('Muy importante', 'Muy importante'),
        ('Importante', 'Importante'),
        ('Poco importante', 'Poco importante'),
        ('Nada importante', 'Nada importante')
    ]
    calificar_atributos_instituto_opciones = [
        ('4. Muy bueno', '4. Muy bueno'),
        ('3. Bueno', '3. Bueno'),
        ('2. Malo', '2. Malo'),
        ('1. Muy malo', '1. Muy malo'), 
    ]
    titulacion_opciones = [
        ('Trabajo de Integración Curricular', 'Trabajo de Integración Curricular'),
        ('Examen complexivo', 'Examen complexivo'),
    ]
    empresa_laboral_tipo_opciones = [
        ('Pública', 'Pública'),
        ('Privada', 'Privada'),
        ('Emprendimiento propio', 'Emprendimiento propio'),
        ('No laboro', 'No laboro')
    ]
    etnias_opciones = [
        ('Mestizo', 'Mestizo'),
        ('Afroecuatoriano', 'Afroecuatoriano'),
        ('Indígena', 'Indígena'),
        ('Blanco', 'Blanco'),
        ('Montubio', 'Montubio'),
        ('Amazonico', 'Amazonico'),
    ]
    estadocivil_opciones = [
        ('Soltero/a', 'Soltero/a'),
        ('Unión de Hechos' , 'Unión de Hechos'),
        ('Divorciado/a', 'Divorciado/a'),
        ('Casado/a' ,'Casado/a'),
        ('Viudo/a' , 'Viudo/a'),
    ]
    jornada_opciones = [
        ('Tiempo Completo', 'Tiempo Completo'),
        ('Medio Tiempo', 'Medio Tiempo'),
        ('Tiempo Parcial', 'Tiempo Parcial'),
    ]
    zona_opciones = [
        ('Urbana', 'Urbana'),
        ('Rural', 'Rural')

    ]   
    cursos_opciones = [
        ('Ninguno', 'Ninguno'),
        ('1-3',  '1-3'),
        ('4-6', '4-6'),
        ('7-9', '7-9'),
        ('10 o más', '10 o más'),

    ]

    ##-------- Datos Personales------------ ##
    base_pregraduado = models.OneToOneField(GraduadoPre, on_delete=models.CASCADE, related_name='graduado')
    is_graduado = models.BooleanField(default=True)
    correo_personal = models.EmailField(max_length=84)
    f_nacimiento = models.DateField()
    direccion = models.CharField(max_length=350)
    telefono_fijo = models.CharField(max_length=15, null = True , blank = True, default='')
    celular = models.CharField(max_length=15)
    nacionalidad = models.CharField(max_length=30,null = True, blank = True, default='')
    etnia = models.CharField(choices=etnias_opciones,max_length = 50, null = True, blank = True, default='')
    sexo = models.CharField(max_length = 20)
    estado_civil = models.CharField(choices=estadocivil_opciones,max_length = 50,null = True, blank = True, default='')
    discapacidad = models.CharField(max_length=5,null = True, blank = True,default='')
    cual_discapacidad = models.CharField(max_length=70,null = True, blank = True,default='')
    fotografia = models.ImageField(upload_to = "perfil", null = True, blank = True)
   
    ##-------- Información Académica------------ ##
    
    campus = models.CharField(max_length=60,choices=campus_opciones)
    titulacion = models.CharField(max_length=35,choices=titulacion_opciones)
    como_fue_la_formacion = models. CharField(max_length = 11)
    periodo_ingreso = models.CharField(max_length = 10)
    si_recomendaria_instituto = models.CharField(max_length = 150)
    no_recomendaria_instituto = models.CharField(max_length = 150)
    formar_parte = models. CharField(max_length = 4)
    materias_reforzar = models.CharField(max_length = 100)
    materias_menos_relevancia = models.CharField(max_length = 100)
    experiencia_cuantas_horas1 = models.CharField(choices= experiencia_cuantas_horas_opciones,max_length = 15, null = True, blank = True, default='')
    experiencia_cuantas_horas2 = models.CharField(choices= experiencia_cuantas_horas_opciones,max_length = 15, null = True, blank = True, default='')
    experiencia_cuantas_horas3 = models.CharField(choices= experiencia_cuantas_horas_opciones,max_length = 15, null = True, blank = True, default='')
    grado_importacia_competencias1 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    grado_importacia_competencias2 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    grado_importacia_competencias3 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    grado_importacia_competencias4 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    grado_importacia_competencias5 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    grado_importacia_competencias6 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    grado_importacia_competencias7 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    grado_importacia_competencias8 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    grado_importacia_competencias9 = models.CharField(choices= grado_importacia_opciones,max_length = 20)
    continuar_profesionalizacion = models.CharField(max_length = 40)
    calificar_atributos_instituto1 = models.CharField(choices= calificar_atributos_instituto_opciones,max_length = 15)
    calificar_atributos_instituto2 = models.CharField(choices= calificar_atributos_instituto_opciones,max_length = 15)
    calificar_atributos_instituto3 = models.CharField(choices= calificar_atributos_instituto_opciones,max_length = 15)
    calificar_atributos_instituto4 = models.CharField(choices= calificar_atributos_instituto_opciones,max_length = 15)
    calificar_atributos_instituto5 = models.CharField(choices= calificar_atributos_instituto_opciones,max_length = 15)
    areas_capacitar_fortalecer = models.CharField(max_length = 25)
    modalidad_capacitaciones_instituto = models.CharField(max_length = 35)
    cada_encuentros_exalumnos = models.CharField(max_length = 20)
    encuentros_exalumnos = models.CharField(max_length = 15)


    ##-------- Situación Laboral------------ ##
    trabaja = models.CharField(max_length=5)
    zona = models.CharField(choices = zona_opciones, max_length = 10,null = True, blank = True,  default='') 
    cargo = models.CharField(max_length = 280,null = True, blank = True,  default='') 
    trabaja_en_empresa_convenio = models.CharField(max_length=5)    
    nombre_empresa = models.CharField(max_length=250,null = True, blank = True)
    empresa_laboral_tipo = models.CharField(max_length=250,choices=empresa_laboral_tipo_opciones,null = True, blank = True)    
    jornada = models.CharField(choices = jornada_opciones, max_length = 50,null = True, blank = True) 
    direccion_empresa = models.CharField(max_length = 350,null = True, blank = True) 
    telefono_empresa = models.CharField(max_length = 20,null = True, blank = True) 
    empresa_es_acorde = models.CharField(max_length = 5)
    importancia_funciones_especialidad1 = models.CharField(choices= grado_importacia_opciones,max_length = 100)
    importancia_funciones_especialidad2 = models.CharField(choices= grado_importacia_opciones,max_length = 100)
    importancia_funciones_especialidad3 = models.CharField(choices= grado_importacia_opciones,max_length = 100)
    importancia_funciones_especialidad4 = models.CharField(choices= grado_importacia_opciones,max_length = 100)
    importancia_funciones_especialidad5 = models.CharField(choices= grado_importacia_opciones,max_length = 100)
    importancia_funciones_especialidad6 = models.CharField(choices= grado_importacia_opciones,max_length = 100)
    importancia_funciones_especialidad7 = models.CharField(choices= grado_importacia_opciones,max_length = 100)
    importancia_funciones_especialidad8 = models.CharField(choices= grado_importacia_opciones,max_length = 100)
    razones_no_econtrar_trabajo = models.CharField(max_length = 350) 
    vincular_laboralmente = models.CharField(max_length = 5)
    conocimientos_practicas = models.CharField(max_length = 40)
    como_encontro_trabajo = models.CharField(max_length = 150)
    aspectos_con_dificultad = models.CharField(max_length = 150)
    rango_sueldo = models.CharField(max_length = 50)
    emprendimiento_impacto = models.CharField(max_length=5)
    emprendimiento_impacto_cual = models.CharField(max_length=150,null=True,blank=True)

    curriculum = models.FileField(upload_to='curriculum_graduados')



    REQUIRED_FIELDS = ['cedula','nombre','apellido']

    class Meta:
        verbose_name = 'Graduado'

        
    def __str__(self):
        return f'{self.nombres},{self.apellidos}'

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_lebel):
        return True   
    
    def calcular_edad(self):
        if self.f_nacimiento:
            fecha_actual = datetime.now().date()
            edad = fecha_actual.year - self.f_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (self.f_nacimiento.month, self.f_nacimiento.day))
            return edad
        else:
            return None
    
    @property
    def edad(self):
        return self.calcular_edad()

 

class Capacitacion(models.Model):
    portada = models.ImageField(upload_to="capacitacion",null = True)
    titulo = models.CharField(max_length=250)
    fecha = models.DateField(null=True, blank=True)
    hora = models.CharField(max_length=100)
    descripcion_corta = models.CharField(max_length=350)  # Nuevo campo de descripción
    enlace = models.URLField()  
    inversión = models.CharField(max_length=30)
    descripcion_completa = RichTextField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.portada.path):
            os.remove(self.portada.path)
        return super().delete(using=using, keep_parents=keep_parents)
    
    def __str__(self):
        return f'{self.titulo}'

class Empleo (models.Model):
    
    portada = models.ImageField(upload_to = "empleo",null = True)
    puesto = models.CharField( max_length=100) 
    descripcion_corta = models.CharField(max_length=350) 
    contactos = models.CharField( max_length=100)
    ciudad = models.CharField( max_length=20, default="Loja")
    fecha = models.DateTimeField(default=timezone.now)
    autor = models.CharField( max_length=50, default="Anónimo")
    carrera_sugerida = models.CharField (max_length=70, default="")
    descripcion_completa = RichTextField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.portada.path):
            os.remove(self.portada.path)
        return super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f'{self.puesto}'

class Emprendimiento (models.Model):   
    
    portada = models.ImageField(upload_to = "emprendimiento", null = True)
    titulo = models.CharField(max_length=100) 
    descripcion_corta = models.CharField(max_length=500) 
    propietario = models.CharField(max_length=100, default="ISTL") 
    contacto = models.CharField(max_length=100) 
    fecha = models.DateTimeField(default=timezone.now)
    descripcion_completa = RichTextField(null=True, blank=True)
    
    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.portada.path):
            os.remove(self.portada.path)
        return super().delete(using=using, keep_parents=keep_parents)
    
    def __str__(self):
        return f'{self.titulo}' 


class Configuraciones (models.Model):   
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    image_home = models.ImageField(upload_to = "settings", null = True)
    about = models.CharField(max_length=900)
    image_mision = models.ImageField(upload_to = "settings", null = True)
    mision = models.CharField(max_length=900) 
    image_vision = models.ImageField(upload_to = "settings", null = True)
    vision = models.CharField(max_length=900) 
    teacher_in_charge_image = models.ImageField(upload_to = "settings", null = True) 
    teacher_in_charge_name = models.CharField(max_length=100) 
    teacher_in_charge_detail = models.CharField(max_length=500) 
    color_primary = ColorField(max_length=25)
    color_secundary = ColorField(max_length=25)
    favicon = models.ImageField(upload_to = "settings", null = True)
    image_nav = models.ImageField(upload_to = "settings", null = True)
    image_login = models.ImageField(upload_to = "settings", null = True)


    
