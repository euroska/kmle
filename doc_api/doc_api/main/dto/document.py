import werkzeug
from flask_restx import Namespace, fields, reqparse


class DocumentDTO:
    api = Namespace("document", description="Document related operations")
    upload = reqparse.RequestParser()
    upload.add_argument(
        "document",
        type=werkzeug.datastructures.FileStorage,
        location="files",
        required=True,
        help="Uploaded file",
    )
    meta = api.model(
        "meta",
        {
            "timeOfCreation": fields.DateTime(
                description="Date of creation",
                dt_format="iso8601",
                required=True,
                attribute="time_of_creation",
            ),
            "creator": fields.String(description="Author's name", required=True,),
            "wordCount": fields.Integer(
                description="Number of words", required=True, attribute="word_count",
            ),
            "language": fields.String(
                description="Language of document", required=True,
            ),
        },
    )

    hash = api.model(
        "hash",
        {
            "name": fields.String(description="Hash function name", required=True,),
            "value": fields.String(description="Hash function value", required=True,),
        },
    )

    document = api.model(
        "document",
        {
            "uuid": fields.String(required=True, description="Document uuid"),
            "name": fields.String(required=True, description="Document name"),
            "size": fields.Integer(required=True, description="Document size"),
            "meta": fields.Nested(meta),
            "hashes": fields.List(fields.Nested(hash)),
        },
    )
