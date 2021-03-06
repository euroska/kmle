import uuid
import hashlib
import requests

from typing import List, Dict
from dateutil.parser import parse as parse_datetime
from sqlalchemy.orm import defer
from flask import current_app as app
from doc_api.main import db
from doc_api.main.model.document import Document, DocumentHash, DocumentMeta


def hash_document(data: bytes, hash_function_list: List[str] = None):
    """ create hashes of document """
    if hash_function_list is None:
        hash_function_list = app.config["HASH_FUNCTIONS"]

    result = {}
    for hash_function in hash_function_list:
        result[hash_function] = getattr(hashlib, hash_function)(data).hexdigest()

    return result


def add_document(name: str, data: bytes):
    """ Add document """
    # hash document and check for document collision
    document_hashes = hash_document(data)

    for hash_function, hash_data in document_hashes.items():
        document_hash = DocumentHash.query.filter_by(
            name=hash_function, value=hash_data
        ).first()

        if document_hash:
            return document_hash.document

    # create document
    document = create_document(name, data)

    # add hashes
    db.session.add(document)
    [
        db.session.add(document_hash)
        for document_hash in create_document_hashes(
            document, document_hashes=document_hashes
        )
    ]
    db.session.add(create_document_meta(document))
    db.session.commit()
    return document


def create_document(name: str, data: bytes):
    """ calculate document hashes """
    return Document(uuid=uuid.uuid4(), name=name, data=data, size=len(data))


def create_document_hashes(document: Document, document_hashes: Dict[str, str] = None):
    # create default document hashes
    if document_hashes is None:
        document_hashes = hash_document(document.data)

    return [
        DocumentHash(
            uuid=uuid.uuid4(),
            document_uuid=document.uuid,
            name=hash_function,
            value=hash_value,
        )
        for hash_function, hash_value in document_hashes.items()
    ]


def create_document_meta(document: Document):
    """ Get metadata from apache tika """
    request = requests.put(
        f"{app.config['TIKA_SERVER']}/meta",
        data=document.data,
        headers={"Accept": "application/json"},
    )
    response_json = request.json()

    # create document
    return DocumentMeta(
        uuid=document.uuid,
        time_of_creation=(
            parse_datetime(response_json["Creation-Date"])
            if "Creation-Date" in response_json
            else None
        ),
        creator=response_json.get("Author"),
        word_count=response_json.get(  # TODO: This section is not clean!!!
            "meta:word-count",
            len(
                requests.put(
                    f"{app.config['TIKA_SERVER']}/tika", data=document.data,
                ).text.split()
            ),
        ),
        language=response_json.get("language"),
    )


def list_documents(start=0, offset=0):
    return Document.query.options(defer("data")).all()


def get_document(uuid: uuid.UUID):
    return Document.query.filter_by(uuid=uuid).first()
