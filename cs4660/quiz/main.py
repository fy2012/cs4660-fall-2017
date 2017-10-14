"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs
from queue import Queue

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"


def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)


def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)


def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response


def bfs(node_id_a, node_id_b):
    queue = Queue()
    graph = {}
    path = []
    got_result = False

    queue.put(node_id_a)

    while queue.not_empty and got_result == False:
        room_id = queue.get()
        room_state = get_state(room_id)
        for node in room_state['neighbors']:
            if node['id'] not in graph:
                graph[node['id']] = room_id
                if node_id_b == node['id']:
                    got_result = True
                    break
                queue.put(node['id'])

    current_position_id = node_id_b
    room_state = get_state(current_position_id)
    current_room_name = room_state['location']['name'] + ' ID:' + current_position_id
    while current_position_id != node_id_a:
        room_id = graph[current_position_id]
        room_state = get_state(room_id)
        room_name = room_state['location']['name']+ ' ID:' + room_id
        path.append(room_name + ':' + current_room_name + ':' + str(transition_state(room_id, current_position_id)['event']['effect']))
        current_position_id = room_id
        room_state = get_state(current_position_id)
        current_room_name = room_state['location']['name'] + ' ID:' + current_position_id

    path.reverse()
    return path


if __name__ == "__main__":
    # Your code starts here

    node_id_a = '7f3dc077574c013d98b2de8f735058b4'
    node_id_b = 'dadbd109410c73d838efec4867e4db57'

    path = bfs(node_id_a, node_id_b)

    for value in path:
        print(value)

