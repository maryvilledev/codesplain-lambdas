from marshmallow import Schema, fields

class Filter(Schema):
    color = fields.String(required=True)
    count = fields.Integer(required=True)
    prettyTokenName = fields.String(required=True)
    selected = fields.Boolean(required=True)

class Annotation(Schema):
    annotation = fields.String(required=True)
    lineNumber = fields.Integer(required=True)
    lineText = fields.String(required=True)

class Annotations(Schema):
    annotations = fields.Nested(Annotation, many=True, required=True)

class AST(Schema):
    begin = fields.Number(required=True)
    end = fields.Number(required=True)
    tags = fields.List(fields.String(), required=True)
    nodeType = fields.String(attribute="type", required=True)
    children = fields.List(fields.Nested("self", many=True), required=True)

class Snippet(Schema):
    annotations = fields.Nested(Annotations, required=True)
    AST = fields.Nested(AST, required=True)
    filters = fields.Nested(Filter, many=True, required=True)
    readOnly = fields.Boolean(required=True)
    snippet = fields.String(required=True)
    snippetKey = fields.String(required=True)
    snippetLanguage = fields.String(required=True)
    snippetTitle = fields.String(required=True)
