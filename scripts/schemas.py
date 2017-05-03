from marshmallow import Schema, fields

class Filter(Schema):
    color: fields.String()
    count: fields.Integer()
    prettyTokenName: fields.String()
    selected: fields.Boolean()

class Annotation(Schema):
    annoation: fields.String()
    lineNumber: fields.Integer()
    lineText: fields.String()

class Annotations(Schema):
    annotations: fields.Nested(Annotation, many=True)
