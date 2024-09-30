from flask_restx import fields
from flask_restx.reqparse import RequestParser

class PhrasesRequestSchema:
    def __init__(self, namespace):
        self.namespace = namespace

    def create(self):
        return self.namespace.model('Phrases Create', {
            'phrase': fields.String(required=True)
        })
    def update(self):
        return self.namespace.model('Phrases Update', {
            'id': fields.Integer(required=True),
            'status' : fields.Boolean(required=True)
        })