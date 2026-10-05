from customer import CustomerEnquiry
from enquiry_email import EnquiryEmailSender
from enquiry_storage import EnquiryStorage
import logging


logger = logging.getLogger(__name__)


class EnquiryHandler:
    """
    Handles collection and storage of customer project enquiries.
    """

    def __init__(self, email_sender=None):
        self.customer = CustomerEnquiry()

        self.storage = EnquiryStorage()
        self.email_sender = email_sender or EnquiryEmailSender()

        self.current_step = 0

        self.steps = [
            "name",
            "phone",
            "email",
            "service",
            "project_type",
            "location",
            "project_description",
            "budget",
            "timeline"
        ]

    def start(self, service=""):
        """
        Start a new customer enquiry.
        """

        self.customer = CustomerEnquiry(service=service)

        self.current_step = 0

        if service:
            self.steps = [
                "name",
                "phone",
                "email",
                "project_type",
                "location",
                "project_description",
                "budget",
                "timeline"
            ]
            return (
                f"Great — you've selected {service}.\n\n"
                "By continuing, you agree that Azeem Emporium may use these "
                "details to respond to your enquiry.\n\n"
                "First, what is your name?"
            )

        self.steps = [
            "name",
            "phone",
            "email",
            "service",
            "project_type",
            "location",
            "project_description",
            "budget",
            "timeline"
        ]

        return (
            "I'd be happy to help you start a project enquiry. By continuing, "
            "you agree that Azeem Emporium may use these details to respond "
            "to your enquiry.\n\n"
            "First, what is your name?"
        )

    def process_answer(self, answer):
        """
        Store the customer's answer and move
        to the next question.
        """

        answer = answer.strip()

        if not answer:
            return "Please provide an answer."

        field = self.steps[self.current_step]

        setattr(
            self.customer,
            field,
            answer
        )

        self.current_step += 1

        if self.current_step >= len(self.steps):
            return self.finish()

        return self.next_question()

    def next_question(self):
        """
        Return the next question for the customer.
        """

        questions = {
            "name":
                "What is your name?",

            "phone":
                "What is your phone number?",

            "email":
                "What is your email address?",

            "service":
                (
                    "Which service are you interested in?\n\n"
                    "Please choose one of the service buttons above."
                ),

            "project_type":
                "What type of project are you planning?",

            "location":
                "Where is the project located?",

            "project_description":
                "Please describe your project briefly.",

            "budget":
                (
                    "What is your estimated project budget? "
                    "You can say 'I'm not sure' if you don't know yet."
                ),

            "timeline":
                "When would you like the project to start?"
        }

        field = self.steps[self.current_step]

        return questions[field]

    def finish(self):
        """
        Save the completed enquiry and
        return a confirmation message.
        """

        self.storage.save_enquiry(self.customer)
        try:
            delivery = self.email_sender.send(self.customer)
            if not delivery.sent:
                logger.warning("Enquiry email was not sent: %s", delivery.detail)
        except Exception:
            # The enquiry is already safely recorded. A notification fault must
            # never make the customer think their submission was lost.
            logger.exception("Enquiry email delivery failed")

        return (
            "Thank you! Your project enquiry has been recorded.\n\n"
            f"Name: {self.customer.name}\n"
            f"Phone: {self.customer.phone}\n"
            f"Email: {self.customer.email}\n"
            f"Service: {self.customer.service}\n"
            f"Project Type: {self.customer.project_type}\n"
            f"Location: {self.customer.location}\n"
            f"Description: {self.customer.project_description}\n"
            f"Budget: {self.customer.budget}\n"
            f"Timeline: {self.customer.timeline}\n\n"
            "An Azeem Emporium team member can review your "
            "enquiry and follow up with you."
        )

    def is_complete(self):
        """
        Check whether the enquiry is complete.
        """

        return self.customer.is_complete()

    def get_customer(self):
        """
        Return the collected customer information.
        """

        return self.customer
