import json
import importlib.util
import tempfile
import unittest
from pathlib import Path

from customer import CustomerEnquiry
from enquiry_storage import EnquiryStorage
from enquiry import EnquiryHandler


class EnquiryStorageTests(unittest.TestCase):
    def test_save_enquiry_creates_and_appends_to_json_storage(self):
        with tempfile.TemporaryDirectory() as directory:
            storage = EnquiryStorage(Path(directory) / "enquiries.json")
            storage.save_enquiry(CustomerEnquiry(
                name="Ama", phone="123", service="Construction"
            ))
            storage.save_enquiry(CustomerEnquiry(
                name="Kojo", phone="456", service="Logistics"
            ))

            with storage.file_path.open(encoding="utf-8") as file:
                stored_enquiries = json.load(file)

        self.assertEqual(
            [enquiry["name"] for enquiry in stored_enquiries],
            ["Ama", "Kojo"]
        )
        self.assertEqual(stored_enquiries[0]["service"], "Construction")

    def test_completed_handler_enquiry_is_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            handler = EnquiryHandler()
            storage = EnquiryStorage(Path(directory) / "enquiries.json")
            handler.storage = storage
            handler.start()

            for answer in [
                "Ama", "123", "ama@example.com", "Construction",
                "House", "Accra", "A family home", "100000", "June"
            ]:
                handler.process_answer(answer)

            with storage.file_path.open(encoding="utf-8") as file:
                stored_enquiries = json.load(file)

        self.assertEqual(len(stored_enquiries), 1)
        self.assertEqual(stored_enquiries[0]["name"], "Ama")
        self.assertEqual(stored_enquiries[0]["location"], "Accra")

    @unittest.skipUnless(
        importlib.util.find_spec("flask"),
        "Flask is not installed; run pip install -r requirements.txt"
    )
    def test_api_keeps_an_enquiry_in_its_session_and_saves_it(self):
        import api

        with tempfile.TemporaryDirectory() as directory:
            api.chatbots.clear()
            client = api.app.test_client()
            first_response = client.post("/chat", json={
                "message": "I want to start a project"
            })
            session_id = first_response.get_json()["session_id"]
            bot = api.chatbots[session_id]
            storage = EnquiryStorage(Path(directory) / "enquiries.json")
            bot.enquiry_handler.storage = storage

            for answer in [
                "Ama", "123", "ama@example.com", "Construction",
                "House", "Accra", "A family home", "100000", "June"
            ]:
                response = client.post("/chat", json={
                    "message": answer,
                    "session_id": session_id
                })
                self.assertEqual(response.status_code, 200)

            with storage.file_path.open(encoding="utf-8") as file:
                stored_enquiries = json.load(file)

        self.assertEqual(len(stored_enquiries), 1)
        self.assertEqual(stored_enquiries[0]["name"], "Ama")
        self.assertEqual(stored_enquiries[0]["location"], "Accra")


if __name__ == "__main__":
    unittest.main()
