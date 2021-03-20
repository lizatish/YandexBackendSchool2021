OrdersPostRequest = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'order_id': {
                        'type': 'integer',
                        'minimum': 0
                    },
                    'weight': {
                        'type': 'number',
                        'minimum': 0.01,
                        'maximum': 50
                    },
                    'region': {
                        'type': 'integer',
                        'minimum': 0
                    },
                    'delivery_hours': {
                        'type': 'array',
                        "minItems": 1,
                        'items': {
                            'type': 'string',
                            "pattern": '^[0-9]{2}[:]{1}[0-9]{2}[-]{1}[0-9]{2}[:]{1}[0-9]{2}$',
                        }
                    }},
                'required': ['order_id', 'weight', 'region', 'delivery_hours']
            }
        }
    },
    'required': ['data']
}
