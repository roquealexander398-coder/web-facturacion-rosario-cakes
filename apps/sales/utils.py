from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from ..company.models import CompanyConfig


def generate_invoice_pdf(sale):
    """Generar PDF de factura."""
    company = CompanyConfig.get_config()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=24,
    ))

    story = []
    story.append(Paragraph('FACTURA', styles['CustomTitle']))
    story.append(Spacer(1, 0.25 * inch))

    company_info = [
        f'Empresa: {company.company_name}',
        f'RNC: {company.rnc}',
        f'Tel: +1 (849) 785-4475',
        f'Email: {company.email}',
        f'Dirección: {company.address}',
    ]
    for info in company_info:
        story.append(Paragraph(info, styles['Normal']))
    story.append(Spacer(1, 0.25 * inch))

    factura_info = [
        f'Número: {sale.invoice_number}',
        f'Fecha: {sale.date.strftime("%d/%m/%Y %H:%M")}',
        f'Cliente: {sale.client.name}',
        f'Identificación: {sale.client.identification}',
    ]
    for info in factura_info:
        story.append(Paragraph(info, styles['Normal']))
    story.append(Spacer(1, 0.25 * inch))

    data = [['Cant.', 'Producto', 'Precio Unit.', 'Descuento', 'Total']]
    for detail in sale.details.all():
        data.append([
            str(detail.quantity),
            detail.product.name,
            f'{company.currency_symbol} {detail.price:,.2f}',
            f'{company.currency_symbol} {detail.discount:,.2f}',
            f'{company.currency_symbol} {detail.total:,.2f}',
        ])

    def format_amount(value):
        return f"{company.currency_symbol} {value:,.2f}"

    data.append(['', '', '', 'Subtotal:', format_amount(sale.subtotal)])
    data.append(['', '', '', 'Descuento:', format_amount(sale.discount)])
    data.append(['', '', '', f'ITBIS ({sale.tax_rate}%):', format_amount(sale.tax)])
    data.append(['', '', '', 'TOTAL:', format_amount(sale.total)])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -5), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
    ]))

    story.append(table)
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph('¡Gracias por su compra!', styles['Heading2']))
    story.append(Paragraph(f'Estado: {sale.get_status_display()}', styles['Normal']))

    doc.build(story)
    return buffer.getvalue()
