"""Create and email a PDF summary for completed customer enquiries."""

import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime
from html import escape
from io import BytesIO
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


DEFAULT_RECIPIENTS = (
    "ammar@azeememporium.com",
    "ibra@azeememporium.com",
    "mira@azeememporium.com",
    "info@azeememporium.com",
)
RESEND_EMAILS_URL = "https://api.resend.com/emails"


@dataclass(frozen=True)
class DeliveryResult:
    """Outcome of attempting internal enquiry notification delivery."""

    sent: bool
    detail: str


class EnquiryEmailSender:
    """Send enquiry summaries through Resend when its credentials are configured."""

    def __init__(self, api_key=None, sender=None, recipients=None):
        self.api_key = api_key or os.getenv("RESEND_API_KEY", "")
        self.sender = sender or os.getenv("ENQUIRY_FROM_EMAIL", "")
        self.recipients = recipients or self._configured_recipients()

    @staticmethod
    def _configured_recipients():
        configured = os.getenv("ENQUIRY_RECIPIENTS", "")
        if not configured.strip():
            return DEFAULT_RECIPIENTS
        return tuple(
            address.strip() for address in configured.split(",")
            if address.strip()
        )

    def send(self, enquiry):
        """Email a completed enquiry PDF to the internal Azeem Emporium team."""
        if not self.api_key or not self.sender:
            return DeliveryResult(
                sent=False,
                detail="Email delivery is not configured."
            )

        filename = self._filename(enquiry)
        payload = {
            "from": self.sender,
            "to": list(self.recipients),
            "subject": f"New {enquiry.service} enquiry from {enquiry.name}",
            "html": (
                "<p>A new customer enquiry has been submitted through "
                "azeememporium.com.</p>"
                "<p>The full project brief is attached as a PDF.</p>"
            ),
            "attachments": [{
                "filename": filename,
                "content": base64.b64encode(
                    build_enquiry_pdf(enquiry)
                ).decode("ascii"),
            }],
        }
        request = Request(
            RESEND_EMAILS_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=15) as response:
                if 200 <= response.status < 300:
                    return DeliveryResult(sent=True, detail="Email sent.")
                return DeliveryResult(
                    sent=False,
                    detail=f"Email provider returned HTTP {response.status}."
                )
        except HTTPError as error:
            return DeliveryResult(
                sent=False,
                detail=f"Email provider returned HTTP {error.code}."
            )
        except URLError:
            return DeliveryResult(
                sent=False,
                detail="Could not reach the email provider."
            )

    @staticmethod
    def _filename(enquiry):
        safe_name = "-".join(enquiry.name.lower().split()) or "customer"
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"azeem-enquiry-{safe_name}-{timestamp}.pdf"


def build_enquiry_pdf(enquiry):
    """Return a polished, one-page PDF containing an enquiry's details."""
    document_buffer = BytesIO()
    document = SimpleDocTemplate(
        document_buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "EnquiryTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#093926"),
        fontSize=22,
        leading=26,
        alignment=TA_LEFT,
        spaceAfter=4 * mm,
    )
    heading_style = ParagraphStyle(
        "EnquiryHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#093926"),
        fontSize=12,
        leading=15,
        spaceBefore=4 * mm,
        spaceAfter=2 * mm,
    )
    label_style = ParagraphStyle(
        "EnquiryLabel",
        parent=styles["BodyText"],
        textColor=colors.HexColor("#5B665F"),
        fontSize=8.5,
        leading=11,
    )
    value_style = ParagraphStyle(
        "EnquiryValue",
        parent=styles["BodyText"],
        textColor=colors.HexColor("#17241D"),
        fontSize=10,
        leading=14,
    )

    def text(value):
        return escape(str(value or "Not provided")).replace("\n", "<br/>")

    rows = [
        ("Customer name", enquiry.name),
        ("Phone", enquiry.phone),
        ("Email", enquiry.email),
        ("Service", enquiry.service),
        ("Project type", enquiry.project_type),
        ("Location", enquiry.location),
        ("Estimated budget", enquiry.budget),
        ("Preferred timeline", enquiry.timeline),
    ]
    contact_table = Table(
        [
            [Paragraph(label, label_style), Paragraph(text(value), value_style)]
            for label, value in rows
        ],
        colWidths=[43 * mm, 121 * mm],
        hAlign="LEFT",
    )
    contact_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF3EF")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#D5DED7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))

    story = [
        Paragraph("Azeem Emporium Limited", title_style),
        Paragraph("New customer project enquiry", heading_style),
        Paragraph(
            f"Submitted: {text(enquiry.created_at)}", label_style
        ),
        Spacer(1, 4 * mm),
        contact_table,
        Paragraph("Project description", heading_style),
        Paragraph(text(enquiry.project_description), value_style),
        Spacer(1, 7 * mm),
        Paragraph(
            "Generated automatically from azeememporium.com.", label_style
        ),
    ]
    document.build(story)
    return document_buffer.getvalue()
