import json

from config import (
    COMPANY_INFO_FILE,
    SERVICES_FILE,
    FAQ_FILE
)


class KnowledgeBase:
    """
    Loads and provides access to the chatbot's
    company information, services and FAQs.
    """

    def __init__(self):
        self.company_info = {}
        self.services = []
        self.faqs = []

        self.load_data()

    def load_json(self, file_path):
        """
        Load a JSON file and return its contents.
        """

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def load_data(self):
        """
        Load all chatbot data files.
        """

        company_data = self.load_json(
            COMPANY_INFO_FILE
        )

        services_data = self.load_json(
            SERVICES_FILE
        )

        faq_data = self.load_json(
            FAQ_FILE
        )

        self.company_info = company_data

        self.services = services_data.get(
            "services",
            []
        )

        self.faqs = faq_data.get(
            "faqs",
            []
        )

    def get_company_info(self):
        """
        Return company information.
        """

        return self.company_info

    def get_services(self):
        """
        Return all available services.
        """

        return self.services

    def get_faqs(self):
        """
        Return all FAQs.
        """

        return self.faqs

    def find_service(self, service_id):
        """
        Find a service using its ID.
        """

        for service in self.services:
            if service.get("id") == service_id:
                return service

        return None

    def find_faq(self, faq_id):
        """
        Find an FAQ using its ID.
        """

        for faq in self.faqs:
            if faq.get("id") == faq_id:
                return faq

        return None