CouriersPostRequest = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'data': {
            'type': 'array',
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'courier_id': {
                        'type': 'integer',
                        'minimum': 0
                    },
                    'courier_type': {
                        'type': 'string',
                        'enum': ['foot', 'bike', 'car']
                    },
                    'regions': {
                        'type': 'array',
                        'minItems': 1,
                        'items': {'type': 'integer', 'minimum': 0}
                    },
                    'working_hours': {
                        'type': 'array',
                        "minItems": 1,
                        'items': {
                            'type': 'string',
                            "pattern": '^[0-9]{2}[:]{1}[0-9]{2}[-]{1}[0-9]{2}[:]{1}[0-9]{2}$',
                        }
                    }},
                'required': ['courier_id', 'courier_type', 'regions', 'working_hours']
            },
        }
    },
    'required': ['data'],
}
