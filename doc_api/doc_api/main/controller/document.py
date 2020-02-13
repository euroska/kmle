from flask import request, make_response
from flask_restx import Resource

from ..dto.document import DocumentDTO
from ..service.document import *

api = DocumentDTO.api


@api.route('/')
class DocumentList(Resource):
    @api.doc('List of uploaded document')
    @api.marshal_with(DocumentDTO.document, code=200)
    def get(self):
        ''' List all documents '''
        documents = [document for document in list_documents()]
        print(documents)
        return documents

    @api.doc('Create a new document')
    @api.marshal_with(DocumentDTO.document, code=201)
    @api.expect(DocumentDTO.upload, validate=True)
    def post(self):
        ''' Creates a new Document '''
        document = request.files['document']
        return add_document(
            document.filename,
            document.stream.read()
        )


@api.route('/<uuid:uuid>')
@api.param('uuid', 'The Document identifier')
@api.response(404, 'Document not found.')
class Document(Resource):
    @api.doc('Get a document')
    @api.response(200, 'Document octet stream.')
    @api.produces(['application/octet-stream'])
    def get(self, uuid):
        ''' Get a document given its identifier '''
        document = get_document(uuid)
        if not document:
            api.abort(404)

        else:
            response = make_response(document.data, 200)
            response.mimetype = 'application/octet-stream'
            return response
