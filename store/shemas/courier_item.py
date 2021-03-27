CourierItem = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
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
        }
    }
}
