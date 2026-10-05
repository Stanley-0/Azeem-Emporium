import re


class Matcher:
    """
    Matches customer messages with FAQs and services.
    """

    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def normalize_text(self, text):
        """
        Convert text to a simple format for matching.
        """

        text = text.lower()

        # Remove punctuation
        text = re.sub(r"[^\w\s]", "", text)

        # Remove extra spaces
        text = " ".join(text.split())

        return text

    def calculate_score(self, message, keywords):
        """
        Calculate how well a message matches a list of keywords.
        """

        score = 0

        for keyword in keywords:

            keyword = self.normalize_text(keyword)

            if keyword in message:
                # Longer keywords are generally more specific.
                score += len(keyword.split())

        return score

    def find_best_faq(self, message):
        """
        Find the FAQ that best matches the customer's message.
        """

        message = self.normalize_text(message)

        best_faq = None
        best_score = 0

        for faq in self.knowledge_base.get_faqs():

            questions = faq.get("questions", [])

            score = self.calculate_score(
                message,
                questions
            )

            if score > best_score:
                best_score = score
                best_faq = faq

        if best_faq is None:
            return None

        return {
            "type": "faq",
            "id": best_faq.get("id"),
            "answer": best_faq.get("answer"),
            "score": best_score
        }

    def find_best_service(self, message):
        """
        Find the service that best matches the customer's message.
        """

        message = self.normalize_text(message)

        best_service = None
        best_score = 0

        for service in self.knowledge_base.get_services():

            keywords = service.get("keywords", [])

            score = self.calculate_score(
                message,
                keywords
            )

            if score > best_score:
                best_score = score
                best_service = service

        if best_service is None:
            return None

        return {
            "type": "service",
            "id": best_service.get("id"),
            "name": best_service.get("name"),
            "description": best_service.get("description"),
            "score": best_score
        }

    def find_match(self, message):
        """
        Find the best overall match between FAQs and services.
        """

        faq_match = self.find_best_faq(message)

        service_match = self.find_best_service(message)

        faq_score = (
            faq_match["score"]
            if faq_match
            else 0
        )

        service_score = (
            service_match["score"]
            if service_match
            else 0
        )

        if faq_score == 0 and service_score == 0:
            return None

        if faq_score >= service_score:
            return faq_match

        return service_match