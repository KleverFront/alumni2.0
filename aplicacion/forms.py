from ckeditor.widgets import CKEditorWidget
from colorfield.widgets import ColorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class GraduadoPreForm(UserCreationForm):
    class Meta:
        model = UsuarioBase
        exclude = ['id']
        fields = ['nombres', 'apellidos', 'cedula', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
        



    def save(self, commit=True):
        usuario_base = super().save(commit=False)

        graduado_pre = GraduadoPre()

        if commit:
            usuario_base.save()
            graduado_pre.base = usuario_base
            graduado_pre.save()

        return graduado_pre
    


class ChangePassword(UserCreationForm):
    class Meta:
        model = UsuarioBase
        fields = ['password1', 'password2']   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})

    def save(self, commit=True):
        usuario_base = super().save(commit=True)

        graduadopre, created = GraduadoPre.objects.get_or_create(base=usuario_base)
        if commit:
            usuario_base.save()
            graduadopre.base = usuario_base
            graduadopre.save()

        return usuario_base



class GraduadoPreEditForm(forms.ModelForm): 
    class Meta:
        model = UsuarioBase
        exclude = ['id']
        fields = ['nombres', 'apellidos', 'cedula', 'email']


    
    def save(self, commit=True):
        usuario_base = super().save(commit=False)

        # Obtener la instancia existente de Administrador si ya existe
        graduadopre, created = GraduadoPre.objects.get_or_create(base=usuario_base)


        # Guardar el UsuarioBase y el Administrador
        if commit:
            usuario_base.save()
            graduadopre.save()

        return usuario_base



    
    

class CarreraGraduadoForm(forms.ModelForm):
    class Meta:
        model = CarreraGraduado
        fields = ['carreras', 'periodo_graduado']
    
    carreras_opciones = [
        ('','Seleccione una Carrera'),
        ('Tecnología en Agroindustrias', 'Tecnología en Agroindustrias'),
        ('Tecnología Superior en Contabilidad', 'Tecnología Superior en Contabilidad'),
        ('Tecnología Superior en Control de Incendios y Operaciones de Rescate','Tecnología Superior en Control de Incendios y Operaciones de Rescate'),
        ('Tecnología Superior en Desarrollo de Software', 'Tecnología Superior en Desarrollo de Software'),
        ('Tecnología Superior en Desarrollo Infantil Integral', 'Tecnología Superior en Desarrollo Infantil Integral'),
        ('Tecnología Superior en Electricidad', 'Tecnología Superior en Electricidad'),
        ('Tecnología Superior en Mecánica Automotriz', 'Tecnología Superior en Mecánica Automotriz'),
        ('Tecnología Superior en Procesamiento de Alimentos', 'Tecnología Superior en Procesamiento de Alimentos'),
        ('Tecnología Superior en Seguridad Ciudadana y Orden Público','Tecnología Superior en Seguridad Ciudadana y Orden Público'),
        ('Otro', 'Otro'),
    ]
    
    carreras = forms.ChoiceField(
    choices=carreras_opciones,
    widget=forms.Select(attrs={'class': 'form-control'}),
    )

    periodo_graduado = forms.CharField(
        max_length=8,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Período de graduación'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




class AdministradorCreationForm(UserCreationForm):
    class Meta:
        model = UsuarioBase 
        exclude = ['is_staff'] 
        fields = ['cedula', 'nombres', 'apellidos', 'email', 'password1', 'password2']

    imagen = forms.ImageField(required=False)  # Agregado campo específico de Administrador

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})

    def save(self, commit=True):
        usuario_base = super().save(commit=False)

        # Guardar campos específicos de Administrador
        imagen = self.cleaned_data.get('imagen', None)
        

        # Crear instancia de Administrador
        administrador = Administrador(imagen=imagen)

        # Establecer is_staff como True
        usuario_base.is_staff = True

        if commit:
            usuario_base.save()

            # Asignar la instancia de UsuarioBase al Administrador
            administrador.base = usuario_base
            administrador.save()
        return administrador
        


