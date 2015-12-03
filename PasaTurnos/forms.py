# -*- encoding: utf-8 -*-
# Clase para la creación de formularios personalizados en django
from django import forms
# Tablas de BD ACOCOMET
from PasaTurnos.models import Empresa, Gerente, Ejecutivo, Cajero, TipoAtencion, \
Servicio, Ventanilla, Cliente, Encuesta, Video

# Elecciones para genero
GENERO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        )

# Elecciones para encuesta
ENCUESTA = (
        ('M', 'Malo'),
        ('B', 'Bueno'),
        ('MB', 'Muy Bueno'),
        )

# Formulario para agregar empresa
class frmAgregarEmpresa(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la empresa'}))
	numero_registro = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'00000-0'}))
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	fax = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	sitio_web = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'www.sitioweb.com'}))
	class Meta:
		model = Empresa
		fields = ('nombre',
        		'numero_registro',
        		'telefono',
        		'fax',
        		'direccion',
        		'correo_electronico',
        		'sitio_web')

# Formulario para editar empresa
class frmEditarEmpresa(forms.ModelForm):
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	fax = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	sitio_web = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'www.sitioweb.com'}))
	class Meta:
		model = Empresa
		fields = ('telefono',
        		'fax',
        		'direccion',
        		'correo_electronico',
        		'sitio_web')

# Formulario para Agregar gerentes
class frmAgregarGerente(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	dui = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'00000000-0'}))
	nit = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-000000-000-0'}))
	# Campo personalizado con choice específico
	genero = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENERO)
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	
	apodo_usuario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	contrasenha_usuario = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	class Meta:
		model = Gerente
		fields = ('nombre',
			'apellido',
			'dui',
			'nit',
			'genero',
			'telefono',
			'correo_electronico')

# Formulario para editar gerentes
class frmEditarGerente(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	class Meta:
		model = Gerente
		fields = ('nombre',
				'apellido',
				'telefono',
				'correo_electronico')

# Formulario para agregar ejecutivos
class frmAgregarEjecutivo(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	dui = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'00000000-0'}))
	nit = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-000000-000-0'}))
	# Campo personalizado con choice específico
	genero = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENERO)
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	
	apodo_usuario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	contrasenha_usuario = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	class Meta:
		model = Ejecutivo
		fields = ('nombre',
			'apellido',
			'dui',
			'nit',
			'genero',
			'telefono',
			'correo_electronico')

# Formulario para editar ejecutivos
class frmEditarEjecutivo(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	class Meta:
		model = Ejecutivo
		fields = ('nombre',
				'apellido',
				'telefono',
				'correo_electronico')

# Formulario para agregar cajeros
class frmAgregarCajero(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	dui = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'00000000-0'}))
	nit = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-000000-000-0'}))
	# Campo personalizado con choice específico
	genero = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENERO)
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	
	apodo_usuario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	contrasenha_usuario = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	class Meta:
		model = Cajero
		fields = ('nombre',
			'apellido',
			'dui',
			'nit',
			'genero',
			'telefono',
			'correo_electronico')

