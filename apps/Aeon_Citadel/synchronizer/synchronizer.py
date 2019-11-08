def sync_check(event, action):
    if action == 'requestLatest':
        return True
    name = event['name']
    legal_actions = set([])
    if event is None or event == '' or name == 'default':
        legal_actions = set(['newroom'])
    elif name == 'enemy':
        legal_actions = set(['attack', 'dodge', 'charge'])
    elif name == 'win':
        legal_actions = set(['newroom'])

    if action in legal_actions:
        return True
    else:
        return False
