def sync_check(event, action):
    if action == 'requestLatest':
        return True
    event_type = event.get('type', '')
    legal_actions = set([])
    # if event is None or event == '' or event_type == 'default':
    if event_type == 'start':
        legal_actions = set(['start'])
    elif event_type == 'move':
        legal_actions = set(['t', 'r', 'b', 'l'])
    elif event_type == 'enemy':
        legal_actions = set(['attack', 'dodge', 'charge'])
    elif event_type == 'message':
        legal_actions = set(['confirm'])
    elif event_type == 'option':
        legal_actions = set(event.get('legalKeys', []))

    if action in legal_actions:
        return True
    else:
        return False
