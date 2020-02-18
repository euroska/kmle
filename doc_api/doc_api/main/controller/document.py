from io import BytesIO
from flask import current_app as app
from flask import request, send_file
from flask_restx import Resource

from ..dto.document import DocumentDTO
from ..service.document import get_document, list_documents, add_document

api = DocumentDTO.api  # pylint: disable=invalid-name


@api.route("/")
@api.header("Access-Control-Allow-Origin", "*")
class DocumentList(Resource):
    @api.doc("List of uploaded document")
    @api.marshal_with(DocumentDTO.document, code=200)
    def get(self):  # pylint: disable=no-self-use
        """ List all documents """
        return list_documents()

    @api.doc(responses={406: "Not Acceptable"})
    @api.doc("Create a new document")
    @api.marshal_with(DocumentDTO.document, code=201)
    @api.expect(DocumentDTO.upload, validate=True)
    def post(self):  # pylint: disable=no-self-use
        """ Creates a new Document """
        document = request.files["document"]
        if document.filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSION"]:
            return add_document(document.filename, document.stream.read())

        api.abort(406)


@api.route("/<uuid:uuid>")
@api.param("uuid", "The Document identifier")
@api.response(404, "Document not found.")
@api.header("Access-Control-Allow-Origin", "*")
class Document(Resource):
    @api.doc("Get a document")
    @api.response(200, "Document octet stream.")
    @api.produces(["application/octet-stream"])
    def get(self, uuid):  # pylint: disable=no-self-use
        """ Get a document given its identifier """
        document = get_document(uuid)
        if not document:
            api.abort(404)

        return send_file(
            BytesIO(document.data),
            mimetype="application/octet-stream",
            as_attachment=True,
            attachment_filename=document.name,
        )
