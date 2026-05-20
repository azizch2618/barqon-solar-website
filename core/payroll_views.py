from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os
from django.conf import settings
from .models import StaffProfile, CompanyProfile, Payroll

def generate_payroll_slip_pdf(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    staff = payroll.staff
    company = CompanyProfile.objects.first()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="salary_slip_{payroll.month_year.strftime("%b_%Y")}_{staff.name.replace(" ", "_").lower()}.pdf"'
    
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
        
        # Build address string properly
        address_parts = []
        if company.address: address_parts.append(company.address)
        if not address_parts: address_parts.append("Solar Engineering & Solutions")
        
        header_data.append([img, [
            Paragraph(f"{company.company_name}", header_name_style),
            Spacer(1, 2),
            Paragraph(f"<font size=10 color='#475569'><b>{', '.join(address_parts)}</b></font>", styles['Normal']),
            Paragraph(f"<font size=9 color='#64748b'>Contact: {company.phone or '+92 300 0000000'} | Email: {company.email or 'info@barqon.pk'}</font>", styles['Normal'])
        ]])
    else:
        header_data.append(["", [
            Paragraph(f"<b>{company.company_name}</b>", header_style),
            Paragraph(company.address or "Solar Engineering & Solutions", styles['Normal'])
        ]])
        
    header_table = Table(header_data, colWidths=[1.2*inch, 6.0*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (1,0), (1,0), 10),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(header_table)
    
    # Premium Double Line Separator
    elements.append(Spacer(1, 10))
    line_table = Table([[""]], colWidths=[7.2*inch])
    line_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 3, colors.HexColor("#3b82f6")), # Thicker main line
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 5))
    line_table_sub = Table([[""]], colWidths=[7.2*inch])
    line_table_sub.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor("#94a3b8")), # Thin subtle line
    ]))
    elements.append(line_table_sub)
    elements.append(Spacer(1, 20))
    
    # Title Section - Centered and Boxed
    title_data = [
        [Paragraph("OFFICIAL SALARY SLIP", ParagraphStyle('SlipTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#1e293b"), alignment=1))]
    ]
    title_table = Table(title_data, colWidths=[7.2*inch])
    title_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(title_table)
    elements.append(Spacer(1, 20))

    # --- PERIOD INFO ---
    period_data = [
        [Paragraph(f"Payroll Period: <b>{payroll.month_year.strftime('%B %Y')}</b>", ParagraphStyle('Left', parent=styles['Normal'])),
         Paragraph(f"Voucher ID: <b>SLP-{payroll.id:05d}</b>", ParagraphStyle('Right', parent=styles['Normal'], alignment=2))]
    ]
    period_table = Table(period_data, colWidths=[3.6*inch, 3.6*inch])
    elements.append(period_table)
    elements.append(Spacer(1, 10))
    
    # --- EMPLOYEE & BANK INFO ---
    info_data = [
        [Paragraph("EMPLOYEE INFORMATION", ParagraphStyle('Section', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', textColor=colors.white)), 
         Paragraph("PAYMENT DESTINATION", ParagraphStyle('Section', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', textColor=colors.white))],
        
        [[Paragraph("Employee ID:", label_style), Paragraph(f"BQ-{staff.id:04d}", value_style),
          Paragraph("Full Name:", label_style), Paragraph(staff.name, value_style),
          Paragraph("Designation:", label_style), Paragraph(staff.get_role_display(), value_style),
          Paragraph("CNIC / ID:", label_style), Paragraph(staff.cnic or "N/A", value_style)],
         
         [Paragraph("Bank Name:", label_style), Paragraph(staff.get_bank_name_display() if staff.bank_name else "N/A", value_style),
          Paragraph("Account Title:", label_style), Paragraph(staff.account_title or "N/A", value_style),
          Paragraph("Account / IBAN:", label_style), Paragraph(staff.account_number or "N/A", value_style),
          Paragraph("Status:", label_style), Paragraph(payroll.get_status_display(), value_style)]]
    ]
    
    info_table = Table(info_data, colWidths=[3.6*inch, 3.6*inch])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")), # Slate header
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 30))
    
    # --- SALARY BREAKDOWN TABLE ---
    earnings_data = [
        [Paragraph("EARNINGS & ADJUSTMENTS", ParagraphStyle('White', parent=styles['Normal'], textColor=colors.white, fontName='Helvetica-Bold')), 
         Paragraph("AMOUNT (PKR)", ParagraphStyle('WhiteRight', parent=styles['Normal'], textColor=colors.white, fontName='Helvetica-Bold', alignment=2))],
        
        ["Basic Monthly Salary", f"{payroll.basic_salary:,.2f}"],
        ["Performance Commissions", f"{payroll.commissions:,.2f}"],
        ["Special Bonuses / Incentives", f"{payroll.bonus:,.2f}"],
        [Paragraph("Deductions (Advance/Tax/Loan)", ParagraphStyle('Deduct', parent=styles['Normal'], textColor=colors.HexColor("#ef4444"))), 
         Paragraph(f"- {payroll.deductions:,.2f}", ParagraphStyle('DeductRight', parent=styles['Normal'], textColor=colors.HexColor("#ef4444"), alignment=2))],
        
        [Paragraph("NET PAYABLE AMOUNT", ParagraphStyle('Total', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.white)), 
         Paragraph(f"PKR {payroll.total_amount:,.2f}", ParagraphStyle('TotalRight', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.white, alignment=2))]
    ]
    
    e_table = Table(earnings_data, colWidths=[5.2*inch, 2.0*inch])
    e_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")), # Dark slate
        ('GRID', (0,1), (-1,-2), 0.5, colors.HexColor("#e2e8f0")),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#10b981")), # Vibrant emerald
        ('TOPPADDING', (0,-1), (-1,-1), 15),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 15),
    ]))
    elements.append(e_table)
    elements.append(Spacer(1, 60))
    
    # Notes Section
    if payroll.notes:
        elements.append(Paragraph("OFFICIAL REMARKS:", label_style))
        elements.append(Paragraph(payroll.notes, ParagraphStyle('Italic', parent=styles['Italic'], textColor=colors.HexColor("#475569"))))
        elements.append(Spacer(1, 50))
    
    # --- FOOTER SIGNATURES ---
    elements.append(Spacer(1, 40))
    sig_data = [
        [Paragraph("<b>Prepared By</b>", ParagraphStyle('Sig', parent=styles['Normal'], alignment=1, fontSize=9)),
         Paragraph("<b>Employee Signature</b>", ParagraphStyle('Sig', parent=styles['Normal'], alignment=1, fontSize=9)), 
         Paragraph("<b>Authorized Approval</b>", ParagraphStyle('Sig', parent=styles['Normal'], alignment=1, fontSize=9))],
        [Paragraph(f"<font size=8 color='#64748b'>System Generated</font>", ParagraphStyle('SigDate', parent=label_style, alignment=1)),
         Paragraph(f"<font size=8 color='#64748b'>{staff.name}</font>", ParagraphStyle('SigDate', parent=label_style, alignment=1)),
         Paragraph(f"<font size=8 color='#64748b'>Official Stamp Area</font>", ParagraphStyle('SigSub', parent=styles['Normal'], alignment=1))]
    ]
    sig_table = Table(sig_data, colWidths=[2.4*inch, 2.4*inch, 2.4*inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEABOVE', (0,0), (0,0), 0.75, colors.black), 
        ('LINEABOVE', (1,0), (1,0), 0.75, colors.black), 
        ('LINEABOVE', (2,0), (2,0), 0.75, colors.black), 
        ('TOPPADDING', (0,0), (-1,0), 8),
        ('BOTTOMPADDING', (0,1), (-1,1), 20),
    ]))
    elements.append(sig_table)
    
    # Final Footer Line
    elements.append(Spacer(1, 1.2*inch))
    elements.append(Paragraph("<hr color='#cbd5e1'/>", styles['Normal']))
    elements.append(Paragraph("<font size=8 color='#64748b'>Certified computer-generated document. For official BARQON Solar Solutions payroll records only.</font>", ParagraphStyle('Foot', alignment=1)))
    
    doc.build(elements)
    return response