# Formulario para editar cajeros
class frmEditarCajero(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	class Meta:
		model = Cajero
		fields = ('nombre',
				'apellido',
				'telefono',
				'correo_electronico')


#from django.forms.models import ModelForm
# Select para formulario de servicios
class slTipoAtencion(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s" %obj.descripcion

class frmAgregarServicio(forms.ModelForm):
	descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	tipo_atencion_id = slTipoAtencion(widget=forms.Select(attrs={'class':'form-control selectpicker', 'data-live-search':'true'}), 
									queryset=TipoAtencion.objects.all(),
									empty_label="Seleccione un tipo")
	class Meta:
		model = Servicio
		fields = ('descripcion', 'tipo_atencion_id')

class frmEditarServicio(forms.ModelForm):
	descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	tipo_atencion_id = slTipoAtencion(widget=forms.Select(attrs={'class':'form-control selectpicker', 'data-live-search':'true'}), 
									queryset=TipoAtencion.objects.all(),
									empty_label="Seleccione un tipo")
	class Meta:
		model = Servicio
		fields = ('descripcion', 'tipo_atencion_id')

class slCajero(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s" %(obj.nombre, obj.apellido)

class frmAgregarCaja(forms.ModelForm):
	# Obtengo los id de los usuarios que tienen caja asignadas
	#Ventanilla = Ventanilla.objects.exclude(tipo_atencion_id=2).values('user_id')
	Ventanilla = Ventanilla.objects.exclude(tipo_atencion_id__descripcion='Atencion al cliente').values('user_id')
	idUsers = []
	for i in range(len(Ventanilla)):
		idUsers.append(int(Ventanilla[i]['user_id']))
	Cajero = Cajero.objects.exclude(user_id__in=idUsers)
	
	descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	cajero_id = slCajero(widget=forms.Select(attrs={'class':'form-control selectpicker', 'data-live-search':'true'}), 
									queryset=Cajero,
									empty_label="Seleccione un cajero")
	class Meta:
		model = Ventanilla
		fields = ('descripcion',)

class frmEditarCaja(forms.ModelForm):
	# Obtengo los id de los usuarios que tienen caja asignadas
	Ventanilla = Ventanilla.objects.exclude(tipo_atencion_id__descripcion='Atencion al cliente').values('user_id')
	idUsers = []
	for i in range(len(Ventanilla)):
		idUsers.append(int(Ventanilla[i]['user_id']))
	Cajero = Cajero.objects.exclude(user_id__in=idUsers)

	descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	cajero_id = slCajero(widget=forms.Select(attrs={'class':'form-control selectpicker', 'data-live-search':'true'}), 
									#queryset=Cajero.objects.all(),
									queryset=Cajero,
									empty_label="Seleccione un cajero")
									#empty_label=idUsers[1])
	class Meta:
		model = Ventanilla
		fields = ('descripcion',)

class slEjecutivo(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "%s %s" %(obj.nombre, obj.apellido)

class frmAgregarCajaEjecutivo(forms.ModelForm):
	# Obtengo los id de los usuarios que tienen caja asignadas
	#Ventanilla = Ventanilla.objects.exclude(tipo_atencion_id=1).values('user_id')
	Ventanilla = Ventanilla.objects.exclude(tipo_atencion_id__descripcion='Caja').values('user_id')
	idUsers = []
	for i in range(len(Ventanilla)):
		idUsers.append(int(Ventanilla[i]['user_id']))
	Ejecutivo = Ejecutivo.objects.exclude(user_id__in=idUsers)

	descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	ejecutivo_id = slEjecutivo(widget=forms.Select(attrs={'class':'form-control selectpicker', 'data-live-search':'true'}), 
									queryset=Ejecutivo,
									empty_label="Seleccione un ejecutivo")
	class Meta:
		model = Ventanilla
		fields = ('descripcion',)

class frmEditarCajaEjecutivo(forms.ModelForm):
	# Obtengo los id de los usuarios que tienen caja asignadas
	#Ventanilla = Ventanilla.objects.exclude(tipo_atencion_id=1).values('user_id')
	Ventanilla = Ventanilla.objects.exclude(tipo_atencion_id__descripcion='Caja').values('user_id')
	idUsers = []
	for i in range(len(Ventanilla)):
		idUsers.append(int(Ventanilla[i]['user_id']))
	Ejecutivo = Ejecutivo.objects.exclude(user_id__in=idUsers)

	descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
	ejecutivo_id = slEjecutivo(widget=forms.Select(attrs={'class':'form-control selectpicker', 'data-live-search':'true'}), 
									#queryset=Ejecutivo.objects.all(),
									queryset=Ejecutivo,
									empty_label="Seleccione un ejecutivo")
	class Meta:
		model = Ventanilla
		fields = ('descripcion',)

class frmAgregarCliente(forms.ModelForm):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	dui = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'00000000-0'}))
	genero = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENERO)
	fecha_nacimiento = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'placeholder':'dd/mm/aaaa'}))
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	class Meta:
		model = Cliente
		fields = (
			'nombre',
			'apellido',
			'dui',
			'genero',
			'fecha_nacimiento',
			'telefono',
			'correo_electronico'
			)

class frmEditarCliente(forms.ModelForm):
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))
	class Meta:
		model = Cliente
		fields = (
			'telefono',
			'correo_electronico'
			)

class frmEncuesta(forms.ModelForm):
	respuesta = forms.ChoiceField(widget=forms.RadioSelect(), choices=ENCUESTA)
	class Meta:
		model = Encuesta
		fields = ('respuesta',)

class frmVideo(forms.ModelForm):
	descripcion = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':'3'}))
	class Meta:
		model = Video
		fields = ('descripcion', 'ruta')

class frmEditarPerfil(forms.Form):
	nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000-0000'}))
	correo_electronico = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre.usuario@proveedor.com'}))