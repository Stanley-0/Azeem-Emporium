from config import (
    WELCOME_MESSAGE,
    FALLBACK_MESSAGE,
    GOODBYE_MESSAGE,
    PROJECT_ENQUIRY_MESSAGE
)

from knowledge_base import KnowledgeBase
from matcher import Matcher
from enquiry import EnquiryHandler


class Chatbot:
    """
    Main Azeem Emporium customer chatbot.
    """

    def __init__(self):
        self.knowledge_base = KnowledgeBase()

        self.matcher = Matcher(
            self.knowledge_base
        )

        self.enquiry_handler = EnquiryHandler()

        self.enquiry_active = False
        self.running = True

    def get_welcome_message(self):
        """
        Return the chatbot welcome message.
        """

        return WELCOME_MESSAGE

    def process_message(self, message, selected_service=""):
        """
        Process a customer's message.
        """

        message = message.strip()

        if not message:
            return "Please enter a message so I can help you."

        # If an enquiry is currently active,
        # send the answer to the enquiry handler.
        if self.enquiry_active:

            response = self.enquiry_handler.process_answer(
                message
            )

            if self.enquiry_handler.current_step >= len(
                self.enquiry_handler.steps
            ):
                self.enquiry_active = False

            return response

        # Check for goodbye messages.
        if self.is_goodbye(message):
            self.running = False
            return GOODBYE_MESSAGE

        # A service selected in the site chat begins an enquiry with that
        # service already recorded, so the next question can be the visitor's
        # name rather than asking them to repeat their selection.
        if selected_service:
            self.enquiry_active = True
            return self.enquiry_handler.start(selected_service)

        # Check whether the customer wants
        # to start a project enquiry.
        if self.is_enquiry_request(message):

            self.enquiry_active = True

            return self.enquiry_handler.start()

        # Search the knowledge base.
        match = self.matcher.find_match(message)

        # A typed request that matches one of our services should begin the
        # same guided enquiry as a service chosen from the chat buttons.
        # This captures the visitor's contact and project details while the
        # selected service is still clear.
        service_match = self.matcher.find_best_service(message)
        if service_match:
            self.enquiry_active = True
            return self.enquiry_handler.start(service_match["name"])

        if match is None:
            return FALLBACK_MESSAGE

        return self.format_response(match)

    def is_goodbye(self, message):
        """
        Check whether the customer wants
        to end the conversation.
        """

        goodbye_words = [
            "bye",
            "goodbye",
            "good bye",
            "see you",
            "thanks bye",
            "thank you bye"
        ]

        message = message.lower().strip()

        return any(
            word in message
            for word in goodbye_words
        )

    def is_enquiry_request(self, message):
        """
        Detect whether the customer wants
        a quotation, consultation or project enquiry.
        """

        enquiry_keywords = [
            "quotation",
            "quote",
            "estimate",
            "project estimate",
            "construction estimate",
            "project enquiry",
            "project inquiry",
            "consultation",
            "book a consultation",
            "speak to someone",
            "talk to someone",
            "start a project",
            "i want to build",
            "i want to construct",
            "building project"
        ]

        message = message.lower().strip()

        return any(
            keyword in message
            for keyword in enquiry_keywords
        )

    def format_response(self, match):
        """
        Convert a matcher result into a
        customer-friendly response.
        """

        if match["type"] == "faq":
            return match["answer"]

        if match["type"] == "service":

            return (
                f"{match['name']}\n\n"
                f"{match['description']}"
            )

        return FALLBACK_MESSAGE
