from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy.orm import Session

from app.services.reporte_service import ReporteService


class ReportePdfService:
    azul = colors.HexColor("#2563EB")
    azul_oscuro = colors.HexColor("#172554")
    gris = colors.HexColor("#64748B")
    gris_claro = colors.HexColor("#F1F5F9")
    borde = colors.HexColor("#CBD5E1")

    def __init__(self, db: Session):
        self.reportes = ReporteService(db)

    def generar(self) -> bytes:
        resumen = self.reportes.resumen()
        pagos = self.reportes.pagos_por_periodo()
        asistencias = self.reportes.asistencias_por_empleado()
        buffer = BytesIO()
        documento = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=28 * mm,
            bottomMargin=20 * mm,
            title="Reporte general de Staffy",
            author="Staffy",
        )
        estilos = self._estilos()
        contenido = [
            Paragraph("Reporte general", estilos["titulo"]),
            Paragraph(
                f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}",
                estilos["subtitulo"],
            ),
            Spacer(1, 7 * mm),
            self._tabla_resumen(resumen, estilos),
            Spacer(1, 9 * mm),
            Paragraph("Pagos por periodo", estilos["seccion"]),
            Spacer(1, 3 * mm),
            self._tabla_pagos(pagos, estilos),
            Spacer(1, 9 * mm),
            Paragraph("Asistencias por empleado", estilos["seccion"]),
            Spacer(1, 3 * mm),
            self._tabla_asistencias(asistencias, estilos),
        ]
        documento.build(contenido, onFirstPage=self._encabezado_pie, onLaterPages=self._encabezado_pie)
        return buffer.getvalue()

    def _estilos(self):
        estilos = getSampleStyleSheet()
        estilos.add(
            ParagraphStyle(
                name="TituloStaffy",
                parent=estilos["Title"],
                fontName="Helvetica-Bold",
                fontSize=22,
                leading=27,
                textColor=self.azul_oscuro,
                alignment=0,
                spaceAfter=2 * mm,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="SubtituloStaffy",
                parent=estilos["Normal"],
                fontName="Helvetica",
                fontSize=9,
                leading=12,
                textColor=self.gris,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="SeccionStaffy",
                parent=estilos["Heading2"],
                fontName="Helvetica-Bold",
                fontSize=13,
                leading=17,
                textColor=self.azul_oscuro,
                spaceAfter=0,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="CeldaStaffy",
                parent=estilos["Normal"],
                fontName="Helvetica",
                fontSize=8.5,
                leading=11,
                textColor=colors.HexColor("#334155"),
            )
        )
        estilos.add(
            ParagraphStyle(
                name="CeldaDerechaStaffy",
                parent=estilos["CeldaStaffy"],
                alignment=TA_RIGHT,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="IndicadorEtiquetaStaffy",
                parent=estilos["Normal"],
                fontName="Helvetica",
                fontSize=7.5,
                leading=10,
                textColor=self.gris,
                alignment=TA_CENTER,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="IndicadorValorStaffy",
                parent=estilos["Normal"],
                fontName="Helvetica-Bold",
                fontSize=13,
                leading=17,
                textColor=self.azul_oscuro,
                alignment=TA_CENTER,
            )
        )
        return {
            "titulo": estilos["TituloStaffy"],
            "subtitulo": estilos["SubtituloStaffy"],
            "seccion": estilos["SeccionStaffy"],
            "celda": estilos["CeldaStaffy"],
            "celda_derecha": estilos["CeldaDerechaStaffy"],
            "indicador_etiqueta": estilos["IndicadorEtiquetaStaffy"],
            "indicador_valor": estilos["IndicadorValorStaffy"],
        }

    def _tabla_resumen(self, resumen: dict, estilos) -> Table:
        indicadores = [
            ("Empleados activos", str(resumen["total_empleados"])),
            ("Pagos calculados", self._moneda(resumen["total_pagos"])),
            ("Tardanzas", str(resumen["total_tardanzas"])),
            ("Faltas", str(resumen["total_faltas"])),
        ]
        datos = [
            [Paragraph(etiqueta, estilos["indicador_etiqueta"]) for etiqueta, _ in indicadores],
            [Paragraph(valor, estilos["indicador_valor"]) for _, valor in indicadores],
        ]
        tabla = Table(datos, colWidths=[43.5 * mm] * 4, rowHeights=[9 * mm, 12 * mm])
        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), self.gris_claro),
                    ("BOX", (0, 0), (-1, -1), 0.6, self.borde),
                    ("INNERGRID", (0, 0), (-1, -1), 0.6, self.borde),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        return tabla

    def _tabla_pagos(self, pagos: list[dict], estilos) -> Table:
        datos = [["Periodo", "Boletas", "Total pagado"]]
        if pagos:
            datos.extend(
                [
                    Paragraph(str(pago["periodo"]), estilos["celda"]),
                    Paragraph(str(pago["cantidad_boletas"]), estilos["celda_derecha"]),
                    Paragraph(self._moneda(pago["total_pagado"]), estilos["celda_derecha"]),
                ]
                for pago in pagos
            )
        else:
            datos.append([Paragraph("No hay pagos registrados.", estilos["celda"]), "", ""])
        tabla = Table(datos, colWidths=[52 * mm, 48 * mm, 74 * mm], repeatRows=1)
        estilo = self._estilo_tabla()
        if not pagos:
            estilo.add("SPAN", (0, 1), (-1, 1))
        tabla.setStyle(estilo)
        return tabla

    def _tabla_asistencias(self, asistencias: list[dict], estilos) -> Table:
        datos = [["Empleado", "Asistio", "Tarde", "Falto"]]
        if asistencias:
            datos.extend(
                [
                    Paragraph(
                        f"<b>{self._texto_seguro(item['empleado_nombre'])}</b><br/>"
                        f"<font color='#64748B'>{self._texto_seguro(item['empleado_codigo'])}</font>",
                        estilos["celda"],
                    ),
                    Paragraph(str(item["asistio"]), estilos["celda_derecha"]),
                    Paragraph(str(item["tarde"]), estilos["celda_derecha"]),
                    Paragraph(str(item["falto"]), estilos["celda_derecha"]),
                ]
                for item in asistencias
            )
        else:
            datos.append([Paragraph("No hay empleados registrados.", estilos["celda"]), "", "", ""])
        tabla = Table(datos, colWidths=[78 * mm, 32 * mm, 32 * mm, 32 * mm], repeatRows=1)
        estilo = self._estilo_tabla()
        if not asistencias:
            estilo.add("SPAN", (0, 1), (-1, 1))
        tabla.setStyle(estilo)
        return tabla

    def _estilo_tabla(self) -> TableStyle:
        return TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), self.azul_oscuro),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, self.gris_claro]),
                ("GRID", (0, 0), (-1, -1), 0.35, self.borde),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ]
        )

    def _encabezado_pie(self, canvas, documento):
        ancho, alto = A4
        canvas.saveState()
        canvas.setFillColor(self.azul)
        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawString(18 * mm, alto - 15 * mm, "STAFFY")
        canvas.setStrokeColor(self.borde)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, alto - 18 * mm, ancho - 18 * mm, alto - 18 * mm)
        canvas.line(18 * mm, 15 * mm, ancho - 18 * mm, 15 * mm)
        canvas.setFillColor(self.gris)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(18 * mm, 10 * mm, "Reporte de recursos humanos")
        canvas.drawRightString(ancho - 18 * mm, 10 * mm, f"Pagina {documento.page}")
        canvas.restoreState()

    @staticmethod
    def _moneda(valor: float) -> str:
        return f"S/ {float(valor):,.2f}"

    @staticmethod
    def _texto_seguro(valor: str) -> str:
        return str(valor).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
