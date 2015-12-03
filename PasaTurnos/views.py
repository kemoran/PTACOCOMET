# -*- encoding: utf-8 -*-
from django.shortcuts import render, render_to_response
# Clase para redireccionar
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
#CLASE UTILIZADA PARA UTILIZAR LAS RUTAS POR EL NOMBRE
from django.core.urlresolvers import reverse, reverse_lazy
# Clase para enviar variables del settings(Staticas) a las plantillas
from django.template import RequestContext
# Clase de formularios de modulos de django
from django.contrib.auth.forms import AuthenticationForm
# Clase para acceso y salir del sistema
from django.contrib.auth import authenticate, login, logout
# Clase para observar si una consulta me devuelve resultados
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
# Clase para generacion de PDF
from geraldo.generators import PDFGenerator
# Decoradores
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
# Reporte
from PasaTurnos.reports import rpTicket
# Tablas de BD Auth ej: User, permissions
from django.contrib.auth.models import User, Permission
# Tablas de la BD PasaTurnos
from PasaTurnos.models import Empresa, Gerente, Ejecutivo, Cajero, Servicio, Ventanilla, \
TipoAtencion, Ticket, Cliente, Encuesta, Video
# Formularios personalizados
from PasaTurnos.forms import frmAgregarEmpresa, frmEditarEmpresa, frmAgregarGerente, frmEditarGerente, \
frmAgregarEjecutivo, frmEditarEjecutivo, frmAgregarCajero, frmEditarCajero, frmAgregarServicio, frmEditarServicio, \
frmAgregarCaja, frmEditarCaja, frmAgregarCajaEjecutivo, frmEditarCajaEjecutivo, frmAgregarCliente, frmEncuesta, \
frmVideo, frmEditarCliente, frmEditarPerfil
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
#Serializador
from django.core import serializers

# Create your views here.
def Index(request):
	try:
		iEmpresa = Empresa.objects.get(pk=1)
		return render(request, 'Acceso.html', {'Mensaje':''})
	except ObjectDoesNotExist, e:
		#return HttpResponseRedirect('/AdmonSistema/Empresa/Agregar/')
		return HttpResponseRedirect('/AdmonSistema/Empresa/Agregar/')
	#return render(request, 'Acceso.html')

def PantallaAsignacion(request):
	Ventanillas = Ventanilla.objects.filter(tipo_atencion_id__descripcion='Atencion al cliente').values('id', 'descripcion')
	Cajeros = Ventanilla.objects.filter(tipo_atencion_id__descripcion='Caja').values('id', 'descripcion')
	iVideo = Video.objects.all()
	return render(request, 'PantallaAsignacion.html', {'Ventanillas':Ventanillas, 'Cajeros':Cajeros, 'iVideo':iVideo})

def Acceso(request):
	try:
		iEmpresa = Empresa.objects.get(pk=1)
	except ObjectDoesNotExist, e:
		return HttpResponseRedirect('/AdmonSistema/Empresa/Agregar/')
	Mensaje = ''
	if request.user.is_authenticated():
		return HttpResponseRedirect('/Sistema/')
	else:
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('Sistema')
				else:
					Mensaje = 'Verifica si tu usuario está activo'
			else:
				Mensaje = 'Usuario y/o contraseña incorrecto'
		return render(request, 'Acceso.html', {'Mensaje':Mensaje})

@login_required(login_url=reverse_lazy('Acceso'))
def CerrarSesion(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url=reverse_lazy('Acceso'))
def Sistema(request):
	ifrmEncuesta = frmEncuesta()
	return render(request, 'Sistema.html', {'ifrmEncuesta':ifrmEncuesta})

@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('Sistema'))
def ConsultarEmpresa(request):
	try:
		iEmpresa = Empresa.objects.all()
		VAgregar = 1
	except ObjectDoesNotExist:
		iEmpresa = ''
		VAgregar = 0
	return render(request, 'ConsultarEmpresa.html', {'iEmpresa':iEmpresa, 'VAgregar':VAgregar})

# Al inicio del sistema se solicita la información de la empresa para poder crear el administrador
def AgregarEmpresa(request):
	if request.method == 'POST':
		ifrmAgregarEmpresa = frmAgregarEmpresa(request.POST)
		if ifrmAgregarEmpresa.is_valid():
			ifrmAgregarEmpresa.save()
			# Creación de servicios
			iTipoAtencion = TipoAtencion(descripcion = 'Atencion al cliente')
			iTipoAtencion.save()
			iTipoAtencion = TipoAtencion(descripcion = 'Caja')
			iTipoAtencion.save()
			iCliente = Cliente(
					nombre = ' ',
					apellido = ' ',
					dui = '00000000-0',
					genero = 'M',
					fecha_nacimiento = '2000-01-01'
				)
			iCliente.save()
			if request.user.is_authenticated():
				return HttpResponseRedirect('/AdmonSistema/Empresa/Consultar/')
				#return HttpResponseRedirect('/')
			else:
				#return HttpResponseRedirect('/AdmonSistema/Empresa/Consultar/')
				return HttpResponseRedirect('/')
	else:
		ifrmAgregarEmpresa = frmAgregarEmpresa()
	return render(request, 'AgregarEmpresa.html', {'ifrmAgregarEmpresa':ifrmAgregarEmpresa})

@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('Sistema'))
def EditarEmpresa(request, id):
	iEmpresa = Empresa.objects.get(pk=id)
	if request.method == 'POST':
		ifrmEditarEmpresa = frmEditarEmpresa(request.POST, instance=iEmpresa)
		if ifrmEditarEmpresa.is_valid():
			ifrmEditarEmpresa.save()
			return HttpResponseRedirect('/AdmonSistema/Empresa/Consultar/')
	else:
		ifrmEditarEmpresa = frmEditarEmpresa(instance=iEmpresa)
	return render(request, 'EditarEmpresa.html', {'ifrmEditarEmpresa':ifrmEditarEmpresa, 'tbl':iEmpresa})