class AdministradorEditForm(forms.ModelForm):
    class Meta:
        model = UsuarioBase 
        exclude = ['is_staff'] 
        fields = ['cedula', 'nombres', 'apellidos', 'email']

    imagen = forms.ImageField(required=False)  # Agregado campo específico de Administrador

    def save(self, commit=True):
        usuario_base = super().save(commit=False)


        # Guardar campos específicos de Administrador
        imagen = self.cleaned_data.get('imagen', None)

        
        # Obtener la instancia existente de Administrador si ya existe
        administrador, created = Administrador.objects.get_or_create(base=usuario_base)

        if not administrador.imagen and imagen:
            administrador.imagen = imagen
        elif administrador.imagen and imagen:  # Si no se proporciona una nueva imagen, conserva la imagen existente
            administrador.imagen = imagen

        # Actualizar campos de Administrador

        # Guardar el UsuarioBase y el Administrador
        if commit:
            usuario_base.save()
            administrador.save()

        return usuario_base


class AuthenticationBaseForm(forms.Form):
    cedula = forms.CharField(max_length=30, required=True, help_text='Ingrese su cédula')
    password = forms.CharField(widget=forms.PasswordInput(attrs={  'type': 'password'}) )
    class Meta:
        model = UsuarioBase
        fields = ['cedula', 'password']

    def clean(self):
        cleaned_data = super().clean()
        cedula = cleaned_data.get('cedula')
        password = cleaned_data.get('password')

        

        return cleaned_data
        

