def sync_check(event, action):
    if action == 'requestLatest':
        return True
    legal_actions = set([])
    if event is None:
        legal_actions = set(['newroom'])
    elif event['name'] == 'enemy':
        legal_actions = set(['attack', 'withdraw', 'struggle'])

    if action in legal_actions:
        return True
    else:
        return False
