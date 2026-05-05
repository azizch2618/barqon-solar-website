from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from io import BytesIO
from datetime import date
from xhtml2pdf import pisa
from decimal import Decimal

def generate_proposal_pdf(proposal):
    """
    Generates an ULTRA PREMIUM Tesla/Apple-style PDF quotation.
    Uses HTML/CSS with xhtml2pdf for high-fidelity design.
    """
    lead = proposal.lead
    calc = getattr(lead, 'calculation', None)
    if not calc: return None

    # --- Data Preparation ---
    total_cost = float(calc.total_cost)
    system_size = float(calc.system_size_kw)
    panel_count = int(calc.panel_count)
    
    # Financial Breakdown Calculation (Tesla-style grouping)
    equipment_cost = total_cost * 0.70
    structure_cost = total_cost * 0.15
    installation_cost = total_cost * 0.15
    
    # Itemized Breakdown for Page 2
    items = [
        {"label": "Solar PV Modules", "specs": "Tier-1 550W+ Bifacial", "qty": panel_count, "total": total_cost * 0.45},
        {"label": "Smart Hybrid Inverter", "specs": f"{system_size}kW High Efficiency", "qty": 1, "total": total_cost * 0.25},
        {"label": "Mounting Structure", "specs": "Reinforced Galvanized Iron", "qty": 1, "total": total_cost * 0.10},
        {"label": "AC/DC Cabling", "specs": "99.9% Pure Copper Solar Cables", "qty": 1, "total": total_cost * 0.08},
        {"label": "Switchgear & Protection", "specs": "DC/AC Breakers & SPDs", "qty": 1, "total": total_cost * 0.07},
        {"label": "Installation & Service", "specs": "Engineering & Commissioning", "qty": 1, "total": total_cost * 0.05},
    ]

    context = {
        'lead': lead,
        'calculation': calc,
        'today': date.today(),
        'equipment_cost': equipment_cost,
        'structure_cost': structure_cost,
        'installation_cost': installation_cost,
        'items': items,
    }

    # Render HTML
    html_content = render_to_string('automation/proposal_pdf.html', context)
    
    # Convert to PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)
    
    if not pdf.err:
        pdf_content = result.getvalue()
        filename = f"BARQON_Premium_Quotation_{lead.id:04d}.pdf"
        proposal.pdf_file.save(filename, ContentFile(pdf_content))
        proposal.status = 'final'
        proposal.save()
        return proposal.pdf_file.url
    
    return None
