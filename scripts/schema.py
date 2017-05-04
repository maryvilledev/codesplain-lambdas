from cerberus import schema_registy

filter_schema = {
    'color': {
        'type': 'string',
        'required': True,
    },
    'count': {
        'type': 'integer',
        'required': True,
    },
    'prettyTokenName': {
        'type': 'string',
        'required': True,
    },
    'selected': {
        'type': 'boolean',
        'required': True,
    }
}
schema_registy.add('filter', filter_schema)

annotation_schema = {
    'annotation': {
        'type': 'string',
        'required': True,
    },
    'lineNumber': {
        'type': 'integer',
        'required': True,
    },
    'lineText': {
        'type': 'string',
        'required': True,
    },
}

schema_registy.add('annotation', annotation_schema)

ast_schema = {
    'begin': {
        'type': 'integer',
        'required': True,
    },
    'end': {
        'type': 'integer',
        'required': True,
    },
    'type': {
        'type': 'string',
        'required': True,
    },
    'tags': {
        'type': 'list',
        'schema': {
            'type': 'string'
        },
        'required': True,
    },
    'children': {
        'type': 'list',
        'schema': 'ast_schema',
        'required': True,
    }
}

schema_registy.add('ast', ast_schema)

snippet_schema = {
    'annotations': {
        'type': 'dict',
        'keyschema': {
            'type': 'integer',
        },
        'valueschema': 'annotation_schema',
        'required': True,
    },
    'filters': {
        'type': 'dict',
        'keyschema': {
            'type': 'string'
        },
        'valueschema': 'filter_schema',
        'required': True,
    },
    'readOnly': {
        'type': 'boolean',
        'required': True,
    },
    'snippet': {
        'type': 'string',
        'required': True,
    },
    'snippetKey': {
        'type': 'string',
        'required': True
    },
    'snippetLanguage': {
        'type': 'string',
        'required': True
    },
    'snippetTitle': {
        'type': 'string',
        'required': True
    },
}

schema_registy.add('snippet', snippet_schema)
