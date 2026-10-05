import json
from pathlib import Path


class EnquiryStorage:
    """
    Saves customer project enquiries to a JSON file.
    """

    def __init__(self):
        self.folder = Path(__file__).resolve().parent / "enquiries"

        self.file = self.folder / "customer_enquiries.json"

        self.create_storage()

    def create_storage(self):
        """
        Create the enquiries folder and JSON file
        if they do not already exist.
        """

        self.folder.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file.exists():

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

    def load_enquiries(self):
        """
        Load existing customer enquiries.
        """

        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save_enquiry(self, customer):
        """
        Save a new customer enquiry.
        """

        enquiries = self.load_enquiries()

        enquiries.append(
            customer.to_dict()
        )

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                enquiries,
                file,
                indent=4
            )

        return True