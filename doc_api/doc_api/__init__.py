from flask_restx import Api
from flask import Blueprint

from .main.controller.document import api as document_ns

blueprint = Blueprint("api", __name__)  # pylint: disable=invalid-name

api = Api(  # pylint: disable=invalid-name
    blueprint,
    title="DOCUMENT STORAGE",
    version="1.0",
    description="Document semantic storage",
)

api.add_namespace(document_ns, path="/v1/document")