class CapacitacionForm(forms.ModelForm):
    class Meta:
        model = Capacitacion
        fields = [
            'portada',
            'titulo',
            'fecha',
            'hora',
            'descripcion_corta',
            'enlace',
            'inversión',
            'descripcion_completa',
        ]
        labels = {
            'portada': 'Portada',
            'titulo': 'Titulo',
            'fecha': 'Fecha',
            'hora': 'Hora',
            'descripcion_corta':'Descripción Corta (150 a 200 palabras max)',
            'enlace': 'Enlace',
            'inversión': 'Inversión',
            'descripcion_completa':'Descripción Completa',
        }
        widgets = {
            'portada': forms.FileInput(attrs={'class': 'file-control mb-3'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'fecha': forms.DateInput (attrs={'class': 'form-control mb-2','type':'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control mb-2','type': 'time'}),
            'descripcion_corta': forms.Textarea(attrs={'class':'form-control mb-2','id':'descripcion_corta' ,'style':'height:65px;'}),
            'enlace': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'inversión': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'descripcion_completa': forms.CharField(widget=CKEditorWidget())
        }
        

class FiltroEmpleoForm(forms.Form):

    puesto_buscar = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control me-2','type': 'search',}), required=False)

    areas_opciones = [
        ('', 'Cualquier Área'),
        ('Tecnología en Agroindustrias', 'Tecnología en Agroindustrias'),
        ('Tecnología Superior en Contabilidad', 'Tecnología Superior en Contabilidad'),
        ('Tecnología Superior en Control de Incendios y Operaciones de Rescate','Tecnología Superior en Control de Incendios y Operaciones de Rescate'),
        ('Tecnología Superior en Desarrollo de Software', 'Tecnología Superior en Desarrollo de Software'),
        ('Tecnología Superior en Desarrollo Infantil Integral', 'Tecnología Superior en Desarrollo Infantil Integral'),
        ('Tecnología Superior en Electricidad', 'Tecnología Superior en Electricidad'),
        ('Tecnología Superior en Mecánica Automotriz', 'Tecnología Superior en Mecánica Automotriz'),
        ('Tecnología Superior en Procesamiento de Alimentos', 'Tecnología Superior en Procesamiento de Alimentos'),
        ('Tecnología Superior en Seguridad Ciudadana y Orden Público','Tecnología Superior en Seguridad Ciudadana y Orden Público'),
        ('Otro', 'Otro'),
    ]
    areas = forms.ChoiceField(choices=areas_opciones, required=False)


class EmpleoForm(forms.ModelForm):

    CARRERA_SUGERIDA_CHOICES = [
        ('','Seleccione una Carrera'),
        ('Tecnología en Agroindustrias', 'Tecnología en Agroindustrias'),
        ('Tecnología Superior en Contabilidad', 'Tecnología Superior en Contabilidad'),
        ('Tecnología Superior en Control de Incendios y Operaciones de Rescate','Tecnología Superior en Control de Incendios y Operaciones de Rescate'),
        ('Tecnología Superior en Desarrollo de Software', 'Tecnología Superior en Desarrollo de Software'),
        ('Tecnología Superior en Desarrollo Infantil Integral', 'Tecnología Superior en Desarrollo Infantil Integral'),
        ('Tecnología Superior en Electricidad', 'Tecnología Superior en Electricidad'),
        ('Tecnología Superior en Mecánica Automotriz', 'Tecnología Superior en Mecánica Automotriz'),
        ('Tecnología Superior en Procesamiento de Alimentos', 'Tecnología Superior en Procesamiento de Alimentos'),
        ('Tecnología Superior en Seguridad Ciudadana y Orden Público','Tecnología Superior en Seguridad Ciudadana y Orden Público'),
        ('Otro', 'Otro'),
    ]

    carrera_sugerida = forms.ChoiceField(
        choices=CARRERA_SUGERIDA_CHOICES ,
        widget=forms.Select(attrs={'class': 'form-control mb-4'})
    )

    
    class Meta:
        model = Empleo
        fields = [
            'portada',
            'puesto',
            'descripcion_corta',
            'contactos',
            'ciudad',
            'autor',
            'carrera_sugerida',
            'descripcion_completa',    
        ]
        labels = {
            'portada': 'Portada',
            'puesto':'Puesto',
            'descripcion_corta':'Descripción Corta (150 a 200 palabras max)',
            'contactos':'Contactos',
            'ciudad' : 'Ciudad',
            'autor' : 'Autor',
            'carrera_sugerida' : 'Carrera Sugerida',
            'descripcion_completa':'Descripción Completa',
        }
        widgets = {
            'portada':forms.FileInput(attrs={'class':'form-control-file mb-4'}),
            'puesto': forms.TextInput(attrs={'class':'form-control mb-4'}),
            'descripcion_corta': forms.Textarea(attrs={'class':'form-control mb-2','id':'descripcion_corta' ,'style':'height:65px;'}),
            'contactos': forms.TextInput(attrs={'class':'form-control mb-4'}),
            'ciudad': forms.TextInput(attrs={'class':'form-control mb-4'}),
            'autor': forms.TextInput(attrs={'class':'form-control mb-4'}),
            'carrera_sugerida': forms.Select(),
            'descripcion_completa':forms.CharField(widget=CKEditorWidget())
          
        }


class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = [
            'portada',
            'titulo',
            'descripcion_corta',
            'propietario',
            'contacto',
            'descripcion_completa',
        ]  
        labels = {
            'portada':'Portada',
            'titulo':'Titulo',
            'descripcion_corta':'Descripción Corta (150 a 200 palabras max)',
            'propietario':'Propietario',
            'contacto':'Contacto',
            'descripcion_completa':'Descripción Completa',
        }
        widgets = {
            'portada':forms.FileInput(attrs={'class':'form-control mb-3 '}),
            'titulo': forms.TextInput(attrs={'class':'form-control mb-2 '}),
            'descripcion_corta': forms.Textarea(attrs={'class':'form-control mb-2','id':'descripcion_corta' ,'style':'height:65px;'}),
            'propietario': forms.TextInput(attrs={'class':'form-control mb-2'}),
            'contacto': forms.TextInput(attrs={'class':'form-control mb-2'}),
            'descripcion_completa':forms.CharField(widget=CKEditorWidget())
        }



class GraduadoForm(forms.ModelForm):

    sexos_opciones = [
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
    ]

    OPCIONES_COMO_FUE_LA_FORMACION = [
        ('Muy buena', 'Muy buena'),
        ('Bueno', 'Bueno'),
        ('Neutro', 'Neutro'),
        ('Regular', 'Regular'),
        ('Mala', 'Mala'),
        ('Otro', 'Otro'),
    ]

    si_recomendaria_instituto_opciones = [
        ('La formación académica le permite crear su propio negocio', 'La formación académica le permite crear su propio negocio'),
        ('Prestigio de la institución en la localidad', 'Prestigio de la institución en la localidad'),
        ('Los recursos físicos y tecnológicos que ofrece el instituto son buenos para el proceso de formación.', 'Los recursos físicos y tecnológicos que ofrece el instituto son buenos para el proceso de formación.'),
        ('Calidad de la planta docente', 'Calidad de la planta docente'),
        ('Conocimientos adquiridos', 'Conocimientos adquiridos')
    ]

    no_recomendaria_instituto_opciones = [
        ('Baja calidad de conocimientos obtenidos', 'Baja calidad de conocimientos obtenidos'),
        ('Los docentes no cuentan con la preparación adecuada', 'Los docentes no cuentan con la preparación adecuada'),
        ('Poco prestigio de la institución', 'Poco prestigio de la institución'),
        ('Los recursos físicos y tecnológicos que ofrece el instituto no son suficientes para el proceso de formación', 'Los recursos físicos y tecnológicos que ofrece el instituto no son suficientes para el proceso de formación'),
        ('Otro', 'Otro')
    ]

    si_no_opciones = [
        ('Si', 'Si'),
        ('No', 'No')

    ]

    continuar_profesionalizacion_opciones = [
        ('En el ISTL', 'En el ISTL'),
        ('En Universidad', 'En Universidad'),
        ('En otros centros de formación superior', 'En otros centros de formación superior'),
        ('Otro', 'Otro')
    ]

    areas_capacitar_fortalecer_opciones = [
        ('Educación', 'Educación'),
        ('Electricidad', 'Electricidad'),
        ('Desarrollo de Software', 'Desarrollo de Software'),
        ('Mecánica Automotriz', 'Mecánica Automotriz'),
        ('Contabilidad', 'Contabilidad'),
        ('Seguridad Industrial', 'Seguridad Industrial'),
        ('Control de calidad', 'Control de calidad'),
        ('Otro', 'Otro')
    ]

    modalidad_capacitaciones_instituto_opciones = [
        ('Seminarios (1 semana)', 'Seminarios (1 semana)'),
        ('Congresos (3 días )', 'Congresos (3 días )'),
        ('Conferencias (2 horas )', 'Conferencias (2 horas )'),
        ('Cursos Virtuales (40 horas)', 'Cursos Virtuales (40 horas)'),
        ('Cursos Presenciales (40 horas)', 'Cursos Presenciales (40 horas)')
    ]

    cada_encuentros_exalumnos_opciones = [
        ('Cada 3 meses', 'Cada 3 meses'),
        ('Cada 6 meses', 'Cada 6 meses'),
        ('Cada año', 'Cada año'),
        ('Otro', 'Otro')
    ]

    encuentros_exalumnos_opciones = [
        ('Académicos', 'Académicos'),
        ('Sociales', 'Sociales'),
        ('Deportivos', 'Deportivos')
    ]

    conocimientos_practicas_opciones = [
        ('No he trabajado todavía', 'No he trabajado todavía'),
        ('Totalmente de acuerdo', 'Totalmente de acuerdo'),
        ('De acuerdo', 'De acuerdo'),
        ('Ni de acuerdo ni  desacuerdo', 'Ni de acuerdo ni  desacuerdo'),
        ('Desacuerdo', 'Desacuerdo'),
        ('Otro', 'Otro')
    ]


    como_encontro_trabajo_opciones = [
        ('Bolsa de trabajo del Instituto', 'Bolsa de trabajo del Instituto'),
        ('Postulación en redes: red socio-empleo, multi-trabajo (páginas especializadas)', 'Postulación en redes: red socio-empleo, multi-trabajo (páginas especializadas)'),
        ('Contactos personales', 'Contactos personales'),
        ('Redes sociales (incluye LinkedIn, Facebook, entre otros)', 'Redes sociales (incluye LinkedIn, Facebook, entre otros)'),
        ('Me contrataron después de las prácticas pre profesionales o fase práctica de carrera dual', 'Me contrataron después de las prácticas pre profesionales o fase práctica de carrera dual'),
        ('Postulación directa en la empresa mediante su plataforma o fuerza laboral', 'Postulación directa en la empresa mediante su plataforma o fuerza laboral'),
        ('Otro', 'Otro')
    ]

    aspectos_con_dificultad_opciones=[
        ('Capacidad para elaborar proyectos en la especialidad', 'Capacidad para elaborar proyectos en la especialidad'),
        ('Identificar, plantear y resolver problemas', 'Identificar, plantear y resolver problemas'),
        ('Utilizar herramientas informáticas', 'Utilizar herramientas informáticas'),
        ('Aprender y mantenerse actualizado', 'Aprender y mantenerse actualizado'),
        ('Capacidad de adaptarse a cambios', 'Capacidad de adaptarse a cambios'),
        ('Creatividad e innovación', 'Creatividad e innovación'),
        ('Optimizar el tiempo y recursos en las tareas asignadas', 'Optimizar el tiempo y recursos en las tareas asignadas'),
        ('Trabajo en equipo', 'Trabajo en equipo'),
        ('Aplicar valores y ética profesional', 'Aplicar valores y ética profesional'),
        ('Redacción de informes orales o escritos', 'Redacción de informes orales o escritos'),
        ('Capacidad de comunicación', 'Capacidad de comunicación'),
        ('Otro', 'Otro')
    ]

    rango_sueldo_opciones = [
        ('$0.00 a $200', '$0.00 a $200'),
        ('$200 a $400', '$200 a $400'),
        ('$400 a $600', '$400 a $600'),
        ('$600 a $800', '$600 a $800'),
        ('$800 a $1000', '$800 a $1000'),
        ('$1000 en adelante', '$1000 en adelante'),
        ('Otro', 'Otro')
    ]

    class Meta:
        model = Graduado
        exclude = ['base_pregraduado']
        fields = [
            #----------Primera Parte---------#
            'correo_personal',
            'f_nacimiento',
            'direccion',
            'telefono_fijo',
            'celular',
            'nacionalidad',
            'etnia',
            'sexo',
            'estado_civil',
            'cual_discapacidad',
            'fotografia',

            #----------Segunda Parte---------#
            'campus',
            'titulacion',
            'como_fue_la_formacion',
            'periodo_ingreso',
            'si_recomendaria_instituto',
            'no_recomendaria_instituto',
            'formar_parte',
            'materias_reforzar',
            'materias_menos_relevancia',
            'experiencia_cuantas_horas1',
            'experiencia_cuantas_horas2',
            'experiencia_cuantas_horas3',
            'grado_importacia_competencias1',
            'grado_importacia_competencias2',
            'grado_importacia_competencias3',
            'grado_importacia_competencias4',
            'grado_importacia_competencias5',
            'grado_importacia_competencias6',
            'grado_importacia_competencias7',
            'grado_importacia_competencias8',
            'grado_importacia_competencias9',
            'continuar_profesionalizacion',
            'calificar_atributos_instituto1',
            'calificar_atributos_instituto2',
            'calificar_atributos_instituto3',
            'calificar_atributos_instituto4',
            'calificar_atributos_instituto5',
            'areas_capacitar_fortalecer',
            'modalidad_capacitaciones_instituto',
            'cada_encuentros_exalumnos',
            'encuentros_exalumnos',

            ##-------- Tercera Parte ------------ ##
            'trabaja',
            'zona',
            'cargo',
            'trabaja_en_empresa_convenio',
            'nombre_empresa',
            'empresa_laboral_tipo',
            'jornada',
            'direccion_empresa',
            'telefono_empresa',
            'empresa_es_acorde',
            'importancia_funciones_especialidad1',
            'importancia_funciones_especialidad2',
            'importancia_funciones_especialidad3',
            'importancia_funciones_especialidad4',
            'importancia_funciones_especialidad5',
            'importancia_funciones_especialidad6',
            'importancia_funciones_especialidad7',
            'importancia_funciones_especialidad8',
            'razones_no_econtrar_trabajo',
            'vincular_laboralmente',
            'conocimientos_practicas',
            'como_encontro_trabajo',
            'aspectos_con_dificultad',
            'rango_sueldo',
            'emprendimiento_impacto',
            'emprendimiento_impacto_cual',
            'curriculum',
        ]
        labels = {

            'correo_institucional': 'Correo Institucional',
            'f_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Direccion',
            'telefono_fijo': 'Telefono Fijo',
            'celular': 'Celular',
            'nacionalidad':'Nacionalidad',
            'etnia':'Etnia',
            'sexo':'Sexo',
            'estado_civil':'Estado Civil',
            'cual_discapacidad':'¿Cúal?',
            'fotografia': 'Foto de Usuario/Graduado',
            #----------Segunda Parte---------#
            'campus': 'Ubicación del campus donde cursó su formación académica',
            'titulacion':'¿Cuál fue el método que uso para titularse?',
            'como_fue_la_formacion': '¿Cómo fue la formación académica que recibió en la carrera?',
            'periodo_ingreso':'¿En que periodo se ingreso a la carrera?',#---
            'si_recomendaria_instituto':'¿Por qué razones Sí recomendaría al instituto ?',
            'no_recomendaria_instituto':'¿Por qué razones No recomendaría al instituto?',
            'formar_parte':'¿Le gustaría formar parte de la asociación de graduados?',
            'materias_reforzar':'De acuerdo a su carrera tecnológica, coméntenos sobre la o las materias que reforzarían para su formación profesional.',
            'materias_menos_relevancia':'Desde su punto de vista, escriba la o las asignaturas que menos relevancia tuvieron en la malla curricular de su especialidad.',
            'experiencia_cuantas_horas1':'Investigación para la realización del trabajo de grado.',
            'experiencia_cuantas_horas2':'Preparación para rendir el examen complexivo de grado.',
            'experiencia_cuantas_horas3':'Tutorías con el docente para la realización de prácticas pre - profesionales',
            'grado_importacia_competencias1':'Aplicar técnicas de análisis y control de procesos.',
            'grado_importacia_competencias2':'Interpretar resultados de análisis de laboratorio o instrumentos tecnológicos.',
            'grado_importacia_competencias3':'Manejar maquinaria, equipos e instrumentos.',
            'grado_importacia_competencias4':'Manejo de técnicas de seguridad e higiene industrial.',
            'grado_importacia_competencias5':'Manejo de normativa legal y medio ambiente vigente.',
            'grado_importacia_competencias6':'Apoyo de proyectos de acuerdo a su tecnología.',
            'grado_importacia_competencias7':'Gestionar, diseñar y elaborar nuevos productos.',
            'grado_importacia_competencias8':'Manejar herramientas tecnológicas administrativas.',
            'grado_importacia_competencias9':'Manejo de tecnicas de comunicación e interrelación personal.',
            'calificar_atributos_instituto1':'Estado y equipamiento de los laboratorios y talleres',
            'calificar_atributos_instituto2':'Estado de las aulas',
            'calificar_atributos_instituto3':'Estado de los espacios de esparcimiento (bar, canchas, patio, etc.)',
            'calificar_atributos_instituto4':'Estado de los servicios higiénicos',
            'calificar_atributos_instituto5':'Estado de biblioteca (física o virtual) o estado de recursos en línea',
            'areas_capacitar_fortalecer':'¿En qué áreas le gustaría capacitarse para fortalecer su preparación profesional?',
            'modalidad_capacitaciones_instituto':'¿Qué modalidad considera  para cursar capacitaciones  que ofrezca el Instituto?',
            'cada_encuentros_exalumnos':'¿Cómo considera que debe realizarse  los encuentros de exalumnos?',
            'encuentros_exalumnos':'Considera que los encuentro de exalumnos deben ser:',

            ##-------- Tercera Parte ------------ ##
            'trabaja':'',
            'zona':'La zona donde labora es:',
            'cargo':'¿Cúal es el cargo que desempeña?',
            'trabaja_en_empresa_convenio':'',
            'nombre_empresa':'Nombre de la Institución o empresa donde labora.',
            'empresa_laboral_tipo':'La empresa o institución donde labora es:',
            'jornada':'Su jornada laboral es:',
            'direccion_empresa':'Dirección de la empresa o institución donde labora',
            'telefono_empresa':'Número telefónico de la empresa o institución donde labora.',
            'empresa_es_acorde':'',
            'importancia_funciones_especialidad1':'Supervisión de  los procesos tecnológicos de recepción, procesamiento y almacenamiento de objetos o insumos.',
            'importancia_funciones_especialidad2':'Aplicación de técnicas de  análisis de trabajos.',
            'importancia_funciones_especialidad3':'Control de calidad de procesos o trabajos terminados.',
            'importancia_funciones_especialidad4':'Aplicación de técnicas aprendidas en sus estudios',
            'importancia_funciones_especialidad5':'Operación de equipos y maquinaria.',
            'importancia_funciones_especialidad6':'Coordinación y desarrollo de talleres.',
            'importancia_funciones_especialidad7':'Evaluación del cumplimientos de procesos o trabajos terminados.',
            'importancia_funciones_especialidad8':'Apoyo en la elaboración del análisis técnico para terminar  trabajos establecidos',
            'razones_no_econtrar_trabajo':'¿Cuál cree usted sean las razones de no encontrar trabajo en su especialidad?',
            'vincular_laboralmente':'',
            'conocimientos_practicas':'',
            'como_encontro_trabajo' :'',
            'aspectos_con_dificultad':'',
            'rango_sueldo':'',
            'emprendimiento_impacto_cual': '¿Cúal es su emprendimiento de impacto?',
            'curriculum':'Suba su Curriculum u Hoja de Vida por favor',

        }
        widgets = {

            'correo_institucional': forms.EmailInput(attrs={'class':'mb-2','type':'email','required': True}),
            'f_nacimiento': forms.DateInput (attrs={'class': 'mb-2','type':'date','required': True}),
            'direccion': forms.Textarea(attrs={'class':'mb-2','required': True}),
            'telefono_fijo': forms.NumberInput(attrs={'class':'mb-2','type':'number','required': False}),
            'celular': forms.NumberInput(attrs={'class':'mb-2','type':'number','required': True}),
            'nacionalidad':forms.TextInput(attrs={'class':'mb-2','required': False}),
            'etnia':forms.Select(attrs={'class':'form-select mb-2','required': False}),
            #'sexo':
            'estado_civil':forms.Select(attrs={'class':'form-select mb-2','required': False}),
            'cual_discapacidad':forms.Textarea(attrs={'class':'mb-2','required': False}),
            'fotografia': forms.FileInput(attrs={'class':'mb-3','required': False}),

            #----------Segunda Parte---------#
            'campus':forms.Select(attrs={'class':'form-select mb-2'}),
            'titulacion': forms.Select(attrs={'class':'form-select mb-2','required': False}),
            'periodo_ingreso':forms.TextInput(attrs={'class':'mb-2'}),
            'materias_reforzar':forms.TextInput(attrs={'class':'mb-2'}),
            'materias_menos_relevancia':forms.TextInput(attrs={'class':'mb-2'}),
            'experiencia_cuantas_horas1':forms.Select(attrs={'class':'form-select mb-2'}),
            'experiencia_cuantas_horas2':forms.Select(attrs={'class':'form-select mb-2'}),
            'experiencia_cuantas_horas3':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias1':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias2':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias3':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias4':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias5':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias6':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias7':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias8':forms.Select(attrs={'class':'form-select mb-2'}),
            'grado_importacia_competencias9':forms.Select(attrs={'class':'form-select mb-2'}),
            'calificar_atributos_instituto1':forms.Select(attrs={'class':'form-select mb-2'}),
            'calificar_atributos_instituto2':forms.Select(attrs={'class':'form-select mb-2'}),
            'calificar_atributos_instituto3':forms.Select(attrs={'class':'form-select mb-2'}),
            'calificar_atributos_instituto4':forms.Select(attrs={'class':'form-select mb-2'}),
            'calificar_atributos_instituto5':forms.Select(attrs={'class':'form-select mb-2'}),

            ##-------- Tercera Parte ------------ ##
            'trabaja_en_empresa_convenio':forms.RadioSelect(attrs={'class': 'form-check-input','type': 'radio',}),
            'zona':forms.Select(attrs={'class':'form-select mb-2'}),
            'cargo':forms.TextInput(attrs={'class':'mb-2'}),
            'nombre_empresa':forms.TextInput(attrs={'class':'mb-2'}),
            'empresa_laboral_tipo':forms.Select(attrs={'class':'form-select mb-2'}),
            'jornada':forms.Select(attrs={'class':'form-select mb-2'}),
            'direccion_empresa':forms.TextInput(attrs={'class':'mb-2'}),
            'telefono_empresa':forms.TextInput(attrs={'class':'mb-2'}),
            'importancia_funciones_especialidad1':forms.Select(attrs={'class':'form-select mb-2'}),
            'importancia_funciones_especialidad2':forms.Select(attrs={'class':'form-select mb-2'}),
            'importancia_funciones_especialidad3':forms.Select(attrs={'class':'form-select mb-2'}),
            'importancia_funciones_especialidad4':forms.Select(attrs={'class':'form-select mb-2'}),
            'importancia_funciones_especialidad5':forms.Select(attrs={'class':'form-select mb-2'}),
            'importancia_funciones_especialidad6':forms.Select(attrs={'class':'form-select mb-2'}),
            'importancia_funciones_especialidad7':forms.Select(attrs={'class':'form-select mb-2'}),
            'importancia_funciones_especialidad8':forms.Select(attrs={'class':'form-select mb-2'}),
            'razones_no_econtrar_trabajo':forms.TextInput(attrs={'class':'mb-2'}),
            'emprendimiento_impacto_cual':forms.TextInput(attrs={'class':'mb-2'}),
            'curriculum':forms.FileInput(attrs={'class':'mb-3','required': True}),
        }
    
    sexo = forms.ChoiceField(choices=sexos_opciones)
    discapacidad = forms.ChoiceField(choices=si_no_opciones)
    como_fue_la_formacion = forms.ChoiceField(choices=OPCIONES_COMO_FUE_LA_FORMACION)
    si_recomendaria_instituto = forms.ChoiceField(choices=si_recomendaria_instituto_opciones)
    no_recomendaria_instituto = forms.ChoiceField(choices=no_recomendaria_instituto_opciones)
    formar_parte = forms.ChoiceField(choices=si_no_opciones)
    continuar_profesionalizacion = forms.ChoiceField(choices=continuar_profesionalizacion_opciones)
    areas_capacitar_fortalecer = forms.ChoiceField(choices=areas_capacitar_fortalecer_opciones)
    modalidad_capacitaciones_instituto = forms.ChoiceField(choices=modalidad_capacitaciones_instituto_opciones)
    cada_encuentros_exalumnos = forms.ChoiceField(choices=cada_encuentros_exalumnos_opciones)
    encuentros_exalumnos = forms.ChoiceField(choices=encuentros_exalumnos_opciones)
    trabaja = forms.ChoiceField(choices=si_no_opciones)
    trabaja_en_empresa_convenio = forms.ChoiceField(choices=si_no_opciones)
    empresa_es_acorde = forms.ChoiceField(choices=si_no_opciones)
    vincular_laboralmente = forms.ChoiceField(choices=si_no_opciones)
    conocimientos_practicas = forms.ChoiceField(choices=conocimientos_practicas_opciones)
    como_encontro_trabajo = forms.ChoiceField(choices=como_encontro_trabajo_opciones)
    aspectos_con_dificultad = forms.ChoiceField(choices=aspectos_con_dificultad_opciones)
    rango_sueldo = forms.ChoiceField(choices=rango_sueldo_opciones)
    emprendimiento_impacto = forms.ChoiceField(choices=si_no_opciones)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.instance, 'base'):
            base = self.instance.base
            self.fields['cedula'].initial = base.cedula



class ConfiguracionesForm(forms.ModelForm):
    status_opciones = [
        ('', 'Elija un estado'),
        ('False', 'Inactiva'),
        ('True', 'Activa'),
    ]

    class Meta:
        model = Configuraciones
        fields = [
            'name',
            'image_home',
            'about',
            'image_mision',
            'mision',
            'image_vision',
            'vision',
            'teacher_in_charge_image',
            'teacher_in_charge_name',
            'teacher_in_charge_detail',
            'color_primary',
            'color_secundary',
            'favicon',
            'image_nav',

        ]  
        labels = {
            'name':'Nombre de la Configuracion',
            'status': 'Estado de la Configuración',
            'image_home':'Imagen de Portada Alumni en Home',
            'about':'Sobre Nosotros',
            'image_mision':'Imagen de Misión',
            'mision':'Misión',
            'image_vision':'Imagen de Visión',
            'vision': 'Visión',
            'teacher_in_charge_image':'Imagen de Docente Encargado',
            'teacher_in_charge_name':'Nombre de Docente Encargado',
            'teacher_in_charge_detail':'Detalles de Docente Engargado',
            'color_primary':'Color Primario de Alumni',
            'color_secundary':'Color Secundario de Alumni',
            'favicon':'Favicon de Alumni',
            'image_nav':'Imagen de Nav (Menu de Navegación)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control mb-2 '}),
            'image_home': forms.FileInput(attrs={'class':'form-control mb-3 '}),
            'about': forms.Textarea(attrs={'class':'form-control mb-2','style':'height:65px;'}),
            'image_mision': forms.FileInput(attrs={'class':'form-control mb-3 '}),
            'mision': forms.Textarea(attrs={'class':'form-control mb-2','style':'height:65px;'}),
            'image_vision': forms.FileInput(attrs={'class':'form-control mb-3 '}),
            'vision': forms.Textarea(attrs={'class':'form-control mb-2','style':'height:65px;'}),
            'teacher_in_charge_image': forms.FileInput(attrs={'class':'form-control mb-3 '}),
            'teacher_in_charge_name': forms.TextInput(attrs={'class':'form-control mb-2 '}),
            'teacher_in_charge_detail': forms.Textarea(attrs={'class':'form-control mb-2','style':'height:65px;'}),
            'color_primary': ColorWidget(attrs={'class': 'colorpicker'}),
            'color_secundary':ColorWidget(attrs={'class': 'colorpicker'}),
            'favicon': forms.FileInput(attrs={'class':'form-control mb-3 '}),
            'image_nav': forms.FileInput(attrs={'class':'form-control mb-3 '}),
        }

    status = forms.ChoiceField(choices=status_opciones)

    def save(self, commit=True):
        conf = super().save(commit=False)

        status = self.cleaned_data.get('status', None)
        conf.status = status

        if commit:
            conf.save()

        return conf
