from flask_restx import Api
from flask import Blueprint

from .main.controller.document import api as document_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus web service'
)

api.add_namespace(
    document_ns,
    path='/v1/document'
)
