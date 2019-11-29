def message_event(msg):
    return {
            'type': 'message',
            'content': {
                'name': 'message',
                'msg': msg
            },
        }