@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('Sistema'))
def EliminarEmpresa(request, id):
	iEmpresa = Empresa.objects.get(pk=id)
	iEmpresa.delete()
	return HttpResponseRedirect('/AdmonSistema/Empresa/Consultar/')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AdministracionUsuarios(request):
	return render(request, 'AdministracionUsuarios.html')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def ConsultarCliente(request):
	iCliente = Cliente.objects.all().exclude(dui='00000000-0')
	return render(request, 'ConsultarCliente.html', {'iCliente':iCliente})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AgregarCliente(request):
	Mensaje = ''
	if request.method == 'POST':
		# Convierto el valor de la fecha de nacimiento a formato MySQL, cambiando el parametro en request.POST
		cpPOST = request.POST.copy()
		cpPOST['fecha_nacimiento'] = datetime.strptime(request.POST['fecha_nacimiento'], "%d/%m/%Y").strftime("%Y-%m-%d")
		ifrmAgregarCliente = frmAgregarCliente(cpPOST)
		if ifrmAgregarCliente.is_valid():
			try:
				iCliente = Cliente.objects.get(dui=request.POST['dui'])
				Mensaje = 'Número de documento ya está registrado'
				ifrmAgregarCliente = frmAgregarCliente()
			except ObjectDoesNotExist:
				ifrmAgregarCliente.save()
				return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Cliente/Consultar/')
	else:
		ifrmAgregarCliente = frmAgregarCliente()
	if Mensaje != '':
		return render(request, 'AgregarCliente.html', {'ifrmAgregarCliente':ifrmAgregarCliente, 'Mensaje':Mensaje})
	return render(request, 'AgregarCliente.html', {'ifrmAgregarCliente':ifrmAgregarCliente})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EditarCliente(request, id):
	iCliente = Cliente.objects.get(pk=id)
	if request.method == 'POST':
		ifrmEditarCliente = frmEditarCliente(request.POST, instance=iCliente)
		if ifrmEditarCliente.is_valid():
			ifrmEditarCliente.save()
			return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Cliente/Consultar/')
	else:
		ifrmEditarCliente = frmEditarCliente(instance=iCliente)
	return render(request, 'EditarCliente.html', {'ifrmEditarCliente':ifrmEditarCliente})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EliminarCliente(request, id):
	iCliente = Cliente.objects.get(pk=id)
	iCliente.delete()
	return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Cliente/Consultar/')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def ConsultarGerente(request):
	iGerente = Gerente.objects.all()
	return render(request, 'ConsultarGerente.html', {'iGerente':iGerente})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AgregarGerente(request):
	Mensaje = ''
	if request.method == 'POST':
		ifrmAgregarGerente = frmAgregarGerente(request.POST)
		if ifrmAgregarGerente.is_valid():
			try:
				iUser = User.objects.create_user(request.POST['apodo_usuario'],
												request.POST['correo_electronico'],
												request.POST['contrasenha_usuario'])
				iUser.is_staff = 1
				iUser.first_name = request.POST['nombre']
				iUser.last_name = request.POST['apellido']
				iUser.save()
				# Obtengo el id del usuario ingresado
				idUser = User.objects.latest('id')
				iEmpresa = Empresa.objects.get(pk=1)
				# Creo una nueva instancia del formulario del gerente para agregar el id del la empresa
				nifrmAgregarGerente = ifrmAgregarGerente.save(commit=False)
				nifrmAgregarGerente.empresa_id = iEmpresa
				nifrmAgregarGerente.user = idUser
				nifrmAgregarGerente.save()
				return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Gerente/Consultar/')
			except Exception as e:
				Mensaje1 = 'Gerente ya registrado'
	else:
		ifrmAgregarGerente = frmAgregarGerente()
	return render(request, 'AgregarGerente.html', {'ifrmAgregarGerente':ifrmAgregarGerente, 'Mensaje':Mensaje})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EditarGerente(request, id):
	iGerente = Gerente.objects.get(pk=id)
	if request.method == 'POST':
		ifrmEditarGerente = frmEditarGerente(request.POST, instance=iGerente)
		if ifrmEditarGerente.is_valid():
			ifrmEditarGerente.save()
			return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Gerente/Consultar/')
	else:
		ifrmEditarGerente = frmEditarGerente(instance=iGerente)
	return render(request, 'EditarGerente.html', {'ifrmEditarGerente': ifrmEditarGerente})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EliminarGerente(request, id):
	iGerente = Gerente.objects.get(pk=id)
	iGerente.delete()
	iUser = User.objects.get(pk=int(iEjecutivo.user_id))
	iUser.delete()
	return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Gerente/Consultar/')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def ConsultarEjecutivo(request):
	iEjecutivo = Ejecutivo.objects.all()
	return render(request, 'ConsultarEjecutivo.html', {'iEjecutivo':iEjecutivo})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AgregarEjecutivo(request):
	Mensaje = ''
	if request.method == 'POST':
		ifrmAgregarEjecutivo = frmAgregarEjecutivo(request.POST)
		if ifrmAgregarEjecutivo.is_valid():
			try:
				iUser = User.objects.create_user(request.POST['apodo_usuario'],
												request.POST['correo_electronico'],
												request.POST['contrasenha_usuario'])
				iUser.is_staff = 0
				iUser.first_name = request.POST['nombre']
				iUser.last_name = request.POST['apellido']
				iUser.save()
				# Obtengo el id del usuario ingresado
				idUser = User.objects.latest('id')
				# Busco el permiso que le agregare
				#Permiso = Permission.objects.get(name='Can change tbl ejecutivo')
				# Busco el registro de la empresa para agregar la llave foranea al Gerente
				#idUser.user_permissions.add(Permiso)
				iEmpresa = Empresa.objects.get(pk=1)
				# Creo una nueva instancia del formulario del gerente para agregar el id del la empresa
				nifrmAgregarEjecutivo = ifrmAgregarEjecutivo.save(commit=False)
				nifrmAgregarEjecutivo.empresa_id = iEmpresa
				nifrmAgregarEjecutivo.user = idUser
				nifrmAgregarEjecutivo.save()
				return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Ejecutivo/Consultar/')
			except Exception as e:
				Mensaje1 = 'Ejecutivo ya registrado'
	else:
		ifrmAgregarEjecutivo = frmAgregarEjecutivo()
	return render(request, 'AgregarEjecutivo.html', {'ifrmAgregarEjecutivo':ifrmAgregarEjecutivo, 'Mensaje':Mensaje})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EditarEjecutivo(request, id):
	iEjecutivo = Ejecutivo.objects.get(pk=id)
	if request.method == 'POST':
		ifrmEditarEjecutivo = frmEditarEjecutivo(request.POST, instance=iEjecutivo)
		if ifrmEditarEjecutivo.is_valid():
			ifrmEditarEjecutivo.save()
			return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Ejecutivo/Consultar/')
	else:
		ifrmEditarEjecutivo = frmEditarEjecutivo(instance=iEjecutivo)
	return render(request, 'EditarEjecutivo.html', {'ifrmEditarEjecutivo': ifrmEditarEjecutivo})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EliminarEjecutivo(request, id):
	iEjecutivo = Ejecutivo.objects.get(pk=id)
	iEjecutivo.delete()
	iUser = User.objects.get(pk=int(iEjecutivo.user_id))
	iUser.is_active = 0
	iUser.save()
	return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Ejecutivo/Consultar/')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def ConsultarCajero(request):
	iCajero = Cajero.objects.all()
	return render(request, 'ConsultarCajero.html', {'iCajero':iCajero})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AgregarCajero(request):
	Mensaje = ''
	if request.method == 'POST':
		ifrmAgregarCajero = frmAgregarCajero(request.POST)
		if ifrmAgregarCajero.is_valid():
			try:
				iUser = User.objects.create_user(request.POST['apodo_usuario'],
												request.POST['correo_electronico'],
												request.POST['contrasenha_usuario'])
				iUser.is_staff = 0
				iUser.first_name = request.POST['nombre']
				iUser.last_name = request.POST['apellido']
				iUser.save()
				# Obtengo el id del usuario ingresado
				idUser = User.objects.latest('id')
				# Busco el permiso que le agregare
				#Permiso = Permission.objects.get(name='Can change tbl ejecutivo')
				# Busco el registro de la empresa para agregar la llave foranea al Gerente
				#idUser.user_permissions.add(Permiso)
				iEmpresa = Empresa.objects.get(pk=1)
				# Creo una nueva instancia del formulario del gerente para agregar el id del la empresa
				nifrmAgregarCajero = ifrmAgregarCajero.save(commit=False)
				nifrmAgregarCajero.empresa_id = iEmpresa
				nifrmAgregarCajero.user = idUser
				nifrmAgregarCajero.save()
				return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Cajero/Consultar/')
			except Exception as e:
				Mensaje1 = 'Cajero ya registrado'
	else:
		ifrmAgregarCajero = frmAgregarCajero()
	return render(request, 'AgregarCajero.html', {'ifrmAgregarCajero':ifrmAgregarCajero, 'Mensaje':Mensaje})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EditarCajero(request, id):
	iCajero = Cajero.objects.get(pk=id)
	if request.method == 'POST':
		ifrmEditarCajero = frmEditarCajero(request.POST, instance=iCajero)
		if ifrmEditarCajero.is_valid():
			ifrmEditarCajero.save()
			return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Cajero/Consultar/')
	else:
		ifrmEditarCajero = frmEditarCajero(instance=iCajero)
	return render(request, 'EditarCajero.html', {'ifrmEditarCajero': ifrmEditarCajero})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EliminarCajero(request, id):
	iCajero = Cajero.objects.get(pk=id)
	iCajero.delete()
	iUser = User.objects.get(pk=int(iCajero.user_id))
	iUser.is_active = 0
	iUser.save()
	return HttpResponseRedirect('/AdmonSistema/AdmonUsuarios/Cajero/Consultar/')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def ConsultarServicio(request):
	iServicio = Servicio.objects.all().values('id','descripcion', 'tipo_atencion_id__descripcion')
	return render(request, 'ConsultarServicio.html', {'iServicio':iServicio})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AgregarServicio(request):
	Mensaje = ''
	if request.method == 'POST':
		ifrmAgregarServicio = frmAgregarServicio(request.POST)
		if ifrmAgregarServicio.is_valid():
			try:
				ifrmAgregarServicio.save()
				return HttpResponseRedirect('/AdmonServicio/Catalogo/Servicio/Consultar/')
			except Exception, e:
				Mensaje = 'Registro no almacenado'
	else:
		ifrmAgregarServicio = frmAgregarServicio()
	return render(request, 'AgregarServicio.html', {'ifrmAgregarServicio':ifrmAgregarServicio, 'Mensaje':Mensaje})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EditarServicio(request, id):
	iServicio = Servicio.objects.get(pk=id)
	if request.method == 'POST':
		ifrmEditarServicio = frmEditarServicio(request.POST, instance=iServicio)
		if ifrmEditarServicio.is_valid():
			ifrmEditarServicio.save()
			return HttpResponseRedirect('/AdmonServicio/Catalogo/Servicio/Consultar/')
	else:
		ifrmEditarServicio = frmEditarServicio(instance=iServicio)
	return render(request, 'EditarServicio.html', {'ifrmEditarServicio': ifrmEditarServicio})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EliminarServicio(request, id):
	iServicio = Servicio.objects.get(pk=id)
	iServicio.delete()
	return HttpResponseRedirect('/AdmonServicio/Catalogo/Servicio/Consultar/')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AdministracionEscritorios(request):
	return render(request, 'AdministracionEscritorios.html')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def ConsultarEscritorioCajero(request):
	iVentanilla = Ventanilla.objects.filter(tipo_atencion_id__descripcion='Caja').values('id', 'descripcion', 'user__first_name', 'user__last_name')
	return render(request, 'ConsultarEscritorioCajero.html', {'iVentanilla':iVentanilla})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AgregarEscritorioCajero(request):
	Mensaje = ''
	if request.method == 'POST':
		ifrmAgregarCaja = frmAgregarCaja(request.POST)
		if ifrmAgregarCaja.is_valid():
			try:
				# Verifico si existe el cajero seleccionado, para enviar un mensaje de error
				idCajero = Cajero.objects.get(pk=request.POST['cajero_id'])
				iVentanilla = Ventanilla.objects.get(user_id=idCajero.user.id)
				Mensaje = 'El cajero seleccionado ya esta asignado a un escritorio'
			except ObjectDoesNotExist, e:
				# Obtengo el id del cajero seleccionado para buscar su usuario
				idCajero = Cajero.objects.get(pk=request.POST['cajero_id'])
				# Con el id del usuario, busco el id de usuario de sistema
				idUser = User.objects.get(pk=idCajero.user.id)
				# Obtengo el registro de atencion Caja
				idTipoAtencion = TipoAtencion.objects.get(descripcion='Caja')
				# Detengo el almacenamiento del formulario para crear una nueva instancia y agregarle los nuevos campos
				nifrmAgregarCaja = ifrmAgregarCaja.save(commit=False)
				nifrmAgregarCaja.user = idUser
				nifrmAgregarCaja.tipo_atencion_id = idTipoAtencion
				nifrmAgregarCaja.save()
				return HttpResponseRedirect('/AdmonSistema/AdmonEscritorios/Cajero/Consultar/')
	else:
		ifrmAgregarCaja = frmAgregarCaja()
	return render(request, 'AgregarEscritorioCajero.html', {'ifrmAgregarCaja':ifrmAgregarCaja, 'Mensaje':Mensaje})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EditarEscritorioCajero(request, id):
	Mensaje = ''
	iVentanilla = Ventanilla.objects.get(pk=id)
	if request.method == 'POST':
		ifrmEditarCaja = frmEditarCaja(request.POST, instance=iVentanilla)
		if ifrmEditarCaja.is_valid():
			try:
				# Verifico si existe el cajero seleccionado, para enviar un mensaje de error
				idCajero = Cajero.objects.get(pk=request.POST['id'])
				iVentanilla = Ventanilla.objects.get(user_id=idCajero.user.id)
				Mensaje = 'El cajero seleccionado ya esta asignado a un escritorio'
			except ObjectDoesNotExist, e:
				# Obtengo el id del cajero seleccionado para buscar su usuario
				idCajero = Cajero.objects.get(pk=request.POST['id'])
				# Con el id del usuario, busco el id de usuario de sistema
				idUser = User.objects.get(pk=idCajero.user.id)
				# Obtengo el registro de atencion Caja
				idTipoAtencion = TipoAtencion.objects.get(descripcion='Caja')
				# Detengo el almacenamiento del formulario para crear una nueva instancia y agregarle los nuevos campos
				nifrmEditarCaja = ifrmEditarCaja.save(commit=False)
				nifrmEditarCaja.user = idUser
				nifrmEditarCaja.tipo_atencion_id = idTipoAtencion
				nifrmEditarCaja.save()
				return HttpResponseRedirect('/AdmonSistema/AdmonEscritorios/Cajero/Consultar/')
	else:
		ifrmEditarCaja = frmEditarCaja(instance=iVentanilla)
	return render(request, 'EditarEscritorioCajero.html', {'ifrmEditarCaja':ifrmEditarCaja, 'Mensaje':Mensaje})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EliminarEscritorioCajero(request, id):
	iVentanilla = Ventanilla.objects.get(pk=id)
	iVentanilla.delete()
	return HttpResponseRedirect('/AdmonSistema/AdmonEscritorios/Cajero/Consultar/')

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def ConsultarEscritorioEjecutivo(request):
	iVentanilla = Ventanilla.objects.filter(tipo_atencion_id__descripcion='Atencion al cliente').values('id', 'descripcion', 'user__first_name', 'user__last_name')
	return render(request, 'ConsultarEscritorioEjecutivo.html', {'iVentanilla':iVentanilla})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AgregarEscritorioEjecutivo(request):
	Mensaje = ''
	if request.method == 'POST':
		ifrmAgregarCajaEjecutivo = frmAgregarCajaEjecutivo(request.POST)
		if ifrmAgregarCajaEjecutivo.is_valid():
			try:
				# Verifico si existe el ejecutivo seleccionado, para enviar un mensaje de error
				idEjecutivo = Ejecutivo.objects.get(pk=request.POST['ejecutivo_id'])
				iVentanilla = Ventanilla.objects.get(user_id=idEjecutivo.user.id)
				Mensaje = 'El ejecutivo seleccionado ya esta asignado a un escritorio'
			except ObjectDoesNotExist, e:
				# Obtengo el id del ejecutivo seleccionado para buscar su usuario
				idEjecutivo = Ejecutivo.objects.get(pk=request.POST['ejecutivo_id'])
				# Con el id del usuario, busco el id de usuario de sistema
				idUser = User.objects.get(pk=idEjecutivo.user.id)
				# Obtengo el registro de atencion Caja
				idTipoAtencion = TipoAtencion.objects.get(descripcion='Atencion al cliente')
				# Detengo el almacenamiento del formulario para crear una nueva instancia y agregarle los nuevos campos
				nifrmAgregarCajaEjecutivo = ifrmAgregarCajaEjecutivo.save(commit=False)
				nifrmAgregarCajaEjecutivo.user = idUser
				nifrmAgregarCajaEjecutivo.tipo_atencion_id = idTipoAtencion
				nifrmAgregarCajaEjecutivo.save()
				return HttpResponseRedirect('/AdmonSistema/AdmonEscritorios/Ejecutivo/Consultar/')
	else:
		ifrmAgregarCajaEjecutivo = frmAgregarCajaEjecutivo()
	return render(request, 'AgregarEscritorioEjecutivo.html', {'ifrmAgregarCajaEjecutivo':ifrmAgregarCajaEjecutivo, 'Mensaje':Mensaje})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EditarEscritorioEjecutivo(request, id):
	Mensaje = ''
	iVentanilla = Ventanilla.objects.get(pk=id)
	if request.method == 'POST':
		ifrmEditarCajaEjecutivo = frmEditarCajaEjecutivo(request.POST, instance=iVentanilla)
		if ifrmEditarCajaEjecutivo.is_valid():
			try:
				# Verifico si existe el ejecutivo seleccionado, para enviar un mensaje de error
				idEjecutivo = Ejecutivo.objects.get(pk=request.POST['id'])
				iVentanilla = Ventanilla.objects.get(user_id=idEjecutivo.user.id)
				Mensaje = 'El ejecutivo seleccionado ya esta asignado a un escritorio'
			except ObjectDoesNotExist, e:
				# Obtengo el id del ejecutivo seleccionado para buscar su usuario
				idEjecutivo = Ejecutivo.objects.get(pk=request.POST['id'])
				# Con el id del usuario, busco el id de usuario de sistema
				idUser = User.objects.get(pk=idEjecutivo.user.id)
				# Obtengo el registro de atencion Caja
				idTipoAtencion = TipoAtencion.objects.get(descripcion='Atencion al cliente')
				# Detengo el almacenamiento del formulario para crear una nueva instancia y agregarle los nuevos campos
				nifrmEditarCajaEjecutivo = ifrmEditarCajaEjecutivo.save(commit=False)
				nifrmEditarCajaEjecutivo.user = idUser
				nifrmEditarCajaEjecutivo.tipo_atencion_id = idTipoAtencion
				nifrmEditarCajaEjecutivo.save()
				return HttpResponseRedirect('/AdmonSistema/AdmonEscritorios/Ejecutivo/Consultar/')
	else:
		ifrmEditarCajaEjecutivo = frmEditarCajaEjecutivo(instance=iVentanilla)
	return render(request, 'EditarEscritorioEjecutivo.html', {'ifrmEditarCajaEjecutivo':ifrmEditarCajaEjecutivo, 'Mensaje':Mensaje})

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def EliminarEscritorioEjecutivo(request, id):
	iVentanilla = Ventanilla.objects.get(pk=id)
	iVentanilla.delete()
	return HttpResponseRedirect('/AdmonSistema/AdmonEscritorios/Ejecutivo/Consultar/')

