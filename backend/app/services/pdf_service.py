"""PDF generation service for sanction letters."""
from typing import Dict, Any
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PDFService:
    """Service for generating PDF documents."""
    
    def __init__(self):
        """Initialize PDF service."""
        self.output_dir = os.path.join(settings.UPLOAD_DIR, "sanction_letters")
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_sanction_letter(self, data: Dict[str, Any]) -> str:
        """Generate loan sanction letter PDF."""
        try:
            # Generate filename
            filename = f"sanction_letter_{data['application_number']}.pdf"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create PDF
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Container for elements
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a73e8'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#333333'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            normal_style = styles['Normal']
            normal_style.fontSize = 11
            
            # Header
            elements.append(Paragraph("LoaniFi", title_style))
            elements.append(Paragraph("Personal Loan Sanction Letter", heading_style))
            elements.append(Spacer(1, 0.3 * inch))
            
            # Letter details
            letter_info = [
                f"Sanction Letter No: <b>{data['application_number']}</b>",
                f"Date: <b>{data['sanction_date']}</b>",
            ]
            for info in letter_info:
                elements.append(Paragraph(info, normal_style))
                elements.append(Spacer(1, 0.1 * inch))
            
            elements.append(Spacer(1, 0.2 * inch))
            
            # Customer details
            elements.append(Paragraph("Dear <b>" + data['customer_name'] + "</b>,", normal_style))
            elements.append(Spacer(1, 0.2 * inch))
            
            # Congratulations message
            congrats_text = """We are pleased to inform you that your loan application has been <b>approved</b>. 
            Please find the loan details below:"""
            elements.append(Paragraph(congrats_text, normal_style))
            elements.append(Spacer(1, 0.3 * inch))
            
            # Loan details table
            loan_details = [
                ['Loan Details', ''],
                ['Sanctioned Loan Amount', f"₹{data['loan_amount']:,.2f}"],
                ['Interest Rate (Per Annum)', f"{data['interest_rate']}%"],
                ['Loan Tenure', f"{data['tenure_months']} months"],
                ['Monthly EMI', f"₹{data['monthly_emi']:,.2f}"],
                ['Processing Fee (2% + GST)', f"₹{data['loan_amount'] * 0.02 * 1.18:,.2f}"],
            ]
            
            # Calculate total amounts
            total_interest = (data['monthly_emi'] * data['tenure_months']) - data['loan_amount']
            total_payable = data['loan_amount'] + total_interest
            
            loan_details.append(['Total Interest Payable', f"₹{total_interest:,.2f}"])
            loan_details.append(['Total Amount Payable', f"₹{total_payable:,.2f}"])
            
            table = Table(loan_details, colWidths=[3.5 * inch, 2.5 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Terms and conditions
            elements.append(Paragraph("<b>Terms and Conditions:</b>", heading_style))
            
            terms = [
                "1. The loan will be disbursed to your registered bank account within 24-48 hours of acceptance.",
                "2. EMI will be auto-debited on the same date every month.",
                "3. Late payment charges of ₹500 per day will apply after the due date.",
                "4. Prepayment is allowed after 6 months with 2% prepayment charges.",
                "5. Foreclosure is allowed after 12 months with 4% foreclosure charges.",
                "6. This sanction is valid for 30 days from the date of issue.",
                "7. Loan disbursal is subject to verification of all submitted documents.",
            ]
            
            for term in terms:
                elements.append(Paragraph(term, normal_style))
                elements.append(Spacer(1, 0.05 * inch))
            
            elements.append(Spacer(1, 0.3 * inch))
            
            # Important notes
            elements.append(Paragraph("<b>Important Information:</b>", heading_style))
            important_notes = """Annual Percentage Rate (APR): {apr}%<br/>
            <br/>
            For any queries, please contact our customer support at support@loanifi.com or call 1800-XXX-XXXX.<br/>
            <br/>
            We look forward to serving you!""".format(
                apr=data['interest_rate']
            )
            elements.append(Paragraph(important_notes, normal_style))
            
            elements.append(Spacer(1, 0.5 * inch))
            
            # Signature
            signature_text = """<br/>
            <b>Authorized Signatory</b><br/>
            LoaniFi Financial Services<br/>
            Date: {date}""".format(date=data['sanction_date'])
            
            sig_style = ParagraphStyle(
                'Signature',
                parent=normal_style,
                alignment=TA_RIGHT
            )
            elements.append(Paragraph(signature_text, sig_style))
            
            # Build PDF
            doc.build(elements)
            
            logger.info(
                "sanction_letter_generated",
                application_number=data['application_number'],
                filepath=filepath
            )
            
            return filepath
            
        except Exception as e:
            logger.error("pdf_generation_error", error=str(e))
            raise


# Global PDF service instance
pdf_service = PDFService()


