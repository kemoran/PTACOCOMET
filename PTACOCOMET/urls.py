from django.conf.urls import include, url
from django.contrib import admin
import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'PTPasaTurnos.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Vistas del proyecto
    #url(r'^$', 'PasaTurnos.views.Index'),
    url(r'media/(?P<path>.*)', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    url(r'^$', 'PasaTurnos.views.Acceso', name='Acceso'),
    url(r'^CerrarSesion/$', 'PasaTurnos.views.CerrarSesion', name='CerrarSesion'),
    url(r'^Sistema/$', 'PasaTurnos.views.Sistema', name='Sistema'),
    url(r'^PantallaAsignacion/$', 'PasaTurnos.views.PantallaAsignacion', name='PantallaAsignacion'),

    url(r'^AdmonSistema/Empresa/Consultar/$', 'PasaTurnos.views.ConsultarEmpresa'),
    url(r'^AdmonSistema/Empresa/Agregar/$', 'PasaTurnos.views.AgregarEmpresa', name='AgregarEmpresa'),
    url(r'^AdmonSistema/Empresa/Editar/(?P<id>\d+)/$', 'PasaTurnos.views.EditarEmpresa'),
    url(r'^AdmonSistema/Empresa/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarEmpresa'),

    url(r'^AdmonSistema/AdmonUsuarios/$', 'PasaTurnos.views.AdministracionUsuarios'),
    
    url(r'^AdmonSistema/AdmonUsuarios/Gerente/Consultar/$', 'PasaTurnos.views.ConsultarGerente'),
    url(r'^AdmonSistema/AdmonUsuarios/Gerente/Agregar/$', 'PasaTurnos.views.AgregarGerente'),
    url(r'^AdmonSistema/AdmonUsuarios/Gerente/Editar/(?P<id>\d+)/$', 'PasaTurnos.views.EditarGerente'),
    url(r'^AdmonSistema/AdmonUsuarios/Gerente/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarGerente'),

    url(r'^AdmonSistema/AdmonUsuarios/Ejecutivo/Consultar/$', 'PasaTurnos.views.ConsultarEjecutivo'),
    url(r'^AdmonSistema/AdmonUsuarios/Ejecutivo/Agregar/$', 'PasaTurnos.views.AgregarEjecutivo'),
    url(r'^AdmonSistema/AdmonUsuarios/Ejecutivo/Editar/(?P<id>\d+)/$', 'PasaTurnos.views.EditarEjecutivo'),
    url(r'^AdmonSistema/AdmonUsuarios/Ejecutivo/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarEjecutivo'),

    url(r'^AdmonSistema/AdmonUsuarios/Cajero/Consultar/$', 'PasaTurnos.views.ConsultarCajero'),
    url(r'^AdmonSistema/AdmonUsuarios/Cajero/Agregar/$', 'PasaTurnos.views.AgregarCajero'),
    url(r'^AdmonSistema/AdmonUsuarios/Cajero/Editar/(?P<id>\d+)/$', 'PasaTurnos.views.EditarCajero'),
    url(r'^AdmonSistema/AdmonUsuarios/Cajero/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarCajero'),

    url(r'^AdmonServicio/Catalogo/Servicio/Consultar/$', 'PasaTurnos.views.ConsultarServicio'),
    url(r'^AdmonServicio/Catalogo/Servicio/Agregar/$', 'PasaTurnos.views.AgregarServicio'),
    url(r'^AdmonServicio/Catalogo/Servicio/Editar/(?P<id>\d+)/$', 'PasaTurnos.views.EditarServicio'),
    url(r'^AdmonServicio/Catalogo/Servicio/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarServicio'),

    url(r'^AdmonSistema/AdmonEscritorios/$', 'PasaTurnos.views.AdministracionEscritorios'),
    
    url(r'^AdmonSistema/AdmonEscritorios/Cajero/Consultar/$', 'PasaTurnos.views.ConsultarEscritorioCajero'),
    url(r'^AdmonSistema/AdmonEscritorios/Cajero/Agregar/$', 'PasaTurnos.views.AgregarEscritorioCajero'),
    url(r'^AdmonSistema/AdmonEscritorios/Cajero/Editar/(?P<id>\d+)/$', 'PasaTurnos.views.EditarEscritorioCajero'),
    url(r'^AdmonSistema/AdmonEscritorios/Cajero/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarEscritorioCajero'),

    url(r'^AdmonSistema/AdmonEscritorios/Ejecutivo/Consultar/$', 'PasaTurnos.views.ConsultarEscritorioEjecutivo'),
    url(r'^AdmonSistema/AdmonEscritorios/Ejecutivo/Agregar/$', 'PasaTurnos.views.AgregarEscritorioEjecutivo'),
    url(r'^AdmonSistema/AdmonEscritorios/Ejecutivo/Editar/(?P<id>\d+)/$', 'PasaTurnos.views.EditarEscritorioEjecutivo'),
    url(r'^AdmonSistema/AdmonEscritorios/Ejecutivo/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarEscritorioEjecutivo'),

    url(r'^PantallaGeneradoraTicket/$', 'PasaTurnos.views.PantallaGeneradoraTicket'),
    url(r'^PantallaGeneradoraTicket/GeneradordeTicket/(?P<servicio_id>\d+)/(?P<dui>\S+)/$', 'PasaTurnos.views.GeneradordeTicket'),

    url(r'^Ajax/AgregarClienteAjaxPGT/$', 'PasaTurnos.views.AgregarClienteAjaxPGT'),
    url(r'^Ajax/IdentificarClienteAjaxPGT/(?P<dui>\S+)/$', 'PasaTurnos.views.IdentificarClienteAjaxPGT'),
    
    url(r'^Ajax/LlamarNuevoTicketAjaxPGT/$', 'PasaTurnos.views.LlamarNuevoTicketAjaxPGT'),
    url(r'^NodeJS/LlamarCliente/$', 'PasaTurnos.views.LlamarClienteNodeJSSistema'),

    url(r'^Ajax/VerificarTicketEncuestaAjaxSistema/$', 'PasaTurnos.views.VerificarTicketEncuestaAjaxSistema'),
    url(r'^Ajax/EvaluacionAjaxSistema/$', 'PasaTurnos.views.EvaluacionAjaxSistema'),
    url(r'^Ajax/LlamarNuevoTicketAjaxSistema/$', 'PasaTurnos.views.LlamarNuevoTicketAjaxSistema'),

    url(r'^AdministracionPantalla/$', 'PasaTurnos.views.AdministracionPantalla'),
    url(r'^AdministracionPantalla/Video/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarVideoAdministracionPantalla'),

    url(r'^AdmonSistema/AdmonUsuarios/Cliente/Consultar/$', 'PasaTurnos.views.ConsultarCliente'),
    url(r'^AdmonSistema/AdmonUsuarios/Cliente/Agregar/$', 'PasaTurnos.views.AgregarCliente'),
    url(r'^AdmonSistema/AdmonUsuarios/Cliente/Editar/(?P<id>\d+)/$', 'PasaTurnos.views.EditarCliente'),
    url(r'^AdmonSistema/AdmonUsuarios/Cliente/Eliminar/(?P<id>\d+)/$', 'PasaTurnos.views.EliminarCliente'),

    url(r'^Ajax/CambioContraAjax/$', 'PasaTurnos.views.CambioContraAjax'),
    url(r'^Ajax/VerPerfilAjax/$', 'PasaTurnos.views.VerPerfilAjax'),
    url(r'^Ajax/EditarPerfilAjax/$', 'PasaTurnos.views.EditarPerfilAjax'),

    url(r'^Ajax/RellamarNuevoTicketAjaxPGT/$', 'PasaTurnos.views.RellamarNuevoTicketAjaxPGT'),
    url(r'^NodeJS/RellamarCliente/$', 'PasaTurnos.views.RellamarClienteNodeJSSistema'),
    url(r'^Ajax/RellamarNuevoTicketAjaxSistema/$', 'PasaTurnos.views.RellamarNuevoTicketAjaxSistema'),

    url(r'^Reporte/ReporteAtencion/$', 'PasaTurnos.views.ReporteAtencion'),
    url(r'^Reporte/GenerarReporteAtencion/$', 'PasaTurnos.views.GenerarReporteAtencion'),

    url(r'^Reporte/ReporteEncuesta/$', 'PasaTurnos.views.ReporteEncuesta'),
    url(r'^Reporte/GenerarReporteEncuesta/$', 'PasaTurnos.views.GenerarReporteEncuesta'),

    url(r'^Reporte/ReporteOperario/$', 'PasaTurnos.views.ReporteOperario'),
    url(r'^Reporte/GenerarReporteOperario/$', 'PasaTurnos.views.GenerarReporteOperario'),
]
