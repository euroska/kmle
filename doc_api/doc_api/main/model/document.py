from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .. import db


class Document(db.Model):
    """ Model for store document's content """

    __tablename__ = "document"

    # table fields
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.LargeBinary)
    size = db.Column(db.BigInteger, nullable=False, default=0)

    # relation fields
    meta = db.relationship(
        "DocumentMeta", uselist=False, back_populates="document", lazy="select"
    )
    hashes = db.relationship("DocumentHash", back_populates="document")

    def __repr__(self):
        return "<Document '{}'>".format(self.name)


class DocumentHash(db.Model):
    """ Model for store document's hashes """

    __tablename__ = "document_hash"

    # table fields
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_uuid = db.Column(
        UUID(as_uuid=True), db.ForeignKey("document.uuid"), nullable=False
    )
    name = db.Column(db.String(10), nullable=False)
    value = db.Column(db.String(64), nullable=False, unique=True)

    # relation fields
    document = db.relationship("Document", back_populates="hashes")


class DocumentMeta(db.Model):
    """ Model for store ducment's meta information """

    __tablename__ = "document_meta"

    # table fields
    uuid = db.Column(
        UUID(as_uuid=True), db.ForeignKey("document.uuid"), primary_key=True
    )
    time_of_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    creator = db.Column(db.String(100), nullable=False, default="Anonymouse")
    word_count = db.Column(db.Integer, nullable=False, default=0)
    language = db.Column(db.String(10), nullable=False, default="Unknown")

    # relation fields
    document = db.relationship("Document", back_populates="meta")
