import os
import unittest
import hashlib
import uuid

from flask import current_app
from flask_testing import TestCase
from doc_api.main import db
from doc_api.main.config import basedir
from doc_api.main.model.document import Document
from doc_api.main.service.document import hash_document, add_document
from manage import app


class TestDocumentService(TestCase):
    def create_app(self):
        app.config.from_object("doc_api.main.config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_if_app_has_hash_functions(self):
        self.assertTrue(len(app.config["HASH_FUNCTIONS"]) > 0)

    def test_hash_document(self):
        data = b"123456"
        data_hashed = {
            "md5": "e10adc3949ba59abbe56e057f20f883e",
            "sha1": "7c4a8d09ca3762af61e59520943dc26494f8941b",
            "sha256": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
        }
        result = hash_document(data, hash_function_list=list(data_hashed.keys()))

        for hash_function, hash_data in data_hashed.items():
            self.assertEqual(result[hash_function], hash_data)

    def test_add_document(self):
        document = add_document(name="test.txt", data=b"Hello world")
        self.assertIsInstance(document, Document)
        self.assertIsInstance(document.uuid, uuid.UUID)

        second_document = add_document(name="test.txt", data=b"Hello world")
        self.assertIsInstance(second_document.uuid, uuid.UUID)
        self.assertEqual(document.data, second_document.data)
        self.assertEqual(document.uuid, second_document.uuid)


if __name__ == "__main__":
    unittest.main()
