from pathlib import Path


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

COMPANY_INFO_FILE = DATA_DIR / "company_info.json"

SERVICES_FILE = DATA_DIR / "services.json"

FAQ_FILE = DATA_DIR / "faq.json"

# Completed customer enquiries are stored separately from reference data.
ENQUIRIES_FILE = DATA_DIR / "enquiries.json"


# --------------------------------------------------
# CHATBOT SETTINGS
# --------------------------------------------------

BOT_NAME = "Azeem Emporium Assistant"

COMPANY_NAME = "Azeem Emporium Limited"


# --------------------------------------------------
# CHATBOT MESSAGES
# --------------------------------------------------

WELCOME_MESSAGE = """
Welcome to Azeem Emporium Limited! 👋

I'm the Azeem Emporium customer assistant.

I can help you with:

• Construction
• Civil Engineering
• Project Management
• Logistics & Supplies
• Consultancy
• Project enquiries
• Quotations
• Contact information

How can I help you today?
"""


FALLBACK_MESSAGE = """
I'm sorry, I didn't quite understand your question.

I can help you with:

• Construction
• Civil Engineering
• Project Management
• Logistics & Supplies
• Consultancy
• Project quotations
• Booking a consultation
• Contact information

You can also tell me about a construction project you are planning.
"""


GOODBYE_MESSAGE = """
Thank you for contacting Azeem Emporium Limited.

Have a great day! 👋
"""


# --------------------------------------------------
# PROJECT ENQUIRY SETTINGS
# --------------------------------------------------

PROJECT_ENQUIRY_MESSAGE = """
I'd be happy to help you start a project enquiry.

I'll ask you a few questions so we can understand
your project and connect you with the appropriate
Azeem Emporium team member.
"""