def PantallaGeneradoraTicket(request):
	Mensaje = ''
	ifrmAgregarCliente = frmAgregarCliente()
	iServicio = Servicio.objects.all()
	return render(request, 'PantallaGeneradoraTicket.html', {'Mensaje':Mensaje, 'iServicio':iServicio, 'ifrmAgregarCliente':ifrmAgregarCliente})

def GeneradordeTicket(request, servicio_id, dui):
	#Guardar ticket
	idCliente = Cliente.objects.get(dui=dui)
	idServicio = Servicio.objects.get(id=servicio_id)
	#idVentanilla = Ventanilla.objects.get(pk=1)
	idServicios = []
	if idServicio.tipo_atencion_id.descripcion == 'Caja':
		Servicios = Servicio.objects.exclude(tipo_atencion_id__descripcion='Caja').values('id')
		for i in range(len(Servicios)):
			idServicios.append(int(Servicios[i]['id']))
		print str(datetime.date(datetime.now()))
		Total = Ticket.objects.extra(select={'Total':'COUNT(*)'}, where={"fecha_emicion >= '"+str(datetime.date(datetime.now()))+" 00:00:00'"}).exclude(servicio_id__in=idServicios).values('Total')
		#numTicket = 'C' + str(Ticket.objects.exclude(id_servicio__in=idServicios).filter(fecha_emicion__gte=''+str(datetime.date(datetime.now()))+'').count()+1)
		numTicket = 'C' + str(Total[0]['Total']+1)
	else:
		Servicios = Servicio.objects.exclude(tipo_atencion_id__descripcion='Atencion al cliente').values('id')
		for i in range(len(Servicios)):
			idServicios.append(int(Servicios[i]['id']))
		print str(datetime.date(datetime.now()))
		Total = Ticket.objects.extra(select={'Total':'COUNT(*)'}, where={"fecha_emicion >= '"+str(datetime.date(datetime.now()))+" 00:00:00'"}).exclude(servicio_id__in=idServicios).values('Total')
		#numTicket = 'AT' + str(Ticket.objects.exclude(id_servicio__in=idServicios).filter(fecha_emicion__gte=''+str(datetime.date(datetime.now()))+'').count()+1)
		numTicket = 'AT' + str(Total[0]['Total']+1)
	iTicket = Ticket(
		cliente_id=idCliente,
		#id_ventanilla=idVentanilla,
		servicio_id=idServicio,
		numero=numTicket,
		#fecha_emicion=str(datetime.utcnow()),
		#fecha_emicion=datetime.date(datetime.now()),
		fecha_emicion=timezone.localtime(timezone.now()),
		#fecha_emicion=datetime.datetime.now(),
		#fecha_emicion=str(datetime.date(datetime.now()),
		estado='E' #Espera
	)
	iTicket.save()
	#Generacion de ticket
	try:
		iCliente = Cliente.objects.extra(select={'nombre':'CONCAT(nombre," ",apellido)'}, where={"dui='"+dui+"'"}).values()
		print len(iCliente)
	except DatabaseError:
		# Concatenación en SQLite
		iCliente = Cliente.objects.extra(select={'nombre':'(nombre || " " || apellido)'}, where={"dui='"+dui+"'"}).values()
	qs=[{'nombre':iCliente[0]['nombre'], 'numero_ticket':numTicket}]
	#iHttpResponse = HttpResponse(mimetype='application/pdf') #Modificado para la versión 1.8 (mimetype a content_type)
	iHttpResponse = HttpResponse(content_type='application/pdf')
	#Reporte = rpTicket(queryset=iCliente)
	Reporte = rpTicket(queryset=qs)
	Reporte.generate_by(PDFGenerator, filename=iHttpResponse)
	return iHttpResponse

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('Sistema'))
def AdministracionPantalla(request):
	iVideo = Video.objects.all()
	if request.method == 'POST':
		ifrmVideo = frmVideo(request.POST, request.FILES)
		if ifrmVideo.is_valid():
			ifrmVideo.save()
			return HttpResponseRedirect('/AdministracionPantalla/')
	else:
		ifrmVideo = frmVideo()
	return render(request, 'AdministracionPantalla.html', {'ifrmVideo':ifrmVideo, 'iVideo':iVideo})

