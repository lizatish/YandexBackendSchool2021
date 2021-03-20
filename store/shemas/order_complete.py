OrderComplete = {
    'type': 'object',
    'properties': {
        'courier_id': {
            'type': 'integer',
            'minimum': 0
        },
        'order_id': {
            'type': 'integer',
            'minimum': 0
        },
        'complete_time': {
            'type': 'string',
            "pattern": '^[0-9]{4}[-]{1}[0-1]{1}[1-9]{1}[-]{1}[0-3]{1}[0-9]{1}[T][0-2]{1}[0-9]{1}[:][0-5]{1}[0-9]{1}[:][0-5]{1}[0-9]{1}[.]{1}[0-9]{2}[Z]{1}$',
        }
    },
    'required': ['courier_id', 'order_id', 'complete_time']
}
