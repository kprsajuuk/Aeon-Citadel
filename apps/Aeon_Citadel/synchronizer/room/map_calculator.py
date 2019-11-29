def get_map_dimension(map_arr):
    room = map_arr.get('rooms', [])[-1]
    coor = room.get('coor', [])
    return coor[0], coor[1]


def next_room(direction, map_user, map_level):
    row, col = get_map_dimension(map_user)
    rooms = map_user.get('rooms', [])
    room = rooms[map_user['user']]

    path = room.get('path', [])
    coor = room.get('coor', []).copy()
    if direction in path and len(coor) > 0:
        room['user'] = False
        if direction == 't':
            coor[0] = coor[0] - 1
        elif direction == 'r':
            coor[1] = coor[1] + 1
        elif direction == 'b':
            coor[0] = coor[0] + 1
        elif direction == 'l':
            coor[1] = coor[1] - 1
        index = row*(coor[0]-1)+coor[1]-1
        new_room = map_level[index]
        rooms[index]['path'] = new_room['path']
        if not rooms[index]['show']:
            rooms[index]['show'] = True
            rooms[index]['new'] = True
        else:
            rooms[index]['new'] = False
        rooms[index]['user'] = True
        map_user['user'] = index
        return new_room, map_user
    else:
        return False