def EliminarVideoAdministracionPantalla(request, id):
	iVideo = Video.objects.get(pk=id)
	iVideo.delete()
	return HttpResponseRedirect('/AdministracionPantalla/')

def IdentificarClienteAjaxPGT(request, dui):
	if request.is_ajax() and request.method == 'GET':
		success = False
		try:
			iCliente = Cliente.objects.get(dui=dui)
			success = True
			response = {'success':success}
		except ObjectDoesNotExist:
			errors = 'Verifique el número de documento, o registre al cliente'
			response = {'success':success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def AgregarClienteAjaxPGT(request):
	if request.is_ajax() and request.method == 'POST':
		success = False
		ifrmAgregarCliente = frmAgregarCliente(request.POST)
		if ifrmAgregarCliente.is_valid():
			# Verifico que el cliente no esté registrado
			try:
				iCliente = Cliente.objects.get(dui=request.POST['dui'])
				errors = {'dui':'Número de documento ya está registrado.'}
				response = {'success':success, 'errors':errors}
			except ObjectDoesNotExist:
				ifrmAgregarCliente.save()
				success = True
				response = {'success':success}
		else:
			errors = ifrmAgregarCliente.errors
			response = {'success':success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def LlamarNuevoTicketAjaxSistema(request):
	if request.is_ajax() and request.method == 'POST':
		success = False
		iVentanilla = Ventanilla.objects.get(user=int(request.POST['user_id']))
		
		# Verifico el ultimo ticket en proceso para cambiar su estado
		# Obtengo el Ticket Actual en proceso para cambiarle su estado a Anulado(N) o a Atendido(A)
		try:
			TicketP = Ticket.objects.get(estado='P', ventanilla_id=iVentanilla.id)
			if request.POST['Estado'] == 'A':
				TicketP.estado = 'A'
			else:
				TicketP.estado = 'N'
			TicketP.save()
		except ObjectDoesNotExist:
			print 'Aun no existen tickets atentidos'

		# Obtengo los id de los servicios segun su tipo para verificar de que tipo de ticket es el que se procesará
		idServicios = []
		if iVentanilla.tipo_atencion_id.descripcion == 'Caja':
			Servicios = Servicio.objects.exclude(tipo_atencion_id__descripcion='Atencion al cliente').values('id')
			for i in range(len(Servicios)):
				idServicios.append(int(Servicios[i]['id']))
		else:
			Servicios = Servicio.objects.exclude(tipo_atencion_id__descripcion='Caja').values('id')
			for i in range(len(Servicios)):
				idServicios.append(int(Servicios[i]['id']))
		Tickets = Ticket.objects.all().filter(servicio_id__in=idServicios, estado='E').exclude(fecha_emicion__lte=''+str(datetime.date(datetime.now()))+'').order_by('fecha_emicion').values('id', 'numero')
		if len(Tickets) == 0:
			errors = 'No existen tickets disponibles para atención'
			response = {'success':success, 'errors':errors}
		else:
			# Obtengo el último ticket en base al tipo de servicio requerido para cambiar su estado a En Proceso (P)
			try:	
				iTicket = Ticket.objects.get(pk=int(Tickets[0]['id']))
				iTicket.estado = 'P'
				iTicket.ventanilla_id = iVentanilla
				iTicket.save()
				success = True
				numeroTicket = Tickets[0]['numero']
				print numeroTicket
				response = {'success':success, 'numeroTicket':numeroTicket}
			except ObjectDoesNotExist:
				print 'Error 2'
				errors = 'No existen tickets disponibles para atención'
				response = {'success':success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def LlamarNuevoTicketAjaxPGT(request, id_ventanilla):
	if request.is_ajax() and request.method == 'POST':
		success = False
		response = {'success':success}
		#Ventanilla = iVentanilla.objects.get(pk=id_ventanilla)
		return JsonResponse(response)
	else:
		raise Http404

@csrf_exempt
def LlamarClienteNodeJSSistema(request):
	if request.method == 'POST':
		iVentanilla = Ventanilla.objects.get(user=int(request.POST['user_id']))
		response = {'id': iVentanilla.id, 'descripcion': iVentanilla.descripcion ,'numeroTicket':request.POST['numeroTicket']}
		return JsonResponse(response)
	else:
		raise Http404

def VerificarTicketEncuestaAjaxSistema(request):
	if request.is_ajax() and request.method == 'POST':
		success = False
		iVentanilla = Ventanilla.objects.get(user=int(request.POST['user_id']))
		# Verifico el ultimo ticket en proceso para cambiar su estado
		try:
			TicketP = Ticket.objects.get(estado='P', ventanilla_id=iVentanilla.id)
			success = True
		except ObjectDoesNotExist:
			print 'Aun no existen tickets en proceso'
		response = {'success':success}
		return JsonResponse(response)
	else:
		raise Http404

def EvaluacionAjaxSistema(request):
	if request.is_ajax and request.method == 'POST':
		success = False
		ifrmEncuesta = frmEncuesta(request.POST)
		if ifrmEncuesta.is_valid():
			nifrmEncuesta = ifrmEncuesta.save(commit=False)
			nifrmEncuesta.fecha_emicion = datetime.date(datetime.now())
			#ifrmEncuesta.save()
			nifrmEncuesta.save()
			success = True
			response = {'success':success}
		else:
			errors = ifrmEncuesta.errors
			response = {'success':success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def CambioContraAjax(request):
	if request.is_ajax and request.method == 'POST':
		success = False
		iUser = User.objects.get(pk=int(request.POST['user_id']))
		if iUser.check_password(request.POST['txtContraActual']):
			if request.POST['txtContraNueva'] == request.POST['txtContraConfirm']:
				iUser.set_password(request.POST['txtContraNueva'])
				iUser.save()
				success = True
				mensaje = 'Contraseña modificada exitosamente'
				response = {'success':success, 'mensaje':mensaje}
			else:
				errors = 'Las contraseñas escritas no coinciden'
				response = {'success':success, 'errors':errors}
		else:
			errors = 'Contraseña actual incorrecta'
			response = {'success':success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404


def VerPerfilAjax(request):
	if request.is_ajax() and request.method == 'POST':
		success = False
		try:
			iUser = User.objects.get(pk=int(request.POST['user_id']))
			idUser = User.objects.filter(pk=int(request.POST['user_id'])).values('id', 'first_name', 'last_name', 'email')
			if len(Cajero.objects.filter(user_id=int(idUser[0]['id']))):
				# Perfil de cajero
				iCajero = Cajero.objects.filter(user_id=int(idUser[0]['id'])).values('nombre', 'apellido', 'telefono', 'correo_electronico')
				perfil = {
							'nombre':iCajero[0]['nombre'],
							'apellido':iCajero[0]['apellido'],
							'telefono':iCajero[0]['telefono'],
							'correo':iCajero[0]['correo_electronico']
						}
			elif len(Ejecutivo.objects.filter(user_id=int(idUser[0]['id']))):
				# Perfil de Ejecutivo
				iEjecutivo = Ejecutivo.objects.filter(user_id=int(idUser[0]['id'])).values('nombre', 'apellido', 'telefono', 'correo_electronico')
				perfil = {
							'nombre':iEjecutivo[0]['nombre'],
							'apellido':iEjecutivo[0]['apellido'],
							'telefono':iEjecutivo[0]['telefono'],
							'correo':iEjecutivo[0]['correo_electronico']
						}
			else:
				# Perfil de SuperUser
				perfil = {
							'nombre':idUser[0]['first_name'],
							'apellido':idUser[0]['last_name'],
							'telefono':False,
							'correo':idUser[0]['email']
						}
			#iUser = User.objects.filter(pk=int(request.POST['user_id'])).values('telefono_cliente', '')
			success = True
			#perfil = iUser
			response = {'success':success, 'perfil':perfil}
		except ObjectDoesNotExist, e:
			errors = 'Verifique su usuario'
			response = {'success':success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def EditarPerfilAjax(request):
	if request.is_ajax() and request.method == 'POST':
		success = False
		try:
			iUser = User.objects.get(pk=int(request.POST['user_id']))
			idUser = User.objects.filter(pk=int(request.POST['user_id'])).values('id')
			if len(Cajero.objects.filter(user_id=int(idUser[0]['id']))):
				# Perfil de cajero
				iCajero = Cajero.objects.get(user_id=idUser)
				'''
				iCajero.nombre = request.POST['txtNombre']
				iCajero.apellido = request.POST['txtApellido']
				'''
				iCajero.telefono = request.POST['txtTelefono']
				iCajero.correo_electronico = request.POST['txtCorreo']
				iCajero.save()
				'''
				iUser.first_name = request.POST['txtNombre']
				iUser.last_name = request.POST['txtApellido']
				'''
				iUser.email = request.POST['txtCorreo']
				iUser.save()
			elif len(Ejecutivo.objects.filter(user_id=int(idUser[0]['id']))):
				# Perfil de Ejecutivo
				iEjecutivo = Ejecutivo.objects.get(user_id=idUser)
				'''
				iEjecutivo.nombre = request.POST['txtNombre']
				iEjecutivo.apellido = request.POST['txtApellido']
				'''
				iEjecutivo.telefono = request.POST['txtTelefono']
				iEjecutivo.correo_electronico = request.POST['txtCorreo']
				iEjecutivo.save()
				'''
				iUser.first_name = request.POST['txtNombre']
				iUser.last_name = request.POST['txtApellido']
				'''
				iUser.email = request.POST['txtCorreo']
				iUser.save()
			else:
				# Perfil de SuperUser
				'''
				iUser.first_name = request.POST['txtNombre']
				iUser.last_name = request.POST['txtApellido']
				'''
				iUser.email = request.POST['txtCorreo']
				iUser.save()
			success = True
			mensaje = 'Perfil modificado exitosamente'
			response = {'success':success, 'mensaje':mensaje}
		except ObjectDoesNotExist, e:
			errors = 'Verifique su usuario'
			response = {'success':success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def RellamarNuevoTicketAjaxSistema(request):
	if request.is_ajax() and request.method == 'POST':
		success = False
		iVentanilla = Ventanilla.objects.get(user=int(request.POST['user_id']))
		try:
			TicketP = Ticket.objects.get(estado='P', ventanilla_id=iVentanilla.id)
			success = True
			numeroTicket = TicketP.numero
			response = {'success':success, 'numeroTicket':numeroTicket}
		except ObjectDoesNotExist:
			errors = 'No existe ningún ticket en proceso'
			response = {'success':success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def RellamarNuevoTicketAjaxPGT(request, ventanilla_id):
	if request.is_ajax() and request.method == 'POST':
		success = False
		response = {'success':success}
		#Ventanilla = iVentanilla.objects.get(pk=id_ventanilla)
		return JsonResponse(response)
	else:
		raise Http404


@csrf_exempt
def RellamarClienteNodeJSSistema(request):
	if request.method == 'POST':
		iVentanilla = Ventanilla.objects.get(user=int(request.POST['user_id']))
		response = {'id': iVentanilla.id, 'descripcion': iVentanilla.descripcion ,'numeroTicket':request.POST['numeroTicket']}
		return JsonResponse(response)
	else:
		raise Http404

def ReporteAtencion(request):
	Mensaje = 'Nada'
	return render(request, 'ReporteAtencion.html', {'Mensaje': Mensaje})

def GenerarReporteAtencion(request):
	iServicio = []
	if request.is_ajax() and request.method == 'POST':
		success = False
		try:
			sql = '''SELECT sr.id, sr.descripcion AS Servicio, SUM(IF((tk.estado = "A" AND tk.fecha_emicion BETWEEN "%s" AND DATE_ADD("%s", INTERVAL 1 DAY)),1,0)) AS Atendidos, 
					SUM(IF((tk.estado = "N" AND tk.fecha_emicion BETWEEN "%s" AND DATE_ADD("%s", INTERVAL 1 DAY)),1,0)) AS Nulos 
					FROM servicio AS sr LEFT JOIN ticket AS tk ON tk.servicio_id = sr.id 
					GROUP BY sr.descripcion;''' %(request.POST['fInicio'], request.POST['fFin'], request.POST['fInicio'], request.POST['fFin'])
			#Convierto la consulta en un objeto tipo json
			for i in Servicio.objects.raw(sql):
				iServicio.append({'id':i.id, 'Servicio': i.Servicio, 'Atendidos': int(i.Atendidos), 'Nulos': int(i.Nulos)})
			success = True
			response = {'success': success, 'iServicio': iServicio}
		except:
			errors = 'Debe seleccionar las fechas para generar el reporte'
			response = {'success': success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def ReporteOperario(request):
	Mensaje = 'Nada'
	return render(request, 'ReporteOperario.html', {'Mensaje' : Mensaje})

def GenerarReporteOperario(request):
	iOperario = []
	if request.is_ajax() and request.method == 'POST':
		success = False
		try:
			sql = '''SELECT u.id, u.username, CONCAT(u.first_name,' ',u.last_name) AS Operario,
					SUM(IF((tk.estado = "A" AND tk.fecha_emicion BETWEEN "%s" AND DATE_ADD("%s", INTERVAL 1 DAY)),1,0)) AS Atendidos,
					SUM(IF((tk.estado = "N" AND tk.fecha_emicion BETWEEN "%s" AND DATE_ADD("%s", INTERVAL 1 DAY)),1,0)) AS Nulos
					FROM auth_user AS u
					INNER JOIN ventanilla AS v ON v.user_id = u.id
					LEFT JOIN ticket AS tk ON tk.ventanilla_id = v.id
					GROUP BY u.username;''' %(request.POST['fInicio'], request.POST['fFin'], request.POST['fInicio'], request.POST['fFin'])
			#Convierto la consulta en un objeto tipo json
			for i in User.objects.raw(sql):
				iOperario.append({'id':i.id, 'Operario': i.Operario, 'Atendidos': int(i.Atendidos), 'Nulos': int(i.Nulos)})
			success = True
			response = {'success': success, 'iOperario': iOperario}
		except:
			errors = 'Debe seleccionar las fechas para generar el reporte'
			response = {'success': success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404

def ReporteEncuesta(request):
	Mensaje = 'Nada'
	return render(request, 'ReporteEncuesta.html', {'Mensaje': Mensaje})

def GenerarReporteEncuesta(request):
	iEncuesta = []
	if request.is_ajax() and request.method == 'POST':
		success = False
		try:
			# Convierto la consulta en un objeto tipo json
			sql = '''SELECT id, SUM(IF((respuesta = "M" AND fecha_emicion BETWEEN "%s" AND DATE_ADD("%s", INTERVAL 1 DAY)),1,0)) AS Malos,
					SUM(IF((respuesta = "B" AND fecha_emicion BETWEEN "%s" AND DATE_ADD("%s", INTERVAL 1 DAY)),1,0)) AS Buenos,
					SUM(IF((respuesta = "MB" AND fecha_emicion BETWEEN "%s" AND DATE_ADD("%s", INTERVAL 1 DAY)),1,0)) AS MuyBuenos
					FROM encuesta;''' %(request.POST['fInicio'], request.POST['fFin'], request.POST['fInicio'], request.POST['fFin'], request.POST['fInicio'], request.POST['fFin'])
			for i in Encuesta.objects.raw(sql):
				iEncuesta.append({'Malos': int(i.Malos), 'Buenos': int(i.Buenos), 'MuyBuenos': int(i.MuyBuenos)})
			if(len(iEncuesta)==0):
				errors = 'No existen registros en las fechas seleccionadas'
				response = {'success': success, 'errors':errors}
			else:
				success = True
				response = {'success': success, 'iEncuesta': iEncuesta}
		except:
			errors = 'Debe seleccionar las fechas para generar el reporte'
			response = {'success': success, 'errors':errors}
		return JsonResponse(response)
	else:
		raise Http404