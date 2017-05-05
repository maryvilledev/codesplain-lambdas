from cerberus import Validator, schema_registry

requiredBoolField = { 'type': 'bool', 'required': True }
requiredIntField = { 'type': 'integer', 'required': True }
requiredStringField = { 'type': 'boolean', 'required': True }

annotation_schema = {
    'annotation': {
        'type': 'string',
    },
    'lineNumber': {
        'type': 'integer',
    },
    'lineText': {
        'type': 'string',
    },
}

ast_schema = {
    'begin': {
        'type': 'integer',
    },
    'end': {
        'type': 'integer',
    },
    'type': {
        'type': 'string',
    },
    'tags': {
        'type': 'list',
        'schema': {
            'type': 'string'
        },
    },
    'children': {
        'type': 'list',
        'schema': 'ast_schema',
    }
}

filter_schema = {
    'color': {
        'type': 'string',
    },
    'count': {
        'type': 'integer',
    },
    'prettyTokenName': {
        'type': 'string',
    },
    'selected': {
        'type': 'boolean',
    }
}

schema_registry.add('annotation_schema', annotation_schema)
schema_registry.add('ast_schema', ast_schema)
schema_registry.add('filter_schema', filter_schema)

snippet_schema = {
    'annotations': {
        'type': 'dict',
        'keyschema': {
            'type': 'integer',
        },
        'valueschema': {
            'type': 'dict',
            'schema': 'annotation_schema',
        },
        'required': True
    },
    'filters': {
        'type': 'dict',
        'keyschema': {
            'type': 'string'
        },
        'valueschema': {
            'type': 'dict',
            'schema': 'filter_schema'
        },
        'required': True
    },
    'AST': {
        'type': 'dict',
        'schema': 'ast_schema',
        'required': True
    },
    'readOnly': requiredBoolField,
    'snippet': requiredStringField,
    'snippetKey': requiredStringField,
    'snippetLanguage': requiredStringField,
    'snippetTitle': requiredStringField,
}
