from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os
from django.conf import settings
from .models import CompanyProfile, ProjectFinancials

def generate_project_report_pdf(request, project_financial_id):
    financials = get_object_or_404(ProjectFinancials, id=project_financial_id)
    company = CompanyProfile.objects.first()
    
    response = HttpResponse(content_type='application/pdf')
    filename = f"Project_Report_{financials.owner_name.replace(' ', '_')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    
    styles = getSampleStyleSheet()
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    
    # Custom Styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor("#0f172a"),
        fontName='Helvetica-Bold'
    )
    
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor("#64748b"),
        fontName='Helvetica'
    )
    
    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#0f172a"),
        fontName='Helvetica-Bold'
    )
    
    elements = []
    
    # --- HEADER SECTION ---
    header_data = []
    if os.path.exists(logo_path):
        img = Image(logo_path, width=1.0*inch, height=1.0*inch)
        header_name_style = ParagraphStyle(
            'HeaderName',
            parent=header_style,
            fontSize=24,
            leading=30,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor("#1e293b")
        )
        header_data.append([img, [
            Paragraph(f"{company.company_name}", header_name_style),
            Spacer(1, 2),
            Paragraph(f"<font size=10 color='#475569'><b>{company.address or 'Solar Solutions'}</b></font>", styles['Normal']),
            Paragraph(f"<font size=9 color='#64748b'>Contact: {company.phone} | Email: {company.email}</font>", styles['Normal'])
        ]])
    else:
        header_data.append(["", [
            Paragraph(f"<b>{company.company_name}</b>", header_style),
            Paragraph(company.address or "Solar Solutions", styles['Normal'])
        ]])
        
    header_table = Table(header_data, colWidths=[1.2*inch, 6.0*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (1,0), (1,0), 10),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))
    
    # Title
    title_data = [[Paragraph("PROJECT COMPLETION & FINANCIAL REPORT", ParagraphStyle('SlipTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.white, alignment=1))]]
    title_table = Table(title_data, colWidths=[7.2*inch])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1e293b")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(title_table)
    elements.append(Spacer(1, 20))

    # --- PROJECT INFO ---
    info_data = [
        [Paragraph("PROJECT OWNER", ParagraphStyle('Section', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', textColor=colors.white)), 
         Paragraph("PROJECT DETAILS", ParagraphStyle('Section', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', textColor=colors.white))],
        [[Paragraph("Owner Name:", label_style), Paragraph(financials.owner_name, value_style),
          Paragraph("Completion Date:", label_style), Paragraph(financials.created_at.strftime("%d %B, %Y"), value_style)],
         [Paragraph("Project Title:", label_style), Paragraph(financials.project.title if financials.project else "N/A", value_style),
          Paragraph("Location:", label_style), Paragraph(financials.project.location if financials.project else "N/A", value_style),
          Paragraph("System Size:", label_style), Paragraph(f"{financials.project.system_size_kw if financials.project else 'N/A'} kW", value_style)]]
    ]
    info_table = Table(info_data, colWidths=[3.6*inch, 3.6*inch])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # --- RELEVANT DETAILS / NOTES ---
    if financials.details:
        elements.append(Paragraph("PROJECT REMARKS / NOTES", ParagraphStyle('NotesHeader', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', textColor=colors.HexColor("#1e293b"))))
        elements.append(Spacer(1, 5))
        elements.append(Paragraph(financials.details, ParagraphStyle('Notes', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor("#475569"), leading=12)))
        elements.append(Spacer(1, 20))

    # --- ITEMS BREAKDOWN ---
    items_header = [
        [Paragraph("Item / Description", ParagraphStyle('White', parent=styles['Normal'], textColor=colors.white, fontName='Helvetica-Bold')), 
         Paragraph("Qty", ParagraphStyle('White', parent=styles['Normal'], textColor=colors.white, fontName='Helvetica-Bold', alignment=1)),
         Paragraph("Market Cost", ParagraphStyle('White', parent=styles['Normal'], textColor=colors.white, fontName='Helvetica-Bold', alignment=1)),
         Paragraph("Selling Price", ParagraphStyle('White', parent=styles['Normal'], textColor=colors.white, fontName='Helvetica-Bold', alignment=1)),
         Paragraph("Total (Selling)", ParagraphStyle('White', parent=styles['Normal'], textColor=colors.white, fontName='Helvetica-Bold', alignment=1))]
    ]
    
    items_data = []
    for item in financials.items:
        qty = float(item.get('qty', 0))
        cost = float(item.get('cost', 0))
        price = float(item.get('price', 0))
        items_data.append([
            Paragraph(f"<b>{item.get('name', 'N/A')}</b><br/><font size=8 color='#64748b'>{item.get('description', '')}</font>", styles['Normal']),
            f"{qty}",
            f"{cost:,.2f}",
            f"{price:,.2f}",
            f"{(qty * price):,.2f}"
        ])
    
    # Add empty rows if needed to maintain structure
    if not items_data:
        items_data.append(["No items recorded", "", "", "", ""])

    items_table = Table(items_header + items_data, colWidths=[3.0*inch, 0.6*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#475569")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))

    # --- FINANCIAL SUMMARY ---
    summary_data = [
        [Paragraph("FINANCIAL SUMMARY", ParagraphStyle('Summary', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#1e293b"))), ""],
        ["Total Investment (Market Value):", f"PKR {financials.total_cost:,.2f}"],
        ["Total Revenue (Selling Amount):", f"PKR {financials.total_revenue:,.2f}"],
        [Paragraph("NET PROFIT / LOSS", ParagraphStyle('Total', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.white)), 
         Paragraph(f"PKR {financials.profit_loss:,.2f}", ParagraphStyle('TotalRight', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.white, alignment=2))]
    ]
    
    summary_table = Table(summary_data, colWidths=[5.2*inch, 2.0*inch])
    summary_table.setStyle(TableStyle([
        ('SPAN', (0,0), (1,0)),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('PADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,1), (-1,-2), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#10b981") if financials.profit_loss >= 0 else colors.HexColor("#ef4444")),
    ]))
    elements.append(summary_table)
    
    # Footer
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("<hr color='#cbd5e1'/>", styles['Normal']))
    elements.append(Paragraph(f"<font size=8 color='#64748b'>Report Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | BARQON Solar Solutions Official Document</font>", ParagraphStyle('Foot', alignment=1)))
    
    doc.build(elements)
    return response
