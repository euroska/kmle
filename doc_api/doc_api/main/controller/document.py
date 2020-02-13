from flask import request
from flask_restx import Resource

from ..util.dto import DocumentDTO
from ..service.document import *

api = DocumentDTO.api


@api.route('/')
class DocumentList(Resource):
    @api.doc('List of uploaded document')
    @api.marshal_with(DocumentDTO.document, code=200)
    def get(self):
        """List all registered users"""
        documents = [document for document in list_documents()]
        print(documents)
        return documents

    @api.doc('Create a new document')
    @api.marshal_with(DocumentDTO.document, code=201)
    @api.expect(DocumentDTO.upload, validate=True)
    def post(self):
        """Creates a new User """
        document = request.files['document']
        return add_document(
            document.filename,
            document.stream.read()
        )

    #def put(self):
        #data = request.json
        #return sa


@api.route('/<uuid:uuid>')
@api.param('uuid', 'The Document identifier')
@api.response(404, 'User not found.')
class Document(Resource):
    @api.doc('get a user')
    @api.marshal_with(DocumentDTO.document)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
