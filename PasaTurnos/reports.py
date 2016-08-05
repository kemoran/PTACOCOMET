# -*- encoding: utf-8 -*-
import os
RUTA = os.path.dirname(os.path.abspath(__file__))

#from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from geraldo import Report, ReportBand, Label, ObjectValue, SystemField, BAND_WIDTH, landscape, Image

class rpTicket(Report):
	title = 'ACOCOMET de R.L.'
	author = 'ACOCOMET de R.L.'
	page_size = 7.8*cm,5.5*cm
	margin_left = 0.5*cm
	margin_top = 0.5*cm
	margin_right = 0.5*cm
	margin_bottom = 0.5*cm

	# Cabecera del reporte
	class band_page_header(ReportBand):
		height = 1.3*cm
		elements = [
			Image(
				top=0.1*cm, left=0, width=2.0*cm, height=2.0*cm,
				filename=os.path.join(RUTA, '../PTACOCOMET/static/SysWeb/ACOCOMET-rpthumbnail.PNG'),
				),
			SystemField(expression='%(report_title)s', top=0.1*cm, left=0, width=BAND_WIDTH,
				style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_CENTER}
				),
			Label(text='Cooperatíva Financiera Única', top=0.8*cm, left=0, width=BAND_WIDTH,
				style={'fontName': 'Helvetica-Bold', 'fontSize': 10, 'alignment': TA_CENTER}
				),
		]
		borders = {'bottom': True}

	# Cuerpo del reporte
	class band_detail(ReportBand):
		elements = [
			Label(text='¡Gracias por visitarnos!', top=0.4*cm, left=0, width=BAND_WIDTH,
				style={'fontName': 'Helvetica-Bold', 'fontSize': 9, 'alignment': TA_CENTER}
				),
			ObjectValue(attribute_name='nombre', top=1.0*cm, left=0, width=BAND_WIDTH,
				style={'fontName': 'Helvetica-Bold', 'fontSize': 9, 'alignment': TA_CENTER}
				),
			Label(text='Su turno de espera es:', top=1.6*cm, left=0, width=BAND_WIDTH,
				style={'fontName': 'Helvetica-Bold', 'fontSize': 9, 'alignment': TA_CENTER}
				),
			ObjectValue(attribute_name='numero_ticket', top=2.3*cm, left=0, width=BAND_WIDTH,
				style={'fontName': 'Helvetica-Bold', 'fontSize': 18, 'alignment': TA_CENTER}
				),
		]


"""
class rpGraficoAtenciones(Report):
	title = 'Reporte grafico de atenciones en servicios'

	class band_summary(ReportBand):
		height = 5*cm
		elements = [
			Image(filename=os.path.join(RUTA, 'output/matplotlib.png'), left=11*cm, top=0.2*cm)
		]
"""