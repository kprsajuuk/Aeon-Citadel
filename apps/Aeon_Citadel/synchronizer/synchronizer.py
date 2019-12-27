def sync_check(event, action):
    event_type = event.get('type', '')
    if action == 'requestLatest':
        return True
    if event_type == 'pass':
        return True
    legal_actions = set([])
    # if event is None or event == '' or event_type == 'default':
    if event_type == 'start':
        legal_actions = set(['start'])
    elif event_type == 'move':
        legal_actions = set(['t', 'r', 'b', 'l', 'act'])
    elif event_type == 'enemy':
        legal_actions = set(['attack', 'dodge', 'charge', 'endBattle'])
    elif event_type == 'message':
        legal_actions = set(['confirm'])
    elif event_type == 'option':
        legal_actions = set(event.get('legalKeys', []))

    if action in legal_actions:
        return True
    else:
        return False
