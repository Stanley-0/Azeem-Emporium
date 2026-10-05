from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class CustomerEnquiry:
    """
    Stores information provided by a customer
    about a project or service enquiry.
    """

    name: str = ""
    phone: str = ""
    email: str = ""

    service: str = ""
    project_type: str = ""
    location: str = ""

    project_description: str = ""

    budget: str = ""
    timeline: str = ""

    created_at: str = ""

    def __post_init__(self):
        """
        Automatically record when the enquiry was created.
        """

        if not self.created_at:
            self.created_at = datetime.now().isoformat(
                timespec="seconds"
            )

    def to_dict(self):
        """
        Convert the customer enquiry into a dictionary.
        """

        return asdict(self)

    def is_complete(self):
        """
        Check whether the important customer information
        has been provided.
        """

        required_fields = [
            self.name,
            self.phone,
            self.service,
            self.location,
            self.project_description
        ]

        return all(
            field.strip()
            for field in required_fields
        )